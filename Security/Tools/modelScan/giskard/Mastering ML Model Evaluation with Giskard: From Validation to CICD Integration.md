https://www.giskard.ai/knowledge/machine-learning-validation-with-giskard 

Mastering ML Model Evaluation with Giskard: From Validation to CI/CD Integration
Learn how to integrate vulnerability scanning, model validation, and CI/CD pipeline optimization to ensure reliability and security of your AI models. Discover best practices, workflow simplification, and techniques to monitor and maintain model integrity. From basic setup to more advanced uses, this article offers invaluable insights to enhance your model development and deployment process.

Imagine effortlessly ensuring fairness, performance, and reliability in your machine learning models. Have you ever wondered how to guarantee that your AI models perform flawlessly and ethically? Enter Giskard.

Giskard is an open-source tool designed for data scientists and machine learning engineers. It's your key to detecting and addressing potential issues in your models. In this tutorial, we'll show you how to harness the power of Giskard:

Discover hands-on techniques to detect potential issues.
Learn how to generate test suites using Giskard.
Explore the seamless integration of Giskard into your CI/CD pipeline.
How to Install Giskard for ML Model Testing
Setting up a virtual environment
Isolating our project dependencies is essential. Let's start by creating a virtual environment.

Create a Project Directory: Begin by creating a new directory for your project and navigating to it:
mkdir giskard-tutorial
cd giskard-tutorial
view rawcd.py hosted with ❤ by GitHub
Install `pipenv`: We'll use `pipenv` for managing dependencies. Install it using `pip`:
pip install pipenv
view rawpipenv.py hosted with ❤ by GitHub
Create a Virtual Environment: Now, create a virtual environment and install the required Python version (in this case, Python 3.9):
pipenv install --python 3.9
view rawve.py hosted with ❤ by GitHub
This command generates a `Pipfile` and `Pipfile.lock` to manage your project's dependencies.

Installing Giskard
With our virtual environment in place, let's proceed to install Giskard and its dependencies.

1. Install Giskard with `pipenv`: Inside your project directory, run:

pipenv install "giskard>=2.0.0b"
view rawinst.py hosted with ❤ by GitHub
This command ensures Giskard is installed within your virtual environment. For more detailed installation instructions, refer to the Giskard documentation.

2. Alternative Installation: If you prefer not to use virtual environments, you can also install Giskard directly with `pip`:

pip install "giskard>=2.0.0b" -U -q
view rawpip.py hosted with ❤ by GitHub
Data and Model Preparation for Machine Learning Validation
For our analysis, we've selected the Telecom Customer Churn Prediction dataset from Kaggle. Why? Because it's a compact yet diverse dataset, with its blend of numeric and categorical features.

Before we begin to scan our model for potential issues, we'll need to prepare our dataset and model for use with Giskard.

Preparing the dataset
Giskard requires that the dataset be wrapped with `Giskard.Dataset`. Some pointers to keep in mind when wrapping the dataset:

Dataset Type: Ensure your dataset is a `pandas.DataFrame`.
Include Ground Truth: Your dataset should contain the actual ground truth variable (the target variable).
Use Raw Data: Giskard is designed to detect model issues, not data issues. So, use raw data to avoid confusing model issues with preprocessing artifacts.
Recommended Preprocessing Steps
While Giskard focuses on model issues, a few preprocessing steps can enhance dataset reliability:

Remove Duplicates: Get rid of duplicate entries.
Drop Redundant Features: Eliminate unnecessary features. For example, columns like Id might not be needed.
Specify Data Types: Specify the type for each column.
Split the Dataset: Divide it into training, validation, and test sets.
Handle NaN Values: Decide whether to fill them or remove them. [Optional]
The reason for splitting the dataset is to train the model on the training dataset, use the validation dataset to find potential issues with the model using Giskard. Lastly, test model performance on test dataset.

Here's a step-by-step example using a Customer Churn Prediction dataset:

import numpy as np
import pandas as pd
from giskard import Dataset
from sklearn.model_selection import train_test_split

# Load the dataset
DATASET_URL = 'https://raw.githubusercontent.com/Giskard-AI/examples/main/datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv'
churn_df = pd.read_csv(DATASET_URL)

