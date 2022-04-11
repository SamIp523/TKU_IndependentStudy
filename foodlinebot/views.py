from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core import serializers

import re
from linebot.models import *
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def hello_view(request):
    return render(request, 'Homepage.html')

def SuitProduct(request):
    return render(request, 'Suit_Product.html')

def SuitCos(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='Cosmetic',uid=id[0].uid).filter(suitable='適合')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    
    return render(request, 'Suit_Cosmetics.html',
                    {
                      'product': prods
                    }
                 )

def SuitFou(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='Base',uid=id[0].uid).filter(suitable='適合')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    
    return render(request, 'Suit_Foundation.html',
                    {
                      'product': prods
                    }
                 )

def SuitSkin(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='SkinCare',uid=id[0].uid).filter(suitable='適合')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    
    return render(request, 'Suit_SkinCare.html',
                     {
                      'product': prods
                    }
                 )

def NonSuitProduct(request):
    return render(request, 'nonSuit_Product.html')

def NonSuitCos(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='Cosmetic',uid=id[0].uid).filter(suitable='不適合')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    return render(request, 'nonSuit_Cosmetics.html',
                    {
                      'product': prods
                    }
                 )

def NonSuitSkin(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='SkinCare',uid=id[0].uid).filter(suitable='不適合')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    return render(request, 'nonSuit_SkinCare.html',
                    {
                      'product': prods
                    }
                 )

def NonSuitFou(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='Base',uid=id[0].uid).filter(suitable='不適合')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    
    return render(request, 'nonSuit_Foundation.html',
                    {
                      'product': prods
                    }
                 )

def WaitProduct(request):
    return render(request,'wait_Product.html')

def WaitProductCos(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='Cosmetic',uid=id[0].uid).filter(suitable='未知')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    
    return render(request,'wait_Cosmetics.html',
                     {
                      'product': prods
                    }
                 )

def WaitProductFou(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='Base',uid=id[0].uid).filter(suitable='未知')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    return render(request,'wait_Foundation.html',
                    {
                      'product': prods
                    }
                 )

def WaitProductCare(request):
    id = Temp.objects.all()
    prod = User_Product.objects.filter(ptype='SkinCare',uid=id[0].uid).filter(suitable='未知')
    json_serializer = serializers.get_serializer("json")()
    prods = json_serializer.serialize(prod)
    
    return render(request,'wait_SkinCare.html',
                    {
                      'product': prods
                    }
                 )






