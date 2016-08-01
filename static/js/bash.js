//loading......
var myGlobalHandlers = {
	onCreate: function(){
		$('systemWorking').style.display="none";
		Element.show('systemWorking');
	},
	onComplete: function() {
		if(Ajax.activeRequestCount == 0){
			Element.hide('systemWorking');
		}
	}
};
Ajax.Responders.register(myGlobalHandlers);

//clean str space.
function trim(str){
  var regExp=/^\s*(.*?)\s*$/;
  return str.replace(regExp, "$1");
}

//post push form.
function submitmodule(Pushformpost)
{
	$('placeholder').innerHTML ='';
	document.getElementById("placeholder").style.visibility="hidden";
	url_string=trim($F('PushURLid')) ;
	var url = "/push/executive/";  
        if (url_string=="")
        {
                ymPrompt.alert({title:'系统提示：',width:350,height:150,message:'提交失败：请输入推送的URL清单！'});
		document.PushForm.PushURLid.focus();
		return false;
        }

	var myAjax = new Ajax.Request(
		url, 
		{ 
		method:'post', 
		parameters:Form.serialize($(Pushformpost)),
		onComplete: showResponse
		}
	);
	function showResponse(originalRequest)
	{		
		document.getElementById("placeholder").style.visibility="visible";
		$('placeholder').innerHTML =originalRequest.responseText+$('placeholder').innerHTML;
	}
}