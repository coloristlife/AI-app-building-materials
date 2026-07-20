https://www.giskard.ai/knowledge/how-to-test-ml-models-4-metamorphic-testing  


How to test ML models? #4 🎚 Metamorphic testing

Metamorphic testing are adapted to Machine Learning. This tutorial describes the theory, examples and code to implement it.

Metamorphic testing is increasingly popular in AI because it's particularly adapted to the Machine Learning context. In a nutshell, it's about assessing the behavior of your AI model after perturbations (changes of input data). As a benefit, it enables you to implement tests of your AI without knowing the ground truth label.

Maybe you have never heard about it, and you wonder why it's useful?

This article will use the latest research to explain how important metamorphic testing is for ML. It will then provide concrete illustrations with different types of data and code examples to implement them.

Why is metamorphic testing perfect for Machine Learning?
The challenges of unit testing in ML
Usually, to implement a unit test in software testing, you need to define the system's correct output after the program's execution for a given input (scenario). But what happens when you don't have in mind all the input scenarios inputs that need to be tested? Worse, what happens when you don't even know the correct output for a given input (the oracle problem)? 

Particularly in Machine Learning, the oracle problem can be really challenging. For example, how to know the ground truth default probability that should return a credit scoring model for a given credit demander? Even an experienced bank advisor could not precisely specify the correct default probability before the default event happens. But without defining a mapping between inputs and outputs of the credit scoring model, there is no possibility of creating a unit test for this ML classifier.

Even if we suppose this mapping is possible, how many input scenarios do we need to unit test a credit scoring model? For instance, a first input scenario can be a credit demander called Bob that is asking for a loan of $10,000, has $2500 in his bank account, and lives in Dallas. A second input scenario can be a credit demander Alice that is asking for a loan of $15,000, has $5500 in her bank account, and lives in Chicago. And so on. The testing scenarios can be infinite in Machine Learning since the data represent an unlimited number of input cases.

Enter metamorphic testing
Unlike unit testing, metamorphic testing (MT) is a property-based software testing technique. It means that MT describes the system functionality in terms of generic relations between inputs rather than as mappings between input and output. Introduced a long time ago by Chen (1998) in software testing, metamorphic testing is increasingly used in Machine Learning because of the shortcomings of unit testing presented above.

But what is precisely metamorphic testing? Since a picture is worth a thousand words, the below drawing represents in red the two main concepts of metamorphic testing: perturbation and metamorphic relation.

Metamorphic testing for Machine Learning
Metamorphic testing for Machine Learning
While the ML model maps an input (data example) to an output (scoring or classification labels), MT maps a perturbation relation between inputs to a metamorphic relation between outputs. For example, a metamorphic testing for credit scoring can be that if you switch the credit demander's gender from male to female (perturbation), the default probability should not increase (metamorphic relation).

Here are the most used metamorphic relations in the scientific literature:

Invariance: metamorphic invariance relations mean that the output should remain invariant after the perturbation. A typical example is NLP classification, where one may want a prediction to remain invariant when switching synonyms in the input text (Ribeiro, 2020).
Increasing: metamorphic increasing relations mean that the output should increase after perturbation. For example, the credit default score may increase when the bank account has less cash. 
Decreasing: metamorphic decreasing relations mean that the output should decrease after perturbation. For example, the credit default score may decrease if the credit demander has a full-time job instead of a part-time job.
As we saw in the above examples, these 3 metamorphic relations can be applied to various perturbations depending on the data type. Let's see how metamorphic testing can be implemented for textual, categorical, and numerical perturbations.

Examples of metamorphic testing in ML
Metamorphic testing for textual perturbations
There are many types of textual perturbation that can be implemented for metamorphic testing in Machine Learning. The Checklist paper from Ribeiro et al. (2020) proposes a good review addressing various textual perturbation techniques such as typo generations, synonyms/antonyms switch, or adding words.

As a practical example, let's implement the metamorphic invariance relation after synonyms substitutions in NLP classification. To do so, let's suppose we're classifying emails into some topics. We want at least half of the emails to remain invariant after the substitution by synonyms. This metamorphic test can be easily implemented thanks to the following Python code that uses wordnet synonyms to generate perturbations.

```
"""
Summary: Tests if the model prediction is invariant when the feature values are perturbed
Description: Test if the predicted classification label remains the same after
feature values perturbation.The test is passed when the percentage of unchanged
rows is higher than the threshold
Args:
    df(GiskardDataset):
        Dataset used to compute the test
    model(GiskardModel):
        Model used to compute the test
    perturbation_dict(dict):
        Dictionary of the perturbations. It provides the perturbed features as key
        and a perturbation lambda function as value
    threshold(float):
        Threshold of the ratio of invariant rows
Returns:
    actual_slices_size:
        total number of rows of actual dataset
    number_of_perturbed_rows:
        Number of perturbed rows
    metric:
        The ratio of unchanged rows over the perturbed rows
    passed:
        TRUE if metric > threshold
    output_df:
        Dataframe of rows where the prediction changes due to perturbation
"""

import nlpaug.augmenter.word as naw  
aug = naw.SynonymAug(aug_src='wordnet')


# Perturbation: all the words of the email are substituted by WordNet's synonym
perturbation = {
    "Content": lambda x: aug.augment(x["Content"])
}

tests.metamorphic.test_metamorphic_invariance(
    df=actual_ds,
    model=model,
    perturbation_dict=perturbation,  
    threshold=0.5
)
view rawTextual_metamorphic_testing.py hosted with ❤ by GitHub
```

