/**
 * Created by renhuijun on 2017/6/15.
 */
$(function(){
            var tagA=$('.tagA');
            var sort=parseInt($('#filter_box').attr('data-sort'));
            tagA.eq(sort-1).css('color','#f80').sibling().css('color','#333');
        });