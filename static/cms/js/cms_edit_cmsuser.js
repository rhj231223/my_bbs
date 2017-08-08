/**
 * Created by renhuijun on 2017/6/12.
 */
$(function(){
    var submit=$('#submit');
    submit.click(function(event){
        event.preventDefault()

        var user_id=$(this).attr('data-user-id');
        var selected_box=$(':checkbox:checked');
        var roles=[];
        selected_box.each(function(){
            role_id=$(this).val()
            roles.push(role_id)
        });

        rhjajax.ajax({
            url:'/edit_cmsuser/',
            type:'post',
            data:{
                user_id:user_id,
                roles:roles

            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast(msg='恭喜!用户组修改成功！')
                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })


    })
});

$(function(){
   var black_btn=$("#black_btn");
    black_btn.click(function(event){
        event.preventDefault()

        user_id=$(this).attr('data-user-id');
        is_active=parseInt($(this).attr('data-is-active'));

        rhjajax.ajax({
            url:'/blacklist/',
            type:'post',
            data:{
                user_id:user_id,
                is_active:is_active
            },
            success:function(data){
                if(data['code']==200){
                    msg='';
                    if(is_active==1){
                        msg='拉黑操作成功!'
                    }else{
                        msg='移除黑名单成功！'
                    }
                    xtalert.alertSuccessToast(msg=msg)
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