/**
 * Created by renhuijun on 2017/6/12.
 */
$(function(){
    var graph_btn=$('#graph_btn');
    graph_btn.css({
        cursor:'pointer',
        padding:0,
        margin:0
    })
    graph_btn.click(function(event){
        event.preventDefault();

        oldSrc=graph_btn.children('img').attr('src')
        newSrc=xtparam.setParam(oldSrc,'xxx',Math.random());
        graph_btn.children('img').attr('src',newSrc)


    })
});
