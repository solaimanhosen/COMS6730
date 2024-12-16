from openai import OpenAI
import os
import re
import sys
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

#user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"
user_input = "'I've had a high temperature, vomiting, chills, and intense itching. I also have a headache and am perspiring a lot. My discomfort has also been brought on by nausea and muscle ache.'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"

response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}])

reply = response.choices[0].message.content.strip()
print(reply)

pattern = r"\d+\.\s([^\n]+)"
matches = re.findall(pattern, reply, re.MULTILINE)
print(matches)

result = None
response = None