@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                uid = event.source.user_id

                if event.message.text == '紀錄':
                    Temp.objects.all().delete()
                    message = TemplateSendMessage(
                        alt_text='記錄Template無法顯示',
                        template=ButtonsTemplate(
                            thumbnail_image_url='https://cheeek.me/wp-content/uploads/2018/09/117244283.jpg',
                            title='紀錄',
                            text='紀錄之產品將存於已記錄',
                            actions=[
                                MessageTemplateAction(
                                    label='手動輸入', text='紀錄產品'
                                ),
                                MessageTemplateAction(
                                    label='掃描QRcode(限Android)', text='掃描QRcode'
                                ),
                                MessageTemplateAction(
                                    label='掃描產品條碼', text='掃描產品條碼'
                                ),
                                MessageTemplateAction(
                                    label='查看已記錄', text='查看已記錄商品'
                                )
                            ]
                        )
                    )
                    line_bot_api.reply_message(event.reply_token, message)
                elif event.message.text == '搜尋':
                    Temp.objects.all().delete()
                    message = TemplateSendMessage(
                        alt_text='搜尋Template無法顯示',
                        template=ButtonsTemplate(
                            thumbnail_image_url='https://cheeek.me/wp-content/uploads/2018/09/117244283.jpg',
                            title='搜尋',
                            text='僅搜尋產品成分',
                            actions=[
                                MessageTemplateAction(
                                    label='搜尋產品', text='搜尋產品'
                                )
                            ]
                        )
                      )

                    line_bot_api.reply_message(event.reply_token, message)
                elif event.message.text == '比對':
                    Temp.objects.all().delete()
                    message = TemplateSendMessage(
                        alt_text='比對Template無法顯示',
                        template=ButtonsTemplate(
                            thumbnail_image_url='https://cheeek.me/wp-content/uploads/2018/09/117244283.jpg',
                            title='比對',
                            text='比對與已紀錄之產品成分是否適合',
                            actions=[
                                MessageTemplateAction(
                                    label='手動輸入', text='比對產品'
                                ),
                                MessageTemplateAction(
                                    label='掃描QRcode', text='掃描QRcode'
                                ),
                                MessageTemplateAction(
                                    label='掃描產品條碼', text='掃描產品條碼'
                                )
                            ]
                        )
                    )

                    line_bot_api.reply_message(event.reply_token, message)
                elif event.message.text == '掃描QRcode':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous,uid,event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)    
                
                elif event.message.text == '掃描產品條碼':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous,uid,event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)
                    
                elif event.message.text == '紀錄產品':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous, uid, event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)
                
                elif event.message.text == '美妝新聞':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous, uid, event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)
                
                elif event.message.text == '推薦':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous, uid, event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)    
                
                elif event.message.text == '查看已記錄商品':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous, uid, event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)
                                
                elif event.message.text == '搜尋產品':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous, uid, event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.text == '比對產品':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous, uid, event.message.text)
                    line_bot_api.reply_message(event.reply_token, message)
                
                elif event.message.text == '回報':
                    Temp.objects.all().delete()
                    updatestate(uid, 1, 0)
                    status = get_statusDB(uid)
                    message = message_continuous(status.continuous, uid, event.message.text) 
                    line_bot_api.reply_message(event.reply_token, message)
                    
                else:
                    try:
                        status = get_statusDB(uid)
                    except:
                        updatestate(uid,0,0)
                        message = TextSendMessage(text='歡迎使用美妝守門人\n已幫你建立基本資訊供後續功能使用')
                        line_bot_api.reply_message(event.reply_token, message)

                    if (status.continuous == 0 and status.cnt == 0):
                        updatestate(uid, 0, 0)
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        message = message_continuous(status.continuous, uid, event.message.text)
                        line_bot_api.reply_message(event.reply_token, message)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def updatestate(userid, count, countin):
    states = CustomerState.objects.filter(uid=userid)
    if not states:
        states = CustomerState.objects.create(uid=userid, continuous=countin, cnt=count)
    else:
        states = CustomerState.objects.filter(uid=userid).update(continuous=countin, cnt=count)


def get_statusDB(userid):
    ans = CustomerState.objects.get(uid=userid)
    # db.close()
    return ans


