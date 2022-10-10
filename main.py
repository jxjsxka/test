from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

# 今日天气
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

# 明日天气
def get_tomorrow_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][1]
  return weather['weather'], math.floor(weather['low']), math.floor(weather['high'])

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

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, min_temperature, max_temperature = get_weather()
min_to_max = str(min_temperature) + "° ~ " + str(max_temperature) + "°"
tomorrow_wea, tomorrow_min_temperature, tomorrow_max_temperature = get_tomorrow_weather()
tomorrow_min_to_max = str(tomorrow_min_temperature) + "° ~ " + str(tomorrow_max_temperature) + "°"
data = {
  "city":{"value":"有你的地方", "color":get_random_color()},
  # 今日天气
  "weather":{"value":wea, "color":get_random_color()},
  "temperature":{"value":temperature, "color":get_random_color()},
  "min_to_max":{"value":min_to_max, "color":get_random_color()},
  # 明日天气
  "tomorrow_wea":{"value":tomorrow_wea, "color":get_random_color()},
  "tomorrow_min_to_max":{"value":tomorrow_min_to_max, "color":get_random_color()},
  
  "love_days":{"value":get_count(), "color":get_random_color()},
  "birthday_left":{"value":get_birthday(), "color":get_random_color()},
  "words":{"value":get_words(), "color":get_random_color()}
}

res = wm.send_template(user_id, template_id, data)
print(res)





# from datetime import date, datetime
# import math
# from wechatpy import WeChatClient
# from wechatpy.client.api import WeChatMessage, WeChatTemplate
# import requests
# import os
# import random

# today = datetime.now()
# start_date = os.environ['START_DATE']
# city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']

# app_id = os.environ["APP_ID"]
# app_secret = os.environ["APP_SECRET"]

# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]

# # 今日天气
# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

# # 明日天气
# def get_tomorrow_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][1]
#   return weather['weather'], math.floor(weather['low']), math.floor(weather['high'])

# def get_count():
#   delta = today - datetime.strptime(start_date, "%Y-%m-%d")
#   return delta.days

# def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days

# def get_words():
#   words = requests.get("https://api.shadiao.pro/chp")
#   if words.status_code != 200:
#     return get_words()
#   return words.json()['data']['text']

# def get_random_color():
#   return "#%06x" % random.randint(0, 0xFFFFFF)

# client = WeChatClient(app_id, app_secret)

# wm = WeChatMessage(client)
# wea, temperature, min_temperature, max_temperature = get_weather()
# tomorrow_wea, tomorrow_min_temperature, tomorrow_max_temperature = get_tomorrow_weather()
# data = {
#   "city":{"value":"有你的地方", "color":get_random_color()},
#   # 今日天气
#   "weather":{"value":wea, "color":get_random_color()},
#   "temperature":{"value":temperature, "color":get_random_color()},
#   "min_temperature":{"value":min_temperature, "color":get_random_color()},
#   "max_temperature":{"value":max_temperature, "color":get_random_color()},
#   # 明日天气
#   "tomorrow_wea":{"value":tomorrow_wea, "color":get_random_color()},
#   "tomorrow_min_temperature":{"value":tomorrow_min_temperature, "color":get_random_color()},
#   "tomorrow_max_temperature":{"value":tomorrow_max_temperature, "color":get_random_color()},
  
#   "love_days":{"value":get_count(), "color":get_random_color()},
#   "birthday_left":{"value":get_birthday(), "color":get_random_color()},
#   "words":{"value":get_words(), "color":get_random_color()}
# }

# res = wm.send_template(user_id, template_id, data)
# print(res)
