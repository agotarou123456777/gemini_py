import google.generativeai as genai
import PIL.Image
import os

ENV_KEY_NAME = "GOOGLE_API_KEY"
MODEL_NAME = 'gemini-2.0-flash'

genai.configure(api_key=os.environ[ENV_KEY_NAME])
img = PIL.Image.open('resource/dog.jpg')

model = genai.GenerativeModel(MODEL_NAME)
response = model.generate_content(["画像について説明して", img])
print(response.text)