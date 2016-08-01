///import core
///commands 模板
///commandsName  template
///commandsTitle  模板
///commandsDialog  dialogs\template\template.html
(function() {
    UE.plugins['template'] = function(){
        var me = this;
        UE.commands['template'] = {
            execCommand : function(cmd,obj) {
                obj.html&&me.execCommand("inserthtml",obj.html);
            },
            queryCommandState : function(){
                return this.highlight ? -1 : 0;
            }
        };
        me.addListener("click",function(type,evt){
            var el = evt.target || evt.srcElement,
                range = me.selection.getRange();
            var tnode = domUtils.findParent(el,function(node){
                if(node.className && domUtils.hasClass(node,"ue_t")){
                    return node;
                }
            },true);
            tnode&&range.selectNode(tnode).shrinkBoundary().select();
        });
        me.addListener("keydown",function(type, evt){
            var range = me.selection.getRange();
            if(!range.collapsed){
                if(!evt.ctrlKey && !evt.metaKey && !evt.shiftKey && !evt.altKey){
                    var tnode = domUtils.findParent(range.startContainer,function(node){
                        if(node.className && domUtils.hasClass(node,"ue_t")){
                            return node;
                        }
                    },true);
                    if(tnode){
                        domUtils.removeClasses(tnode,["ue_t"]);
                    }
                }
            }
        });
    };
})();
