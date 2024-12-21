# Prompt Injection Attacks on LLM: Medical Diagnosis by Symptom Elaboration

To run the project, please follow the steps included below. You also require API keys from OpenAI to run the project.

## Setting up the Environment

To make your environment ready to run the project, we need to do three things:

1. Install python 3.
2. Replace API key placeholder in .env file with your open ai API key.
3. Install the dependencies.

To install the dependencies required for this project, run the following command in your terminal or command prompt:

```bash
pip install -r requirements.txt

```

## Generate Attacks

To generate Attacks with modified clinical note, run one of the attacks scripts. For example, run the following command:

```bash
python SynonymReplacementAttack.py

```

We can run different attack script to generate a different attack.

 ## Attack Execution

To Execute one of the attack, run the following command:

```bash
python ExtractDiseasesFromSymptoms.py -i IrrelevantSymptoms_100.csv -o IrrelevantSymptoms_DiseasesOutcomes.csv

```
This will extract the diseases from the attack and create a csv file with diseases with the attack and without the attack.

The -i and -o arguments are to provide input and output file to the program. Please, make to sure to change the command line argument values to execute from differnt attack dataset.

 ## Evaluation
 For clinical bert evaluation run the notebook ClinicalBert.ipynb. 
 This is for training the clinical bert model with a classifier head attached to its end and also fro evaluating
 Have to specify the datasets for training the clinical bert model
 The symptom2Disease dataset will be used here for training so that it can predict the diseases.
 The dataset for training file path is specified in the 3rd cell in variable name 'file_path'
 The dataset for attack is specified in 3rd cell as well in the variable name 'file_path_attack_dataset'
 Assign the value to that variable with required dataset file path for different attacks
 For example to evaluate synonym replacemnet attack have the variable name as file_path = 'SynonymAttacks.csv'


 For GPT 3.5 model evalution 
 Run the notebook Attack_Evaluation_(GPT-3.5)
 Just change the name file_path in the third cell with the output file from 'ExtractDiseasesFromSymptoms.py'
 eg it could be 'SynonymAttacks_DiseasesOutcomes.csv' as the  output from running 'ExtractDiseasesFromSymptoms.py'
 with input as 'SynonymAttacks.csv'
 
