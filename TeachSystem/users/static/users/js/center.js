$(document).ready(function () {

    // 注销登录按钮
    $("#signout").click(function () {
        weui.confirm("确认退出登录吗？",
            {
                title: "退出登录",
                buttons: [
                    {
                        label: '取消',
                        type: 'default',
                        onClick: function () {
                            console.log('取消')
                        }
                    },
                    {
                        label: '确定',
                        type: 'primary',
                        onClick: function () {
                            console.log('确定')
                            // 请求后台取消openid和kp相连
                            let studentid = $('#studentid').text()
                            console.log(studentid)
                            if(studentid){
                                $.get('/user/logout/', {studentid: studentid}, function (response) {
                                    if(response=="ok"){
                                    $(location).prop('href', 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx425d2aedb363e9c6&redirect_uri=https%3a%2f%2fwww.gdutwuwenda.cn%2fuser%2flogin%2f&response_type=code&scope=snsapi_base&state=123#wechat_redirect')
                                    }else {
                                        weui.alert(response+"貌似出错了！")
                                    }
                                })
                            }
                        }
                    }]
            });
    });

});