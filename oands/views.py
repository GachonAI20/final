import io
from urllib import request as ur
from urllib.request import urlopen

import cloudinary.uploader
from django.shortcuts import render

# import pytesseract to convert text in image to string
import pytesseract

from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
import PIL
import urllib.request as ur
import io
from urllib.request import urlretrieve
# from django.views.decorators.csrf import csrf_exempt
# import json
# import urllib.request
from io import BytesIO
from PIL import Image
# from django.http import HttpRequest as rq

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


import time
# file='https://firebasestorage.googleapis.com/v0/b/ocr-test2-9b5be.appspot.com/images%2Fexxx.png?alt=media'
# file2 = 'https://firebasestorage.googleapis.com/v0/b/ocr-test2-9b5be.appspot.com/o/images%2Fexxx.png?alt=media&token=018185c4-b4d7-4ae6-8bb4-1bc127d55da0'
# storage = firebase.storage()
import sys

# Create your views here.

# connect with firebase
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        return ocr_summarize(request)


def ocr_summarize(request):
    text = ""
    error_message = ""
    request_img = ""
    # eng_to_kor=""
    try:
        request_img = request.data['image']
        request_img=request_img.replace("\/","/")
        text = img_open(str(request_img))

        # text = pytesseract.image_to_string(img, lang='kor+eng')
        # text = text.encode("ascii", "ignore")
        # text = text.decode()

        #     # translate eng to kor through Papago API
        #     client_id = "7cyuDLUY3kSNzmFs_i88" # 개발자센터에서 발급받은 Client ID 값
        #     client_secret = "NMYcZYMSNp" # 개발자센터에서 발급받은 Client Secret 값
        #     encText = urllib.parse.quote(text)
        #     data = "source=en&target=ko&text=" + encText
        #     url = "https://openapi.naver.com/v1/papago/n2mt"
        #     request = urllib.request.Request(url)
        #     request.add_header("X-Naver-Client-Id",client_id)
        #     request.add_header("X-Naver-Client-Secret",client_secret)
        #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        #     rescode = response.getcode()
        #
        #     if(rescode==200):
        #         response_body = response.read()
        #         result=response_body.decode('utf-8')
        #         d=json.loads(result)
        #         eng_to_kor = d['message']['result']['translatedText']
        #         # print(response_body)
        #         # print(eng_to_kor)
        #     else:
        #         eng_to_kor = "error code: "+rescode

    except:
        error_message = 'please check file contains text'

    # summarize text
    summarized_text=Summerization(text)

    context = {
        'text': text,
        'error_message': error_message,
        'request_img': request_img,
        'summarized_text': summarized_text
    }
    # return render(request, 'formpage.html', context)
    return JsonResponse(context)

def img_open(imgUrl):
    res = ur.urlopen(imgUrl).read()
    # Image open
    f=io.BytesIO(res)
    img=Image.open(f)
    text = pytesseract.image_to_string(img, lang='kor+eng')
    return text


# summarize text
# 한국어 추출 요약

from konlpy.tag import Okt
from typing import List
from lexrankr import LexRank

class OktTokenizer:
    okt: Okt = Okt()
    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens
def Summerization(text):
    # 1. init using Okt tokenizer
    mytokenizer: OktTokenizer = OktTokenizer()
    lexrank: LexRank = LexRank(mytokenizer)
    # text = ""

    # 2. summarize (like, pre-computation)
    lexrank.summarize(text)

    summerization = []

    # 3. probe (like, query-time)
    summaries: List[str] = lexrank.probe()
    for summary in summaries:
        summerization.append(summary)

    return summerization

