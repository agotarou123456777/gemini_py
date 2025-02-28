import google.generativeai as genai
import os
import PIL.Image


ENV_KEY_NAME = "GOOGLE_API_KEY"
MODEL_NAME = 'gemini-2.0-flash'

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

genai.configure(api_key=os.environ[ENV_KEY_NAME])
img = PIL.Image.open('resource/dog.jpg')

model = genai.GenerativeModel(MODEL_NAME)

user_prompt = []
user_prompt.append(
"""
画像の内容に関するクイズを出して! 正解とヒントはいわないで!
"""
)

user_prompt.append(
"""
正解をおしえて!
"""
)

messages = []
for idx, prompt in enumerate(user_prompt):
  
  if idx == 0:
    user_part = {
      "role" : "user",
      "parts" : [prompt, img]
    }
    messages.append(user_part)
    
  else:
    model_part = {
      "role" : "model",
      "parts" : [response.text]
    }
    user_part = {
      "role" : "user",
      "parts" : [prompt]
    }
    messages.append(model_part)
    messages.append(user_part)
  
  response = model.generate_content(messages)
  print(f"** Chat Turn {idx} **")
  print("[user]" , prompt)  
  print("[model]\n", response.text)  
    
'''
messages = [
    {'role':'user',
     'parts': [user_prompt[0], img]},
]
response = model.generate_content(messages)

print("** Turn 1 ** \n", response.text)
print()


messages = [
    {'role':'user',
     'parts': [prompt, img]},
    {'role':'model',
     'parts': [response.text]},
    {'role':'user',
     'parts': ["正解をおしえて!"]},
]
response = model.generate_content(messages)
print("** Turn 2 ** \n", response.text)
'''
