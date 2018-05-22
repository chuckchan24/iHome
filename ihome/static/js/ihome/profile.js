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

$(document).ready(function () {
    // TODO: 在页面加载完毕向后端查询用户的信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0') {
            // 获取信息成功
            // 设置用户头像img标签src
            $('#user-avatar').attr('src', resp.data.avatar_url);
            // 设置用户用户名
            $('#user-name').val(resp.data.username);
        }
        else {
            // 获取信息失败
            alert(resp.errmsg);
        }
    })

    // TODO: 管理上传用户头像表单的行为
    $('#form-avatar').submit(function (e) {
        e.preventDefault();

        $(this).ajaxSubmit({
            'url': '/api/v1.0/user/avatar',
            'type': 'post',
            'headers': {
                'X-CSRFToken': getCookie('csrf_token')
            },
            'success': function (resp) {
                if (resp.errno == '0') {
                    // success on uploading
                    // 设置用户头像img标签src
                    $('#user-avatar').attr('src', resp.data.avatar_url);
                }
                else {
                    // fail in uploading
                    alert(resp.errmsg);
                }
            }
        })
    })

    // TODO: 管理用户名修改的逻辑
    $('#form-name').submit(function (e) {
        e.preventDefault();

        // 获取参数
        var username = $('#user-name').val();

        if (!username) {
            alert('请输入用户名');
            return;
        }

        var params = {
          'username': username
        };

        // 请求修改用户名
        $.ajax({
                "url": "/api/v1.0/user/name",  // 请求的url地址
                "type": "put",  // 请求方式，默认是get
                "contentType": "application/json",
                "data": JSON.stringify(params),  // 请求时传递的数据
                "headers": {
                    "X-CSRFToken": getCookie("csrf_token")
                },
                "success": function (resp) {
                    if (resp.errno == '0') {
                        // 修改成功
                        showSuccessMsg();
                    }
                    else {
                        // 修改失败
                        alert(resp.errmsg);
                    }
                }
        });

    })
});
