function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息


    // TODO: 管理实名信息表单的提交行为
    $('#form-auth').submit(function (e) {
        e.preventDefault();

        // 获取用户输入的实名认证信息
        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();

        if (!real_name || !id_card) {
            $('.error-msg').show();
            return;
        }

        // 组织参数
        var params = {
            'real_name': real_name,
            'id_card': id_card
        };
        $.ajax({
                "url": "/api/v1.0/user/auth",  // 请求的url地址
                "type": "post",  // 请求方式，默认是get
                "contentType": "application/json",
                "data": JSON.stringify(params),  // 请求时传递的数据
                "headers": {
                    "X-CSRFToken": getCookie("csrf_token")
                },
                "success": function (resp) {
                    if (resp.errno == '0') {
                        // 成功认证
                        // 警用真实姓名和身份证号输入框
                        $('#real-name').attr('disabled', true);
                        $('#id-card').attr('disabled', true);
                        // 隐藏实名认证提交按钮
                        $('.btn-success').hide();
                    }
                    else if (resp.errno == '4101') {
                        // 用户未登录
                        location.href = 'login.html';
                    }
                    else {
                        // 认证失败
                        alert(resp.errmsg);
                    }
                }
        });

    })

});