# from https://langchain-ai.github.io/langgraph/tutorials/tot/tot/
# pip install -U langgraph langchain-openai

#######  Prerequisites ############

import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")
# To visualize the algorithm
trace = True
if trace:
    _set_env("LANGSMITH_API_KEY")
    os.environ["LANGSMITH_PROJECT"] = "ToT Tutorial"

  
####### Task Definition ############

import operator
from typing import List, Literal, Union, NamedTuple, Optional
from pydantic import BaseModel, Field

OperatorType = Literal["+", "-", "*", "/"]
TokenType = Union[float, OperatorType]

## We use these schemas to prompt the LLM to generate equations that evaluate to 24.


class Equation(BaseModel):
    """The formula combining the provided numbers to reach the target of 24."""

    tokens: List[TokenType] = Field(
        description="The stack of tokens and operators in reverse-polish notation. Example: [3, 4, '+', -1, '*'] would evaluate to (3 + 4) * -1 = -7.",
    )

    def compute(self) -> float:
        op_funcs = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }
        stack = []
        for token in self.tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                b, a = stack.pop(), stack.pop()
                stack.append(op_funcs[token](a, b))

        return stack[0]


class GuessEquations(BaseModel):
    """Submit multiple equations as guesses."""

    reasoning: str = Field(
        description="The reasoning behind the submitted guesses. Explain how you arrived at these equations."
    )

    equations: List[Equation] = Field(
        description="The list of equations to submit as guesses."
    )


## These objects will represent a single "candidate" (or scored candidate) within our agent's state.
# You can update the candidate object to match your own task.


class Candidate(NamedTuple):
    candidate: Equation
    score: Optional[float] = None
    feedback: Optional[str] = None

    def __str__(self):
        try:
            computed = self.candidate.compute()
        except Exception as e:
            computed = f"Invalid equation: {self.candidate.tokens}; Error: {repr(e)}"

        return f"Equation({self.candidate.tokens}) = {computed} (Reward: {self.score})"

##### Fetch data
import requests
import csv

csv_data = requests.get(
    "https://storage.googleapis.com/benchmarks-artifacts/game-of-24/24.csv"
).content.decode("utf-8")
# Get just the Puzzles column (column index 1)
puzzles = [row[1].strip() for row in csv.reader(csv_data.splitlines()[1:])]

print(f"Example puzzles: {puzzles[:3]}")


class ScoredCandidate(Candidate):
    candidate: Equation
    score: float
    feedback: str

###### Expander ############

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are playing the Game of 24. Using the provide numbers, create an equation that evaluates to 24.\n"
            "Submit exactly {k} guesses for this round.",
        ),
        ("user", "Solve the 24 game for these numbers: {problem}.{candidate}"),
    ],
).partial(candidate="")
llm = ChatOpenAI(model="gpt-4o-mini")

bound_llm = llm.with_structured_output(GuessEquations)
solver = prompt | bound_llm

######### Scorer
def compute_score(problem: str, candidate: Candidate) -> ScoredCandidate:
    numbers = list(map(int, problem.split()))
    # Check that the candidate equation uses all 4 numbers exactly once
    used_numbers = [
        token for token in candidate.candidate.tokens if isinstance(token, float)
    ]
    if sorted(used_numbers) != sorted(numbers):
        score = 0
        feedback = "The equation must use all 4 numbers exactly once."
        return ScoredCandidate(
            candidate=candidate.candidate, score=score, feedback=feedback
        )
    try:
        result = candidate.candidate.compute()
        score = 1 / (1 + abs(24 - result))
        feedback = f"Result: {result}"
    except Exception as e:
        score = 0
        feedback = f"Invalid equation. Error: {repr(e)}"
    return ScoredCandidate(
        candidate=candidate.candidate, score=score, feedback=feedback
    )


######### Graph ############

import operator
from typing import Optional, Dict, Any
from typing_extensions import Annotated, TypedDict
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Send


def update_candidates(
    existing: Optional[list] = None,
    updates: Optional[Union[list, Literal["clear"]]] = None,
) -> List[str]:
    if existing is None:
        existing = []
    if updates is None:
        return existing
    if updates == "clear":
        return []
    # Concatenate the lists
    return existing + updates


