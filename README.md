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

The -i and -o arguments are to provide input and output file to the program. Please, make to sure to change the command line argument values to execute from differnt attack dataset.

 ## Evaluation
 
