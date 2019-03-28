import hashlib
from django.http import HttpResponse


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
    return "hello~"


def test_func(request):
    return HttpResponse('Hello world!')