class ToTState(TypedDict):
    problem: str
    candidates: Annotated[List[Candidate], update_candidates]
    scored_candidates: Annotated[List[ScoredCandidate], update_candidates]
    depth: Annotated[int, operator.add]


class Context(TypedDict, total=False):
    max_depth: int
    threshold: float
    k: int
    beam_size: int


class EnsuredContext(TypedDict):
    max_depth: int
    threshold: float
    k: int
    beam_size: int


def _ensure_context(ctx: Context) -> EnsuredContext:
    """Get params that configure the search algorithm."""
    return {
        "max_depth": ctx.get("max_depth", 10),
        "threshold": ctx.get("threshold", 0.9),
        "k": ctx.get("k", 5),
        "beam_size": ctx.get("beam_size", 3),
    }


class ExpansionState(ToTState):
    seed: Optional[Candidate]


def expand(
    state: ExpansionState, *, runtime: Runtime[Context]
) -> Dict[str, List[Candidate]]:
    """Generate the next state."""
    ctx = _ensure_context(runtime.context)
    if not state.get("seed"):
        candidate_str = ""
    else:
        candidate_str = "\n\n" + str(state["seed"])
    try:
        equation_submission = solver.invoke(
            {
                "problem": state["problem"],
                "candidate": candidate_str,
                "k": ctx["k"],
            },
        )
    except Exception:
        return {"candidates": []}
    new_candidates = [
        Candidate(candidate=equation) for equation in equation_submission.equations
    ]
    return {"candidates": new_candidates}


def score(state: ToTState) -> Dict[str, Any]:
    """Evaluate the candidate generations."""
    candidates = state["candidates"]
    scored = []
    for candidate in candidates:
        scored.append(compute_score(state["problem"], candidate))
    return {"scored_candidates": scored, "candidates": "clear"}


def prune(state: ToTState, *, runtime: Runtime[Context]) -> Dict[str, Any]:
    scored_candidates = state["scored_candidates"]
    beam_size = _ensure_context(runtime.context)["beam_size"]
    organized = sorted(
        scored_candidates, key=lambda candidate: candidate[1], reverse=True
    )
    pruned = organized[:beam_size]
    return {
        # Update the starting point for the next iteration
        "candidates": pruned,
        # Clear the old memory
        "scored_candidates": "clear",
        # Increment the depth by 1
        "depth": 1,
    }


def should_terminate(
    state: ToTState, runtime: Runtime[Context]
) -> Union[Literal["__end__"], Send]:
    ctx = _ensure_context(runtime.context)
    solved = state["candidates"][0].score >= ctx["threshold"]
    if solved or state["depth"] >= ctx["max_depth"]:
        return "__end__"
    return [
        Send("expand", {**state, "somevalseed": candidate})
        for candidate in state["candidates"]
    ]


# Create the graph
builder = StateGraph(state_schema=ToTState, context_schema=Context)

# Add nodes
builder.add_node(expand)
builder.add_node(score)
builder.add_node(prune)

# Add edges
builder.add_edge("expand", "score")
builder.add_edge("score", "prune")
builder.add_conditional_edges("prune", should_terminate, path_map=["expand", "__end__"])

# Set entry point
builder.add_edge("__start__", "expand")

# Compile the graph
graph = builder.compile(checkpointer=InMemorySaver())



############ Run ############

for step in graph.stream(
    {"problem": puzzles[42]},
    config={"configurable": {"thread_id": "test_1"}},
    context={"depth": 10},
):
    print(step)