# Pre-process the dataset
CATEGORICAL_COLUMNS = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']
NUMERIC_COLUMNS = ['tenure', 'MonthlyCharges', 'TotalCharges']

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna()
    df = df.drop('customerID', axis=1)
    df['PaymentMethod'] = df['PaymentMethod'].str.replace(' (automatic)', '', regex=False)
    df[CATEGORICAL_COLUMNS + ['Churn']] = df[CATEGORICAL_COLUMNS + ['Churn']].astype('object')
    return df

churn_df = preprocess(churn_df)

# Train-validation-test split
X_train, X_valid, y_train, y_valid = train_test_split(churn_df.drop('Churn', axis=1), churn_df.Churn, test_size=0.3, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid, y_valid, test_size=0.5, random_state=42)

# Wrap the dataset with Giskard
raw_data = pd.concat([X_valid, y_valid], axis=1)
wrapped_data = Dataset(
    df = raw_data,  # A pandas.DataFrame that contains the raw data (before all the pre-processing steps) and the actual ground truth variable
    target = 'Churn',  # Ground truth variable
    name = "Churn classification dataset",  # Optional
    cat_columns = CATEGORICAL_COLUMNS  # List of categorical columns. Optional, but is a MUST if available. Inferred automatically if not.
)
view rawcustomer_churn_prediction.py hosted with ❤ by GitHub
To find out more about wrapping a dataset, check out the Giskard documentation.

Preparing the model for evaluation
Just like the dataset, Giskard requires your model to be wrapped with `Giskard.Model`. Giskard is model-agnostic, supporting machine learning models from various frameworks such as TensorFlow, PyTorch, and scikit-learn.

First things first, ensure your model is trained on the training set. A trained model is crucial as Giskard identifies issues based on the model's performance.

For this tutorial, let's use a simple logistic regression model from scikit-learn:

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Pre-process steps for the pipeline
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), NUMERIC_COLUMNS),
    ('cat', OneHotEncoder(handle_unknown='ignore',drop='first'), CATEGORICAL_COLUMNS)
])

# Define the pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

# Train the model
pipeline.fit(X_train, y_train)
view rawsklean_model.py hosted with ❤ by GitHub
There are two ways to wrap a model:

Prediction Function: Create a function that takes a `pandas.DataFrame` as input and returns a `numpy.ndarray` of prediction probabilities.
Model Object: Define a custom class that inherits from Giskard's Model and implements the `model_predict` method. This method should take a `pandas.DataFrame` as input and return a `numpy.ndarray` of prediction probabilities.
In both cases, your function or method should encapsulate all data preprocessing steps, such as categorical encoding and numerical scaling. Why is this necessary will be explained shortly below.

For this tutorial, we used a sklearn pipeline to incorporate the preprocessing steps.

Here's an example of wrapping a model using the prediction function method:

from giskard import Model, scan

# Define the prediction function
def prediction_function(df: pd.DataFrame) -> np.ndarray:
    # The pre-processor can be a pipeline of one-hot encoding, imputer, scaler, etc. OR
    # Perform the pre-processing steps manually here
    return pipeline.predict_proba(df)

# Wrap the model with Giskard
wrapped_model = Model(
    model = prediction_function,                # A prediction function that encapsulates all the data pre-processing steps and that could be executed with the dataset used by the scan.
    model_type = "classification",              # Either regression, classification or text_generation.
    classification_labels = pipeline.classes_,  # Their order MUST be identical to the prediction_function's output order
    name = "Churn classification",              # Name of the wrapped model [Optional]
    feature_names = X_valid.columns.to_list(),  # Default: all columns of your dataset [Optional]
    classification_threshold = 0.5,             # Default: 0.5 [Optional]
)
view rawwrapping_model.py hosted with ❤ by GitHub
Let's summarize, we've prepared a raw validation dataset and trained a model on the training dataset. On the training dataset, we applied some preprocessing techniques to ensure the model trains properly.

We aim to use our wrapped model on the wrapped dataset to spot potential issues. To predict accurately on this dataset, the model must apply the same preprocessing steps.

Behind the scenes, Giskard will call the ‘prediction_function’ with the raw data, apply the pre-processing steps, and then obtain the probabilities of the predictions.

Why is this important? Giskard uses the predicted probabilities to perform statistical tests. These tests help identify areas in the dataset where the model may have issues. Giskard then relates these issues back to the corresponding segments of the raw dataset. We'll see this more clearly when we look at the scan results.

To find out more about wrapping a model, check out the Giskard documentation.

Scan your ML model to detect vulnerabilities
Now that we've wrapped our dataset and model with Giskard, it's time to embark on the exciting journey of scanning the model for potential issues.

