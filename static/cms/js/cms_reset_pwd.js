/**
 * Created by renhuijun on 2017/6/11.
 */
$(function(){
    var submit=$(':submit');
    submit.click(function(event){
        event.preventDefault();
        var old_password=$("input[name=old_password]");
        var new_password=$("input[name=new_password]");
        var new_password_repeat=$("input[name=new_password_repeat]");

        rhjajax.ajax({
            url:'/reset_pwd/',
            type:'post',
            data:{
                old_password:old_password.val(),
                new_password:new_password.val(),
                new_password_repeat:new_password_repeat.val()
            },
            success:function(data){
                if(data['code']==200){
                    old_password.val('');
                    new_password.val('');
                    new_password_repeat.val('');
                    xtalert.alertSuccessToast(msg='恭喜！密码修改成功')

                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })


    })
});
