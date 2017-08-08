/**
 * Created by renhuijun on 2017/6/17.
 */
$(function(){
    var black_btn=$('#black_btn');
    black_btn.click(function(event){
        event.preventDefault();

       user_id=$(this).attr('data-user-id');
        is_active=$(this).attr('data-is-active')

        rhjajax.ajax({
            url:'/edit_frontuser/',
            type:'post',
            data:{
               user_id:user_id,
                is_active:is_active
            },
            success:function(data){
                if(data['code']==200){
                    msg='';
                    if(is_active=='0'){
                        msg='加入黑名单成功!'
                    }else{
                        msg='移除黑名单成功!'
                    }
                    xtalert.alertSuccessToast(msg=msg);
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
