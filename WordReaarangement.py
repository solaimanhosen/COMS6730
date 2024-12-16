from openai import OpenAI
import os
import re
import sys
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

#user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

#orig_note = "I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought on by nausea and muscle ache."
orig_note = "I have to constantly to go the bathroom to relieve myself, but cant seem to empty my bladder. I get these very strong and uncontrollable urges to pee and sometimes get dark or bloody pee"
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
for i in range(0,len(matches)):
    if i == 3:
       #print(matches[i])
       system_prompt = "You are a helpful medical note paraphraser. Respond by modifying the clinical note by prioritizing one symptom over all of them and mentioning about it at the very beggining, do not change any other symptom or the context. Do not Explain or provide any other text just provide the modified clinical note"
       user_input_mod = user_input_mod+  "  \'"+matches[i]+"\'" 
       break

user_input_mod = user_input_mod + " such these are in the very beginning before other symptoms and they have to be explained in a few sentences these sentences solely dedicated to this symptom ,Please do not change any other symptoms or their context.The rest of the symptoms would be in the later sentences.Just provide the modified clinal note and no other text" 
print(user_input_mod)

response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": user_input_mod}])
modified_clinical_note = response.choices[0].message.content.strip()
print(modified_clinical_note)
result = None
response = None
