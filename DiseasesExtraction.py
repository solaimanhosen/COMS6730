from openai import OpenAI
import os
import re
import sys
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

system_prompt = "You are a helpful medical symptom extractor. Respond by listing the symptoms only in number format. Do not Explain or provide any other text"

#user_input = "'I was in the middle of a workout when I suddenly developed a headache, chest pain, and dizziness. It's been hard for me to maintain my balance since then'. Please extract only the symptoms listed in numbered format just one symptom per line and nothing else"
user_input = "Person X has been experiencing constipation and belly pain, which is progressively worsening and significantly impacting their daily life. The belly pain is localized in the abdominal area, is constant, and has persisted for an extended period without fluctuation throughout the day. The discomfort started recently and appears to be steadily worsening over time. There are no specific relieving factors or exacerbating factors mentioned, and the pain remains consistent in severity. Additionally, the constipation and associated discomfort have contributed to an overall decline in comfort and quality of life. Other symptoms or their severity remain unchanged from the initial report. Can you please provide underlying diseases , just the list of diseases in numbered format and no other text"

response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}])

reply = response.choices[0].message.content.strip()
print(reply)
#sys.exit()
#pattern = r"\d+\.\s[^\d]*(?:\n(?!\d+\.).*)*"
pattern = r"\d+\.\s([^\n]+)"
matches = re.findall(pattern, reply, re.MULTILINE)
print(matches)
result = None
response = None
