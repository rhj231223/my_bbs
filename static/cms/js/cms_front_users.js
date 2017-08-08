/**
 * Created by renhuijun on 2017/6/17.
 */
$(function(){
    var sort_btn=$('select[name=sort]');
    sort_btn.change(function(){
        value=$(this).val();
        oldSrc=window.location.href;
        newSrc=xtparam.setParam(oldSrc,'sort',value);
        window.location=newSrc
    })
});