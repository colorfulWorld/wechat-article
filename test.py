import requests as req
import re
from html import unescape
from urllib.parse import urlencode

rInfo = r'<h4[\s\S]*?href="([\s\S]*?)".*?>([\s\S]*?)<\/a>[\s\S]*?<\/h4>\s*<p[\s\S]*?>([\s\S]*?)<\/p>'
HOST = 'http://weixin.sogou.com/'
entry = HOST + "weixin?type=2&query=Python&page={}"
html  = req.get(entry.format(1)) # 第一页
infos = re.findall(rInfo, html)
print(html)

def remove_tags(s):
  return re.sub(r'<.*?>', '', s)

def weixin_params(link):
  html = req.get(link)
  rParams = r'var (biz =.*?".*?");\s*var (sn =.*?".*?");\s*var (mid =.*?".*?");\s*var (idx =.*?".*?");'
  params = re.findall(rParams, html)
  if len(params) == 0:
    return None
  return {i.split('=')[0].strip(): i.split('=', 1)[1].strip('|" ') for i in params[0]}


for (link, title, abstract) in infos:
  title    = unescape(self.remove_tag(title))
  abstract = unescape(self.remove_tag(abstract))
  params   = weixin_params(link)  
  if params is not None:
    link = "http://mp.weixin.qq.com/s?" + urlencode(params)
    print(link, title, abstract)