Metamorphic testing for categorical perturbation
Metamorphic testing can also be implemented for categorical perturbation. As an illustration, for a credit scoring model, one can expect that the default score increases (metamorphic relation) when the demander has a part-time job instead of a full-time one (perturbation). We can then verify that more than half of the dataset (threshold = 0.5) has an increasing default probability after this perturbation.

This metamorphic test can be easily implemented thanks to the following Python code.


```
"""
Summary: Tests if the model probability decreases when the feature values are perturbed

Description: Test if the model probability of a given classification_label is
decreasing after feature values perturbation.The test is passed when the percentage of
rows that are decreasing is higher than the threshold

Args:
    df(GiskardDataset):
        Dataset used to compute the test
    model(GiskardModel):
        Model used to compute the test
    perturbation_dict(dict):
        Dictionary of the perturbations. It provides the perturbed features as key
        and a perturbation lambda function as value
    threshold(float):
        Threshold of the ratio of increasing rows
    classification_label(str):
        One specific label value from the target column

Returns:
    actual_slices_size:
        Total number of rows of actual dataset
    number_of_perturbed_rows:
        Number of perturbed rows
    metric:
        The ratio of increasing rows over the perturbed rows
    passed:
        TRUE if metric > threshold
    output_df:
        Dataframe containing the rows whose probability doesn't increase after perturbation

"""
#Perturbation:  we want to increase the cash amount in the bank account by 20%
perturbation = {
    "account_money_amount": lambda x: x["account_money_amount"] * 0.20,
}

#The credit default score should decrease when we increase the cash in the bank account of the credit demander
tests.metamorphic.test_metamorphic_decreasing(
    df=actual_ds,
    model=model,
    perturbation_dict=perturbation, 
    classification_label='Default',
    threshold=0.5
)
"""
#Perturbation:  we want to switch credit demanders' job from full-time to part-time
perturbation = {
     "job": lambda x: "part-time" if x["job"] == "full-time" else x["job"])
}

#The credit default score should increase when credit demanders have part-time job rather than full-time job
tests.metamorphic.test_metamorphic_increasing(
    df=actual_ds,
    model=model,
    perturbation_dict=perturbation, 
    classification_label='Default',
    threshold=0.5
)
view rawCategorical_metamorphic_testing.py hosted with ❤ by GitHub

```

Metamorphic testing for numerical perturbation
Let's take the example of a perturbation on a numerical variable. Let's take back the credit scoring model example. One can expect that the default score decreases (metamorphic relation) when the cash amount in the demander's bank account increases (perturbation). More precisely, we can verify that more than half of the dataset (threshold = 0.5) has a decreasing default probability after the perturbation.

This metamorphic test can be easily implemented thanks to the following Python code.
```
"""
Summary: Tests if the model probability decreases when the feature values are perturbed
Description: Test if the model probability of a given classification_label is
decreasing after feature values perturbation.The test is passed when the percentage of
rows that are decreasing is higher than the threshold
Args:
    df(GiskardDataset):
        Dataset used to compute the test
    model(GiskardModel):
        Model used to compute the test
    perturbation_dict(dict):
        Dictionary of the perturbations. It provides the perturbed features as key
        and a perturbation lambda function as value
    threshold(float):
        Threshold of the ratio of increasing rows
    classification_label(str):
        One specific label value from the target column
Returns:
    actual_slices_size:
        Total number of rows of actual dataset
    number_of_perturbed_rows:
        Number of perturbed rows
    metric:
        The ratio of increasing rows over the perturbed rows
    passed:
        TRUE if metric > threshold
    output_df:
        Dataframe containing the rows whose probability doesn't increase after perturbation
"""
#Perturbation:  we want to increase the cash amount in the bank account by 20%
perturbation = {
    "account_money_amount": lambda x: x["account_money_amount"] * 0.20,
}

#The credit default score should decrease when we increase the cash in the bank account of the credit demander
tests.metamorphic.test_metamorphic_decreasing(
    df=actual_ds,
    model=model,
    perturbation_dict=perturbation, 
    classification_label='Default',
    threshold=0.5
)
view rawNumerical_metamorphic_testing.py hosted with ❤ by GitHub
‍```

All these metamorphic relations and perturbations are pre-completed in the open source Giskard solution. You can try them by installing Giskard and playing with the demo ML projects loaded by default. You can even create more custom and complex tests with Giskard. Have a look at the documentation to start implementing them.

Conclusion
Metamorphic testing is well adapted for Machine Learning because they do not require defining a strong mapping between test inputs and outputs. These are particularly interesting when they are combined with other automatic data generation tools to create realistic perturbations.

At Giskard, we provide open-source metamorphic relations and perturbations for Machine Learning. Try our demo projects preloaded in the app to learn more about testing in Machine Learning.

Check our Github!

References
Barr, E. T., Harman, M., McMinn, P., Shahbaz, M., & Yoo, S. (2014). The oracle problem in software testing: A survey. IEEE transactions on software engineering, 41 (5), 507-525.
Chen, T. Y., Cheung, S. C., & Yiu, S. M. (2020). Metamorphic testing: a new approach for generating next test cases. arXiv preprint arXiv:2002.12543.
Ribeiro, M. T., Wu, T., Guestrin, C., & Singh, S. (2020). Beyond accuracy: Behavioral testing of NLP models with CheckList.
{{richtext-style-text-line}}