from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), weather['date'], weather['low'], weather['high']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def translate(query):
  #百度翻译的网址
  url = "https://fanyi.baidu.com/transapi"
  #构建头部，构建form表单数据发送post请求
  headers = {"User-Agent": "Mozilla/5.0 (Linux; Android    6.0; Nexus 5 Build/MRA58N)AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/72.0.3626.121   Mobile Safari/537.36"}
  data = {
    "from": "zh",
    "to": "en",
    "query": query,
    "transtype": "realtime",
    "simple_means_flag": "3",
    "sign": "198772.518981",
    "token": "a2618f73c47d96db078aae0c6672e7e3"
  }
  response = requests.post(url = url, data = data, headers = headers)
  html = response.content.decode()
  #得到的html是json文件格式的内容，所以之后用json提取数据
  html = json.loads(html)
  rep = html["data"][0]["dst"]
  return rep

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, todayDate, min_temperature, max_temperature = get_weather()
words1 = get_words()
data = {
  "weather":{"value":wea, "color":get_random_color()},
  "temperature":{"value":temperature, "color":get_random_color()},
  "todayDate":{"value":todayDate, "color":get_random_color()},
  "min_temperature":{"value":min_temperature, "color":get_random_color()},
  "max_temperature":{"value":max_temperature, "color":get_random_color()},
  "love_days":{"value":get_count(), "color":get_random_color()},
  "birthday_left":{"value":get_birthday(), "color":get_random_color()},
  "words":{"value":words1, "color":get_random_color()},
  "words2":{"value":translate(words1), "color":get_random_color()}
}
res = wm.send_template(user_id, template_id, data)
print(res)
