import google.generativeai as genai
import os
import PIL.Image as Image

def load_images_from_dir(dir_path):
  
  images = []
  files = sorted(os.listdir(dir_path))
  
  for file in files:
    file_path = os.path.join(dir_path, file)
    try:
      images.append(Image.open(file_path))
    except Exception as e:
      print(f"Error loading image {file}: {e}")
      images.append(None)
  return images

def getLoopCount(max_image_each_query, num_overlap):
  i = 0
  s = 0
  e = 0 
  while True:
    
    if i == 0:
      s = 0
      e = s + max_image_each_query 
    else:
      s = e + 1 - num_overlap
      e = s + max_image_each_query
    if e > num_images:
      break
    
    i += 1
  
  return i + 1


ENV_KEY_NAME          = "GOOGLE_API_KEY"
MODEL_NAME            = 'gemini-2.0-flash'
MAX_IMAGES            = 80   # 最大投稿可能枚数
MAX_IMAGES_EACH_QUERY = 20   # 問い合わせ1回あたりの最大投稿画像数
IMAGE_OVERLAP_NUM     = 5    # 問い合わせ重複画像数
REFERENCE_IMAGES      = "resource/action_sample"
MAIN_IMAGES           = "export/KVID0169_1fps"

generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}



# *** prompt設定 ***

'''参考画像に付与するテキスト'''
reference_prompt = \
"""\
いまから提示する画像は参考画像です。
次の指示にしたがって、json形式のデータを出力してください。
また、参考画像の回答例は下記のjsonデータです。
{'start' : '15:19:53.372', 'stop' : '15:20:02.404',  'action' : ['作業版の右上から出ているケーブルをまとめます', '結束バンドで結束します']},
"""

'''1枚目の問い合わせに付与するテキスト'''
first_prompt = \
"""\
添付画像は工場内での作業を撮影した映像を一定間隔で抜き出したものです。
画像内の左上の数値は映像のタイムスタンプを表しています。
タイムスタンプは、「HH:MM:SS.ms」のフォーマットになっています。
以下の指定フォーマットに沿ったjson形式で回答してください。
json形式データ以外での回答は不要です。

【指定フォーマット】
{
    'start'  : string, 
    'stop'   : string, 
    'action' : List[string]
}

・ startとstopは各作業の開始時のタイムスタンプと終了時のタイムスタンプを格納してください。
・ actionには各作業における動作説明を格納してください。
・ actionは作業ごとにひとまとめにして、作業内で複数の動作を行っている場合はactionのリストに動作を追加してください。
・ 動作が不明な場合はactionは「動作不明」で回答してください。
・ 画像内に人がいない場合はactionは「-」で回答してください。
・ 動作は詳細に回答し、でっちあげたり嘘を言わないでください。

【出力例】
[
{'start' : '7:15:12.123', 'stop' : '7:15:15.234',  'action' : ['作業パネルの右側のハンドルを回します', '作業パネルを開きます']},
{'start' : '7:15:15.234', 'stop' : '7:15:20.635',  'action' : ['作業版の緑色のスイッチを1秒長押しします', '黄色のスイッチを3回押します']},
{'start' : '7:15:20.635', 'stop' : '7:17:01.611',  'action' : '-'},
{'start' : '7:17:01.611', 'stop' : '7:17:31.439',  'action' : ['白枠で囲まれたエリアに移動します', '段ボールを持ち上げます', '黄色のエリアにダンボールを持って移動します', 'ダンボールを降ろします']}
]
"""

# *** 画像設定 ***
ref_images = load_images_from_dir(REFERENCE_IMAGES)
main_images = load_images_from_dir(MAIN_IMAGES)
print("num of images in directory : ", len(main_images))
main_images_usage = main_images[:MAX_IMAGES]
num_images = len(main_images_usage)
print("num of images (use) : ", num_images)

num_loop = getLoopCount(max_image_each_query=MAX_IMAGES_EACH_QUERY, num_overlap=IMAGE_OVERLAP_NUM)
print("num loop : ", num_loop)

for i in range(num_loop):
  print(f"\n** Create Model [id:{i}] **")
  
  if i == 0:
    s = 0
    e = s + MAX_IMAGES_EACH_QUERY -1
      
  else:
    s = e + 1 - IMAGE_OVERLAP_NUM
    e = s + MAX_IMAGES_EACH_QUERY - 1
  
  print(f"image index [{s}:{e}]")
    
  messages = []
  genai.configure(api_key=os.environ[ENV_KEY_NAME])
  model = genai.GenerativeModel(MODEL_NAME)
  # reference user query
  prompt = [reference_prompt]
  parts = prompt + ref_images
  user_part = {
    "role" : "user",
    "parts" : parts
  }
  messages.append(user_part)
  
  response = model.generate_content(messages)
  
  # model response
  model_part = {
    "role" : "model",
    "parts" : [response.text]
  }
  messages.append(model_part)
  
  # user main query
  prompt = [first_prompt]
  parts = prompt + main_images[s:e]
  user_part = {
    "role" : "user",
    "parts" : parts
  }
  messages.append(user_part)
  
  response = model.generate_content(messages)
  
  print("🤖 [model]\n", response.text)