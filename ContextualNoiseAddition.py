from openai import OpenAI
import os
import re
import sys

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

#user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

orig_note = "I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought on by nausea and muscle ache."
user_input_orig_note_prompt = "'"+orig_note+"'.  Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input_orig_note_prompt}])

reply = response.choices[0].message.content.strip()

pattern = r"\d+\.\s([^\n]+)"
matches = re.findall(pattern, reply, re.MULTILINE)
print(matches)
orig_note_promt = "'"+orig_note+"'.For this clinical note please provide a numbered list of possible diseases just one disease per line and no other text"
#print(orig_note_promt)
#sys.exit()
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": orig_note}])
reply = response.choices[0].message.content.strip()
print(reply)
pattern = r"\d+\.\s([^\n]+)"
matches =[]
matches = re.findall(pattern, reply, re.MULTILINE)
print(matches)
while matches ==[]:
    reprompt = "You have not provided the list of possible diseases in numbered list. Please provide them in numbered list and no other text"
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": reprompt}])
    reply = response.choices[0].message.content.strip()
    pattern = r"\d+\.\s([^\n]+)"
    matches = re.findall(pattern, reply, re.MULTILINE)
    print(matches)

modified_note_prompt= "'"+orig_note+"'.For this clinical note elaborate a few sentences on this particular symptom '"+matches[1]+"' .Please elaborate on this symptom in terms of aspects such as eating habits of patient, physical activities,\
time of the day the symptom triggers,duration of the symptom and the effects on mental health like anxiety,distress.Please make sure that you include \
all the mentioned aspects and then please make sure to include the details of other symptoms in subsequent lines, not in the same lines as the additional symptom description added.\
Please do not modify any other symptom or its context.Finally provide provide the modified clinical note and no other text"


#disease = "Cohn's disease"
#user_input_mod = "Please provide one most prominent symptom of this disease "+disease+" Please provide only one most significant symptom and no other text"
#print(modified_note)
#sys.exit()
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": modified_note_prompt}])
modified_note = response.choices[0].message.content.strip()
print(modified_note)

