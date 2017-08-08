/**
 * Created by renhuijun on 2017/6/14.
 */
$(function(){
    var submit=$('#submit');
    submit.click(function(event){
        event.preventDefault();

        var title=$('input[name=title]');
        var board_id=$('select[name=board_id]');
        var content=window.editor.$txt;
        var graph_captcha=$('input[name=graph_captcha]')

        rhjajax.ajax({
            url:'/add_post/',
            type:'post',
            data:{
                title:title.val(),
                board_id:board_id.val(),
                content:content.html(),
                graph_captcha:graph_captcha.val()
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertConfirm({
                        text:'恭喜！帖子发布成功，是否再发一篇',
                        confirmText:'再发一篇',
                        cancelText:'返回首页',
                        confirmCallback:function(){
                            title.val('');
                            window.editor.clear();
                            graph_captcha.val('');
                            $('graph_btn').click()
                        },
                        cancelCallback:function(){
                            setTimeout(function(){
                                window.location='/'
                            },500)
                        }


                    })
                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })


    })
});