/**
 * Created by .
 * CustomUser: taoqili
 * Date: 11-8-18
 * Time: 下午3:18
 * To change this template use File | Settings | File Templates.
 */
/**
 * ajax工具类
 */
UE.ajax = function() {
	return {
		/**
		 * 向url发送ajax请求
		 * @param url
		 * @param ajaxOptions
		 */
		request:function(url, ajaxOptions) {
            var ajaxRequest = creatAjaxRequest(),
                //是否超时
                timeIsOut = false,
                //默认参数
                defaultAjaxOptions = {
                    method:"POST",
                    timeout:5000,
                    async:true,
                    data:{},//需要传递对象的话只能覆盖
                    onsuccess:function() {
                    },
                    onerror:function() {
                    }
                };

			if (typeof url === "object") {
				ajaxOptions = url;
				url = ajaxOptions.url;
			}
			if (!ajaxRequest || !url) return;
			var ajaxOpts = ajaxOptions ? utils.extend(defaultAjaxOptions,ajaxOptions) : defaultAjaxOptions;

			var submitStr = json2str(ajaxOpts);  // { name:"Jim",city:"Beijing" } --> "name=Jim&city=Beijing"
			//如果用户直接通过data参数传递json对象过来，则也要将此json对象转化为字符串
			if (!utils.isEmptyObject(ajaxOpts.data)){
                submitStr += (submitStr? "&":"") + json2str(ajaxOpts.data);
			}
            //超时检测
            var timerID = setTimeout(function() {
                if (ajaxRequest.readyState != 4) {
                    timeIsOut = true;
                    ajaxRequest.abort();
                    clearTimeout(timerID);
                }
            }, ajaxOpts.timeout);

			var method = ajaxOpts.method.toUpperCase();
            var str = url + (url.indexOf("?")==-1?"?":"&") + (method=="POST"?"":submitStr+ "&noCache=" + +new Date);
			ajaxRequest.open(method, str, ajaxOpts.async);
			ajaxRequest.onreadystatechange = function() {
				if (ajaxRequest.readyState == 4) {
					if (!timeIsOut && ajaxRequest.status == 200) {
						ajaxOpts.onsuccess(ajaxRequest);
					} else {
						ajaxOpts.onerror(ajaxRequest);
					}
				}
			};
			if (method == "POST") {
				ajaxRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
				ajaxRequest.send(submitStr);
			} else {
				ajaxRequest.send(null);
			}
		}
	};

	/**
	 * 将json参数转化成适合ajax提交的参数列表
	 * @param json
	 */
	function json2str(json) {
		var strArr = [];
		for (var i in json) {
			//忽略默认的几个参数
			if(i=="method" || i=="timeout" || i=="async") continue;
			//传递过来的对象和函数不在提交之列
			if (!((typeof json[i]).toLowerCase() == "function" || (typeof json[i]).toLowerCase() == "object")) {
				strArr.push( encodeURIComponent(i) + "="+encodeURIComponent(json[i]) );
			}
		}
		return strArr.join("&");

	}

	/**
	 * 创建一个ajaxRequest对象
	 */
	function creatAjaxRequest() {
		var xmlHttp = null;
		if (window.XMLHttpRequest) {
			xmlHttp = new XMLHttpRequest();
		} else {
			try {
				xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				try {
					xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
				} catch (e) {
				}
			}
		}
		return xmlHttp;
	}
}();
