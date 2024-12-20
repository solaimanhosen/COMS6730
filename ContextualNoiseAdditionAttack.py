from openai import OpenAI
import os
import re
import sys
import pandas as pd
import time
import csv
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

#user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

file_path = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/Symptom2Disease.csv'
file_path_write = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/ContexualNoiseAttacks.csv'
df = pd.read_csv(file_path)
print(df.head())
shuffled_df = df.sample(frac=1, random_state=500).reset_index(drop=True)
print(shuffled_df.head())
#sys.exit()
row_index = 0;
print(len(df))
#sys.exit()
symptomsAttackData = []
origSymptomsData =[]
symptomsAttackData.append(['Original_text','Attack_text'])
for index, row in df.iterrows():
    #orig_note = "I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought on by nausea and muscle ache."
    orig_note = row['text'];
    user_input_orig_note_prompt = "'"+orig_note+"'.  Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

    response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input_orig_note_prompt}])

    reply = response.choices[0].message.content.strip()

    pattern = r"\d+\.\s([^\n]+)"
    matches = re.findall(pattern, reply, re.MULTILINE)
    print(matches)
    '''
    while matches ==[]:
        reprompt = "You have not provided the list of symptoms in numbered list. Please provide them in numbered list and no other text"
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": reprompt}])
        reply = response.choices[0].message.content.strip()
        pattern = r"\d+\.\s([^\n]+)"
        matches = re.findall(pattern, reply, re.MULTILINE)
        print(matches)
    #sys.exit()
    '''
    modified_note_prompt= "'"+orig_note+"'.For this clinical note please elaborate some additional information such as the duration of the symptoms and some personal attributes of the person such educational background,job,achievemnets,\
        religion, number of sibblings,maritial status,ethinicity, number of children and the effects of symptoms on mental health like anxiety,distress and how the impact of symptoms affects the individual's personel life\
        .Please make sure that you include all the mentioned aspects and do not include any other irrelevant information, then include the all the existing symptoms in the original note.\
        Please do not modify any other symptom or its context."
    
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": modified_note_prompt}])
    modified_clinical_note = response.choices[0].message.content.strip()
    
    modified_note_tokens = modified_clinical_note.split(" ")
    while len(modified_note_tokens) <10:
        '''
        modified_note_prompt= "'"+orig_note+"'.For this clinical note please elaborate some additional information such as the duration of the symptoms and some personal attributes of the person such educational background,job,achievemnets,\
        religion, number of sibblings,maritial status,ethinicity, number of children and the effects of symptoms on mental health like anxiety,distress and how the impact of symptoms affects the individual's personel life\
        .Please make sure that you include all the mentioned aspects and do not include any other irrelevant information and then give out the clinal note mentioned above .\
        Please do not modify any other symptom or its context."
        '''
        re_prompt = modified_note_prompt + ".The previous clinical note provided by you is not appropraite, please\
        provide a legitimate one considering the constraints mentioned."
        
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": re_prompt}])
        modified_clinical_note = response.choices[0].message.content.strip()
        modified_note_tokens = modified_clinical_note.split(" ")


    
    print(modified_clinical_note)
    symptomsAttackData.append([orig_note,modified_clinical_note])
    row_index = row_index+1;
    if row_index%5==0:
        time.sleep(1)
        #break;
    if row_index ==50:
        break;  
file = open(file_path_write, mode='a',encoding='utf-8', newline='')
writer = csv.writer(file)
writer.writerows(symptomsAttackData)
file.close()

