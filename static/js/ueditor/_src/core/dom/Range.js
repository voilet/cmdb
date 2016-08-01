///import editor.js
///import core/utils.js
///import core/browser.js
///import core/dom/dom.js
///import core/dom/dtd.js
///import core/dom/domUtils.js
/**
 * @class baidu.editor.dom.Range    Range类
 */
/**
 * @description Range类实现
 * @author zhanyi
 */
(function () {
    var guid = 0,
            fillChar = domUtils.fillChar,
            fillData;

    /**
     * 更新range的collapse状态
     * @param  {Range}   range    range对象
     */
    function updateCollapse( range ) {
        range.collapsed =
                range.startContainer && range.endContainer &&
                        range.startContainer === range.endContainer &&
                        range.startOffset == range.endOffset;
    }

    function setEndPoint( toStart, node, offset, range ) {
        //如果node是自闭合标签要处理
        if ( node.nodeType == 1 && (dtd.$empty[node.tagName] || dtd.$nonChild[node.tagName]) ) {
            offset = domUtils.getNodeIndex( node ) + (toStart ? 0 : 1);
            node = node.parentNode;
        }
        if ( toStart ) {
            range.startContainer = node;
            range.startOffset = offset;
            if ( !range.endContainer ) {
                range.collapse( true );
            }
        } else {
            range.endContainer = node;
            range.endOffset = offset;
            if ( !range.startContainer ) {
                range.collapse( false );
            }
        }
        updateCollapse( range );
        return range;
    }

    function execContentsAction( range, action ) {
        //调整边界
        //range.includeBookmark();
        var start = range.startContainer,
                end = range.endContainer,
                startOffset = range.startOffset,
                endOffset = range.endOffset,
                doc = range.document,
                frag = doc.createDocumentFragment(),
                tmpStart, tmpEnd;
        if ( start.nodeType == 1 ) {
            start = start.childNodes[startOffset] || (tmpStart = start.appendChild( doc.createTextNode( '' ) ));
        }
        if ( end.nodeType == 1 ) {
            end = end.childNodes[endOffset] || (tmpEnd = end.appendChild( doc.createTextNode( '' ) ));
        }
        if ( start === end && start.nodeType == 3 ) {
            frag.appendChild( doc.createTextNode( start.substringData( startOffset, endOffset - startOffset ) ) );
            //is not clone
            if ( action ) {
                start.deleteData( startOffset, endOffset - startOffset );
                range.collapse( true );
            }
            return frag;
        }
        var current, currentLevel, clone = frag,
                startParents = domUtils.findParents( start, true ), endParents = domUtils.findParents( end, true );
        for ( var i = 0; startParents[i] == endParents[i]; ) {
            i++;
        }
        for ( var j = i, si; si = startParents[j]; j++ ) {
            current = si.nextSibling;
            if ( si == start ) {
                if ( !tmpStart ) {
                    if ( range.startContainer.nodeType == 3 ) {
                        clone.appendChild( doc.createTextNode( start.nodeValue.slice( startOffset ) ) );
                        //is not clone
                        if ( action ) {
                            start.deleteData( startOffset, start.nodeValue.length - startOffset );
                        }
                    } else {
                        clone.appendChild( !action ? start.cloneNode( true ) : start );
                    }
                }
            } else {
                currentLevel = si.cloneNode( false );
                clone.appendChild( currentLevel );
            }
            while ( current ) {
                if ( current === end || current === endParents[j] ) {
                    break;
                }
                si = current.nextSibling;
                clone.appendChild( !action ? current.cloneNode( true ) : current );
                current = si;
            }
            clone = currentLevel;
        }
        clone = frag;
        if ( !startParents[i] ) {
            clone.appendChild( startParents[i - 1].cloneNode( false ) );
            clone = clone.firstChild;
        }
        for ( var j = i, ei; ei = endParents[j]; j++ ) {
            current = ei.previousSibling;
            if ( ei == end ) {
                if ( !tmpEnd && range.endContainer.nodeType == 3 ) {
                    clone.appendChild( doc.createTextNode( end.substringData( 0, endOffset ) ) );
                    //is not clone
                    if ( action ) {
                        end.deleteData( 0, endOffset );
                    }
                }
            } else {
                currentLevel = ei.cloneNode( false );
                clone.appendChild( currentLevel );
            }
            //如果两端同级，右边第一次已经被开始做了
            if ( j != i || !startParents[i] ) {
                while ( current ) {
                    if ( current === start ) {
                        break;
                    }
                    ei = current.previousSibling;
                    clone.insertBefore( !action ? current.cloneNode( true ) : current, clone.firstChild );
                    current = ei;
                }
            }
            clone = currentLevel;
        }
        if ( action ) {
            range.setStartBefore( !endParents[i] ? endParents[i - 1] : !startParents[i] ? startParents[i - 1] : endParents[i] ).collapse( true );
        }
        tmpStart && domUtils.remove( tmpStart );
        tmpEnd && domUtils.remove( tmpEnd );
        return frag;
    }
    /**
     * Range类
     * @param {Document} document 编辑器页面document对象
     */
    var Range = dom.Range = function ( document ) {
        var me = this;
        me.startContainer =
                me.startOffset =
                        me.endContainer =
                                me.endOffset = null;
        me.document = document;
        me.collapsed = true;
    };

    /**
     * 删除fillData
     * @param doc
     * @param excludeNode
     */
    function removeFillData( doc, excludeNode ) {
        try {
            if ( fillData && domUtils.inDoc( fillData, doc ) ) {
                if ( !fillData.nodeValue.replace( fillCharReg, '' ).length ) {
                    var tmpNode = fillData.parentNode;
                    domUtils.remove( fillData );
                    while ( tmpNode && domUtils.isEmptyInlineElement( tmpNode ) && !tmpNode.contains( excludeNode ) ) {
                        fillData = tmpNode.parentNode;
                        domUtils.remove( tmpNode );
                        tmpNode = fillData;
                    }
                } else {
                    fillData.nodeValue = fillData.nodeValue.replace( fillCharReg, '' );
                }
            }
        } catch ( e ) {
        }
    }

    /**
     *
     * @param node
     * @param dir
     */
    function mergSibling( node, dir ) {
        var tmpNode;
        node = node[dir];
        while ( node && domUtils.isFillChar( node ) ) {
            tmpNode = node[dir];
            domUtils.remove( node );
            node = tmpNode;
        }
    }
    Range.prototype = {
        /**
         * 克隆选中的内容到一个fragment里
         * @public
         * @function
         * @name    baidu.editor.dom.Range.cloneContents
         * @return {Fragment}    frag|null 返回选中内容的文本片段或者空
         */
        cloneContents:function () {
            return this.collapsed ? null : execContentsAction( this, 0 );
        },
        /**
         * 删除所选内容
         * @public
         * @function
         * @name    baidu.editor.dom.Range.deleteContents
         * @return {Range}    删除选中内容后的Range
         */
        deleteContents:function () {
            var txt;
            if ( !this.collapsed ) {
                execContentsAction( this, 1 );
            }
            if ( browser.webkit ) {
                txt = this.startContainer;
                if ( txt.nodeType == 3 && !txt.nodeValue.length ) {
                    this.setStartBefore( txt ).collapse( true );
                    domUtils.remove( txt );
                }
            }
            return this;
        },
        /**
         * 取出内容
         * @public
         * @function
         * @name    baidu.editor.dom.Range.extractContents
         * @return {String}    获得Range选中的内容
         */
        extractContents:function () {
            return this.collapsed ? null : execContentsAction( this, 2 );
        },
        /**
         * 设置range的开始位置
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setStart
         * @param    {Node}     node     range开始节点
         * @param    {Number}   offset   偏移量
         * @return   {Range}    返回Range
         */
        setStart:function ( node, offset ) {
            return setEndPoint( true, node, offset, this );
        },
        /**
         * 设置range结束点的位置
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setEnd
         * @param    {Node}     node     range结束节点
         * @param    {Number}   offset   偏移量
         * @return   {Range}    返回Range
         */
        setEnd:function ( node, offset ) {
            return setEndPoint( false, node, offset, this );
        },
        /**
         * 将开始位置设置到node后
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setStartAfter
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setStartAfter:function ( node ) {
            return this.setStart( node.parentNode, domUtils.getNodeIndex( node ) + 1 );
        },
        /**
         * 将开始位置设置到node前
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setStartBefore
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setStartBefore:function ( node ) {
            return this.setStart( node.parentNode, domUtils.getNodeIndex( node ) );
        },
        /**
         * 将结束点位置设置到node后
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setEndAfter
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setEndAfter:function ( node ) {
            return this.setEnd( node.parentNode, domUtils.getNodeIndex( node ) + 1 );
        },
        /**
         * 将开始设置到node的最开始位置  <element>^text</element>
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setEndAfter
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setStartAtFirst:function ( node ) {
            return this.setStart( node, 0 );
        },
        /**
         * 将开始设置到node的最开始位置  <element>text^</element>
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setEndAfter
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setStartAtLast:function ( node ) {
            return this.setStart( node, node.nodeType == 3 ? node.nodeValue.length : node.childNodes.length );
        },
        /**
         * 将结束设置到node的最开始位置  <element>^text</element>
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setEndAfter
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setEndAtFirst:function ( node ) {
            return this.setEnd( node, 0 );
        },
        /**
         * 将结束设置到node的最开始位置  <element>text^</element>
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setEndAfter
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setEndAtLast:function ( node ) {
            return this.setEnd( node, node.nodeType == 3 ? node.nodeValue.length : node.childNodes.length );
        },
        /**
         * 将结束点位置设置到node前
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setEndBefore
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        setEndBefore:function ( node ) {
            return this.setEnd( node.parentNode, domUtils.getNodeIndex( node ) );
        },
        /**
         * 选中指定节点
         * @public
         * @function
         * @name    baidu.editor.dom.Range.selectNode
         * @param    {Node}     node     节点
         * @return   {Range}    返回Range
         */
        selectNode:function ( node ) {
            return this.setStartBefore( node ).setEndAfter( node );
        },
        /**
         * 选中node下的所有节点
         * @public
         * @function
         * @name    baidu.editor.dom.Range.selectNodeContents
         * @param {Element} node 要设置的节点
         * @return   {Range}    返回Range
         */
        selectNodeContents:function ( node ) {
            return this.setStart( node, 0 ).setEnd( node, node.nodeType == 3 ? node.nodeValue.length : node.childNodes.length );
        },

        /**
         * 克隆range
         * @public
         * @function
         * @name    baidu.editor.dom.Range.cloneRange
         * @return {Range} 克隆的range对象
         */
        cloneRange:function () {
            var me = this, range = new Range( me.document );
            return range.setStart( me.startContainer, me.startOffset ).setEnd( me.endContainer, me.endOffset );

        },

        /**
         * 让选区闭合
         * @public
         * @function
         * @name    baidu.editor.dom.Range.collapse
         * @param {Boolean} toStart 是否在选区开始位置闭合选区，true在开始位置闭合，false反之
         * @return {Range}  range对象
         */
        collapse:function ( toStart ) {
            var me = this;
            if ( toStart ) {
                me.endContainer = me.startContainer;
                me.endOffset = me.startOffset;
            }
            else {
                me.startContainer = me.endContainer;
                me.startOffset = me.endOffset;
            }

            me.collapsed = true;
            return me;
        },
        /**
         * 调整range的边界，“缩”到合适的位置
         * @public
         * @function
         * @name    baidu.editor.dom.Range.shrinkBoundary
         * @param    {Boolean}     ignoreEnd      是否考虑前面的元素
         */
        shrinkBoundary:function ( ignoreEnd ) {
            var me = this, child,
                    collapsed = me.collapsed;
            while ( me.startContainer.nodeType == 1 //是element
                    && (child = me.startContainer.childNodes[me.startOffset]) //子节点也是element
                    && child.nodeType == 1 && !domUtils.isBookmarkNode( child )
                    && !dtd.$empty[child.tagName] && !dtd.$nonChild[child.tagName] ) {
                me.setStart( child, 0 );
            }
            if ( collapsed ) {
                return me.collapse( true );
            }
            if ( !ignoreEnd ) {
                while ( me.endContainer.nodeType == 1//是element
                        && me.endOffset > 0 //如果是空元素就退出 endOffset=0那么endOffst-1为负值，childNodes[endOffset]报错
                        && (child = me.endContainer.childNodes[me.endOffset - 1]) //子节点也是element
                        && child.nodeType == 1 && !domUtils.isBookmarkNode( child )
                        && !dtd.$empty[child.tagName] && !dtd.$nonChild[child.tagName] ) {
                    me.setEnd( child, child.childNodes.length );
                }
            }
            return me;
        },
        /**
         * 找到startContainer和endContainer的公共祖先节点
         * @public
         * @function
         * @name    baidu.editor.dom.Range.getCommonAncestor
         * @param {Boolean} includeSelf 是否包含自身
         * @param {Boolean} ignoreTextNode 是否忽略文本节点
         * @return   {Node}   祖先节点
         */
        getCommonAncestor:function ( includeSelf, ignoreTextNode ) {
            var start = this.startContainer,
                    end = this.endContainer;
            if ( start === end ) {
                if ( includeSelf && start.nodeType == 1 && this.startOffset == this.endOffset - 1 ) {
                    return start.childNodes[this.startOffset];
                }
                //只有在上来就相等的情况下才会出现是文本的情况
                return ignoreTextNode && start.nodeType == 3 ? start.parentNode : start;
            }
            return domUtils.getCommonAncestor( start, end );

        },
        /**
         * 切割文本节点，将边界扩大到element
         * @public
         * @function
         * @name    baidu.editor.dom.Range.trimBoundary
         * @param {Boolean}  ignoreEnd    为真就不处理结束边界
         * @return {Range}    range对象
         * @example <b>|xxx</b>
         * startContainer = xxx; startOffset = 0
         * 执行后
         * startContainer = <b>;  startOffset = 0
         * @example <b>xx|x</b>
         * startContainer = xxx;  startOffset = 2
         * 执行后
         * startContainer = <b>; startOffset = 1  因为将xxx切割成2个节点了
         */
        trimBoundary:function ( ignoreEnd ) {
            this.txtToElmBoundary();
            var start = this.startContainer,
                    offset = this.startOffset,
                    collapsed = this.collapsed,
                    end = this.endContainer;
            if ( start.nodeType == 3 ) {
                if ( offset == 0 ) {
                    this.setStartBefore( start );
                } else {
                    if ( offset >= start.nodeValue.length ) {
                        this.setStartAfter( start );
                    } else {
                        var textNode = domUtils.split( start, offset );
                        //跟新结束边界
                        if ( start === end ) {
                            this.setEnd( textNode, this.endOffset - offset );
                        } else if ( start.parentNode === end ) {
                            this.endOffset += 1;
                        }
                        this.setStartBefore( textNode );
                    }
                }
                if ( collapsed ) {
                    return this.collapse( true );
                }
            }
            if ( !ignoreEnd ) {
                offset = this.endOffset;
                end = this.endContainer;
                if ( end.nodeType == 3 ) {
                    if ( offset == 0 ) {
                        this.setEndBefore( end );
                    } else {
                        if ( offset >= end.nodeValue.length ) {
                            this.setEndAfter( end );
                        } else {
                            domUtils.split( end, offset );
                            this.setEndAfter( end );
                        }
                    }
                }
            }
            return this;
        },
        /**
         * 如果选区在文本的边界上，就扩展选区到文本的父节点上
         * @public
         * @function
         * @name    baidu.editor.dom.Range.txtToElmBoundary
         * @return {Range}    range对象
         * @example <b> |xxx</b>
         * startContainer = xxx;  startOffset = 0
         * 执行后
         * startContainer = <b>; startOffset = 0
         * @example <b> xxx| </b>
         * startContainer = xxx; startOffset = 3
         * 执行后
         * startContainer = <b>; startOffset = 1
         */
        txtToElmBoundary:function () {
            function adjust( r, c ) {
                var container = r[c + 'Container'],
                        offset = r[c + 'Offset'];
                if ( container.nodeType == 3 ) {
                    if ( !offset ) {
                        r['set' + c.replace( /(\w)/, function ( a ) {
                            return a.toUpperCase();
                        } ) + 'Before']( container );
                    } else if ( offset >= container.nodeValue.length ) {
                        r['set' + c.replace( /(\w)/, function ( a ) {
                            return a.toUpperCase();
                        } ) + 'After' ]( container );
                    }
                }
            }

            if ( !this.collapsed ) {
                adjust( this, 'start' );
                adjust( this, 'end' );
            }
            return this;
        },

        /**
         * 在当前选区的开始位置前插入一个节点或者fragment
         * @public
         * @function
         * @name    baidu.editor.dom.Range.insertNode
         * @param {Node/DocumentFragment}    node    要插入的节点或fragment
         * @return  {Range}    返回range对象
         */
        insertNode:function ( node ) {
            var first = node, length = 1;
            if ( node.nodeType == 11 ) {
                first = node.firstChild;
                length = node.childNodes.length;
            }
            this.trimBoundary( true );
            var start = this.startContainer,
                    offset = this.startOffset;
            var nextNode = start.childNodes[ offset ];
            if ( nextNode ) {
                start.insertBefore( node, nextNode );
            } else {
                start.appendChild( node );
            }
            if ( first.parentNode === this.endContainer ) {
                this.endOffset = this.endOffset + length;
            }
            return this.setStartBefore( first );
        },
        /**
         * 设置光标位置
         * @public
         * @function
         * @name    baidu.editor.dom.Range.setCursor
         * @param {Boolean}   toEnd   true为闭合到选区的结束位置后，false为闭合到选区的开始位置前
         * @return  {Range}    返回range对象
         */
        setCursor:function ( toEnd, notFillData ) {
            return this.collapse( !toEnd ).select( notFillData );
        },
        /**
         * 创建书签
         * @public
         * @function
         * @name    baidu.editor.dom.Range.createBookmark
         * @param {Boolean}   serialize    true：为true则返回对象中用id来分别表示书签的开始和结束节点
         * @param  {Boolean}   same        true：是否采用唯一的id，false将会为每一个标签产生一个唯一的id
         * @returns {Object} bookmark对象
         */
        createBookmark:function ( serialize, same ) {
            var endNode,
                    startNode = this.document.createElement( 'span' );
            startNode.style.cssText = 'display:none;line-height:0px;';
            startNode.appendChild( this.document.createTextNode( '\uFEFF' ) );
            startNode.id = '_baidu_bookmark_start_' + (same ? '' : guid++);

            if ( !this.collapsed ) {
                endNode = startNode.cloneNode( true );
                endNode.id = '_baidu_bookmark_end_' + (same ? '' : guid++);
            }
            this.insertNode( startNode );
            if ( endNode ) {
                this.collapse( false ).insertNode( endNode );
                this.setEndBefore( endNode );
            }
            this.setStartAfter( startNode );
            return {
                start:serialize ? startNode.id : startNode,
                end:endNode ? serialize ? endNode.id : endNode : null,
                id:serialize
            }
        },
        /**
         *  移动边界到书签，并删除书签
         *  @public
         *  @function
         *  @name    baidu.editor.dom.Range.moveToBookmark
         *  @params {Object} bookmark对象
         *  @returns {Range}    Range对象
         */
        moveToBookmark:function ( bookmark ) {
            var start = bookmark.id ? this.document.getElementById( bookmark.start ) : bookmark.start,
                    end = bookmark.end && bookmark.id ? this.document.getElementById( bookmark.end ) : bookmark.end;
            this.setStartBefore( start );
            domUtils.remove( start );
            if ( end ) {
                this.setEndBefore( end );
                domUtils.remove( end );
            } else {
                this.collapse( true );
            }
            return this;
        },
        /**
         * 调整边界到一个block元素上，或者移动到最大的位置
         * @public
         * @function
         * @name    baidu.editor.dom.Range.enlarge
         * @params {Boolean}  toBlock    扩展到block元素
         * @params {Function} stopFn      停止函数，若返回true，则不再扩展
         * @return   {Range}    Range对象
         */
        enlarge:function ( toBlock, stopFn ) {
            var isBody = domUtils.isBody,
                    pre, node, tmp = this.document.createTextNode( '' );
            if ( toBlock ) {
                node = this.startContainer;
                if ( node.nodeType == 1 ) {
                    if ( node.childNodes[this.startOffset] ) {
                        pre = node = node.childNodes[this.startOffset]
                    } else {
                        node.appendChild( tmp );
                        pre = node = tmp;
                    }
                } else {
                    pre = node;
                }
                while ( 1 ) {
                    if ( domUtils.isBlockElm( node ) ) {
                        node = pre;
                        while ( (pre = node.previousSibling) && !domUtils.isBlockElm( pre ) ) {
                            node = pre;
                        }
                        this.setStartBefore( node );
                        break;
                    }
                    pre = node;
                    node = node.parentNode;
                }
                node = this.endContainer;
                if ( node.nodeType == 1 ) {
                    if ( pre = node.childNodes[this.endOffset] ) {
                        node.insertBefore( tmp, pre );
                    } else {
                        node.appendChild( tmp );
                    }
                    pre = node = tmp;
                } else {
                    pre = node;
                }
                while ( 1 ) {
                    if ( domUtils.isBlockElm( node ) ) {
                        node = pre;
                        while ( (pre = node.nextSibling) && !domUtils.isBlockElm( pre ) ) {
                            node = pre;
                        }
                        this.setEndAfter( node );
                        break;
                    }
                    pre = node;
                    node = node.parentNode;
                }
                if ( tmp.parentNode === this.endContainer ) {
                    this.endOffset--;
                }
                domUtils.remove( tmp );
            }

            // 扩展边界到最大
            if ( !this.collapsed ) {
                while ( this.startOffset == 0 ) {
                    if ( stopFn && stopFn( this.startContainer ) ) {
                        break;
                    }
                    if ( isBody( this.startContainer ) ) {
                        break;
                    }
                    this.setStartBefore( this.startContainer );
                }
                while ( this.endOffset == (this.endContainer.nodeType == 1 ? this.endContainer.childNodes.length : this.endContainer.nodeValue.length) ) {
                    if ( stopFn && stopFn( this.endContainer ) ) {
                        break;
                    }
                    if ( isBody( this.endContainer ) ) {
                        break;
                    }
                    this.setEndAfter( this.endContainer );
                }
            }
            return this;
        },
        /**
         * 调整边界
         * @public
         * @function
         * @name    baidu.editor.dom.Range.adjustmentBoundary
         * @return   {Range}    Range对象
         * @example
         * <b>xx[</b>xxxxx] ==> <b>xx</b>[xxxxx]
         * <b>[xx</b><i>]xxx</i> ==> <b>[xx</b>]<i>xxx</i>
         *
         */
        adjustmentBoundary:function () {
            if ( !this.collapsed ) {
                while ( !domUtils.isBody( this.startContainer ) &&
                        this.startOffset == this.startContainer[this.startContainer.nodeType == 3 ? 'nodeValue' : 'childNodes'].length
                        ) {
                    this.setStartAfter( this.startContainer );
                }
                while ( !domUtils.isBody( this.endContainer ) && !this.endOffset ) {
                    this.setEndBefore( this.endContainer );
                }
            }
            return this;
        },
        /**
         * 给选区中的内容加上inline样式
         * @public
         * @function
         * @name    baidu.editor.dom.Range.applyInlineStyle
         * @param {String} tagName 标签名称
         * @param {Object} attrObj 属性
         * @return   {Range}    Range对象
         */
        applyInlineStyle:function ( tagName, attrs, list ) {
            if ( this.collapsed )return this;
            this.trimBoundary().enlarge( false,
                    function ( node ) {
                        return node.nodeType == 1 && domUtils.isBlockElm( node )
                    } ).adjustmentBoundary();
            var bookmark = this.createBookmark(),
                    end = bookmark.end,
                    filterFn = function ( node ) {
                        return node.nodeType == 1 ? node.tagName.toLowerCase() != 'br' : !domUtils.isWhitespace( node );
                    },
                    current = domUtils.getNextDomNode( bookmark.start, false, filterFn ),
                    node,
                    pre,
                    range = this.cloneRange();
            while ( current && (domUtils.getPosition( current, end ) & domUtils.POSITION_PRECEDING) ) {
                if ( current.nodeType == 3 || dtd[tagName][current.tagName] ) {
                    range.setStartBefore( current );
                    node = current;
                    while ( node && (node.nodeType == 3 || dtd[tagName][node.tagName]) && node !== end ) {
                        pre = node;
                        node = domUtils.getNextDomNode( node, node.nodeType == 1, null, function ( parent ) {
                            return dtd[tagName][parent.tagName];
                        } );
                    }
                    var frag = range.setEndAfter( pre ).extractContents(), elm;
                    if ( list && list.length > 0 ) {
                        var level, top;
                        top = level = list[0].cloneNode( false );
                        for ( var i = 1, ci; ci = list[i++]; ) {
                            level.appendChild( ci.cloneNode( false ) );
                            level = level.firstChild;
                        }
                        elm = level;
                    } else {
                        elm = range.document.createElement( tagName );
                    }
                    if ( attrs ) {
                        domUtils.setAttributes( elm, attrs );
                    }
                    elm.appendChild( frag );
                    range.insertNode( list ? top : elm );
                    //处理下滑线在a上的情况
                    var aNode;
                    if ( tagName == 'span' && attrs.style && /text\-decoration/.test( attrs.style ) && (aNode = domUtils.findParentByTagName( elm, 'a', true )) ) {
                        domUtils.setAttributes( aNode, attrs );
                        domUtils.remove( elm, true );
                        elm = aNode;
                    } else {
                        domUtils.mergSibling( elm );
                        domUtils.clearEmptySibling( elm );
                    }
                    //去除子节点相同的
                    domUtils.mergChild( elm, tagName, attrs );
                    current = domUtils.getNextDomNode( elm, false, filterFn );
                    domUtils.mergToParent( elm );
                    if ( node === end ) {
                        break;
                    }
                } else {
                    current = domUtils.getNextDomNode( current, true, filterFn );
                }
            }
            return this.moveToBookmark( bookmark );
        },
        /**
         * 去掉inline样式
         * @public
         * @function
         * @name    baidu.editor.dom.Range.removeInlineStyle
         * @param  {String/Array}    tagName    要去掉的标签名
         * @return   {Range}    Range对象
         */
        removeInlineStyle:function ( tagName ) {
            if ( this.collapsed )return this;
            tagName = utils.isArray( tagName ) ? tagName : [tagName];
            this.shrinkBoundary().adjustmentBoundary();
            var start = this.startContainer, end = this.endContainer;
            while ( 1 ) {
                if ( start.nodeType == 1 ) {
                    if ( utils.indexOf( tagName, start.tagName.toLowerCase() ) > -1 ) {
                        break;
                    }
                    if ( start.tagName.toLowerCase() == 'body' ) {
                        start = null;
                        break;
                    }
                }
                start = start.parentNode;
            }
            while ( 1 ) {
                if ( end.nodeType == 1 ) {
                    if ( utils.indexOf( tagName, end.tagName.toLowerCase() ) > -1 ) {
                        break;
                    }
                    if ( end.tagName.toLowerCase() == 'body' ) {
                        end = null;
                        break;
                    }
                }
                end = end.parentNode;
            }
            var bookmark = this.createBookmark(),
                    frag,
                    tmpRange;
            if ( start ) {
                tmpRange = this.cloneRange().setEndBefore( bookmark.start ).setStartBefore( start );
                frag = tmpRange.extractContents();
                tmpRange.insertNode( frag );
                domUtils.clearEmptySibling( start, true );
                start.parentNode.insertBefore( bookmark.start, start );
            }
            if ( end ) {
                tmpRange = this.cloneRange().setStartAfter( bookmark.end ).setEndAfter( end );
                frag = tmpRange.extractContents();
                tmpRange.insertNode( frag );
                domUtils.clearEmptySibling( end, false, true );
                end.parentNode.insertBefore( bookmark.end, end.nextSibling );
            }
            var current = domUtils.getNextDomNode( bookmark.start, false, function ( node ) {
                return node.nodeType == 1;
            } ), next;
            while ( current && current !== bookmark.end ) {
                next = domUtils.getNextDomNode( current, true, function ( node ) {
                    return node.nodeType == 1;
                } );
                if ( utils.indexOf( tagName, current.tagName.toLowerCase() ) > -1 ) {
                    domUtils.remove( current, true );
                }
                current = next;
            }
            return this.moveToBookmark( bookmark );
        },
        /**
         * 得到一个自闭合的节点
         * @public
         * @function
         * @name    baidu.editor.dom.Range.getClosedNode
         * @return  {Node}    闭合节点
         * @example
         * <img />,<br />
         */
        getClosedNode:function () {
            var node;
            if ( !this.collapsed ) {
                var range = this.cloneRange().adjustmentBoundary().shrinkBoundary();
                if ( range.startContainer.nodeType == 1 && range.startContainer === range.endContainer && range.endOffset - range.startOffset == 1 ) {
                    var child = range.startContainer.childNodes[range.startOffset];
                    if ( child && child.nodeType == 1 && (dtd.$empty[child.tagName] || dtd.$nonChild[child.tagName]) ) {
                        node = child;
                    }
                }
            }
            return node;
        },
        /**
         * 根据range选中元素
         * @public
         * @function
         * @name    baidu.editor.dom.Range.select
         * @param  {Boolean}    notInsertFillData        true为不加占位符
         */
        select:browser.ie ? function ( notInsertFillData, textRange ) {
            var nativeRange;
            if ( !this.collapsed )
                this.shrinkBoundary();
            var node = this.getClosedNode();
            if ( node && !textRange ) {
                try {
                    nativeRange = this.document.body.createControlRange();
                    nativeRange.addElement( node );
                    nativeRange.select();
                } catch ( e ) {}
                return this;
            }
            var bookmark = this.createBookmark(),
                    start = bookmark.start,
                    end;
            nativeRange = this.document.body.createTextRange();
            nativeRange.moveToElementText( start );
            nativeRange.moveStart( 'character', 1 );
            if ( !this.collapsed ) {
                var nativeRangeEnd = this.document.body.createTextRange();
                end = bookmark.end;
                nativeRangeEnd.moveToElementText( end );
                nativeRange.setEndPoint( 'EndToEnd', nativeRangeEnd );
            } else {
                if ( !notInsertFillData && this.startContainer.nodeType != 3 ) {
                    //使用<span>|x<span>固定住光标
                    var tmpText = this.document.createTextNode( fillChar ),
                            tmp = this.document.createElement( 'span' );
                    tmp.appendChild( this.document.createTextNode( fillChar ) );
                    start.parentNode.insertBefore( tmp, start );
                    start.parentNode.insertBefore( tmpText, start );
                    //当点b,i,u时，不能清除i上边的b
                    removeFillData( this.document, tmpText );
                    fillData = tmpText;
                    mergSibling( tmp, 'previousSibling' );
                    mergSibling( start, 'nextSibling' );
                    nativeRange.moveStart( 'character', -1 );
                    nativeRange.collapse( true );
                }
            }
            this.moveToBookmark( bookmark );
            tmp && domUtils.remove( tmp );
            //IE在隐藏状态下不支持range操作，catch一下
            try{
                nativeRange.select();
            }catch(e){}
            return this;
        } : function ( notInsertFillData ) {
            var win = domUtils.getWindow( this.document ),
                    sel = win.getSelection(),
                    txtNode;
            //FF下关闭自动长高时滚动条在关闭dialog时会跳
            browser.gecko && browser.version < 140000 ? this.document.body.focus() : win.focus();
            if ( sel ) {
                sel.removeAllRanges();
                // trace:870 chrome/safari后边是br对于闭合得range不能定位 所以去掉了判断
                // this.startContainer.nodeType != 3 &&! ((child = this.startContainer.childNodes[this.startOffset]) && child.nodeType == 1 && child.tagName == 'BR'
                if ( this.collapsed ) {
                    //opear如果没有节点接着，原生的不能够定位,不能在body的第一级插入空白节点
                    if ( notInsertFillData && browser.opera && !domUtils.isBody( this.startContainer ) && this.startContainer.nodeType == 1 ) {
                        var tmp = this.document.createTextNode( '' );
                        this.insertNode( tmp ).setStart( tmp, 0 ).collapse( true );
                    }
                    if ( !notInsertFillData ) {
                        txtNode = this.document.createTextNode( fillChar );
                        //跟着前边走
                        this.insertNode( txtNode );
                        removeFillData( this.document, txtNode );
                        mergSibling( txtNode, 'previousSibling' );
                        mergSibling( txtNode, 'nextSibling' );
                        fillData = txtNode;
                        this.setStart( txtNode, browser.webkit ? 1 : 0 ).collapse( true );
                    }
                }
                var nativeRange = this.document.createRange();
                nativeRange.setStart( this.startContainer, this.startOffset );
                nativeRange.setEnd( this.endContainer, this.endOffset );
                sel.addRange( nativeRange );
            }
            return this;
        },
        /**
         * 滚动到可视范围
         * @public
         * @function
         * @name    baidu.editor.dom.Range.scrollToView
         * @param    {Boolean}   win       操作的window对象，若为空，则使用当前的window对象
         * @param    {Number}   offset     滚动的偏移量
         * @return   {Range}    Range对象
         */
        scrollToView:function ( win, offset ) {
            win = win ? window : domUtils.getWindow( this.document );
            var span = this.document.createElement( 'span' );
            //trace:717
            span.innerHTML = '&nbsp;';
            var tmpRange = this.cloneRange();
            tmpRange.insertNode( span );
            domUtils.scrollToView( span, win, offset );
            domUtils.remove( span );
            return this;
        }
    };
})();