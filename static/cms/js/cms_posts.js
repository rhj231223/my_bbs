/**
 * Created by renhuijun on 2017/6/15.
 */
//选择url
$(function(){
    var sort=$('select[name=sort]');
    sort.change(function(event){
        value=$(this).val();

        newSrc=xtparam.setParam(window.location.href,'sort',value)
        newSrc=xtparam.setParam(newSrc,'page',1)
        window.location=newSrc
    });


});

$(function(){
    var board_id=$('select[name=board_id]');
    board_id.change(function(event){
        value=$(this).val();

        newSrc=xtparam.setParam(window.location.href,'board_id',value)
        newSrc=xtparam.setParam(newSrc,'page',1)
        window.location=newSrc
    })
});

$(function(){
    var all=$('select[name=all]');
    all.change(function(event){
        value=$(this).val();
        newSrc=xtparam.setParam(window.location.href,'all',value);
        newSrc=xtparam.setParam(newSrc,'page',1);
        window.location=newSrc
    })
});

// 加精
$(function(){
    var btn=$('.highlight_btn');
    btn.click(function(event){
        event.preventDefault()

        var post_id=$(this).attr('data-post-id');
        var is_highlight=$(this).attr('data-is-highlight');
        console.log(post_id);
        console.log(is_highlight);

        rhjajax.ajax({
            url:'/highlight/',
            type:'post',
            data:{
                post_id:post_id,
                is_highlight:is_highlight
            },
            success:function(data){
                if(data['code']==200){
                    msg='';
                    if(is_highlight=='1'){
                        msg='加精操作成功！'
                    }else{
                        msg='取消加精成功'
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

$(function(){
    btn=$('.removed_btn')
    btn.click(function(event){
        event.preventDefault();

        var post_id=$(this).attr('data-post-id');
        var is_removed=$(this).attr('data-is-removed');

        rhjajax.ajax({
            url:'/post_removed/',
            type:'post',
            data:{
                post_id:post_id,
                is_removed:is_removed

            },
            success:function(data){
                if(data['code']==200){
                    msg=''
                    if(is_removed=='1'){
                        msg='移除操作成功!'
                    }else{
                        msg='取消移除成功!'
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