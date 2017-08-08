/**
 * Created by renhuijun on 2017/6/17.
 */
$(function(){
    var star_btn=$('#star_btn');
    star_btn.click(function(event){
        event.preventDefault();

        var post_id=$(this).attr('data-post-id');
        var is_star=$(this).attr('data-is-star');

        rhjajax.ajax({
            url:'/post_star/',
            type:'post',
            data:{
                post_id:post_id,
                is_star:is_star
            },
            success:function(data){
                if(data['code']==200){
                    msg=''
                    if(is_star=='1'){
                        msg='点赞操作成功!'
                    }else{
                        msg='取消赞成功!'
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