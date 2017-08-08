/**
 * Created by renhuijun on 2017/6/15.
 */
$(function(){
    var submit=$('#submit');
    submit.click(function(event){
        event.preventDefault()

        var post_id=$(this).attr('data-post-id');
        var content=window.editor.$txt.html();
        var origin_comment_id=$(this).attr('data-comment-id');

        rhjajax.ajax({
            url:'/add_comment/'+post_id+'/',
            type:'post',
            data:{
                post_id:post_id,
                content:content,
                origin_comment_id:origin_comment_id
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast(msg='评论发布成功!')
                    setTimeout(function(){
                        window.location='/post_detail/'+post_id+'/'
                    },1200)
                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })


    })
});
