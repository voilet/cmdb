/**
 * Created by voilet on 15/4/22.
 */


function urlParam(name) {
    var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
        return results[1] || 0;
}

function select_all(){
   $(document).on("click","#select_all",function(e){
   var selected = $("#select_all").prop("checked");
   if(selected){
     $("input[name='node_name']").prop('checked',true);
   }else{
     $("input[name='node_name']").prop("checked",false);
   }
 });
}
