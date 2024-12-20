from openai import OpenAI
import os
import re
import sys
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

system_prompt = "You are a helpful disease diagnosing agent as you will listing the possible diseases from symptoms. Do not Explain or provide any other text"

orig_note = "This morning when I woke up, I discovered an extremely bad rash on my skin. There are several pus-filled pimples and blackheads all around. My skin has also been moving around a lot."

#user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

#orig_note = "I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought on by nausea and muscle ache."
#orig_note = "I have to constantly to go the bathroom to relieve myself, but cant seem to empty my bladder. I get these very strong and uncontrollable urges to pee and sometimes get dark or bloody pee"
#user_input_orig_note_prompt = "'"+orig_note+"'.  Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

orig_note_promt = "'"+orig_note+"'.For this clinical note please provide a numbered list of possible diseases just one disease per line and no other text"
print(orig_note_promt)
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
#print(reply)
#sys.exit()
#pick a disease not in the list of diseases just hard coding it for now.
disease = "Cohn's disease"
user_input_mod = "Please provide one most prominent symptom of this disease "+disease+" Please provide only one most significant symptom and no other text"
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": user_input_mod}])
additional_symptom = response.choices[0].message.content.strip()
print("the symptom is")
print(additional_symptom)

modified_note = "'"+orig_note+"'.For this clinical include this symptom too '"+additional_symptom+"' Please elaborate on this symptom in few sentences right in the very beginning of the clinical\
note and then please make sure to include the details of other symptoms in subsequent lines, not in the same line as the additional symptom added.Please do not modify any other symptom or its context.Just provide the modified clinical note and no other text"
print(modified_note)
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": modified_note}])
modified_note = response.choices[0].message.content.strip()
print(modified_note)

