/**
 * Created by renhuijun on 2017/6/17.
 */
$(function(){
    var avatar_btn=$('#avatar_btn')
    xtqiniu.setUp({
        browse_button:'avatar_btn',
        success:function(up,file,info){
            var fileUrl=file.name
            avatar_btn.attr('src',fileUrl);
        }
    })
});

$(function(){
    var submit=$('#submit');
    submit.click(function(event){
        event.preventDefault()

        var username=$('input[name=username]').val();
        var realname=$('input[name=realname]').val();
        var qq=$('input[name=qq]').val();
        var avatar=$('#avatar_btn').attr('src');
        var signature=$('textarea[name=signature]').val();

        rhjajax.ajax({
            url:'/account/settings/',
            type:'post',
            data:{
                username:username,
                realname:realname,
                qq:qq,
                avatar:avatar,
                signature:signature

            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast(msg='恭喜个人信息保存成功！')
                    setTimeout(function(){
                        window.location.reload()
                    },1200)
                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })

    })
});