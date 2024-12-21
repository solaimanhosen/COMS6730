from openai import OpenAI
import os
import re
import sys
import csv
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

#file_path = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/Symptom2Disease.csv'
file_path = 'Datasets/Symptom2Disease.csv'
#file_path_write = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/IrrelevantSymptoms_100.csv'
file_path_write = 'Datasets/IrrelevantSymptoms_100.csv'
df = pd.read_csv(file_path)
print(df.head())
shuffled_df = df.sample(frac=1, random_state=42).reset_index(drop=True)
print(shuffled_df.head())
#sys.exit()
row_index = 0;
print(len(df))
#sys.exit()
symptomsAttackData = []
symptomsAttackData.append(['Original_text','Attack_text'])
origSymptomsData =[]

for index, row in df.iterrows():
    orig_note = row['text']
    user_input_orig_note_prompt = "'"+orig_note+"'.  Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

    #prompt to extract the symptoms from GPT-3.5
    response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input_orig_note_prompt}])

    reply = response.choices[0].message.content.strip()
    
    
    pattern = r"\d+\.\s([^\n]+)"
    matches = re.findall(pattern, reply, re.MULTILINE)

    irrelevant_symptom_addition_prompt = "These are the symptoms "

    #create a string of all the symptoms
    for i in range(0,len(matches)):
        irrelevant_symptom_addition_prompt = irrelevant_symptom_addition_prompt+ " "+matches[i]

    #create the prompt to created attacked clinical note by adding an irrelevant symptom of low severity
    #such that it does not relate to any of the symptoms mentioned
    irrelevant_symptom_addition_prompt = irrelevant_symptom_addition_prompt+ "Please provide a symptom that is absolutely not related to the \
    to the given symptoms and is very low in severity.Just mention the symptom and emphasize the attributes of the symptom in a couple of lines and do not mention the underlying cause  ,\
    do not highlight the symptom in your reply\
    or its priority.Finally add the original clinical note \
    \' "+orig_note+"\' . Do not tag or label the original note just blend it with the existing note also do not change the symptoms \
     or add any additional text "

    response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": irrelevant_symptom_addition_prompt}])

    modified_clinical_note = response.choices[0].message.content.strip()

    symptomsAttackData.append([orig_note,modified_clinical_note])
    row_index = row_index+1;
    if row_index%5==0:
        time.sleep(1)
        #break;
    if row_index ==50:
        break; 
    print(modified_clinical_note) 
    
file = open(file_path_write, mode='a',encoding='utf-8', newline='')
writer = csv.writer(file)
writer.writerows(symptomsAttackData)
file.close()
