  $("#btn_cmd").click(function(){
        $.ajax({
       type: "GET",
       url: "/salt/3/" })  .done(function( data ) {
        $("#salt_cmd").html(data);
      });
  });

$(document).ready(function(){
  $("#btn_grains").click(function(){
        $.ajax({
       type: "GET",
       url: "/salt/garins/"})  .done(function( data ) {
        $("#salt_cmd").html(data);
      });
  });
});


$(document).ready(function(){
  $('#button').click(function(){
    jQuery.ajax({
      url: "/salt/cmd/",                  // 提交的页面
      data: $('#reasonform').serialize(), // 从表单中获取数据
      type: "POST",                       // 设置请求类型为"POST"，默认为"GET"
      beforeSend: function(){             // 设置表单提交前方法
        //alert('表单提交前');
      },
      error: function(request){           // 设置表单提交出错
        alert("表单提交出错，请稍候再试");
      },
      dataType:'text',
      success: function(msg){
          $("#salt_cmd_run").html(msg)
      }
    });
    return false;
  });
});
//garins
$(document).ready(function(){
  $('#button_garins').click(function(){
    jQuery.ajax({
      url: "/salt/garins/",                  // 提交的页面
      data: $('#reasonform_garins').serialize(), // 从表单中获取数据
      type: "POST",                       // 设置请求类型为"POST"，默认为"GET"
      beforeSend: function(){             // 设置表单提交前方法
        //alert('表单提交前');
      },
      error: function(request){           // 设置表单提交出错
        alert("表单提交出错，请稍候再试");
      },
      dataType:'text',
      success: function(msg){
          $("#salt_cmd_run").html(msg)
      }
    });
    return false;
  });
});

//ssh jinja
$(document).ready(function(){
  $('#button_jinja').click(function(){
    jQuery.ajax({
      url: "/salt/jinja/",                  // 提交的页面
      data: $('#reasonform_jinja').serialize(), // 从表单中获取数据
      type: "POST",                       // 设置请求类型为"POST"，默认为"GET"
      beforeSend: function(){             // 设置表单提交前方法
        //alert('表单提交前');
      },
      error: function(request){           // 设置表单提交出错
        alert("表单提交出错，请稍候再试");
      },
      dataType:'text',
      success: function(msg){
          $("#jinja_add").html(msg)
      }
    });
    return false;
  });
});

//add sale-ssh node
$(document).ready(function(){
  $('#button_node').click(function(){
    jQuery.ajax({
      url: "/salt/add_node/",                  // 提交的页面
      data: $('#reasonform_node').serialize(), // 从表单中获取数据
      type: "POST",                       // 设置请求类型为"POST"，默认为"GET"
      beforeSend: function(){             // 设置表单提交前方法
        //alert('表单提交前');
      },
      error: function(request){           // 设置表单提交出错
        alert("表单提交出错，请稍候再试");
      },
      dataType:'text',
      success: function(msg){
          $("#button_node_lr").html(msg)
      }
    });
    return false;
  });
});

//add sale-ssh node install
$(document).ready(function(){
  $('#salt_node_post').click(function(){
    jQuery.ajax({
      url: "/salt/node_shell/",                  // 提交的页面
      data: $('#salt_node_add').serialize(), // 从表单中获取数据
      type: "POST",                       // 设置请求类型为"POST"，默认为"GET"
      beforeSend: function(){             // 设置表单提交前方法
        //alert('表单提交前');
      },
      error: function(request){           // 设置表单提交出错
        alert("表单提交出错，请稍候再试");
      },
      dataType:'text',
      success: function(msg){
          $("#salt_node_lr").html(msg)
      }
    });
    return false;
  });
});

//单个安装服务
$(document).ready(function(){
  $('#but_salt_state_sls').click(function(){
    jQuery.ajax({
      url: "/salt/node_server/",                  // 提交的页面
      data: $('#salt_sls').serialize(), // 从表单中获取数据
      type: "POST",                       // 设置请求类型为"POST"，默认为"GET"
      beforeSend: function(){             // 设置表单提交前方法
        //alert('表单提交前');
      },
      error: function(request){           // 设置表单提交出错
        alert("表单提交出错，请稍候再试");
      },
      dataType:'text',
      success: function(msg){
          $("#voilet_sls").html(msg)
      }
    });
    return false;
  });
});

