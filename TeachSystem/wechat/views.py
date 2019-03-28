import hashlib
import requests
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply

@csrf_exempt
def we_chat_main(request):
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echo_str = request.GET.get('echostr', None)
        # 服务器配置中的token
        token = '19970825'
        # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hash_list = [token, timestamp, nonce]
        hash_list.sort()
        hash_str = ''.join([s for s in hash_list])
        hash_str = hashlib.sha1(hash_str.encode("utf-8")).hexdigest()
        if hash_str == signature:
            return HttpResponse(echo_str)
        else:
            return HttpResponse("field")
    else:
        other_content = auto_reply(request)
        return HttpResponse(other_content)


def auto_reply(request):
    wx_xml = request.body
    msg = parse_message(wx_xml)
    if msg.type == "text":
        send_data = {
            "perception":
                {
                    "inputText":
                        {
                            "text": None
                        }
                },
            "userInfo":
                {
                    "apiKey": "1d6a5a9e97f74ef085e22e65d3f6efff",
                    "userId": "123456"
                }
        }
        ul_url = "http://openapi.tuling123.com/openapi/api/v2"
        send_data["perception"]["inputText"]["text"] = msg.content
        r = requests.post(url=ul_url, data=json.dumps(send_data))
        text_reply = create_reply(r.json()['results'][0]['values']['text'], message=msg)
    else:
        text_reply = create_reply('我只会看文字消息', message=msg)
    return text_reply.render()


def test_func(request):
    return HttpResponse('Hello world!')

