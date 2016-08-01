UEDITOR_CONFIG = window.UEDITOR_CONFIG || {};

var baidu = window.baidu || {};

window.baidu = baidu;

window.UE = baidu.editor =  {};

UE.plugins = {};

UE.commands = {};

UE.instants = {};

UE.I18N = {};

//UE.defaultplugins = {};
//
//UE.commands = function(){
//    var commandList = {},tmpList= {};
//    return {
//
//        register : function(commandsName,pluginName){
//            commandsName = commandsName.split(',');
//            for(var i= 0,ci;ci=commandsName[i++];){
//                commandList[ci] = pluginName;
//            }
//
//        },
//        get : function(commandName){
//            return commandList[commandName];
//        },
//        getList : function(){
//            return commandList;
//        }
//    }
//}();

UE.version = "1.2.3.0";

var dom = UE.dom = {};