///import editor.js
///import core/utils.js
///import core/browser.js
///import core/dom/dom.js
///import core/dom/dtd.js
/**
 * for getNextDomNode getPreviousDomNode
 */
function getDomNode( node, start, ltr, startFromChild, fn, guard ) {
    var tmpNode = startFromChild && node[start],
            parent;
    !tmpNode && (tmpNode = node[ltr]);
    while ( !tmpNode && (parent = (parent || node).parentNode) ) {
        if ( parent.tagName == 'BODY' || guard && !guard( parent ) ) {
            return null;
        }
        tmpNode = parent[ltr];
    }
    if ( tmpNode && fn && !fn( tmpNode ) ) {
        return  getDomNode( tmpNode, start, ltr, false, fn );
    }
    return tmpNode;
}
var attrFix = ie && browser.version < 9 ? {
            tabindex:"tabIndex",
            readonly:"readOnly",
            "for":"htmlFor",
            "class":"className",
            maxlength:"maxLength",
            cellspacing:"cellSpacing",
            cellpadding:"cellPadding",
            rowspan:"rowSpan",
            colspan:"colSpan",
            usemap:"useMap",
            frameborder:"frameBorder"
        } : {
            tabindex:"tabIndex",
            readonly:"readOnly"
        },
        styleBlock = utils.listToMap( [
            '-webkit-box', '-moz-box', 'block' ,
            'list-item' , 'table' , 'table-row-group' ,
            'table-header-group', 'table-footer-group' ,
            'table-row' , 'table-column-group' , 'table-column' ,
            'table-cell' , 'table-caption'
        ] );
