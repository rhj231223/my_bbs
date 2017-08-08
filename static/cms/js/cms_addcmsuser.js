/**
 * Created by renhuijun on 2017/6/12.
 */
$(function(){
    var submit=$('#submit');
    submit.click(function(event){
        event.preventDefault();

        var email=$('input[name=email]');
        var username=$('input[name=username]');
        var password=$('input[name=password]');
        var roles=$(':checkbox:checked');
        var selected_roles=[];
        roles.each(function(){
            role_id=$(this).val();
            selected_roles.push(role_id)
        });

        rhjajax.ajax({
            url:'/add_cmsuser/',
            type:'post',
            data:{
                email:email.val(),
                username:username.val(),
                password:password.val(),
                roles:selected_roles

            },
            success:function(data){
                if(data['code']==200){
                    email.val('');
                    username.val('');
                    password.val('');
                    roles.each(function(){
                        $(this).prop('checked',false)
                    });
                    xtalert.alertSuccessToast(msg='恭喜！cms用户添加成功!')

                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }
        })

    })
});