def message_continuous(countin, uid, userMessage):
    msg = ''
    #20
    if countin == 0 and userMessage == '紀錄產品':
        message = []
        message = TextSendMessage(text='請問需要記錄產品/刪除產品',quick_reply=QuickReply(
            items=[
                    QuickReplyButton(
                        image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/13898481211537356036-512.png',
                        action=MessageAction(label="紀錄產品", text="儲存產品")
                        ),
                    QuickReplyButton(
                        image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/2790131631558965374-512.png',
                        action=MessageAction(label="刪除產品", text="刪除產品")
                    )
                ]
            )
        )
        updatestate(uid, 1, 20)
    
    elif countin == 20 and userMessage == '刪除產品':
            items = User_Product.objects.filter(uid=uid)
            if len(items) == 1:
                itname = items[0].unfit_prod
                message = TextSendMessage(text='以下是您已經儲存的產品，請點擊該產品進行刪除',quick_reply=QuickReply(
                    items=[
                            QuickReplyButton(
                                image_url='',
                                action=MessageAction(label=items[0].unfit_prod[:10], text=items[0].unfit_prod[:10])
                                )
                        ]
                    )
                )
            elif len(items) == 2:
                message = TextSendMessage(text='以下是您已經儲存的產品，請點擊該產品進行刪除',quick_reply=QuickReply(
                    items=[
                            QuickReplyButton(
                                image_url='',
                                action=MessageAction(label=items[0].unfit_prod[:10], text=items[0].unfit_prod[:10])
                                ),
                            QuickReplyButton(
                                image_url='',
                                action=MessageAction(label=items[1].unfit_prod[:10], text=items[1].unfit_prod[:10])
                                ),
                        ]
                    )
                )
            else:
                message = TextSendMessage(text='以下是您已經儲存的產品，請點擊該產品進行刪除',quick_reply=QuickReply(
                    items=[
                            QuickReplyButton(
                                image_url='',
                                action=MessageAction(label=items[0].unfit_prod[:10], text=items[0].unfit_prod[:10])
                                ),
                            QuickReplyButton(
                                image_url='',
                                action=MessageAction(label=items[1].unfit_prod[:10], text=items[1].unfit_prod[:10])
                                ),
                            QuickReplyButton(
                                image_url='',
                                action=MessageAction(label=items[2].unfit_prod[:10], text=items[2].unfit_prod[:10])
                                )
                        ]
                    )
                )
            updatestate(uid, 1, 21)
            
    elif countin == 21:
        User_Product.objects.get(uid=uid,unfit_prod=userMessage).delete()
        message = TextSendMessage(text='已將'+userMessage+'刪除成功!')
        updatestate(uid, 0, 0)
    
    
    elif countin == 20 and userMessage == '儲存產品':
            message = TextSendMessage(text='請問需要紀錄的是哪一種產品，請選擇該產品是否與自身合適',quick_reply=QuickReply(
                items=[
                        QuickReplyButton(
                            image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/13126182031582884276-512.png',
                            action=MessageAction(label="適合產品", text="適合產品")
                            ),
                        QuickReplyButton(
                            image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/16618812301557740370-512.png',
                            action=MessageAction(label="不適合產品", text="不適合產品")
                        ),
                        QuickReplyButton(
                            image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/9411509341557740371-512.png',
                            action=MessageAction(label="不確定產品", text="不確定產品")
                        )
                    ]
                )
            )
            updatestate(uid, 1, 22)
    
    elif countin == 22:
        Temp.objects.create(uid=uid, product=userMessage)
        message = TextSendMessage(text='請輸入品牌名稱')
        updatestate(uid, 1, 23)
        
    elif countin == 23:
        prod = []
        try:
            userpro = CosmeticProduct.objects.filter(brand__icontains=userMessage)
            for i in range(len(userpro)):
                if len(userpro[i].pname)>10:
                    pass
                else:
                    prod.append(userpro[i])

            message = []
            message.append(TextSendMessage(text='請選擇想要儲存的產品'))
            if len(prod) == 1:
                it = TemplateSendMessage(
                    alt_text='圖片失效or資料庫未有資料',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url=prod[0].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[0].pname,
                                    text=prod[0].pname,
                                    data='action=buy&itemid=1'
                                )
                            )
                        ]
                    )
                )
            elif len(prod) == 2:
                it = TemplateSendMessage(
                    alt_text='圖片失效or資料庫未有資料',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url=prod[0].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[0].pname,
                                    text=prod[0].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[1].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[1].pname,
                                    text=prod[1].pname,
                                    data='action=buy&itemid=1'
                                )
                            )
                        ]
                    )
                )
            elif len(prod) == 3:
                it = TemplateSendMessage(
                    alt_text='圖片失效or資料庫未有資料',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url=prod[0].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[0].pname,
                                    text=prod[0].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[1].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[1].pname,
                                    text=prod[1].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[2].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[2].pname,
                                    text=prod[2].pname,
                                    data='action=buy&itemid=1'
                                )
                            )
                        ]
                    )
                )
            elif len(prod) == 4:
                it = TemplateSendMessage(
                    alt_text='圖片失效or資料庫未有資料',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url=prod[0].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[0].pname,
                                    text=prod[0].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[1].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[1].pname,
                                    text=prod[1].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[2].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[2].pname,
                                    text=prod[2].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[3].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[3].pname,
                                    text=prod[3].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                        ]
                    )
                )
            else:
                it = TemplateSendMessage(
                    alt_text='圖片失效or資料庫未有資料',
                    template=ImageCarouselTemplate(
                        columns=[
                            ImageCarouselColumn(
                                image_url=prod[0].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[0].pname,
                                    text=prod[0].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[1].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[1].pname,
                                    text=prod[1].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[2].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[2].pname,
                                    text=prod[2].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[3].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[3].pname,
                                    text=prod[3].pname,
                                    data='action=buy&itemid=1'
                                )
                            ),
                            ImageCarouselColumn(
                                image_url=prod[4].picurl,
                                action=PostbackTemplateAction(
                                    label=prod[4].pname,
                                    text=prod[4].pname,
                                    data='action=buy&itemid=1'
                                )
                            )
                        ]
                    )
                )                

            message.append(it)
            updatestate(uid, 1,24)
        except:
            message = []
            message.append(TextSendMessage(text='找不到相關產品的資訊，非常抱歉!'))
            message.append(StickerSendMessage(package_id=11537,sticker_id=52002755))
            updatestate(uid,0,0)
    
    elif countin == 24:
            pnamepic = CosmeticProduct.objects.get(pname=userMessage)
            if pnamepic.id > 2400:
                de = pnamepic.id-2000
                ingred = CosmeticIngredient.objects.get(id=de)
            else:
                ingred = CosmeticIngredient.objects.get(id=pnamepic.id)
            fit = Temp.objects.get(uid=uid).product
            if fit == '適合產品':
                    User_Product.objects.create(
                        suitable='適合',
                        uid=uid,
                        unfit_prod=userMessage,
                        picurl=pnamepic.picurl,
                        ingredient=ingred.ingredient,
                        acne=ingred.acne,
                        pchar=ingred.pchar,
                        dalton=ingred.dalton,
                        safeness=ingred.safeness,
                        score=ingred.score,
                        stimulation=ingred.stimulation,
                        ptype=pnamepic.kind
                    )
            elif fit == '不適合產品':
                    User_Product.objects.create(
                        suitable='不適合',
                        uid=uid,
                        unfit_prod=userMessage,
                        picurl=pnamepic.picurl,
                        ingredient=ingred.ingredient,
                        acne=ingred.acne,
                        pchar=ingred.pchar,
                        dalton=ingred.dalton,
                        safeness=ingred.safeness,
                        score=ingred.score,
                        stimulation=ingred.stimulation,
                        ptype=pnamepic.kind
                    )
            else:
                 User_Product.objects.create(
                         suitable='未知',
                         uid=uid,
                         wait_prod=userMessage,
                         picurl=pnamepic.picurl,
                         ingredient=ingred.ingredient,
                         acne=ingred.acne,
                         pchar=ingred.pchar,
                         dalton=ingred.dalton,
                         safeness=ingred.safeness,
                         score=ingred.score,
                         stimulation=ingred.stimulation,
                         ptype=pnamepic.kind
                    )

            message = []
            message.append(TextSendMessage(text='儲存完成!'))
            message.append(StickerSendMessage(package_id=11537, sticker_id=52002734))        
            Temp.objects.all().delete()
            updatestate(uid, 0, 0)
    #30
    elif countin == 0 and userMessage == '掃描產品條碼':
        message = TemplateSendMessage(
            alt_text='掃描產品條碼Template無法顯示',
            template=ButtonsTemplate(
                title='掃描產品條碼',
                text='進入後將產品條碼拍照後轉為文字並將條碼之對應數字傳回對話訊息',
                actions=[
                    URITemplateAction(
                        label='掃描產品條碼', uri='https://line.me/R/nv/camera/ocr'
                    )
                ]
            )
        )
        updatestate(uid,1,30)
    
    elif countin == 30:
        message = []
        productn = CosmeticProduct.objects.get(pname=userMessage)
        message.append(TextSendMessage(text=productn))
        message.append(StickerSendMessage(package_id=11539, sticker_id=52114131))
        updatestate(uid,0,0)
    #40
    elif countin == 0 and userMessage == '美妝新聞':
        message = []
        message.append(TextSendMessage(text='提供最新的美妝網站連結供您參考'))
        message.append(TextSendMessage(text='https://www.urcosme.com/beautynews'))
        message.append(TextSendMessage(text='https://www.elle.com/tw/beauty/news/'))
        message.append(StickerSendMessage(package_id=11537, sticker_id=52002738))
    #50
    elif countin == 0 and userMessage == '查看已記錄商品':
        Temp.objects.create(uid=uid)
        message = TemplateSendMessage(
            alt_text='已記錄商品頁面損壞',
            template=ButtonsTemplate(
                title='查看已記錄商品',
                text='點擊後可隨意瀏覽已儲存商品種類',
                actions=[
                    URITemplateAction(
                        label='開啟頁面', uri='https://lee.tku3a.nctu.me/hello/'
                    )
                ]
            )
        )
        updatestate(uid, 0, 0)
    
    #60
    elif countin == 0 and userMessage == '掃描QRcode':
        message = TemplateSendMessage(
            alt_text='掃描QRCode Template無法顯示',
            template=ButtonsTemplate(
                title='掃描QRCode',
                text='對準發票上之QRCode，掃描後結果即顯示於聊天室',
                actions=[
                    URITemplateAction(
                        label='掃描QRCode(限Android)', uri='https://liff.line.me/1654432888-3nAgx1WL'  # 這行要改
                    )
                ]
            )
        )
        
        updatestate(uid, 1, 8)
    
    elif countin == 8:
       cnt = 1 
       try:
            item = str(qrcode_detail(userMessage))
            cnt += 1
       except:
            pass
       message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='請確認回覆以下是否為您的發票明細:\n' + item,
                actions=[
                    MessageTemplateAction(
                        label='確認',
                        text='儲存商品'
                    ),
                    MessageTemplateAction(
                        label='取消',
                        text='取消儲存'
                    ),
                ]
            )
        )
       #Temp.objects.create(uid=uid,pname=item)
       updatestate(uid,1,9)
    
    elif countin == 9:
        if userMessage == '儲存商品':
            #item = Temp.objects.get(uid=uid)
            #pro = str(item.pname)
            #User_Product.objects.create(uid=uid,wait_prod=pro)
            message = []
            message.append(TextSendMessage(text='完成儲存!'))
            message.append(StickerSendMessage(package_id=2, sticker_id=516))
        else:
            pass
            message = TextSendMessage(text='結束儲存')
        Temp.objects.all().delete()
        updatestate(uid, 0, 0)
    
    
    

    
    #70
    elif countin == 0 and userMessage == '搜尋產品':
        updatestate(uid, 1, 4)
        message = TextSendMessage(text='請輸入你想要搜尋的產品品牌')
    elif countin == 4:
        updatestate(uid, 1, 5)
        message = TextSendMessage(text='請輸入你想要搜尋的商品名稱')
    elif countin == 5:
        res = ''
        result = search_productDB(userMessage)
        if type(result) == str:
            message = []
            message.append(TextSendMessage(text=result))
            message.append(TextSendMessage(text='非常抱歉！我們暫時沒有收錄這款產品，如果您願意的話可以回報給客服喔！\n'))
            message.append(StickerSendMessage(package_id=11538, sticker_id=51626522))
        else:
            sp = result.ingredient.split(',')
            for i in sp:
                if i == '"':
                    pass
                else:
                    i = i.replace('[','')
                    i = i.replace(']','')
                    i = i.replace('\'','')
                    res += i + '\n'
            result = '找到'+userMessage+'的成分了!\n'+res
            message = []
            message.append(TextSendMessage(text=result))
            message.append(StickerSendMessage(
                package_id=11539, sticker_id=52114116))
        updatestate(uid, 0, 0)
        
    #80
    elif countin == 0 and userMessage == '推薦':

        message = []
        message.append(TextSendMessage(text='歡迎使用推薦系統!~\n我們的推薦系統可幫助你找到適合且定價優惠的產品'))
        message.append(TextSendMessage(text='請問你的膚質是哪一種類型呢?!~''\uDBC0\uDC84'))
        message.append(TemplateSendMessage(
                            alt_text='確認按鈕失效',
                            template=ConfirmTemplate(text='點選你的膚質狀況',
                            actions=[
                            MessageTemplateAction(
                                label='乾性',
                                text='乾性'
                            ),
                            MessageTemplateAction(
                                label='油性',
                                text='油性'
                            )
                        ]
                    )
                )
            )
        updatestate(uid,1,10)
    
    elif countin == 10:
        Temp.objects.create(uid=uid,userkind=userMessage)
        message = TextSendMessage(text='請問需要哪一種類型的產品', quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    image_url='https://www.flaticon.com/premium-icon/icons/svg/1196/1196219.svg',
                    action=MessageAction(label="洗臉乳", text="洗臉乳")
                    ),
                    QuickReplyButton(
                        image_url='https://cdn0.iconfinder.com/data/icons/beauty-products-3/128/Sunblock-4-512.png',
                        action=MessageAction(label="防曬", text="防曬")
                    ),
                    QuickReplyButton(
                        image_url='https://cdn2.iconfinder.com/data/icons/beauty-33/64/makeup-remover-cosmetics-pad-cleanser-wash-face-512.png',
                        action=MessageAction(label="卸妝", text="卸妝")
                    ),
                    QuickReplyButton(
                        image_url='https://image.flaticon.com/icons/png/512/856/856601.png',
                        action=MessageAction(label="化妝水", text="化妝水")
                    ),
                    QuickReplyButton(
                        image_url='https://cdn0.iconfinder.com/data/icons/beauty-products-3/128/Face_moisturizer-4-512.png',
                        action=MessageAction(label="乳液", text="乳液")
                    ),
                    QuickReplyButton(
                        image_url='https://cdn0.iconfinder.com/data/icons/beauty-products-3/128/Essence-4-512.png',
                        action=MessageAction(label="精華", text="精華")
                    ),
                    QuickReplyButton(
                        image_url='https://cdn0.iconfinder.com/data/icons/beauty-products-3/128/Sheet_mask-4-512.png',
                        action=MessageAction(label="面膜", text="面膜")
                    )
                ]
            )
        )
        updatestate(uid, 1,11)
    
    
    elif countin == 11:
        userprofile = Temp.objects.get(uid=uid) #油性/乾性取出
        kindpro = CosmeticProduct.objects.filter( #找出油/乾性 以及 種類的產品
            product=userMessage
        ).filter(
            suitable=userprofile.userkind
        )
        Temp.objects.all().delete()
        #temp建立產品名稱 品牌 價格 種類
        for i in range(len(kindpro)):
            Temp.objects.create(
                uid=uid,
                pname=kindpro[i].pname,
                price=kindpro[i].price,
                brand=kindpro[i].brand
            )
        message = TextSendMessage(text='請輸入你目前的預算金額')
        updatestate(uid,1,12)
    
    
    elif countin == 12:
        message = []     
        msg = ''
        result = recommand(uid, userMessage)          
        if not result:
            message.append(TextSendMessage(text='沒有可推薦的商品，抱歉!'))
        elif len(result)<3:
            for i in range(len(result)):
                msg += str(i+1)+'.產品名稱:'+str(result[i].pname)+'\n品牌:'+str(result[i].brand)+'\n價格:'+str(result[i].price)+'\n'
        else:
            for i in range(3):
                msg += str(i+1)+'.產品名稱:'+str(result[i].pname)+'\n品牌:'+str(result[i].brand)+'\n價格:'+str(result[i].price)+'\n'
            message.append(TextSendMessage(text='以下是我們根據系統分析後推薦給你的商品'))
            message.append(TextSendMessage(text=msg))
            message.append(StickerSendMessage(package_id=1, sticker_id=13))
            
        Temp.objects.all().delete()
        updatestate(uid, 0, 0)
    
    #90
    elif countin == 0 and userMessage == '回報':
        message = StickerSendMessage(
            package_id=11537, sticker_id=52002749,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/6931268111571662152-512.png',
                        action=MessageAction(label="圖片顯示錯誤", text="圖片顯示錯誤")
                    ),
                    QuickReplyButton(
                        image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/14393104921553233145-512.png',
                        action=MessageAction(label="網址位址錯誤", text="網址位址錯誤")
                    ),
                   QuickReplyButton(
                        image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/5994997231555590637-512.png',
                        action=MessageAction(label="產品資訊錯誤", text="產品資訊錯誤")
                    ),
                    QuickReplyButton(
                        image_url='https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/5537241051579156644-512.png',
                        action=MessageAction(label="查無品項或成分", text="查無品項或成分")
                    ),
                    QuickReplyButton(
                        image_url="https://upload-icon.s3.us-east-2.amazonaws.com/uploads/icons/png/833566731594444098-512.png",
                        action=MessageAction(label="其他", text="其他")
                    ),
                ]
            )
        )
        updatestate(uid, 1, 6)
    elif countin == 6:
        message = TextSendMessage(text='感謝你的回報，我們會盡速處理')
        updatestate(uid, 0, 0)


    #100    
    elif countin == 0 and userMessage == '比對產品':
        message = TextSendMessage(text='請輸入想要比對的產品名稱')
        updatestate(uid, 1, 7)
    elif countin == 7:
        message = Compare_All_Product(uid,userMessage)
        updatestate(uid, 0, 0)
    else:
        updatestate(uid, 0, 0)
        message = TextSendMessage(text=msg+'請正確重新使用功能\n')
    

    return message


