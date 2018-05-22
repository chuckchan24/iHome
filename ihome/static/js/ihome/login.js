function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    // TODO: 添加登录表单提交操作
    $(".form-login").submit(function(e){
        e.preventDefault();
        var mobile = $("#mobile").val();
        var passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }

        // 组织参数
        var params = {
            'mobile': mobile,
            'password': passwd
        };

        // 请求进行登录
        $.ajax({
            "url": "/api/v1.0/session",  // 请求的url地址
            "type": "post",  // 请求方式，默认是get
            "contentType": "application/json",
            "data": JSON.stringify(params),  // 请求时传递的数据
            "headers": {
                "X-CSRFToken": getCookie("csrf_token")
            },
            "success": function (resp) {
                if (resp.errno == '0') {
                    // success on login
                    location.href = 'index.html';
                }
                else {
                    // fail in login
                    $("#password-err span").html(resp.errmsg);
                    $("#password-err").show();
                }
            }
        });
    });
});
