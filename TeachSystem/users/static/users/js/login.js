// 把所有代码写进ready事件的函数中
$(document).ready(function () {

    // 显示错误提示。
    if (flag == '1') {
        weui.topTips('学号或密码错误', 3000);
    }

    //注册表单提交事件
    document.getElementById('login').addEventListener('click', function () {
        // weui.form.checkIfBlur('#registerForm');
        weui.form.validate('#registerForm', function (error) {
            // console.log(error);
            if (!error) {
                var loading = weui.loading('提交中...');
                setTimeout(function () {
                    loading.hide();
                    document.getElementById('registerForm').submit();
                }, 500);
            }
        });
    });
});
