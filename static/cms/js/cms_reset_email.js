/**
 * Created by renhuijun on 2017/6/11.
 */
$(function(){
   var get_captcha=$('#get_captcha');
   get_captcha.css('cursor','pointer');
    get_captcha.click(function(event){
        event.preventDefault();

        var email=$('input[name=email]');

        rhjajax.ajax({
            url:'/get_capthca/',
            type:'get',
            data:{
                email:email.val()
            },
            success:function(data){
             if(data['code']==200){
                 xtalert.alertSuccessToast('邮件发送成功！');

                 }else{
                 xtalert.alertInfo(msg=data['message'])
             }
            }


        })

    })
});

$(function(){
    var submit=$('#sub');
    submit.click(function(event){
        event.preventDefault();

        var email=$('input[name=email]');
        var captcha=$('input[name=captcha]');

        rhjajax.ajax({
            url:'/reset_email/',
            type:'post',
            data:{
                email:email.val(),
                captcha:captcha.val()
            },
            success:function(data){
                if(data['code']==200){
                    email.val('');
                    captcha.val('');
                    xtalert.alertSuccessToast(msg='邮箱修改成功!')
                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })

    })

});

