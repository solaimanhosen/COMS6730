from openai import OpenAI
import os
import re
import sys
import csv
import pandas as pd
import time

file_path = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/IrrelevantSymptoms_100.csv'
file_path_write = 'C:/Users/jabir/OneDrive/Documents/COMS673/Project/Datasets/IrrelevantSymptoms_DiseasesOutcomes.csv'
df = pd.read_csv(file_path)
print(df.head())
shuffled_df = df.sample(frac=1, random_state=80).reset_index(drop=True)
print(shuffled_df.head())
#sys.exit()
row_index = 0;
print(len(df))
#sys.exit()
symptomsAttackData = []
origSymptomsData =[]
DiseasesData_with_attack = []

#DiseasesData_with_attack.append(["Original_note","Attacked_note","Diseases_with_attack","Diseases_without_attack"])

for index, row in df.iterrows():
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="",
    )
    system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

    #user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"
    #with open('your_file.csv', mode='r') as file:

    orig_symptoms = row['Original']
    attack_symptoms = row['Attack']

    #orig_note = "I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought
    #  on by nausea and muscle ache."
    Extract_diseases_without_attack_prompt  = "These are the symptoms"+" "+orig_symptoms+ ",please list the potential 15 diseases in the descending order of possibility with the most probable disease first.Please extract\
    only the diseases listed in numbered format just one disease per line and nothing else and make sure you list down 15 possible diseases"

    Extract_diseases_with_attack_prompt  = "These are the symptoms"+" "+attack_symptoms+ ",please list the 15 potential diseases in the order of highest priority.Please extract\
    only the diseases listed in numbered format just one disease per line and nothing else and make sure you list down 15 possible diseases"

    #user_input_orig_note_prompt = "'"+orig_note+"'.  Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

    response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": Extract_diseases_without_attack_prompt}])

    reply = response.choices[0].message.content.strip()
    print(Extract_diseases_without_attack_prompt)
    print(reply)

    
   
    #print(reply)
    
    pattern = r"\d+\.\s([^\n]+)"
    matches_without_attack = re.findall(pattern, reply, re.MULTILINE)
    #print(matches_without_attack)
    
    while len(matches_without_attack) !=15:
        #reprompt = "You have not provided the list of 15 possible diseases in numbered list. Please provide them in numbered list and no other text"
        reprompt = Extract_diseases_without_attack_prompt+". Previously you did'nt provide a list of 15 possible diseases, please provide\
        the possible diseases in the descending order of possiblitity with the give symptoms"
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": reprompt}])
        reply = response.choices[0].message.content.strip()
        pattern = r"\d+\.\s([^\n]+)"
        #pattern = r"\d+\.\s[^\d]*(?:\n(?!\d+\.).*)*"
        matches_without_attack = re.findall(pattern, reply, re.MULTILINE)
        #print(matches)

    #print(str(matches_without_attack))
    #print(matches_without_attack)
    

    #matches_without_attack = re.sub(r'\[.*?\]', '', str(matches_without_attack)).strip()
    


    matches_without_attack = str(matches_without_attack)
    #matches_without_attack = matches_without_attack[1:5]
    matches_without_attack = matches_without_attack[1:len(matches_without_attack)-1]
    #print(matches_without_attack)
    
    #sys.exit()

    response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": Extract_diseases_with_attack_prompt}])


    #DiseasesData_without_attack.append([orig_symptoms,attack_symptoms,matches_without_attack])
    reply = response.choices[0].message.content.strip()

    pattern = r"\d+\.\s([^\n]+)"
    matches_with_attack = re.findall(pattern, reply, re.MULTILINE)
    #print(matches_with_attack)
    while len(matches_with_attack) !=15:
        #reprompt = "You have not provided the list of 15 possible diseases in numbered list. Please provide them in numbered list and no other text"
        reprompt = Extract_diseases_with_attack_prompt+". Previously you did'nt provide a list of 15 possible diseases, please provide\
        the possible diseases in the descending order of possiblitity with the give symptoms"
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": reprompt}])
        reply = response.choices[0].message.content.strip()
        pattern = r"\d+\.\s([^\n]+)"
        matches_with_attack = re.findall(pattern, reply, re.MULTILINE)
        


    matches_with_attack = str(matches_with_attack)
    #matches_without_attack = matches_without_attack[1:5]
    matches_with_attack = matches_with_attack[1:len(matches_with_attack)-1]
    #print(matches_with_attack)
    #sys.exit()

    DiseasesData_with_attack.append([orig_symptoms,attack_symptoms,matches_without_attack,matches_with_attack])



    row_index = row_index+1;
    if row_index%5==0:
        time.sleep(1)
        #break;
    
    if row_index == 50:
        break;
 
file = open(file_path_write, mode='a',encoding='ISO-8859-1', newline='')
writer = csv.writer(file)
writer.writerows(DiseasesData_with_attack)
file.close()  



#user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"
#user_input = "'I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought on by nausea and muscle ache.'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"
