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

});

