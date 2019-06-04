# wechatpy是一个开发微信公众号的第三方sdk
from wechatpy import WeChatClient

client = WeChatClient(appid="wx425d2aedb363e9c6", secret="57a89d10bbb0754f07b75825491b627e")
print(client.access_token)
json_mc = client.menu.create({  # 设置公众号菜单
    "button":[
        {
            "type":"view",
            "name":"开始学习",
            "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx425d2aedb363e9c6&redirect_uri=https%3a%2f%2fwww.gdutwuwenda.cn%2fcourse%2fcourselist%2f&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
        },
        {
            "type":"view",
            "name":"个人中心",
            "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx425d2aedb363e9c6&redirect_uri=https%3a%2f%2fwww.gdutwuwenda.cn%2fuser%2flogin%2f&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
        },
        {
            "name":"教务相关",
            "sub_button":[
                {
                    "type":"view",
                    "name":"成绩查询",
                    "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx425d2aedb363e9c6&redirect_uri=https%3a%2f%2fwww.gdutwuwenda.cn%2fcourse%2fcoursescore%2f&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                },
                {
                    "type":"view",
                    "name":"意见反馈",
                    "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx425d2aedb363e9c6&redirect_uri=https%3a%2f%2fwww.gdutwuwenda.cn%2fuser%2ffeedback%2f&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                }
            ]
        }
    ]
})
print(json_mc)
