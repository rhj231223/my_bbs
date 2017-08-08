/**
 * Created by renhuijun on 2017/6/14.
 */

//富文本编辑器配置
$(function(){
    var editor=new wangEditor('editor');
    editor.create();
    window.editor=editor;
});

// 初始化到七牛

$(function(){
    var progress=$('#progress_box');
    progress.hide()
    var progress_bar=progress.children(0);
    var upload_btn=$('#upload_btn');
    var submit=$('#submit')

    xtqiniu.setUp({
        browse_button:'upload_btn',
        success:function(up,file,info){
            fileUrl=file.name;
            if(file.type.indexOf('video')>=0){
                videoTag='<video width="640px" height="360px" controls><source src='+fileUrl+'></video>';
                window.editor.$txt.append(videoTag)
            }else{
                imgTag='<img src='+fileUrl+' alt="">';
                window.editor.$txt.append(imgTag)
            }
        },
        fileadded:function (up,files) {
            upload_btn.attr('disabled','disabled');
            upload_btn.text('正在上传中...');
            progress.show()
        },
        progress:function (up,file) {
            var percent=file.percent;
            progress_bar.attr('aria-valuenow',percent);
            progress_bar.css('width',percent+'%');
            progress_bar.text(percent+'%')
        },
        complete:function(){
            progress_bar.attr('aria-valuenow','2');
            progress_bar.css('width','2%');
            progress_bar.text('2%');
            progress.hide()
            upload_btn.removeAttr('disabled');
            upload_btn.text('上传文件或视频');
        }
    })
});