############### results ##############
# {'expand': {'candidates': [Candidate(candidate=Equation(tokens=[12.0, 5.0, '/', 7.0, '*']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[12.0, 1.0, '+', 5.0, '*']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[12.0, 7.0, '*', 1.0, '/']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[5.0, 7.0, '*', 1.0, '*']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[7.0, 5.0, '*', 12.0, '/']), score=None, feedback=None)]}}
# {'score': {'candidates': 'clear', 'scored_candidates': [ScoredCandidate(candidate=Equation(tokens=[12.0, 5.0, '/', 7.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 1.0, '+', 5.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 7.0, '*', 1.0, '/']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[5.0, 7.0, '*', 1.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[7.0, 5.0, '*', 12.0, '/']), score=0, feedback='The equation must use all 4 numbers exactly once.')]}}
# {'prune': {'candidates': [ScoredCandidate(candidate=Equation(tokens=[12.0, 5.0, '/', 7.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 1.0, '+', 5.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 7.0, '*', 1.0, '/']), score=0, feedback='The equation must use all 4 numbers exactly once.')], 'scored_candidates': 'clear', 'depth': 1}}
# {'expand': {'candidates': [Candidate(candidate=Equation(tokens=[12.0, 5.0, '-', 1.0, '*']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[1.0, 7.0, '*', 5.0, '+']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[12.0, 1.0, '+', 5.0, '*']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[7.0, 5.0, '*', 1.0, '-']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[12.0, 1.0, '*', 5.0, '-']), score=None, feedback=None)]}}
# {'expand': {'candidates': []}}
# {'expand': {'candidates': [Candidate(candidate=Equation(tokens=[5.0, 7.0, '*', 12.0, '-']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[1.0, 5.0, 7.0, '*', 12.0, '-', '+']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[12.0, 1.0, '*', 5.0, 7.0, '/']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[12.0, 5.0, '*', 7.0, '/', 1.0, '-']), score=None, feedback=None), Candidate(candidate=Equation(tokens=[5.0, 7.0, '*', 1.0, '-', 12.0, '+']), score=None, feedback=None)]}}
# {'score': {'candidates': 'clear', 'scored_candidates': [ScoredCandidate(candidate=Equation(tokens=[12.0, 5.0, '/', 7.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 1.0, '+', 5.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 7.0, '*', 1.0, '/']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[5.0, 7.0, '*', 12.0, '-']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[1.0, 5.0, 7.0, '*', 12.0, '-', '+']), score=1.0, feedback='Result: 24.0'), ScoredCandidate(candidate=Equation(tokens=[12.0, 1.0, '*', 5.0, 7.0, '/']), score=0.07692307692307693, feedback='Result: 12.0'), ScoredCandidate(candidate=Equation(tokens=[12.0, 5.0, '*', 7.0, '/', 1.0, '-']), score=0.05737704918032786, feedback='Result: 7.571428571428571'), ScoredCandidate(candidate=Equation(tokens=[5.0, 7.0, '*', 1.0, '-', 12.0, '+']), score=0.043478260869565216, feedback='Result: 46.0'), ScoredCandidate(candidate=Equation(tokens=[12.0, 5.0, '-', 1.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[1.0, 7.0, '*', 5.0, '+']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 1.0, '+', 5.0, '*']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[7.0, 5.0, '*', 1.0, '-']), score=0, feedback='The equation must use all 4 numbers exactly once.'), ScoredCandidate(candidate=Equation(tokens=[12.0, 1.0, '*', 5.0, '-']), score=0, feedback='The equation must use all 4 numbers exactly once.')]}}
# {'prune': {'candidates': [ScoredCandidate(candidate=Equation(tokens=[1.0, 5.0, 7.0, '*', 12.0, '-', '+']), score=1.0, feedback='Result: 24.0'), ScoredCandidate(candidate=Equation(tokens=[12.0, 1.0, '*', 5.0, 7.0, '/']), score=0.07692307692307693, feedback='Result: 12.0'), ScoredCandidate(candidate=Equation(tokens=[12.0, 5.0, '*', 7.0, '/', 1.0, '-']), score=0.05737704918032786, feedback='Result: 7.571428571428571')], 'scored_candidates': 'clear', 'depth': 1}}
#
final_state = graph.get_state({"configurable": {"thread_id": "test_1"}})
winning_solution = final_state.values["candidates"][0]
search_depth = final_state.values["depth"]
if winning_solution[1] == 1:
    print(f"Found a winning solution in {search_depth} steps: {winning_solution}")
else:
    print(
        f"Failed to find a winning solution in {search_depth} steps. Best guess: {winning_solution}"
    )
  
# Found a winning solution in 2 steps: [Equation(tokens=[1.0, 5.0, 7.0, '*', 12.0, '-', '+']), 1.0, 'Result: 24.0']
