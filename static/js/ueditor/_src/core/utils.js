///import editor.js
///import core/utils.js
/**
 * @class baidu.editor.utils     工具类
 */

    var utils = UE.utils =
	/**@lends baidu.editor.utils.prototype*/
    {
		/**
         * 以obj为原型创建实例
         * @public
         * @function
         * @param {Object} obj
         * @return {Object} 返回新的对象
         */
		makeInstance: function(obj) {
            var noop = new Function();
			noop.prototype = obj;
			obj = new noop;
			noop.prototype = null;
			return obj;
		},
        /**
         * 将s对象中的属性扩展到t对象上
         * @public
         * @function
         * @param {Object} t
         * @param {Object} s
         * @param {Boolean} b 是否保留已有属性
         * @returns {Object}  t 返回扩展了s对象属性的t
         */
		extend: function(t, s, b) {
			if (s) {
				for (var k in s) {
					if (!b || !t.hasOwnProperty(k)) {
						t[k] = s[k];
					}
				}
			}
			return t;
		},
		/**
         * 判断是否为数组
         * @public
         * @function
         * @param {Object} array
         * @return {Boolean} true：为数组，false：不为数组
         */
		isArray: function(array) {
			return Object.prototype.toString.apply(array) === '[object Array]';
		},
		/**
         * 判断是否为字符串
         * @public
         * @function
         * @param {Object} str
         * @return {Boolean} true：为字符串。 false：不为字符串
         */
		isString: function(str) {
			return typeof str == 'string' || str.constructor == String;
		},
		/**
         * subClass继承superClass
         * @public
         * @function
         * @param {Object} subClass       子类
         * @param {Object} superClass    超类
         * @return    {Object}    扩展后的新对象
         */
		inherits: function(subClass, superClass) {
			var oldP = subClass.prototype,
			    newP = utils.makeInstance(superClass.prototype);
			utils.extend(newP, oldP, true);
			subClass.prototype = newP;
			return (newP.constructor = subClass);
		},

		/**
         * 为对象绑定函数
         * @public
         * @function
         * @param {Function} fn        函数
         * @param {Object} this_       对象
         * @return {Function}  绑定后的函数
         */
		bind: function(fn, this_) {
			return function() {
				return fn.apply(this_, arguments);
			};
		},

		/**
         * 创建延迟执行的函数
         * @public
         * @function
         * @param {Function} fn       要执行的函数
         * @param {Number} delay      延迟时间，单位为毫秒
         * @param {Boolean} exclusion 是否互斥执行，true则执行下一次defer时会先把前一次的延迟函数删除
         * @return {Function}    延迟执行的函数
         */
		defer: function(fn, delay, exclusion) {
			var timerID;
			return function() {
				if (exclusion) {
					clearTimeout(timerID);
				}
				timerID = setTimeout(fn, delay);
			};
		},



		/**
         * 查找元素在数组中的索引, 若找不到返回-1
         * @public
         * @function
         * @param {Array} array     要查找的数组
         * @param {*} item          查找的元素
         * @param {Number} at       开始查找的位置
         * @returns {Number}        返回在数组中的索引
         */
		indexOf: function(array, item, at) {
            for(var i=at||0,l = array.length;i<l;i++){
               if(array[i] === item){
                   return i;
               }
            }
            return -1;
		},

        findNode : function(nodes,tagNames,fn){
            for(var i=0,ci;ci=nodes[i++];){
                if(fn? fn(ci) : this.indexOf(tagNames,ci.tagName.toLowerCase())!=-1){
                    return ci;
                }
            }
        },
		/**
         * 移除数组中的元素
         * @public
         * @function
         * @param {Array} array       要删除元素的数组
         * @param {*} item            要删除的元素
         */
		removeItem: function(array, item) {
            for(var i=0,l = array.length;i<l;i++){
                if(array[i] === item){
                    array.splice(i,1);
                    i--;
                }
            }
		},

		/**
         * 删除字符串首尾空格
         * @public
         * @function
         * @param {String} str        字符串
         * @return {String} str       删除空格后的字符串
         */
		trim: function(str) {
            return str.replace(/(^[ \t\n\r]+)|([ \t\n\r]+$)/g, '');
		},

		/**
         * 将字符串转换成hashmap
         * @public
         * @function
         * @param {String/Array} list       字符串，以‘，’隔开
         * @returns {Object}          转成hashmap的对象
         */
		listToMap: function(list) {
            if(!list)return {};
            list = utils.isArray(list) ? list : list.split(',');
            for(var i=0,ci,obj={};ci=list[i++];){
                obj[ci.toUpperCase()] = obj[ci] = 1;
            }
            return obj;
		},

		/**
         * 将str中的html符号转义
         * @public
         * @function
         * @param {String} str      需要转义的字符串
         * @returns {String}        转义后的字符串
         */
		unhtml: function(str,reg) {
           return str ? str.replace(reg || /[&<">]/g, function(m){
               return {
                   '<': '&lt;',
                   '&': '&amp;',
                   '"': '&quot;',
                   '>': '&gt;'
               }[m]
           }) : '';
		},
        html:  function(str) {
            return str ? str.replace(/&((g|l|quo)t|amp);/g, function(m){
                return {
                    '&lt;':'<',
                    '&amp;':'&',
                    '&quot;':'"',
                    '&gt;': '>'
                }[m]
            }) : '';
        },
		/**
         * 将css样式转换为驼峰的形式。如font-size -> fontSize
         * @public
         * @function
         * @param {String} cssName      需要转换的样式
         * @returns {String}        转换后的样式
         */
		cssStyleToDomStyle: function() {
            var test = document.createElement('div').style,
               cache = {
                   'float': test.cssFloat != undefined ? 'cssFloat' : test.styleFloat != undefined ? 'styleFloat': 'float'
               };

            return function(cssName) {
               return cache[cssName] || (cache[cssName] = cssName.toLowerCase().replace(/-./g, function(match){return match.charAt(1).toUpperCase();}));
            };
		}(),
		/**
         * 加载css文件，执行回调函数
         * @public
         * @function
         * @param {document}   doc  document对象
         * @param {String}    path  文件路径
         * @param {Function}   fun  回调函数
         * @param {String}     id   元素id
         */
        loadFile : function(){
            var tmpList = {};
            return function(doc,obj,fun){
                var item = tmpList[obj.src||obj.href];
                if(item){
                    if(utils.isArray(item.funs)){
                        item.ready?fun():tmpList[obj.src||obj.href].funs.push(fun);
                    }
                    return;
                }
                tmpList[obj.src||obj.href] = fun? {'funs' : [fun]} :1;

                if(!doc.body){
                    doc.write('<script src="'+obj.src+'"></script>');
                    return;
                }
                if (obj.id && doc.getElementById(obj.id)) {
                    return;
                }
                var element = doc.createElement(obj.tag);
                delete obj.tag;
                for(var p in obj){
                    element.setAttribute(p,obj[p]);
                }
                element.onload = element.onreadystatechange = function() {
                    if (!this.readyState || /loaded|complete/.test(this.readyState)) {
                        item =  tmpList[obj.src||obj.href];
                        if(item.funs){
                            item.ready = 1;
                            for(var fi;fi=item.funs.pop();){
                                fi();
                            }
                        }
                        element.onload = element.onreadystatechange = null;
                    }
                };
                doc.getElementsByTagName("head")[0].appendChild(element);
            }
        }(),
        /**
         * 判断对象是否为空
         * @param {Object} obj
         * @return {Boolean} true 空，false 不空
         */
        isEmptyObject : function(obj){
            for ( var p in obj ) {
                return false;
            }
            return true;
        },
        isFunction : function (source) {
            // chrome下,'function' == typeof /a/ 为true.
            return '[object Function]' == Object.prototype.toString.call(source);
        },
        fixColor : function (name, value) {
            if (/color/i.test(name) && /rgba?/.test(value)) {
                var array = value.split(",");
                if (array.length > 3)
                    return "";
                value = "#";
                for (var i = 0, color; color = array[i++];) {
                    color = parseInt(color.replace(/[^\d]/gi, ''), 10).toString(16);
                    value += color.length == 1 ? "0" + color : color;
                }
                value = value.toUpperCase();
            }
            return  value;
        },
        /**
        * 只针对border,padding,margin做了处理，因为性能问题
        * @public
        * @function
        * @param {String}    val style字符串
        */
        optCss : function(val){
            var padding,margin,border;
            val = val.replace(/(padding|margin|border)\-([^:]+):([^;]+);?/gi,function(str,key,name,val){
                if(val.split(' ').length == 1){
                    switch (key){
                        case 'padding':
                            !padding && (padding = {});
                            padding[name] = val;
                            return '';
                        case 'margin':
                            !margin && (margin = {});
                            margin[name] = val;
                            return '';
                        case 'border':
                            return val == 'initial' ? '' : str;
                    }
                }
                return str;
            });

            function opt(obj,name){
                if(!obj){
                    return '';
                }
                var t = obj.top ,b = obj.bottom,l = obj.left,r = obj.right,val = '';
                if(!t || !l || !b || !r){
                    for(var p in obj){
                        val +=';'+name+'-' + p + ':' + obj[p]+';';
                    }
                }else{
                    val += ';'+name+':' +
                        (t == b && b == l && l == r ? t :
                            t == b && l == r ? (t + ' ' + l) :
                                l == r ?  (t + ' ' + l + ' ' + b) : (t + ' ' + r + ' ' + b + ' ' + l))+';'
                }
                return val;
            }
            val += opt(padding,'padding') + opt(margin,'margin');
            return val.replace(/^[ \n\r\t;]*|[ \n\r\t]*$/,'').replace(/;([ \n\r\t]+)|\1;/g,';')
                .replace(/(&((l|g)t|quot|#39))?;{2,}/g,function(a,b){
                    return b ? b + ";;" : ';'
                });
        },
        /**
         * DOMContentLoaded 事件注册
         * @public
         * @function
         * @param {Function} 触发的事件
         */
        domReady : function (){
            var isReady = false,
                fnArr = [];
            function doReady(){
                //确保onready只执行一次
                isReady = true;
                for(var ci;ci=fnArr.pop();){
                   ci();
                }
            }
            return function(onready){
                if ( document.readyState === "complete" ) {
                    return onready && setTimeout( onready, 1 );
                }
                onready && fnArr.push(onready);
                isReady && doReady();
                if( browser.ie ){
                    (function(){
                        if ( isReady ) return;
                        try {
                            document.documentElement.doScroll("left");
                        } catch( error ) {
                            setTimeout( arguments.callee, 0 );
                            return;
                        }
                        doReady();
                    })();
                    window.attachEvent('onload',doReady);
                }else{
                    document.addEventListener( "DOMContentLoaded", function(){
                        document.removeEventListener( "DOMContentLoaded", arguments.callee, false );
                        doReady();
                    }, false );
                    window.addEventListener('load',doReady,false);
                }
            }
        }()
	};
    utils.domReady();