Giskard simplifies the scanning process with its `scan` function. Here's how you can use it:

from giskard import scan

# Scan the model
scan_results = scan(wrapped_model, wrapped_data)

# Display the results in the notebook
display(scan_results)
view rawscan.py hosted with ❤ by GitHub
Giskard Scan results:


Scan Results - Performance
Interpreting the scan results is crucial. Giskard has identified issues related to Performance Bias, Overconfidence, and Underconfidence.


Show Details - Performance
For instance, in the Performance Bias category: When the Contract is "One year", the Recall is 100.0% lower than the overall Recall. This "global recall" refers to the recall score for the entire dataset. In this subset, 215 samples have the actual label as Yes, but the model predicts No for all of them.


Show Details - Performance
In the Overconfidence category, take the first issue as an example. For samples where OnlineBackup is "Yes", the Overconfidence rate is 36.2%, compared to a global rate of 26.2%. This means that samples labeled 'Yes' are incorrectly predicted as 'No' with high confidence.

It's beneficial to delve deeper into the scan results to get a better grasp on the model's challenges.

Saving Your Scan Results
You might want to keep a record of your model's check-up. Giskard allows you to save the results in different formats:

# Save the results to a html file
scan_results.to_html("scan_results.html")

# Save the results to a dataframe
results_df = scan_results.to_dataframe()
view rawsave_results.py hosted with ❤ by GitHub
The scan function in Giskard is designed to detect potential issues in machine learning models and datasets. These issues include:

Performance Bias: Occurs when a model performs differently on specific data subsets compared to the overall dataset.
Unrobustness: The model is sensitive to small changes in input data, leading to unpredictable behavior.
Overconfidence: The model assigns high confidence to incorrect predictions, potentially causing erroneous decisions.
Underconfidence: The model lacks confidence in its predictions, leading to cautious decision-making.
Unethical Behavior: When models exhibit sensitivity to gender, ethnicity, religion, or other factors in their predictions.
Data Leakage: Occurs when external information unintentionally influences model creation, leading to inaccurate generalization.
Stochasticity: The model produces different results for the same input due to inherent randomness in certain algorithms.
Spurious Correlation: When a feature appears correlated with model predictions, but the relationship is coincidental rather than meaningful.
These issues can impact the reliability and fairness of machine learning models, and Giskard helps identify and address them. You can learn more about these vulnerabilities in the Giskard documentation.

The Advantages of Test Suites for ML Model Monitoring
The scan function in Giskard helps you spot issues in your model. But how do you ensure these issues are addressed in subsequent versions of the model? This is where test suites come in.

Imagine you've developed a model, Model A, and used Giskard to scan it, revealing 15 issues. To address these, you can set up test suites for each issue. When you later retrain or adjust Model A, you can run these test suites to check if the identified issues have been resolved.

Understanding Test Suites for Effective Machine Learning Validation
Creating test suites in Giskard is straightforward. Think of a test suite as a collection of tests, each focusing on a specific model issue. This ensures a thorough verification of your model, leaving no stone unturned. Giskard offers a library of pre-made tests to make this process even easier.

Creating Your First Test Suite
Wouldn't it be fantastic if you could assemble a test suite that covers all the essential tests identified during the initial model scan? Well, you can! Here's how:

# Create a test suite from the scan results
test_suite = scan_results.generate_test_suite(name="My first test suite")

# You can run the test suite locally to verify that it reproduces the issues
test_suite.run()
view rawtest_suite.py hosted with ❤ by GitHub
Adding Custom Tests
But what if you want to include a specific test in your suite? Suppose you need a test to check if the validation set's accuracy exceeds 0.8. Here's how you can do it:

from giskard import testing

# Add a test to the test suite
test_suite = test_suite.add_test(testing.test_accuracy(wrapped_model, wrapped_data, threshold=0.80))

# Run the test suite
test_suite_results = test_suite.run()
view rawcustom_tests.py hosted with ❤ by GitHub
Giskard Test Suites Result:


Test Suite Results
Extracting Test Suite Results
Now, what if you need to access the results from your test suite? Let's dive into the process:

# Extract the values of the test suite results using the `results` attribute
# The format of the results is a list of dictionaries
test_suite_results.results
view rawextract_test_suite.py hosted with ❤ by GitHub
Why would you want to extract these results? Doing so allows you to save them, integrate them into a CI/CD pipeline, or build a dynamic dashboard to visualize your model's performance over time.

