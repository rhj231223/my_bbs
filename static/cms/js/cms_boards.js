/**
 * Created by renhuijun on 2017/6/13.
 */
$(function(){
    var add_btn=$('#add_board_btn');
    add_btn.click(function(event){
        event.preventDefault();

        xtalert.alertOneInput({
            title:'新版块',
            text:'请输入新添加的版块名称',
            confirmText:'确认',
            cancelText:'取消',
            confirmCallback:function(inputValue){
                rhjajax.ajax({
                    url:'/add_board/',
                    type:'post',
                    data:{
                        board_name:inputValue
                    },
                    success:function(data){
                        if(data['code']==200){
                            xtalert.alertSuccessToast(msg='恭喜版块添加成功')
                            setTimeout(function(){
                                window.location.reload()
                            },1200)
                        }else{
                            xtalert.alertInfo(msg=data['message'])
                        }
                    }
                })
            }
        })
    })
});

$(function(){
   var edit_btn=$('.edit_btn');
    edit_btn.click(function(event){
        event.preventDefault();

        var board_id=$(this).attr('data-board-id');
        var board_name=$(this).attr('data-board-name');
        xtalert.alertOneInput({
            title:'修改版块名',
            placeholder:'原版块名称:'+board_name,
            confirmText:'确认修改',
            cancelText:'放弃修改',
            confirmCallback:function(inputValue){
                rhjajax.ajax({
                    url:'/edit_board/',
                    type:'post',
                    data:{
                        board_id:board_id,
                        board_name:inputValue
                    },
                    success:function(data){
                        if(data['code']==200){
                            xtalert.alertSuccessToast(msg='版块修改成功！')
                            setTimeout(function(){
                                window.location.reload()
                            },1200)
                        }else{
                            xtalert.alertInfo(msg=data['message'])
                        }
                    }
                })
            }
        })

    })
});

$(function(){
    var delete_btn=$('.delete_btn');
    delete_btn.click(function(event){
        event.preventDefault();

        var board_id=parseInt($(this).attr('data-board-id'));
        var board_name=$(this).attr('data-board-name');
        xtalert.alertConfirm({
            text:'确认删除 '+board_name+' 板块吗？',
            confirmText:'确认删除',
            cancelText:'放弃操作',
            confirmColor:'#CC0000',
            confirmCallback:function(){
                rhjajax.ajax({
                    url:'/delete_board/',
                    type:'post',
                    data:{
                        board_id:board_id
                    },
                    success:function(data){
                        if(data['code']==200){
                            xtalert.alertSuccessToast(msg='版块删除成功!');
                           setTimeout(function(){
                                window.location.reload()
                            },1200)
                        }else{
                            xtalert.alertInfo(msg=data['message'])
                        }
                    }
                })
            }

        })

    })
});
