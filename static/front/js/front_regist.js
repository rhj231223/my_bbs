/**
 * Created by renhuijun on 2017/6/12.
 */
$(function(){
    var get_graph=$('#get_graph');
    get_graph.click(function(event){
        event.preventDefault()

        telephone=$('input[name=telephone]')


        rhjajax.ajax({
            url:'/account/sms_captcha/',
            type:'get',
            data:{
                telephone:telephone.val()
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast(msg='邮件发送成功')
                    var timeout=2*60;
                    get_graph.attr('disabled','disabled');
                    timer=setInterval(function(){
                        timeout--;
                        get_graph.text(timeout);
                        if(timeout<=0){
                            get_graph.removeAttr('disabled');
                            get_graph.text('发送验证码');
                            clearInterval(timer)
                        }

                    },1000)
                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })
    })
});
