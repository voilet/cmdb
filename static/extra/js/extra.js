function my_ajax_replace(url,id){
    $('#loading-img').show();
    $.ajax({
      url: url,
      cache: false,
      success: function(html){
        var box = $( '#' + id );
        if( box.length && /input/i.test( box[0].nodeName ) ){
            box.val( html );
        }else{
            box.html( html );
        }
      $('#loading-img').hide();
      }
    });
}

function ajaxCommand(url,option,id){
        var _interVal, commonAjaxXhr,urlRex = /where=(\d+)/ , ajaxWhere = 0, count = 0,
            commonAjax = function(config){//发起ajax请求
                config = $.extend({
                    type:'post',
                    dataType:'json'
                },config);
                commonAjaxXhr = $.ajax(config);
            },
            _exportCommand = function(url){
            var resultBox = document.getElementById('result');
            if ( 'number' !== typeof ajaxWhere ) return; 
                url = url.replace( urlRex,'where=' + ajaxWhere );
                commonAjax({
                    url: url,
                    type:'get',
                    success: function(data){
                        ajaxWhere = data.where;
                        if ( data.result.length ){
                            count = 0;
                            var commandHtml = data.result.join('');
                            document.getElementById(id).innerHTML += commandHtml ;
                            _exportCommand(url);
                        }else{
                            count++;
                            if(count >= 15) return;
                            setTimeout(function(){ _exportCommand(url) }, 1000);
                        }
                        resultBox.scrollTop = resultBox.scrollHeight;
                    }
                });
            };
            commonAjax({
                url: url+'&option='+option,
                type:'get',
                dataType: 'text',
                success: function(data){
                    _exportCommand(data);
                }
            })
    }
