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
pygubu
```
如果您看到这个README时我的fork还是没能合入主线，那么请参照[wiki](https://github.com/loonghao/photoshop-python-api/wiki)进行源码安装：
```bash
git clone https://github.com/TsXor/photoshop-python-api/tree/action_manager_module_integration
cd photoshop-python-api
python setup.py install
```

#### 缺陷
- 只能识别白底黑字的竖排文字  
  不打算自动识别别的类型，但是会允许手动标记黑底白字和横排文字  
- 实战中这个的速度还不是太快  
  但是本人奉行一个观点：比人快就够了  

#### 使用方法：
命令行：  
用`--help`参数执行procedure.py和utils.py查看帮助  
- procedure.py  
	- step1：处理图片并输出excel表格对接翻译  
	- step2：读取excel表格并创建psd  
- utils.py  
	- whiteborder：帮助你给文字加白边  

GUI：  
感谢pygubu给我们提供了方便的GUI设计器！  
双击procedure_gui.pyw启动GUI。  

#### Maybe FAQ
- 表格中出现不是文字的图片怎么办？  
  空着。处理时会自动忽略  

- 表格中一段文字的一部分再次出现了怎么办？  
  小的部分空着。处理时会自动忽略  

- 表格中的文字不全怎么办？  
  请参照图片。表格中的文字是一个“指示器”，用于告诉负责翻译的人“你输入的文字将会被放到这里”。  
  注：这个“图片表格”本身就是为了解决一个“耦合问题”：  
  - 嵌字：能否给我在ps里标明一下每段翻译对应的是哪个字？  
  - 翻译：但是我不会ps啊！  
  - 嵌字：但是我也不会外语啊？  
  
  此时翻译和嵌字这两个本应相互独立的职位耦合了。  

- 跑到一半弹窗报错了！  
  截图发issue  
  很急的话可以试试用mem reduct清理内存后重跑失败的图片  
- 我的CPU占用满了！（我电脑风扇猛转！）  
  正常，用cpu跑easyocr就是会占满。  
  或者您配置一下用gpu跑easyocr就行了。但是配置挺麻烦的。  
  或者可以找某位大佬将ocr部分改成某种网络ocr的api也行。只要能返回文字位置框的ocr都可以。  

- 为啥不试试强大的paddleOCR？  
  试过了，可惜paddleOCR对日语基本识别不出啥。如果您想文化输出的话可以试试（迫真）。  