function addUploadItem(type,path,memberDown){
	 ue=parent.ue;
	 type=type.toLowerCase();
 	 switch(type){
 	  case 'gif':
 		ue.execCommand('insertHtml','<img src="'+path+'" alt=""/>');
 	  	break;
 	  case 'jpg':       
 		ue.execCommand('insertHtml','<img src="'+path+'" alt=""/>');
 	  	break;
 	  case 'png':
 		ue.execCommand('insertHtml','<img src="'+path+'" alt=""/>');
 	  	break;
 	  case 'bmp':
 		ue.execCommand('insertHtml','<img src="'+path+'" alt=""/>');
 	  	break;
 	  case 'jpeg':
 		ue.execCommand('insertHtml','<img src="'+path+'" alt=""/>');
 	  	break;
 	  case 'mp3':
 		ue.execCommand('insertHtml','<object classid="CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95"  id="MediaPlayer" width="450" height="70"><param name=""howStatusBar" value="-1"><param name="AutoStart" value="False"><param name="Filename" value="'+path+'"></object>');
 	  	break;
 	  case 'wma':
 		ue.execCommand('insertHtml','<object classid="CLSID:22d6f312-b0f6-11d0-94ab-0080c74c7e95"  id="MediaPlayer" width="450" height="70"><param name=""howStatusBar" value="-1"><param name="AutoStart" value="False"><param name="Filename" value="'+path+'"></object>');
 	  	break;
 	  case 'rm':
 		ue.execCommand('insertHtml','<object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" width="400" height="300"><param name="SRC" value="'+path+'" /><param name="CONTROLS" VALUE="ImageWindow" /><param name="CONSOLE" value="one" /><param name="AUTOSTART" value="true" /><embed src="'+path+'" nojava="true" controls="ImageWindow" console="one" width="400" height="300"></object><br/><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" width="400" height="32" /><param name="CONTROLS" value="StatusBar" /><param name="AUTOSTART" value="true" /><param name="CONSOLE" value="one" /><embed src="'+path+'" nojava="true" controls="StatusBar" console="one" width="400" height="24" /></object><br/><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" width="400" height="32" /><param name="CONTROLS" value="ControlPanel" /><param name="AUTOSTART" value="true" /><param name="CONSOLE" value="one" /><embed src="'+path+'" nojava="true" controls="ControlPanel" console="one" width="400" height="24" autostart="true" loop="false" /></object>');
 	  	break;
 	  case 'rmvb':
 		ue.execCommand('insertHtml','<object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" width="400" height="300"><param name="SRC" value="'+path+'" /><param name="CONTROLS" VALUE="ImageWindow" /><param name="CONSOLE" value="one" /><param name="AUTOSTART" value="true" /><embed src="'+path+'" nojava="true" controls="ImageWindow" console="one" width="400" height="300"></object><br/><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" width="400" height="32" /><param name="CONTROLS" value="StatusBar" /><param name="AUTOSTART" value="true" /><param name="CONSOLE" value="one" /><embed src="'+path+'" nojava="true" controls="StatusBar" console="one" width="400" height="24" /></object><br/><object classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" width="400" height="32" /><param name="CONTROLS" value="ControlPanel" /><param name="AUTOSTART" value="true" /><param name="CONSOLE" value="one" /><embed src="'+path+'" nojava="true" controls="ControlPanel" console="one" width="400" height="24" autostart="true" loop="false" /></object>');
 	  	break;
 	  case 'ra':
 		ue.execCommand('insertHtml','<object classid="clsid:CFCDAA03-8BE4-11CF-B84B-0020AFBBCCFA" id="RAOCX" width="450" height="60"><param name="_ExtentX" value="6694"><param name="_ExtentY" value="1588"><param name="AUTOSTART" value="true"><param name="SHUFFLE" value="0"><param name="PREFETCH" value="0"><param name="NOLABELS" value="0"><param name="SRC" value="'+path+'"><param name="CONTROLS" value="StatusBar,ControlPanel"><param name="LOOP" value="0"><param name="NUMLOOP" value="0"><param name="CENTER" value="0"><param name="MAINTAINASPECT" value="0"><param name="BACKGROUNDCOLOR" value="#000000"><embed src="'+path+'" width="450" autostart="true" height="60"></embed></object>');
 	  	break;
 	  case 'asf':
 		ue.execCommand('insertHtml','<object classid="clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95" codebase="http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=6,0,02,902" type="application/x-oleobject" standby="Loading..." width="400" height="300"><param name="FileName" VALUE="'+path+'" /><param name="ShowStatusBar" value="-1" /><param name="AutoStart" value="true" /><embed type="application/x-mplayer2" pluginspage="http://www.microsoft.com/Windows/MediaPlayer/" src="'+path+'" autostart="true" width="400" height="300" /></object>');
 	  	break;
 	  case 'avi':
 		ue.execCommand('insertHtml','<object classid="clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95" codebase="http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=6,0,02,902" type="application/x-oleobject" standby="Loading..." width="400" height="300"><param name="FileName" VALUE="'+path+'" /><param name="ShowStatusBar" value="-1" /><param name="AutoStart" value="true" /><embed type="application/x-mplayer2" pluginspage="http://www.microsoft.com/Windows/MediaPlayer/" src="'+path+'" autostart="true" width="400" height="300" /></object>');
 	  	break;
 	  case 'wmv':
 		ue.execCommand('insertHtml','<object classid="clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95" codebase="http://activex.microsoft.com/activex/controls/mplayer/en/nsmp2inf.cab#Version=6,0,02,902" type="application/x-oleobject" standby="Loading..." width="400" height="300"><param name="FileName" VALUE="'+path+'" /><param name="ShowStatusBar" value="-1" /><param name="AutoStart" value="true" /><embed type="application/x-mplayer2" pluginspage="http://www.microsoft.com/Windows/MediaPlayer/" src="'+path+'" autostart="true" width="400" height="300" /></object>');
 	  	break;
 	  case 'swf':
 		ue.execCommand('insertHtml','<object codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=7,0,0,0" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="400" height="300"><param name="movie" value="'+path+'" /><param name="quality" value="high" /><param name="AllowScriptAccess" value="never" /><embed src="'+path+'" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="400" height="300" /></object>');
 	  	break;
 	  default :        
 		ue.execCommand('insertHtml','<a href="'+path+'"><img border="0" src="/static/images/download.gif" alt="" style="margin:0px 2px -4px 0px"/>点击下载此文件</a>');
        break;
     }
}