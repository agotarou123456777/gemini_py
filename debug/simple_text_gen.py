import google.generativeai as genai
import os

ENV_KEY_NAME = "GOOGLE_API_KEY"
MODEL_NAME = 'gemini-2.0-flash'

genai.configure(api_key=os.environ[ENV_KEY_NAME])

model = genai.GenerativeModel(MODEL_NAME)
response = model.generate_content("暑いの対義語は？")
print(response.text)