var domUtils = dom.domUtils = {
    //节点常量
    NODE_ELEMENT:1,
    NODE_DOCUMENT:9,
    NODE_TEXT:3,
    NODE_COMMENT:8,
    NODE_DOCUMENT_FRAGMENT:11,

    //位置关系
    POSITION_IDENTICAL:0,
    POSITION_DISCONNECTED:1,
    POSITION_FOLLOWING:2,
    POSITION_PRECEDING:4,
    POSITION_IS_CONTAINED:8,
    POSITION_CONTAINS:16,
    //ie6使用其他的会有一段空白出现
    fillChar:ie && browser.version == '6' ? '\ufeff' : '\u200B',
    //-------------------------Node部分--------------------------------
    keys:{
        /*Backspace*/ 8:1, /*Delete*/ 46:1,
        /*Shift*/ 16:1, /*Ctrl*/ 17:1, /*Alt*/ 18:1,
        37:1, 38:1, 39:1, 40:1,
        13:1 /*enter*/
    },
    /**
     * 获取两个节点的位置关系
     * @function
     * @param {Node} nodeA     节点A
     * @param {Node} nodeB     节点B
     * @returns {Number}       返回位置关系
     */
    getPosition:function ( nodeA, nodeB ) {
        // 如果两个节点是同一个节点
        if ( nodeA === nodeB ) {
            // domUtils.POSITION_IDENTICAL
            return 0;
        }
        var node,
                parentsA = [nodeA],
                parentsB = [nodeB];
        node = nodeA;
        while ( node = node.parentNode ) {
            // 如果nodeB是nodeA的祖先节点
            if ( node === nodeB ) {
                // domUtils.POSITION_IS_CONTAINED + domUtils.POSITION_FOLLOWING
                return 10;
            }
            parentsA.push( node );
        }
        node = nodeB;
        while ( node = node.parentNode ) {
            // 如果nodeA是nodeB的祖先节点
            if ( node === nodeA ) {
                // domUtils.POSITION_CONTAINS + domUtils.POSITION_PRECEDING
                return 20;
            }
            parentsB.push( node );
        }
        parentsA.reverse();
        parentsB.reverse();
        if ( parentsA[0] !== parentsB[0] ) {
            // domUtils.POSITION_DISCONNECTED
            return 1;
        }
        var i = -1;
        while ( i++, parentsA[i] === parentsB[i] ) {
        }
        nodeA = parentsA[i];
        nodeB = parentsB[i];
        while ( nodeA = nodeA.nextSibling ) {
            if ( nodeA === nodeB ) {
                // domUtils.POSITION_PRECEDING
                return 4
            }
        }
        // domUtils.POSITION_FOLLOWING
        return  2;
    },

    /**
     * 返回节点索引，zero-based
     * @function
     * @param {Node} node     节点
     * @returns {Number}    节点的索引
     */
    getNodeIndex : function (node,normalized) {

        var preNode = node,i=0;
        while(preNode = preNode.previousSibling){
            if(normalized && preNode.nodeType == 3){

                continue;
            }
            i++;

        }
        return i;
    },

    /**
     * 判断节点是否在树上
     * @param node
     */
    inDoc:function ( node, doc ) {
        while ( node = node.parentNode ) {
            if ( node === doc ) {
                return true;
            }
        }
        return false;
    },

    /**
     * 查找祖先节点
     * @function
     * @param {Node}     node        节点
     * @param {Function} tester      以函数为规律
     * @param {Boolean} includeSelf 包含自己
     * @returns {Node}      返回祖先节点
     */
    findParent:function ( node, tester, includeSelf ) {
        if ( !domUtils.isBody( node ) ) {
            node = includeSelf ? node : node.parentNode;
            while ( node ) {
                if ( !tester || tester( node ) || this.isBody( node ) ) {
                    return tester && !tester( node ) && this.isBody( node ) ? null : node;
                }
                node = node.parentNode;
            }
        }
        return null;
    },
    /**
     * 查找祖先节点
     * @function
     * @param {Node}     node        节点
     * @param {String}   tagName      标签名称
     * @param {Boolean} includeSelf 包含自己
     * @returns {Node}      返回祖先节点
     */
    findParentByTagName:function ( node, tagName, includeSelf, excludeFn ) {
        if ( node && node.nodeType && !this.isBody( node ) && (node.nodeType == 1 || node.nodeType) ) {
            tagName = utils.listToMap( utils.isArray( tagName ) ? tagName : [tagName] );
            node = node.nodeType == 3 || !includeSelf ? node.parentNode : node;
            while ( node && node.tagName && node.nodeType != 9 ) {
                if ( excludeFn && excludeFn( node ) ) {
                    break;
                }
                if ( tagName[node.tagName] )
                    return node;
                node = node.parentNode;
            }
        }

        return null;
    },
    /**
     * 查找祖先节点集合
     * @param {Node} node               节点
     * @param {Function} tester         函数
     * @param {Boolean} includeSelf     是否从自身开始找
     * @param {Boolean} closerFirst
     * @returns {Array}     祖先节点集合
     */
    findParents:function ( node, includeSelf, tester, closerFirst ) {
        var parents = includeSelf && ( tester && tester( node ) || !tester ) ? [node] : [];
        while ( node = domUtils.findParent( node, tester ) ) {
            parents.push( node );
        }
        return closerFirst ? parents : parents.reverse();
    },

    /**
     * 往后插入节点
     * @function
     * @param  {Node}     node            基准节点
     * @param  {Node}     nodeToInsert    要插入的节点
     * @return {Node}     返回node
     */
    insertAfter:function ( node, nodeToInsert ) {
        return node.parentNode.insertBefore( nodeToInsert, node.nextSibling );
    },

    /**
     * 删除该节点
     * @function
     * @param {Node} node            要删除的节点
     * @param {Boolean} keepChildren 是否保留子节点不删除
     * @return {Node} 返回要删除的节点
     */
    remove:function ( node, keepChildren ) {
        var parent = node.parentNode,
                child;
        if ( parent ) {
            if ( keepChildren && node.hasChildNodes() ) {
                while ( child = node.firstChild ) {
                    parent.insertBefore( child, node );
                }
            }
            parent.removeChild( node );
        }
        return node;
    },

    /**
     * 取得node节点在dom树上的下一个节点
     * @function
     * @param {Node} node       节点
     * @param {Boolean} startFromChild 为true从子节点开始找
     * @param {Function} fn fn为真的节点
     * @return {Node}    返回下一个节点
     */
    getNextDomNode:function ( node, startFromChild, filter, guard ) {
        return getDomNode( node, 'firstChild', 'nextSibling', startFromChild, filter, guard );
    },
    /**
     * 是bookmark节点
     * @param {Node} node        判断是否为书签节点
     * @return {Boolean}        返回是否为书签节点
     */
    isBookmarkNode:function ( node ) {
        return node.nodeType == 1 && node.id && /^_baidu_bookmark_/i.test( node.id );
    },
    /**
     * 获取节点所在window对象
     * @param {Node} node     节点
     * @return {window}    返回window对象
     */
    getWindow:function ( node ) {
        var doc = node.ownerDocument || node;
        return doc.defaultView || doc.parentWindow;
    },
    /**
     * 得到公共的祖先节点
     * @param   {Node}     nodeA      节点A
     * @param   {Node}     nodeB      节点B
     * @return {Node} nodeA和nodeB的公共节点
     */
    getCommonAncestor:function ( nodeA, nodeB ) {
        if ( nodeA === nodeB )
            return nodeA;
        var parentsA = [nodeA] , parentsB = [nodeB], parent = nodeA, i = -1;
        while ( parent = parent.parentNode ) {
            if ( parent === nodeB ) {
                return parent;
            }
            parentsA.push( parent );
        }
        parent = nodeB;
        while ( parent = parent.parentNode ) {
            if ( parent === nodeA )
                return parent;
            parentsB.push( parent );
        }
        parentsA.reverse();
        parentsB.reverse();
        while ( i++, parentsA[i] === parentsB[i] ) {
        }
        return i == 0 ? null : parentsA[i - 1];

    },
    /**
     * 清除该节点左右空的inline节点
     * @function
     * @param {Node}     node
     * @param {Boolean} ingoreNext   默认为false清除右边为空的inline节点。true为不清除右边为空的inline节点
     * @param {Boolean} ingorePre    默认为false清除左边为空的inline节点。true为不清除左边为空的inline节点
     * @exmaple <b></b><i></i>xxxx<b>bb</b> --> xxxx<b>bb</b>
     */
    clearEmptySibling:function ( node, ingoreNext, ingorePre ) {
        function clear( next, dir ) {
            var tmpNode;
            while ( next && !domUtils.isBookmarkNode( next ) && (domUtils.isEmptyInlineElement( next )
                //这里不能把空格算进来会吧空格干掉，出现文字间的空格丢掉了
                    || !new RegExp( '[^\t\n\r' + domUtils.fillChar + ']' ).test( next.nodeValue ) ) ) {
                tmpNode = next[dir];
                domUtils.remove( next );
                next = tmpNode;
            }
        }

        !ingoreNext && clear( node.nextSibling, 'nextSibling' );
        !ingorePre && clear( node.previousSibling, 'previousSibling' );
    },
    //---------------------------Text----------------------------------
    /**
     * 将一个文本节点拆分成两个文本节点
     * @param {TextNode} node          文本节点
     * @param {Integer} offset         拆分的位置
     * @return {TextNode}   拆分后的后一个文本节
     */
    split:function ( node, offset ) {
        var doc = node.ownerDocument;
        if ( browser.ie && offset == node.nodeValue.length ) {
            var next = doc.createTextNode( '' );
            return domUtils.insertAfter( node, next );
        }
        var retval = node.splitText( offset );
        //ie8下splitText不会跟新childNodes,我们手动触发他的更新
        if ( browser.ie8 ) {
            var tmpNode = doc.createTextNode( '' );
            domUtils.insertAfter( retval, tmpNode );
            domUtils.remove( tmpNode );
        }
        return retval;
    },

    /**
     * 判断是否为空白节点
     * @param {TextNode}   node   节点
     * @return {Boolean}      返回是否为文本节点
     */
    isWhitespace:function ( node ) {
        return !new RegExp( '[^ \t\n\r' + domUtils.fillChar + ']' ).test( node.nodeValue );
    },
    //------------------------------Element-------------------------------------------
    /**
     * 获取元素相对于viewport的像素坐标
     * @param {Element} element      元素
     * @returns {Object}             返回坐标对象{x:left,y:top}
     */
    getXY:function ( element ) {
        var x = 0, y = 0;
        while ( element.offsetParent ) {
            y += element.offsetTop;
            x += element.offsetLeft;
            element = element.offsetParent;
        }
        return {
            'x':x,
            'y':y
        };
    },
    /**
     * 绑原生DOM事件
     * @param {Element|Window|Document} target     元素
     * @param {Array|String} type                  事件类型
     * @param {Function} handler                   执行函数
     */
    on:function ( obj, type, handler ) {

        var types = utils.isArray(type) ? type : [type],
                k = types.length;
        if ( k ) while ( k-- ) {
            type = types[k];
            if ( obj.addEventListener ) {
                obj.addEventListener( type, handler, false );
            } else {
                if ( !handler._d ) {
                    handler._d = {};
                }
                var key = type + handler.toString();
                if ( !handler._d[key] ) {
                    handler._d[key] = function ( evt ) {
                        return handler.call( evt.srcElement, evt || window.event );
                    };
                    obj.attachEvent( 'on' + type, handler._d[key] );
                }
            }
        }

        obj = null;
    },

    /**
     * 解除原生DOM事件绑定
     * @param {Element|Window|Document} obj         元素
     * @param {Array|String} type                   事件类型
     * @param {Function} handler                    执行函数
     */
    un:function ( obj, type, handler ) {
        var types = utils.isArray(type) ? type : [type],
                k = types.length;
        if ( k ) while ( k-- ) {
            type = types[k];
            if ( obj.removeEventListener ) {
                obj.removeEventListener( type, handler, false );
            } else {
                var key = type + handler.toString();
                obj.detachEvent( 'on' + type, handler._d ? handler._d[key] : handler );
                if ( handler._d && handler._d[key] ) {
                    delete handler._d[key];
                }
            }
        }
    },

    /**
     * 比较两个节点是否tagName相同且有相同的属性和属性值
     * @param {Element}   nodeA              节点A
     * @param {Element}   nodeB              节点B
     * @return {Boolean}     返回两个节点的标签，属性和属性值是否相同
     * @example
     * &lt;span  style="font-size:12px"&gt;ssss&lt;/span&gt;和&lt;span style="font-size:12px"&gt;bbbbb&lt;/span&gt; 相等
     *  &lt;span  style="font-size:13px"&gt;ssss&lt;/span&gt;和&lt;span style="font-size:12px"&gt;bbbbb&lt;/span&gt; 不相等
     */
    isSameElement:function ( nodeA, nodeB ) {
        if ( nodeA.tagName != nodeB.tagName ) {
            return 0;
        }
        var thisAttribs = nodeA.attributes,
                otherAttribs = nodeB.attributes;
        if ( !ie && thisAttribs.length != otherAttribs.length ) {
            return 0;
        }
        var attrA, attrB, al = 0, bl = 0;
        for ( var i = 0; attrA = thisAttribs[i++]; ) {
            if ( attrA.nodeName == 'style' ) {
                if ( attrA.specified ) {
                    al++;
                }
                if ( domUtils.isSameStyle( nodeA, nodeB ) ) {
                    continue;
                } else {
                    return 0;
                }
            }
            if ( ie ) {
                if ( attrA.specified ) {
                    al++;
                    attrB = otherAttribs.getNamedItem( attrA.nodeName );
                } else {
                    continue;
                }
            } else {
                attrB = nodeB.attributes[attrA.nodeName];
            }
            if ( !attrB.specified || attrA.nodeValue != attrB.nodeValue ) {
                return 0;
            }
        }
        // 有可能attrB的属性包含了attrA的属性之外还有自己的属性
        if ( ie ) {
            for ( i = 0; attrB = otherAttribs[i++]; ) {
                if ( attrB.specified ) {
                    bl++;
                }
            }
            if ( al != bl ) {
                return 0;
            }
        }
        return 1;
    },

    /**
     * 判断两个元素的style属性是不是一致
     * @param {Element} elementA       元素A
     * @param {Element} elementB       元素B
     * @return   {boolean}   返回判断结果，true为一致
     */
    isSameStyle:function ( elementA, elementB ) {
        var styleA = elementA.style.cssText.replace( /( ?; ?)/g, ';' ).replace( /( ?: ?)/g, ':' ),
                styleB = elementB.style.cssText.replace( /( ?; ?)/g, ';' ).replace( /( ?: ?)/g, ':' );
        if ( browser.opera ) {
            styleA = elementA.style;
            styleB = elementB.style;
            if ( styleA.length != styleB.length )
                return 0;
            for ( var p in styleA ) {
                if ( /^(\d+|csstext)$/i.test( p ) ) {
                    continue;
                }
                if ( styleA[p] != styleB[p] ) {
                    return 0;
                }
            }
            return 1;
        }


        if ( !styleA || !styleB ) {
            return styleA == styleB ? 1 : 0;
        }
        styleA = styleA.split( ';' );
        styleB = styleB.split( ';' );
        if ( styleA.length != styleB.length ) {
            return 0;
        }
        for ( var i = 0, ci; ci = styleA[i++]; ) {
            if ( utils.indexOf( styleB, ci ) == -1 ) {
                return 0;
            }
        }
        return 1;
    },

    /**
     * 检查是否为块元素
     * @function
     * @param {Element} node       元素
     * @param {String} customNodeNames 自定义的块元素的tagName
     * @return {Boolean} 是否为块元素
     */
    isBlockElm:function ( node ) {
        return node.nodeType == 1 && (dtd.$block[node.tagName] || styleBlock[domUtils.getComputedStyle( node, 'display' )]) && !dtd.$nonChild[node.tagName];
    },

    /**
     * 判断是否body
     * @param {Node} 节点
     * @return {Boolean}   是否是body节点
     */
    isBody:function ( node ) {
        return  node && node.nodeType == 1 && node.tagName.toLowerCase() == 'body';
    },
    /**
     * 以node节点为中心，将该节点的父节点拆分成2块
     * @param {Element} node       节点
     * @param {Element} parent 要被拆分的父节点
     * @example <div>xxxx<b>xxx</b>xxx</div> ==> <div>xxx</div><b>xx</b><div>xxx</div>
     */
    breakParent:function ( node, parent ) {
        var tmpNode, parentClone = node, clone = node, leftNodes, rightNodes;
        do {
            parentClone = parentClone.parentNode;
            if ( leftNodes ) {
                tmpNode = parentClone.cloneNode( false );
                tmpNode.appendChild( leftNodes );
                leftNodes = tmpNode;
                tmpNode = parentClone.cloneNode( false );
                tmpNode.appendChild( rightNodes );
                rightNodes = tmpNode;
            } else {
                leftNodes = parentClone.cloneNode( false );
                rightNodes = leftNodes.cloneNode( false );
            }
            while ( tmpNode = clone.previousSibling ) {
                leftNodes.insertBefore( tmpNode, leftNodes.firstChild );
            }
            while ( tmpNode = clone.nextSibling ) {
                rightNodes.appendChild( tmpNode );
            }
            clone = parentClone;
        } while ( parent !== parentClone );
        tmpNode = parent.parentNode;
        tmpNode.insertBefore( leftNodes, parent );
        tmpNode.insertBefore( rightNodes, parent );
        tmpNode.insertBefore( node, rightNodes );
        domUtils.remove( parent );
        return node;
    },

    /**
     * 检查是否是空inline节点
     * @param   {Node}    node      节点
     * @return {Boolean}  返回1为是，0为否
     * @example
     * &lt;b&gt;&lt;i&gt;&lt;/i&gt;&lt;/b&gt; //true
     * <b><i></i><u></u></b> true
     * &lt;b&gt;&lt;/b&gt; true  &lt;b&gt;xx&lt;i&gt;&lt;/i&gt;&lt;/b&gt; //false
     */
    isEmptyInlineElement:function ( node ) {
        if ( node.nodeType != 1 || !dtd.$removeEmpty[ node.tagName ] ) {
            return 0;
        }
        node = node.firstChild;
        while ( node ) {
            //如果是创建的bookmark就跳过
            if ( domUtils.isBookmarkNode( node ) ) {
                return 0;
            }
            if ( node.nodeType == 1 && !domUtils.isEmptyInlineElement( node ) ||
                    node.nodeType == 3 && !domUtils.isWhitespace( node )
                    ) {
                return 0;
            }
            node = node.nextSibling;
        }
        return 1;

    },

    /**
     * 删除空白子节点
     * @param   {Element}   node    需要删除空白子节点的元素
     */
    trimWhiteTextNode:function ( node ) {
        function remove( dir ) {
            var child;
            while ( (child = node[dir]) && child.nodeType == 3 && domUtils.isWhitespace( child ) ) {
                node.removeChild( child )
            }
        }

        remove( 'firstChild' );
        remove( 'lastChild' );
    },

    /**
     * 合并子节点
     * @param    {Node}    node     节点
     * @param    {String}    tagName     标签
     * @param    {String}    attrs     属性
     * @example &lt;span style="font-size:12px;"&gt;xx&lt;span style="font-size:12px;"&gt;aa&lt;/span&gt;xx&lt;/span  使用后
     * &lt;span style="font-size:12px;"&gt;xxaaxx&lt;/span
     */
    mergChild:function ( node, tagName, attrs ) {
        var list = domUtils.getElementsByTagName( node, node.tagName.toLowerCase() );
        for ( var i = 0, ci; ci = list[i++]; ) {
            if ( !ci.parentNode || domUtils.isBookmarkNode( ci ) ) {
                continue;
            }
            //span单独处理
            if ( ci.tagName.toLowerCase() == 'span' ) {
                if ( node === ci.parentNode ) {
                    domUtils.trimWhiteTextNode( node );
                    if ( node.childNodes.length == 1 ) {
                        node.style.cssText = ci.style.cssText + ";" + node.style.cssText;
                        domUtils.remove( ci, true );
                        continue;
                    }
                }
                ci.style.cssText = node.style.cssText + ';' + ci.style.cssText;
                if ( attrs ) {
                    var style = attrs.style;
                    if ( style ) {
                        style = style.split( ';' );
                        for ( var j = 0, s; s = style[j++]; ) {
                            ci.style[utils.cssStyleToDomStyle( s.split( ':' )[0] )] = s.split( ':' )[1];
                        }
                    }
                }
                if ( domUtils.isSameStyle( ci, node ) ) {
                    domUtils.remove( ci, true );
                }
                continue;
            }
            if ( domUtils.isSameElement( node, ci ) ) {
                domUtils.remove( ci, true );
            }
        }

        if ( tagName == 'span' ) {
            var as = domUtils.getElementsByTagName( node, 'a' );
            for ( var i = 0, ai; ai = as[i++]; ) {
                ai.style.cssText = ';' + node.style.cssText;
                ai.style.textDecoration = 'underline';
            }
        }
    },

    /**
     * 封装原生的getElemensByTagName
     * @param  {Node}    node       根节点
     * @param  {String}   name      标签的tagName
     * @return {Array}      返回符合条件的元素数组
     */
    getElementsByTagName:function ( node, name ) {
        var list = node.getElementsByTagName( name ), arr = [];
        for ( var i = 0, ci; ci = list[i++]; ) {
            arr.push( ci )
        }
        return arr;
    },
    /**
     * 将子节点合并到父节点上
     * @param {Element} node    节点
     * @example &lt;span style="color:#ff"&gt;&lt;span style="font-size:12px"&gt;xxx&lt;/span&gt;&lt;/span&gt; ==&gt; &lt;span style="color:#ff;font-size:12px"&gt;xxx&lt;/span&gt;
     */
    mergToParent:function ( node ) {
        var parent = node.parentNode;
        while ( parent && dtd.$removeEmpty[parent.tagName] ) {
            if ( parent.tagName == node.tagName || parent.tagName == 'A' ) {//针对a标签单独处理
                domUtils.trimWhiteTextNode( parent );
                //span需要特殊处理  不处理这样的情况 <span stlye="color:#fff">xxx<span style="color:#ccc">xxx</span>xxx</span>
                if ( parent.tagName == 'SPAN' && !domUtils.isSameStyle( parent, node )
                        || (parent.tagName == 'A' && node.tagName == 'SPAN') ) {
                    if ( parent.childNodes.length > 1 || parent !== node.parentNode ) {
                        node.style.cssText = parent.style.cssText + ";" + node.style.cssText;
                        parent = parent.parentNode;
                        continue;
                    } else {
                        parent.style.cssText += ";" + node.style.cssText;
                        //trace:952 a标签要保持下划线
                        if ( parent.tagName == 'A' ) {
                            parent.style.textDecoration = 'underline';
                        }
                    }
                }
                if ( parent.tagName != 'A' ) {
                    parent === node.parentNode && domUtils.remove( node, true );
                    break;
                }
            }
            parent = parent.parentNode;
        }
    },
    /**
     * 合并左右兄弟节点
     * @function
     * @param {Node}     node
     * @param {Boolean} ingoreNext   默认为false合并上一个兄弟节点。true为不合并上一个兄弟节点
     * @param {Boolean} ingorePre    默认为false合并下一个兄弟节点。true为不合并下一个兄弟节点
     * @example &lt;b&gt;xxxx&lt;/b&gt;&lt;b&gt;xxx&lt;/b&gt;&lt;b&gt;xxxx&lt;/b&gt; ==> &lt;b&gt;xxxxxxxxxxx&lt;/b&gt;
     */
    mergSibling:function ( node, ingorePre, ingoreNext ) {
        function merg( rtl, start, node ) {
            var next;
            if ( (next = node[rtl]) && !domUtils.isBookmarkNode( next ) && next.nodeType == 1 && domUtils.isSameElement( node, next ) ) {
                while ( next.firstChild ) {
                    if ( start == 'firstChild' ) {
                        node.insertBefore( next.lastChild, node.firstChild );
                    } else {
                        node.appendChild( next.firstChild );
                    }
                }
                domUtils.remove( next );
            }
        }

        !ingorePre && merg( 'previousSibling', 'firstChild', node );
        !ingoreNext && merg( 'nextSibling', 'lastChild', node );
    },

    /**
     * 使得元素及其子节点不能被选择
     * @function
     * @param   {Node}     node      节点
     */
    unselectable:ie || browser.opera ? function ( node ) {
        //for ie9
        node.onselectstart = function () {
            return false;
        };
        node.onclick = node.onkeyup = node.onkeydown = function () {
            return false;
        };
        node.unselectable = 'on';
        node.setAttribute( "unselectable", "on" );
        for ( var i = 0, ci; ci = node.all[i++]; ) {
            switch ( ci.tagName.toLowerCase() ) {
                case 'iframe' :
                case 'textarea' :
                case 'input' :
                case 'select' :
                    break;
                default :
                    ci.unselectable = 'on';
                    node.setAttribute( "unselectable", "on" );
            }
        }
    } : function ( node ) {
        node.style.MozUserSelect =
                node.style.webkitUserSelect =
                        node.style.KhtmlUserSelect = 'none';
    },
    /**
     * 删除元素上的属性，可以删除多个
     * @function
     * @param {Element} element      元素
     * @param {Array} attrNames      要删除的属性数组
     */
    removeAttributes:function ( elm, attrNames ) {
        for ( var i = 0, ci; ci = attrNames[i++]; ) {
            ci = attrFix[ci] || ci;
            switch ( ci ) {
                case 'className':
                    elm[ci] = '';
                    break;
                case 'style':
                    elm.style.cssText = '';
                    !browser.ie && elm.removeAttributeNode( elm.getAttributeNode( 'style' ) )
            }
            elm.removeAttribute( ci );
        }
    },
    creElm:function ( doc, tag, attrs ) {
        return this.setAttributes( doc.createElement( tag ), attrs )
    },
    /**
     * 给节点添加属性
     * @function
     * @param {Node} node      节点
     * @param {Object} attrNames     要添加的属性名称，采用json对象存放
     */
    setAttributes:function ( node, attrs ) {
        for ( var name in attrs ) {
            var value = attrs[name];
            switch ( name ) {
                case 'class':
                    //ie下要这样赋值，setAttribute不起作用
                    node.className = value;
                    break;
                case 'style' :
                    node.style.cssText = node.style.cssText + ";" + value;
                    break;
                case 'innerHTML':
                    node[name] = value;
                    break;
                case 'value':
                    node.value = value;
                    break;
                default:
                    node.setAttribute( attrFix[name] || name, value );
            }
        }
        return node;
    },

    /**
     * 获取元素的样式
     * @function
     * @param {Element} element    元素
     * @param {String} styleName    样式名称
     * @return  {String}    样式值
     */
    getComputedStyle:function ( element, styleName ) {
        function fixUnit( key, val ) {
            if ( key == 'font-size' && /pt$/.test( val ) ) {
                val = Math.round( parseFloat( val ) / 0.75 ) + 'px';
            }
            return val;
        }

        if ( element.nodeType == 3 ) {
            element = element.parentNode;
        }
        //ie下font-size若body下定义了font-size，则从currentStyle里会取到这个font-size. 取不到实际值，故此修改.
        if ( browser.ie && browser.version < 9 && styleName == 'font-size' && !element.style.fontSize &&
                !dtd.$empty[element.tagName] && !dtd.$nonChild[element.tagName] ) {
            var span = element.ownerDocument.createElement( 'span' );
            span.style.cssText = 'padding:0;border:0;font-family:simsun;';
            span.innerHTML = '.';
            element.appendChild( span );
            var result = span.offsetHeight;
            element.removeChild( span );
            span = null;
            return result + 'px';
        }
        try {
            var value = domUtils.getStyle( element, styleName ) ||
                    (window.getComputedStyle ? domUtils.getWindow( element ).getComputedStyle( element, '' ).getPropertyValue( styleName ) :
                            ( element.currentStyle || element.style )[utils.cssStyleToDomStyle( styleName )]);

        } catch ( e ) {
            return null;
        }
        return fixUnit( styleName, utils.fixColor( styleName, value ) );
    },

    /**
     * 删除cssClass，可以支持删除多个class
     * @param {Element} element         元素
     * @param {Array} classNames        删除的className
     */
    removeClasses:function ( element, classNames ) {
        classNames = utils.isArray( classNames ) ? classNames : [classNames];
        element.className = (' ' + element.className + ' ').replace(
                new RegExp( '(?:\\s+(?:' + classNames.join( '|' ) + '))+\\s+', 'g' ), ' ' );
    },
    /**
     * 增加一个class
     * @param element
     * @param className
     */
    addClass:function ( element, className ) {
        if ( !this.hasClass( element, className ) ) {
            element.className += " " + className;
        }
    },
    /**
     * 删除元素的样式
     * @param {Element} element元素
     * @param {String} name        删除的样式名称
     */
    removeStyle:function ( node, name ) {
        node.style[utils.cssStyleToDomStyle( name )] = '';
        if ( !node.style.cssText ) {
            domUtils.removeAttributes( node, ['style'] );
        }
    },
    /**
     * 判断元素属性中是否包含某一个classname
     * @param {Element} element    元素
     * @param {String} className    样式名
     * @returns {Boolean}       是否包含该classname
     */
    hasClass:function ( element, className ) {
        return ( ' ' + element.className + ' ' ).indexOf( ' ' + className + ' ' ) > -1;
    },

    /**
     * 阻止事件默认行为
     * @param {Event} evt    需要组织的事件对象
     */
    preventDefault:function ( evt ) {
        evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
    },
    /**
     * 获得元素样式
     * @param {Element} element    元素
     * @param {String}  name    样式名称
     * @return  {String}   返回元素样式值
     */
    getStyle:function ( element, name ) {
        var value = element.style[ utils.cssStyleToDomStyle( name ) ];
        return utils.fixColor( name, value );
    },
    setStyle:function ( element, name, value ) {
        element.style[utils.cssStyleToDomStyle( name )] = value;
    },
    setStyles:function ( element, styles ) {
        for ( var name in styles ) {
            if ( styles.hasOwnProperty( name ) ) {
                domUtils.setStyle( element, name, styles[name] );
            }
        }
    },
    /**
     * 删除_moz_dirty属性
     * @function
     * @param {Node}    node    节点
     */
    removeDirtyAttr:function ( node ) {
        for ( var i = 0, ci, nodes = node.getElementsByTagName( '*' ); ci = nodes[i++]; ) {
            ci.removeAttribute( '_moz_dirty' );
        }
        node.removeAttribute( '_moz_dirty' );
    },
    /**
     * 返回子节点的数量
     * @function
     * @param {Node}    node    父节点
     * @param  {Function}    fn    过滤子节点的规则，若为空，则得到所有子节点的数量
     * @return {Number}    符合条件子节点的数量
     */
    getChildCount:function ( node, fn ) {
        var count = 0, first = node.firstChild;
        fn = fn || function () {
            return 1;
        };
        while ( first ) {
            if ( fn( first ) ) {
                count++;
            }
            first = first.nextSibling;
        }
        return count;
    },

    /**
     * 判断是否为空节点
     * @function
     * @param {Node}    node    节点
     * @return {Boolean}    是否为空节点
     */
    isEmptyNode:function ( node ) {
        return !node.firstChild || domUtils.getChildCount( node, function ( node ) {
            return  !domUtils.isBr( node ) && !domUtils.isBookmarkNode( node ) && !domUtils.isWhitespace( node )
        } ) == 0
    },
    /**
     * 清空节点所有的className
     * @function
     * @param {Array}    nodes    节点数组
     */
    clearSelectedArr:function ( nodes ) {
        var node;
        while ( node = nodes.pop() ) {
            domUtils.removeAttributes( node, ['class'] );
        }
    },
    /**
     * 将显示区域滚动到显示节点的位置
     * @function
     * @param    {Node}   node    节点
     * @param    {window}   win      window对象
     * @param    {Number}    offsetTop    距离上方的偏移量
     */
    scrollToView:function ( node, win, offsetTop ) {
        var getViewPaneSize = function () {
                    var doc = win.document,
                            mode = doc.compatMode == 'CSS1Compat';
                    return {
                        width:( mode ? doc.documentElement.clientWidth : doc.body.clientWidth ) || 0,
                        height:( mode ? doc.documentElement.clientHeight : doc.body.clientHeight ) || 0
                    };
                },
                getScrollPosition = function ( win ) {
                    if ( 'pageXOffset' in win ) {
                        return {
                            x:win.pageXOffset || 0,
                            y:win.pageYOffset || 0
                        };
                    }
                    else {
                        var doc = win.document;
                        return {
                            x:doc.documentElement.scrollLeft || doc.body.scrollLeft || 0,
                            y:doc.documentElement.scrollTop || doc.body.scrollTop || 0
                        };
                    }
                };
        var winHeight = getViewPaneSize().height, offset = winHeight * -1 + offsetTop;
        offset += (node.offsetHeight || 0);
        var elementPosition = domUtils.getXY( node );
        offset += elementPosition.y;
        var currentScroll = getScrollPosition( win ).y;
        // offset += 50;
        if ( offset > currentScroll || offset < currentScroll - winHeight ) {
            win.scrollTo( 0, offset + (offset < 0 ? -20 : 20) );
        }
    },
    /**
     * 判断节点是否为br
     * @function
     * @param {Node}    node   节点
     */
    isBr:function ( node ) {
        return node.nodeType == 1 && node.tagName == 'BR';
    },
    isFillChar:function ( node ) {
        return node.nodeType == 3 && !node.nodeValue.replace( new RegExp( domUtils.fillChar ), '' ).length
    },
    isStartInblock:function ( range ) {
        var tmpRange = range.cloneRange(),
                flag = 0,
                start = tmpRange.startContainer,
                tmp;
        while ( start && domUtils.isFillChar( start ) ) {
            tmp = start;
            start = start.previousSibling
        }
        if ( tmp ) {
            tmpRange.setStartBefore( tmp );
            start = tmpRange.startContainer;
        }
        if ( start.nodeType == 1 && domUtils.isEmptyNode( start ) && tmpRange.startOffset == 1 ) {
            tmpRange.setStart( start, 0 ).collapse( true );
        }
        while ( !tmpRange.startOffset ) {
            start = tmpRange.startContainer;
            if ( domUtils.isBlockElm( start ) || domUtils.isBody( start ) ) {
                flag = 1;
                break;
            }
            var pre = tmpRange.startContainer.previousSibling,
                    tmpNode;
            if ( !pre ) {
                tmpRange.setStartBefore( tmpRange.startContainer );
            } else {
                while ( pre && domUtils.isFillChar( pre ) ) {
                    tmpNode = pre;
                    pre = pre.previousSibling;
                }
                if ( tmpNode ) {
                    tmpRange.setStartBefore( tmpNode );
                } else {
                    tmpRange.setStartBefore( tmpRange.startContainer );
                }
            }
        }
        return flag && !domUtils.isBody( tmpRange.startContainer ) ? 1 : 0;
    },
    isEmptyBlock:function ( node ) {
        var reg = new RegExp( '[ \t\r\n' + domUtils.fillChar + ']', 'g' );
        if ( node[browser.ie ? 'innerText' : 'textContent'].replace( reg, '' ).length > 0 ) {
            return 0;
        }
        for ( var n in dtd.$isNotEmpty ) {
            if ( node.getElementsByTagName( n ).length ) {
                return 0;
            }
        }
        return 1;
    },

    setViewportOffset:function ( element, offset ) {
        var left = parseInt( element.style.left ) | 0;
        var top = parseInt( element.style.top ) | 0;
        var rect = element.getBoundingClientRect();
        var offsetLeft = offset.left - rect.left;
        var offsetTop = offset.top - rect.top;
        if ( offsetLeft ) {
            element.style.left = left + offsetLeft + 'px';
        }
        if ( offsetTop ) {
            element.style.top = top + offsetTop + 'px';
        }
    },
    fillNode:function ( doc, node ) {
        var tmpNode = browser.ie ? doc.createTextNode( domUtils.fillChar ) : doc.createElement( 'br' );
        node.innerHTML = '';
        node.appendChild( tmpNode );
    },
    moveChild:function ( src, tag, dir ) {
        while ( src.firstChild ) {
            if ( dir && tag.firstChild ) {
                tag.insertBefore( src.lastChild, tag.firstChild );
            } else {
                tag.appendChild( src.firstChild );
            }
        }
    },
    //判断是否有额外属性
    hasNoAttributes:function ( node ) {
        return browser.ie ? /^<\w+\s*?>/.test( node.outerHTML ) : node.attributes.length == 0;
    },
    //判断是否是编辑器自定义的参数
    isCustomeNode:function ( node ) {
        return node.nodeType == 1 && node.getAttribute( '_ue_custom_node_' );
    },
    isTagNode:function ( node, tagName ) {
        return node.nodeType == 1 && node.tagName.toLowerCase() == tagName;
    }
};
var fillCharReg = new RegExp( domUtils.fillChar, 'g' );