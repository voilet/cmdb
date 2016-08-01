///import editor.js
///import core/utils.js

    /**
     * 事件基础类
     * @public
     * @class
     * @name baidu.editor.EventBase
     */
    var EventBase = UE.EventBase = function(){};

    EventBase.prototype = /**@lends baidu.editor.EventBase.prototype*/{
        /**
         * 注册事件监听器
         * @public
         * @function
         * @param {String} types 事件名
         * @param {Function} listener 监听器数组
         */
        addListener : function ( types, listener ) {
            types = utils.trim(types).split(' ');
            for(var i= 0,ti;ti=types[i++];){
                getListener( this, ti, true ).push( listener );
            }
        },
        /**
         * 移除事件监听器
         * @public
         * @function
         * @param {String} types 事件名
         * @param {Function} listener 监听器数组
         */
        removeListener : function ( types, listener ) {
            types = utils.trim(types).split(' ');
            for(var i= 0,ti;ti=types[i++];){
                utils.removeItem( getListener( this, ti ) || [], listener );
            }
        },
        /**
         * 触发事件
         * @public
         * @function
         * @param {String} type 事件名
         * 
         */
        fireEvent : function ( types ) {
            types = utils.trim(types).split(' ');
            for(var i= 0,ti;ti=types[i++];){
                var listeners = getListener( this, ti ),
                    r, t, k;
                if ( listeners ) {
                    k = listeners.length;
                    while ( k -- ) {
                        t = listeners[k].apply( this, arguments );
                        if ( t !== undefined ) {
                            r = t;
                        }
                    }
                }
                if ( t = this['on' + ti.toLowerCase()] ) {
                    r = t.apply( this, arguments );
                }
            }
            return r;
        }
    };
    /**
     * 获得对象所拥有监听类型的所有监听器
     * @public
     * @function
     * @param {Object} obj  查询监听器的对象
     * @param {String} type 事件类型
     * @param {Boolean} force  为true且当前所有type类型的侦听器不存在时，创建一个空监听器数组
     * @returns {Array} 监听器数组
     */
    function getListener( obj, type, force ) {
        var allListeners;
        type = type.toLowerCase();
        return ( ( allListeners = ( obj.__allListeners || force && ( obj.__allListeners = {} ) ) )
            && ( allListeners[type] || force && ( allListeners[type] = [] ) ) );
    }

