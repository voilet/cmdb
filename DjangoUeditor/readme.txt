Ueditor HTML编辑器是百度开源的HTML编辑器，

本模块帮助在Django应用中集成百度Ueditor HTML编辑器。
安装包中已经集成Ueditor v1.3.6

使用Django-Ueditor非常简单，方法如下：

1、安装方法
	
	**方法一：下载安装包，在命令行运行：
		python setup.py install
	**方法二：使用pip工具在命令行运行(推荐)：
   		pip install DjangoUeditor

2、在INSTALL_APPS里面增加DjangoUeditor app，如下：
     
		INSTALLED_APPS = (
			#........
    		'DjangoUeditor',
		)


3、在urls.py中增加：

	url(r'^ueditor/',include('DjangoUeditor.urls' )),

4、在models中这样定义：
	
	from DjangoUeditor.models import UEditorField
	class Blog(models.Model):
    	Name=models.CharField(,max_length=100,blank=True)
    	Content=UEditorField('内容	',height=100,width=500,default='test',imagePath="uploadimg/",imageManagerPath="imglib",toolbars='mini',options={"elementPathEnabled":True},filePath='upload',blank=True)

	说明：
	UEditorField继承自models.TextField,因此你可以直接将model里面定义的models.TextField直接改成UEditorField即可。
	UEditorField提供了额外的参数：
        toolbars:配置你想显示的工具栏，取值为mini,normal,full,besttome, 代表小，一般，全部,涂伟忠贡献的一种样式。如果默认的工具栏不符合您的要求，您可以在settings里面配置自己的显示按钮。参见后面介绍。
        imagePath:图片上传的路径,如"images/",实现上传到"{{MEDIA_ROOT}}/images"文件夹
        filePath:附件上传的路径,如"files/",实现上传到"{{MEDIA_ROOT}}/files"文件夹
        scrawlPath:涂鸦文件上传的路径,如"scrawls/",实现上传到"{{MEDIA_ROOT}}/scrawls"文件夹,如果不指定则默认=imagepath
        imageManagerPath:图片管理器显示的路径，如"imglib/",实现上传到"{{MEDIA_ROOT}}/imglib",如果不指定则默认=imagepath。
        options：其他UEditor参数，字典类型。参见Ueditor的文档ueditor_config.js里面的说明。
        css:编辑器textarea的CSS样式
        width，height:编辑器的宽度和高度，以像素为单位。

5、在表单中使用非常简单，与常规的form字段没什么差别，如下：
	
	class TestUeditorModelForm(forms.ModelForm):
    	class Meta:
        	model=Blog
	***********************************
	如果不是用ModelForm，可以有两种方法使用：

	1: 使用forms.UEditorField

	from  DjangoUeditor.forms import UEditorField
	class TestUEditorForm(forms.Form):
	    Description=UEditorField("描述",initial="abc",width=600,height=800)
	
	2: widgets.UEditorWidget

	from  DjangoUeditor.widgets import UEditorWidget
	class TestUEditorForm(forms.Form):
		Content=forms.CharField(label="内容",widget=UEditorWidget(width=800,height=500, imagePath='aa', filePath='bb',toolbars={}))
	
	widgets.UEditorWidget和forms.UEditorField的输入参数与上述models.UEditorField一样。

6、Settings配置
     
      在Django的Settings可以配置以下参数：
            UEDITOR_SETTINGS={
                "toolbars":{           #定义多个工具栏显示的按钮，允行定义多个
                    "name1":[[ 'source', '|','bold', 'italic', 'underline']],
                    "name2",[]
                },
                "images_upload":{
                    "allow_type":"jpg,png",    #定义允许的上传的图片类型
                    "max_size":"2222kb"        #定义允许上传的图片大小，0代表不限制
                },
                "files_upload":{
                     "allow_type":"zip,rar",   #定义允许的上传的文件类型
                     "max_size":"2222kb"       #定义允许上传的文件大小，0代表不限制
                 },,
                "image_manager":{
                     "location":""         #图片管理器的位置,如果没有指定，默认跟图片路径上传一样
                },
            }
7、在模板里面：

    <head>
        ......
        {{ form.media }}        #这一句会将所需要的CSS和JS加进来。
        ......
    </head>
    注：运行collectstatic命令，将所依赖的css,js之类的文件复制到{{STATIC_ROOT}}文件夹里面。

8、高级运用：

     ****************
     动态指定imagePath、filePath、scrawlPath、imageManagerPath
     ****************
     这几个路径文件用于保存上传的图片或附件，您可以直接指定路径，如：
          UEditorField('内容',imagePath="uploadimg/")
     则图片会被上传到"{{MEDIA_ROOT}}/uploadimg"文件夹，也可以指定为一个函数，如：

      def getImagePath(model_instance=None):
          return "abc/"
      UEditorField('内容',imagePath=getImagePath)
      则图片会被上传到"{{MEDIA_ROOT}}/abc"文件夹。
     ****************
     使上传路径(imagePath、filePath、scrawlPath、imageManagerPath)与Model实例字段值相关
     ****************
        在有些情况下，我们可能想让上传的文件路径是由当前Model实例字值组名而成，比如：
        class Blog(Models.Model):
            Name=models.CharField('姓名',max_length=100,blank=True)
            Description=UEditorField('描述',blank=True,imagePath=getUploadPath,toolbars="full")

     id  |   Name    |       Description
     ------------------------------------
     1   |   Tom     |       ...........
     2   |   Jack    |       ...........

      我们想让第一条记录上传的图片或附件上传到"{{MEDIA_ROOT}}/Tom"文件夹,第2条记录则上传到"{{MEDIA_ROOT}}/Jack"文件夹。
      该怎么做呢，很简单。
      def getUploadPath(model_instance=None):
          return "%s/" % model_instance.Name
      在Model里面这样定义：
      Description=UEditorField('描述',blank=True,imagePath=getUploadPath,toolbars="full")
      这上面model_instance就是当前model的实例对象。
      还需要这样定义表单对象：
      from  DjangoUeditor.forms import UEditorModelForm
      class UEditorTestModelForm(UEditorModelForm):
            class Meta:
                model=Blog
      特别注意：
         **表单对象必须是继承自UEditorModelForm，否则您会发现model_instance总会是None。
         **同时在Admin管理界面中，此特性无效，model_instance总会是None。
         **在新建表单中，model_instance由于还没有保存到数据库，所以如果访问model_instance.pk可能是空的。因为您需要在getUploadPath处理这种情况


class UEditorTestModelForm(UEditorModelForm):
    class Meta:
        model=Blog




8、其他事项：

    **本程序版本号采用a.b.ccc,其中a.b是本程序的号，ccc是ueditor的版本号，如1.2.122，1.2是DjangoUeditor的版本号，122指Ueditor 1.2.2.
    **本程序安装包里面已经包括了Ueditor，不需要再额外安装。
    **目前暂时不支持ueditor的插件
    **别忘记了运行collectstatic命令，该命令可以将ueditor的所有文件复制到{{STATIC_ROOT}}文件夹里面
    **Django默认开启了CSRF中间件，因此如果你的表单没有加入{% csrf_token %}，那么当您上传文件和图片时会失败
   