def update_productDB(count, uid, userMessage):
    if count == 1:
        product = Product.objects.create(uid=uid, pbrand=userMessage)
    else:
        product = Product.objects.create(uid=uid, pname=userMessage)




def search_productDB(productname):
    try:
        ingre = CosmeticProduct.objects.filter(pname__icontains=productname)
        if ingre[0].id > 2000:
            ingred2 = CosmeticIngredient.objects.get(id=(ingre[0].id-2000))
        else:
            ingred2 = CosmeticIngredient.objects.get(id=ingre[0].id)
    except:
        ingred = '查無此產品資訊'
    return ingred2

def Compare_All_Product(userid, qName):
    # 從資料庫取得資料
    message = []
    qIngre = []
    found = -1
    try:
        ingred = CosmeticIngredient.objects.filter(pname__icontains=qName)
        qIngre = ingred[0].ingredient.split(',')
        found = 1
        unfit = []
        checkIngre = []
        checkProd = []
        # Start to compare suitable & nonsuitable
        fitprod = []
        unfitprod = []


        
        if len(qIngre) > 0:
            try:
                data = User_Product.objects.filter(uid=userid)
                for i in range(len(data)):
                    if data[i].suitable == '不適合':
                        unfitprod.append(data[i])
                    else:
                        fitprod.append(data[i])
                for i in range(len(qIngre)):
                    for j in range(len(unfitprod)):
                        try:
                            unsafe = unfitprod[j].ingredient.find(qIngre[i])   
                            if unsafe != -1:
                                checkProd.append(unfitprod[j].unfit_prod)      
                                checkIngre.append(qIngre[i])            
                        except:
                            pass
            except Exception as e:
                message.append(TextSendMessage(text='麻煩請先紀錄您曾經使用過的產品，再利用比對功能喔！\n'))
                message.append(TextSendMessage(text=str(e)))
        
            

            for i in range(len(checkIngre)):
                 for j in range(len(fitprod)):
                    try:
                        safe = fitprod[j].ingredient.find(qIngre[i])
                        if safe != -1:
                            checkProd.remove(fitprod[j].unfit_prod)
                            checkIngre.remove(qIngre[i])
                    except:
                        pass
        

        if found == 1:
            try:
                msg = ''
                if len(checkProd) > 0:
                    unique_set = set(checkProd)
                    checkProd = list(unique_set)
                    for i in range(len(checkProd)):
                        msg += str(i+1)+'.'+checkProd[i]+'\n'
                    message.append(TextSendMessage(text='這個產品有包含過去讓您不適的產品成分，如有需要建議查詢醫生的專業意見喔！'))
                    message.append(TextSendMessage(text='以下商品成分與輸入商品成分皆會造成不適\n'+msg))
                    message.append(StickerSendMessage(package_id=11538, sticker_id=51626531))
                else:
                    message.append(TextSendMessage(text='這個產品成分與妳現在適用產品成分一樣安全，可以考慮購入哦！'))
                    message.append(StickerSendMessage(package_id=11539, sticker_id=52114115))
            except Exception as e:
                message.append(TextSendMessage(text='產品查詢成分錯誤發生，請回報'))
                message.append(TextSendMessage(text=str(e)))
                
        else:
            message.append(TextSendMessage(text='查無產品成分'))
            
    except Exception as e:
        message.append(TextSendMessage(text='非常抱歉！我們暫時沒有收錄這款產品，如果您願意的話可以回報給客服喔！\n'))
        message.append(TextSendMessage(text=str(e)))
        message.append(StickerSendMessage(package_id=11538, sticker_id=51626522))

    return message

def recommand(uid,userprice):
    msg = ''
    product = Temp.objects.filter(uid=uid)# 放產品名
    pname = []
    price = []
    brand = []
    for i in range(len(product)):
        pname.append(product[i].pname)
        price.append(product[i].price)
        brand.append(product[i].brand)

    price2 = []
    usp = int(userprice)
    deletprice=[]
    
    cnt=0
    for i in range(len(product)):
        x=(usp-price[i])
        if x<-200:
            pname.remove(pname[i-cnt])
            brand.remove(brand[i-cnt])
            a=price[i]
            deletprice.append(a)
            cnt+=1
            continue
        y=x*x
        price2.append(y)
    
    