To delve deeper into test suites and explore the diverse range of tests Giskard offers, check out the Giskard documentation on Tests and Test Suites.

Enhancing AI Model Validation: Integrating Giskard into CI/CD Pipelines
With our test suite ready, the next step is to incorporate it into a CI/CD pipeline. This allows for automated checks and balances every time there's an update to our model.

In this section, we'll walk you through integrating Giskard with GitHub Actions to create a CI/CD pipeline. This ensures that for every pull request, stakeholders and reviewers receive a concise summary of the model's performance.

What's the advantage? This snapshot not only offers a performance overview but also confirms that the model meets established quality benchmarks before progressing to the next stage.

Save the model and dataset
Before we dive into the pipeline setup, let's ensure we have our model and dataset safely stored.

# Save the model
import pickle

with open("model/model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

# Save the dataset
raw_data.to_csv('data/validation_data.csv', index=False)
view rawsave_model.py hosted with ❤ by GitHub
Building a Python script
Next up, let's craft a Python script that will orchestrate the test suite and record its results. We'll name the file `run_test_suite.py`:

import os
import re
import pickle
import numpy as np
import pandas as pd
import warnings
import logging

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from giskard import Dataset, Model, scan, testing

warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

CATEGORICAL_COLUMNS = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']
NUMERIC_COLUMNS = ['tenure', 'MonthlyCharges', 'TotalCharges']

# Load the validation dataset
logging.info("Loading the validation dataset")
validation_df = pd.read_csv('data/validation_data.csv')
validation_df[CATEGORICAL_COLUMNS] = validation_df[CATEGORICAL_COLUMNS].astype('object')
FEATURES = [col for col in validation_df.columns if col != 'Churn']

# Load the model
logging.info("Loading the model")
with open("model/model.pkl", "rb") as f:
    pipeline = pickle.load(f)

# Wrap the dataset with Giskard
logging.info("Wrapping the dataset with Giskard")
wrapped_data = Dataset(
    df = validation_df,  # A pandas.DataFrame that contains the raw data (before all the pre-processing steps) and the actual ground truth variable
    target = 'Churn',  # Ground truth variable
    name = "Churn classification dataset",  # Optional
    cat_columns = CATEGORICAL_COLUMNS  # List of categorical columns. Optional, but is a MUST if available. Inferred automatically if not.
)

# Define the prediction function
logging.info("Defining the prediction function")
def prediction_function(df: pd.DataFrame) -> np.ndarray:
    return pipeline.predict_proba(df)

# Wrap the model with Giskard
logging.info("Wrapping the model with Giskard")
wrapped_model = Model(
    model = prediction_function,                # A prediction function that encapsulates all the data pre-processing steps and that could be executed with the dataset used by the scan.
    model_type = "classification",              # Either regression, classification or text_generation.
    classification_labels = pipeline.classes_,  # Their order MUST be identical to the prediction_function's output order
    name = "Churn classification",              # Name of the wrapped model [Optional]
    feature_names = FEATURES,                   # Default: all columns of your dataset [Optional]
    classification_threshold = 0.5              # Default: 0.5 [Optional]
)

# Scan the model
logging.info("Scanning the model")
scan_results = scan(wrapped_model, wrapped_data)

# Create a test suite from the scan results and add custom tests
logging.info("Creating a test suite from the scan results and adding custom tests")
test_suite = scan_results.generate_test_suite("My first test suite")
test_suite = test_suite.add_test(testing.test_accuracy(wrapped_model, wrapped_data, threshold=0.75))
test_suite_results = test_suite.run()

if scan_results.has_issues():
    print("Your model has vulnerabilities")
else:
    print("Your model is safe")

# Extract the values of the test suite results using the `results` attribute
logging.info("Extracting the values of the test suite results using the `results` attribute")
output = dict()
for idx, test_result in enumerate(test_suite_results.results):
    test_name = re.sub('"|`|"|"', "", test_result[0])
    output[test_name] = {
        "Status": test_result[1].passed,
        "Threshold": test_result[2]["threshold"],
        "Score": test_result[1].metric,
    }

# To log the results to a pull request comment,
# save the results as a GitHub environment variable
logging.info("Saving the results as a GitHub environment variable")
import json
with open(os.getenv("GITHUB_ENV"), 'a') as fh:
    fh.write(f'TEST_RESULT={json.dumps(output)}')
view rawpython_script.py hosted with ❤ by GitHub
Creating a GitHub workflow YAML file
Turning our attention to the heart of our CI/CD pipeline, we're going to craft a GitHub workflow YAML file that orchestrates the entire process. We'll name this file ci-cd.yml.

To get started, follow these simple steps:

Step 1: Create the .github/workflows Directory

Open your terminal and execute these commands:

# Create the .github/workflows directory
mkdir -p .github/workflows

# Create the ci-cd.yml file
touch .github/workflows/ci-cd.yml
view rawcreate_directory.py hosted with ❤ by GitHub
Step 2: Add the following code to the `ci-cd.yml` file:

name: Giskard-CI-CD

on:
  workflow_dispatch:
  pull_request:
    paths:
      - 'data/**'
      - 'model/**'
      - 'run_test_suite.py'
    branches:
      - main

permissions:
  contents: read

jobs:
    run-giskard-test-suite:
        name: Giskard-Test-Suite
        runs-on: ubuntu-latest
        permissions:
          pull-requests: write

        steps:
          - name: Checkout Code
            uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: 3.9
              cache: 'pipenv'

          - name: Install dependencies
            run: |
              pip install --upgrade pip
              pip install pipenv

          - name: Install dependencies
            working-directory: .
            run: pipenv install --system --deploy

          - name: Execute Giskard Test Suite
            run: python run_test_suite.py
          
          - name: PR comment
            uses: actions/github-script@v6
            with:
              script: |
                github.rest.issues.createComment({
                  issue_number: context.issue.number,
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  body: 'Test Suites Results:\n\n```json\n' + JSON.stringify(JSON.parse(process.env.TEST_RESULT), null, 2) + '\n```'
                })
view rawcicd_file.py hosted with ❤ by GitHub
Review Your Directory Structure
Before we proceed, let's take a quick look at the snapshot of your directory structure:

.
├── .github
│   └── workflows
│       └── ci-cd.yml
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── data
│   └── validation_data.csv
├── model
│   └── model.pkl
└── run_test_suite.py
view rawdirectory_structure hosted with ❤ by GitHub
Pushing the files to GitHub
The next step involves pushing our project files to GitHub. Follow these commands to make it happen:

# Initialize the git repository
git init

# Add the remote repository
git remote add origin "Your GitHub Repository URL"

# Add the files to the staging area
git add .

# Commit the files
git commit -m "Add CI/CD pipeline"

# Create a new branch and switch to it
git checkout -b feature

# Push the files to GitHub
git push -u origin feature
view rawpush.py hosted with ❤ by GitHub
Creating a pull request
Now comes the exciting part! With our files on GitHub, it's time to create a pull request. This action will trigger the GitHub workflow, launching our test suite. The results will then be elegantly presented as a comment on the pull request.

Voila! We've seamlessly integrated Giskard into our CI/CD pipeline, streamlining the process of testing and validating your machine learning models.

With this setup, you'll have the power to ensure the reliability and quality of your models at every turn. And all it takes is a pull request to get the ball rolling!

Snapshots of Triggered Workflow and PR comment:


Snapshots - Triggered Workflow

Snapshots - PR comment
Giskard's Role in Evaluating Machine Learning Models in Real-World Scenarios
Having covered model scanning, test suite creation, and CI/CD pipeline integration with Giskard, let's delve into its practical applications in real-world situations.

Ensuring Model Integrity and Security
Giskard plays a pivotal role in ensuring both the performance and security of your model:

Model Scanning: Begin by analyzing your model with Giskard and create a corresponding test suite.
Performance Testing: Use the test suite to thoroughly assess the model's capabilities and vulnerabilities.
Continuous Monitoring and Data-Driven Insights
Maintaining consistent model performance and data quality is essential. Here's how Giskard assists:

Routine Model Checkups: Even if your model passes all tests, remember to periodically retrain and re-scan it for consistent high performance.
Build Dashboards to Visual Insights: Convert the results from the test suite into visual dashboards. This helps in easy tracking and pinpointing of issues.
Conclusion
In this tutorial, we've explored Giskard's capabilities to enhance your machine learning endeavors. We've looked at issue detection, test suite creation, and CI/CD pipeline integration.

We encourage you to further explore Giskard and see how it can improve your model validation and testing processes.

If you found this helpful, consider giving us a star on Github and becoming part of our Discord community. We appreciate your feedback and hope Giskard becomes an indispensable tool in your quest to create superior ML models.