# -*- coding: utf-8 -*-
from django.conf import settings

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden

from django.views.decorators.csrf import csrf_exempt



from linebot import LineBotApi, WebhookParser

from linebot.exceptions import InvalidSignatureError, LineBotApiError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

import jieba

import jieba.analyse

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

jieba.initialize()





def wea(locate,day):
    start=False
    day1=False
    request = urllib2.Request("http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-001.xml") #parse weather xml
    response = urllib2.urlopen(request)
    xml = response.read()
    fileout = file("doc1.xml","wb")
    fileout.write(xml)
    fileout.close()
    tree = ET.ElementTree(file='doc1.xml')
    root = tree.getroot()
    for child_of_root in root:
        if(child_of_root.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}dataset"):
            for dataset in child_of_root:
                if(dataset.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}location"):
                    for location in dataset:
                        if(location.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}locationName" and location.text==locate): 
                            start=True
                        if(location.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}weatherElement" and start==True ):
                            for weather in location:
                                if(weather.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}time"):
                                    for time in weather:
                                        if(time.tag=="{urn:cwb:gov:tw:cwbcommon:0.1}startTime" and time.text.find(str(day))!=-1):
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
                        
                    mes_seg=jieba.analyse.extract_tags(event.message.text, withWeight=False)
                    #if weather in text then parse weather xml
                    if(mes_seg[0]==u"天氣"):
                        if(mes_seg[2]==u"今天"):
                            day=today
                        elif(mes_seg[2]==u"明天"):
                            day=tommorrow
                        print day
                        #臺和台都可以讀到 可以不加市
                        locate=mes_seg[1]
                        if(locate[0]==u"台"):
                            locate=u"臺"+locate[1:]
                        if(len(locate)==2):
                            locate=locate[0:2]+u"市"
                        weather=wea(locate,day)
                        print type(weather)
                        t=mes_seg[2].encode("utf-8")+locate.encode("utf-8")+weather.encode("utf-8")
                    #else repeat what the user type
                    else:
                        t=event.message.text
                        
                    line_bot_api.reply_message(

                        event.reply_token,
                        
                        TextSendMessage(text= t) 
                        
                        #event.message.text
                        
                    )



        return HttpResponse()

    else:

        return HttpResponseBadRequest()



