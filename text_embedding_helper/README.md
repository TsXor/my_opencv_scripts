### 嵌字助手
我为了简化嵌字过程做的工具脚本  

#### 依赖
```
photoshop-python-api（我的fork）
openpyxl
click
easyocr
opencv-python
numpy
```
如果您看到这个README时我的fork还是没能合入主线，那么请参照[wiki](https://github.com/loonghao/photoshop-python-api/wiki)进行源码安装：
```bash
git clone https://github.com/TsXor/photoshop-python-api/tree/action_manager_module_integration
cd photoshop-python-api
python setup.py install
```

#### 缺陷
只能识别白底黑字的竖排文字  
不打算自动识别别的类型，但是会允许手动标记黑底白字和竖排文字  

#### 使用方法：
暂时只有命令行  
用`--help`参数执行procedure.py和utils.py查看帮助  
- procedure.py  
	- step1：处理图片并输出excel表格对接翻译  
	- step2：读取excel表格并创建psd  
- utils.py  
	- whiteborder：帮助你给文字加白边  