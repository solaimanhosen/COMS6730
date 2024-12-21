from openai import OpenAI
import os
import re
import sys
import csv
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

#file_path = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/Symptom2Disease.csv'
file_path = 'Datasets/Symptom2Disease.csv'

#file_path_write = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/SymptomAttacks_100.csv'
file_path_write = 'Datasets/SymptomAttacks_100.csv'

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
    client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))
    system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

    

    orig_note = row['text']
    
    #prompt to extract symptoms
    user_input_orig_note_prompt = "'"+orig_note+"'.  Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

    response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input_orig_note_prompt}])

    reply = response.choices[0].message.content.strip()
    
    
    pattern = r"\d+\.\s([^\n]+)"
    matches = re.findall(pattern, reply, re.MULTILINE)

    #prompt to extract the synonyms
    user_input_mod = "The original clinical note was " +"\'"+orig_note+"\'"+" Modify the note such that the symptoms"
    for i in range(0,len(matches)):
        system_prompt = "You are a helpful medical symptom synonym extractor. Respond by listing one not very likely synonym of the symptom. Do not Explain or provide any other text"
        user_input = "here is the symptom given in quotes. \'"+ matches[i]+"\'. "+"Please provide a single synonym of the symptom only and no other text besides the synonym of the symptom" 
        response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}])
        
        synomym = response.choices[0].message.content.strip()
        print(matches[i]+":"+synomym)

        if i < len(matches):
            system_prompt = "You are a helpful medical symptom synonym extractor. Respond by modifying the clinical note with the synonym of the symptom mention in the user prompt. Do not Explain or provide any other text just provide the modified user prompt"

            user_input_mod = user_input_mod+  " \'"+matches[i]+"\' is replaced by its synomyn '"+synomym+"'." 
        
    #prompt to create modified clinical note with attack replacing symptoms with their synonyms
    user_input_mod = user_input_mod + " The rest of symptoms and context remaining unchanged.Please provide the updated clinical note only and no other text"
    print(user_input_mod)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_input_mod}])
    modified_clinical_note = response.choices[0].message.content.strip()
    print(modified_clinical_note)
    print("done")
    
    row_index = row_index+1
    print(row_index)
    symptomsAttackData.append([orig_note,modified_clinical_note])
    print(symptomsAttackData)
    if row_index%5==0:
        time.sleep(1)
        #break;

    #generate 50 attacks
    if row_index ==50:
        break;  

file = open(file_path_write, mode='a',encoding='utf-8', newline='')
writer = csv.writer(file)
writer.writerows(symptomsAttackData)
file.close()  

