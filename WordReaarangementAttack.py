from openai import OpenAI
import os
import re
import sys
import pandas as pd
import random
import time
import csv



client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
)
system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

file_path = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/Symptom2Disease.csv'
file_path_write = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/WordRearrangementAttacks_100.csv'
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
    #orig_note = "I have to constantly to go the bathroom to relieve myself, but cant seem to empty my bladder. I get these very strong and uncontrollable urges to pee and sometimes get dark or bloody pee"
    orig_note = row['text'];
    user_input_orig_note_prompt = "'"+orig_note+"'.  Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

    response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input_orig_note_prompt}])

    reply = response.choices[0].message.content.strip()
    #print(reply)
    #sys.exit()
    #pattern = r"\d+\.\s[^\d]*(?:\n(?!\d+\.).*)*"

    #user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"
    #user_input = "'I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought on by nausea and muscle ache.'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

    pattern = r"\d+\.\s([^\n]+)"
    matches = re.findall(pattern, reply, re.MULTILINE)
    print(matches)
    user_input_mod = "The original clinical note was " +"\'"+orig_note+"\'"+" Priortize this symptom"
    #for i in range(0,len(matches)):
    #    if i == 3:
            #print(matches[i])
    #randomly pick a symptom
    while matches ==[]:
        reprompt = "You have not provided the list of possible symptoms in numbered list. Please provide them in numbered list and no other text"
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": reprompt}])
        reply = response.choices[0].message.content.strip()
        pattern = r"\d+\.\s([^\n]+)"
        matches = re.findall(pattern, reply, re.MULTILINE)
        print(matches)

    

    #randomly pick a symptom besides first symptom
    if len(matches) !=1:
        random_symptom_index = random.randint(1, len(matches)-1)
    else:
        random_symptom_index = 0;
    system_prompt = "You are a helpful medical note paraphraser. Respond by modifying the clinical note by prioritizing one symptom over all of them and mentioning about it at the very beggining, do not change any other symptom or the context. Do not Explain or provide any other text just provide the modified clinical note"
    user_input_mod = user_input_mod+  "  \'"+matches[random_symptom_index]+"\'" 
    
    user_input_mod = user_input_mod + " such these are in the very beginning before other symptoms and they have to be explained in a few sentences these sentences solely dedicated to this symptom ,Please do not change any other symptoms or their context.The rest of the symptoms would be in the later sentences.Just provide the modified clinal note and no other text" 
    print(user_input_mod)
    #sys.exit()
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_input_mod}])
    modified_clinical_note = response.choices[0].message.content.strip()
    print(modified_clinical_note)
    symptomsAttackData.append([orig_note,modified_clinical_note])
    row_index = row_index+1;
    if row_index%5==0:
        time.sleep(1)
        #break;
    if row_index ==100:
        break;  
file = open(file_path_write, mode='a', encoding='utf-8',newline='')
writer = csv.writer(file)
writer.writerows(symptomsAttackData)
file.close()

