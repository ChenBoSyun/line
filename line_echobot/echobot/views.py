# -*- coding: utf-8 -*-
from django.conf import settings

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden

from django.views.decorators.csrf import csrf_exempt



from linebot import LineBotApi, WebhookParser

from linebot.exceptions import InvalidSignatureError, LineBotApiError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests
import urllib2
import xml.etree.cElementTree as ET
import datetime

#get today or tomorrow's date
today = datetime.date.today()
oneday = datetime.timedelta(days=1)
tommorrow = today + oneday



line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

parser = WebhookParser(settings.LINE_CHANNEL_SECRET)







def wea(locations):
    start=False
    day1=False
    request = urllib2.Request("http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-001.xml") #parse weather xml
    response = urllib2.urlopen(request)
    weather_data = response.read()
    fileout = file("doc1.xml","wb")
    fileout.write(weather_data)
    fileout.close()
    tree = ET.ElementTree(file='doc1.xml')
    root = tree.getroot()
    #以下為xml結構 由一層一層label往下找
    for child_of_root in root:
        if(child_of_root.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}dataset"):
            for dataset in child_of_root:
                if(dataset.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}location"):
                    for location in dataset:
                        #找到<locationName>且內容為你輸入之地點
                        if(location.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}locationName" and location.text==locations):  
                            #為了判斷是否該在那層結構下尋找的變數
                            start=True 
                        if(location.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}weatherElement" and start==True ):
                            for weather in location:
                                if(weather.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}time"):
                                    for time in weather:
                                        #找到<startTime>且內容為今天或明天日期
                                        if(time.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}startTime" and (time.text.find(str(today))!=-1 or time.text.find(str(tommorrow))!=-1)):
                                            day1=True
                                            
                                        if(time.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}parameter" and day1==True):
                                            for ans in time:
                                                if(ans.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}parameterName"):
                                                    return ans.text

@csrf_exempt
def callback(request):

    if request.method == 'POST':

        signature = request.META['HTTP_X_LINE_SIGNATURE']

        body = request.body.decode('utf-8')



        try:

            events = parser.parse(body, signature)

        except InvalidSignatureError:

            return HttpResponseForbidden()

        except LineBotApiError:

            return HttpResponseBadRequest()



        for event in events:

            if isinstance(event, MessageEvent):

                if isinstance(event.message, TextMessage):
                
                    if(event.message.text.find(u"天氣")!=-1):
                        if(event.message.text.find(u"臺北市")!=-1):
                            location=u"臺北市"
                        
                        elif(event.message.text.find(u"新北市")!=-1):
                            location=u"新北市"
                        
                        elif(event.message.text.find(u"桃園市")!=-1):
                            location=u"桃園市"
                        
                        elif(event.message.text.find(u"臺中市")!=-1):
                            location=u"臺中市"
                        
                        elif(event.message.text.find(u"臺南市")!=-1):
                            location=u"臺南市"
                        
                        elif(event.message.text.find(u"高雄市")!=-1):
                            location=u"高雄市"
                        
                        elif(event.message.text.find(u"基隆市")!=-1):
                            location=u"基隆市"
                        
                        elif(event.message.text.find(u"新竹縣")!=-1):
                            location=u"新竹縣"
                        
                        elif(event.message.text.find(u"新竹市")!=-1):
                            location=u"新竹市"
                        
                        elif(event.message.text.find(u"苗栗縣")!=-1):
                            location=u"苗栗縣"
                        
                        elif(event.message.text.find(u"彰化縣")!=-1):
                            location=u"彰化縣"
                        
                        elif(event.message.text.find(u"南投縣")!=-1):
                            location=u"南投縣"
                        
                        elif(event.message.text.find(u"雲林縣")!=-1):
                            location=u"雲林縣"
                        
                        elif(event.message.text.find(u"嘉義縣")!=-1):
                            location=u"嘉義縣"
                        
                        elif(event.message.text.find(u"嘉義市")!=-1):
                            location=u"嘉義市"
                        
                        elif(event.message.text.find(u"屏東縣")!=-1):
                            location=u"屏東縣"
                        
                        elif(event.message.text.find(u"宜蘭縣")!=-1):
                            location=u"宜蘭縣"
                        
                        elif(event.message.text.find(u"花蓮縣")!=-1):
                            location=u"花蓮縣"
                        
                        elif(event.message.text.find(u"臺東縣")!=-1):
                            location=u"臺東縣"
                        
                        elif(event.message.text.find(u"澎湖縣")!=-1):
                            location=u"澎湖縣"
                        
                        elif(event.message.text.find(u"金門縣")!=-1):
                            location=u"金門縣"
                        
                        elif(event.message.text.find(u"連江縣")!=-1):
                            location=u"連江縣"
                        
                        else:
                            location=u"臺南市"
                                            
                        weather=wea(location)
                        response_message=location.encode("utf-8")+weather.encode("utf-8")
                    #else repeat what the user type
                    else:
                        response_message=event.message.text
                        
                    line_bot_api.reply_message(

                        event.reply_token,
                        
                        TextSendMessage(text= response_message) 
                        
                        #event.message.text
                        
                    )



        return HttpResponse()

    else:

        return HttpResponseBadRequest()



