import google.generativeai as genai
import os

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
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config)

response = model.generate_content("フィボナッチ数列を作成するpythonコードを作成して", stream=True)
for chunk in response:
  print(chunk.text, end = "")