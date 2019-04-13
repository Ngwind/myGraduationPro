$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': $("input:hidden").val()
        }
    });

    //注册表单提交事件
    document.getElementById("login").addEventListener('click',
        function () {
           weui.form.validate("#changepwd",
               function (error) {
                   if(!error){
                       console.log($("#new_password_f").val())
                       if ($("#new_password_f").val() === $("#new_password_s").val()){
                           let loading = weui.loading('提交中...');
                                setTimeout(function () {
                                    loading.hide();
                                    $.post('/user/modpwd/', {
                                        "studentid": $("#studentid").text(),
                                        "old_password": $("#old_password").val(),
                                        "new_password": $("#new_password_s").val()
                                    },
                                        function (data,status) {
                                            console.log(data);
                                            if(data == "success"){
                                                weui.toast('操作成功', {
                                                    duration: 1000,
                                                    callback: function(){
                                                        $(location).prop('href', 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx425d2aedb363e9c6&redirect_uri=https%3a%2f%2fwww.gdutwuwenda.cn%2fuser%2flogin%2f&response_type=code&scope=snsapi_base&state=123#wechat_redirect')
                                                    }
                                                });
                                            }else {
                                                    if(data == "pwderror"){
                                                        weui.topTips('原密码错误，修改密码失败', 2000);
                                                    }else {
                                                        weui.topTips('未知错误，修改密码失败', 2000);
                                                    }
                                                }
                                        })
                                }, 1000);
                       }else {
                           weui.topTips('两次密码不一致', 2000);
                       }
                   }
               })
        });

});
