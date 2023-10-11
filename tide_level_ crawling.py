import pandas as pd
import numpy as np
import requests
from os import name
import xml.etree.ElementTree as et
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote

base_url = 'http://www.khoa.go.kr/api/oceangrid/tideCurPre/search.do?'
#ServiceKey=인증키&ObsCode=관측소 번호&Date=검색 기준 날짜&ResultType=json'
key = 'ServiceKey=PAd4jJpUNixsw98QpatF3w==&'
obscode = 'ObsCode=DT_0032&'
ResultType = 'ResultType=xml'

# 날짜 리스트 얻기
from datetime import datetime, timedelta

def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
    return dates

dates = date_range("2017-01-01", "2021-12-31")

list_api_variable = []
for i in dates:
    list_api_variable.append(base_url+key+obscode+'Date='+ i +'&'+ResultType)
    
# 5년 api 주소 만들기

dict_tide = {}
for i in list_api_variable:
    response = requests.get(i)
    content = response.text
    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    tide_level = xml_obj.findAll('real_value')
    time = xml_obj.findAll('record_time')
    for j, k in zip(tide_level, time):
        dict_tide[k.text] = j.text

index = list(range(42920))
df = pd.DataFrame(dict_tide, index=index)

df_tide = df.iloc[0,:].transpose()

df_tide.to_csv('df_tide.csv')