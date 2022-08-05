### 嵌字助手
我为了简化嵌字过程做的一些...工具脚本  
依赖：[ActionManager.py](https://github.com/TsXor/photoshop-ActionManager-python/blob/main/ActionManager.py) 放在同一目录  
使用方法：
1.  文字大小识别工具  
  命令行执行：`exec.bat <目标psd文件>`  
  输入：一张已经抹掉字的黑白图片，psd格式，最下面是原图的图层，然后是一个涂抹的图层  
  只能识别白底黑字的竖排文字，而且准头不佳，也会被那种注解小字干扰。  
  纯opencv+numpy实现。  
  未来会提升...吧？也许？？？  
2.  文字加白边工具  
  命令行执行它或者双击`text_white_border.py`。  
  然后它会不断问你要加多少个像素的白边，每次你回答后，它就会将你当前选中的文字图层加上白边。  
  没啥好说的，就是快，而且相对于动作来说可以指定像素数。  
