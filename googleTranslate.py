#!/usr/bin/env python

import re
import json
try:
  import urllib2 as request
  from urllib import quote
except:
  from urllib import request
  from urllib.parse import quote

class Translator:
  string_pattern = r"\"(([^\"\\]|\\.)*)\""
  match_string =re.compile(
            r"\,?\[" 
              + string_pattern + r"\," 
              + string_pattern + r"\," 
              + string_pattern + r"\," 
              + string_pattern
            +r"\]")

  def __init__(self, from_lang, to_lang):
    self.from_lang = from_lang
    self.to_lang = to_lang
  
  def translate(self, source):
    json5 = self._get_json5_from_google(source)
    return self._unescape(self._get_translation_from_json5(json5))

  def _get_translation_from_json5(self, content):
    result = ""
    pos = 2
    while True:
      m = self.match_string.match(content, pos)
      if not m:
        break
      result += m.group(1)
      pos = m.end()
    return result 

  def _get_json5_from_google(self, source):
    escaped_source = quote(source, '')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
    req = request.Request(
       url="http://translate.google.com/translate_a/t?client=t&ie=UTF-8&oe=UTF-8"
         +"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
         , headers = headers)
    r = request.urlopen(req)
    return r.read().decode('utf-8')

  def _unescape(self, text):
    return json.loads('"%s"' % text)

def googleTranslate(str, fromLang, toLang):
  return Translator(fromLang, toLang).translate(str)

if __name__ == "__main__":
  print googleTranslate('hello', 'en', 'ru')

