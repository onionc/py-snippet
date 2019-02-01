### 1. 实战Word批量

需要处理批量替换word的一些数据，数据源从Excel中来。

Excel的百分数会变为数字，以及浮点数会多好多精度，为了原汁原味的数据，直接复制数据到文本文件。通过\t来分隔即可，最后一个值多\n得注意。

然后在Word中加变量用`{XXXX}`格式的得转一下`{}`，时间关系，用了 `TEMP_XXX`之类的，`str.replace()`去替换模板数据即可。*女朋友发现Word有邮件合并功能，类似模板替换。*

### 2. 进阶-GUI工具

#### 2.1 预备，查漏补缺

#####1）界面

看《PyQt快速开发与实战》学习Qt designer生成ui、通过eric6或者命令编译py文件、信号槽机制、简单的[如何让界面和逻辑分离](https://www.cnblogs.com/tkinter/p/5632284.html)，以及以前的PyQt入门，打算直接上手做。

界面逻辑分离可以通过两种方式：（注 `Ui_m`为界面生成的py代码文件）

```python
# coding:utf-8
from PyQt5.QtWidgets import QMainWindow,  QApplication
from Ui_m import Ui_MainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def open_file(self):
        print('open file...')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window_obj = MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window_obj)
    main_window_obj.show()
    sys.exit(app.exec_())
```

```python
# coding:utf-8
from PyQt5.QtWidgets import QMainWindow,  QApplication
from Ui_m import Ui_MainWindow
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def open_file(self):
        print('open file...')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window_obj = MainWindow()
    main_window_obj.show()
    sys.exit(app.exec_())
```

##### 2） Excel数据处理

用常规的`sheet.cell_value(i, j)`获取数据，会有一些意外的情况，比如有些数字之后会多.0，百分比会是小数，小数多精度，太大的数字为科学计数法，日期也为浮点数，总之就是所得非所见。要所见即所得的话，直接复制，存取文本文件吧，每一列默认通过\t区分。



##### 3） 数据读取

基本的Excel和Word数据读取：

```python
import xlrd
import docx

def read_xls():
    """ 读取excel """
    workbook = xlrd.open_workbook(r'02.xls')
    sheet = workbook.sheet_by_index(0)

    cols = sheet.ncols
    rows = sheet.nrows
    
    data = []
    for i in range(rows):
        
        if i==0:
            continue
        row_content = []
        for j in range(1, cols):
            # print(sheet.cell_value(i, j), sheet.cell(i, j).ctype)
            row_content.append(str(sheet.cell_value(i, j)))

        data.append(row_content)
    return data


def read_docs():
    """ 读取word数据 """
    doc=docx.Document(r'./01.docx')
    text = []
    for i in doc.paragraphs:
        text.append(i.text)
    data = '\n'.join(text)
    return data

if __name__ == '__main__':
    e_data = read_xls()
    w_data = read_docs()
```

#### 2.2 主要流程

- 打开word模板（需要手动输入所有的模板变量）
- 检测所有的模板变量
- 添加一行数据
- 定义路由规则
- 测试数据
- 执行多行

#### 2.3 画界面

![word_ui.png](http://image.acfuu.com/mdImages/201901/word_ui.png)

本来打算模板变量select选择后，radio选择相应的数据源，发现一篇[Qt程序学习（三）------QTreeWidget、右键菜单、动态改变comboBox、QTreeWidgetItem的对应列的文字编辑](https://blog.csdn.net/qq_19528953/article/details/52270129)，结合`QTreeWidget`、`Combo Box` 可以实现想要的一一对应功能。学习一番QTreeWidget和Combo Box基本操作（在逻辑小节）。

 ![word_ui_2.png](http://image.acfuu.com/mdImages/201901/word_ui_2.png)



#### 2.4 写逻辑

叮！项目压测时候，发现excel的csv文件，文本文件打开是用`,`逗号分隔的。可以直接处理excel了（虽然有局限，如果数据中有逗号就得更改系统配置，显然不现实）。

所以流程变为：

- 读取docx文件和csv两个文件之后（word文件上面有，csv可以直接`csv.reader()`读取）
- 添加规则（一个模板变量对应一个下拉框）
- 生成数据

就可以了，第一条上面查漏补缺有，第三条刚开始的脚本逻辑处理都写过了，所以重点放在添加规则，首先需要熟悉一下`QTreeWidget` 和 `Combo Box`。

##### 1） QTreeWidget 操作

实例化

```python
self.treeWidget = QtWidgets.QTreeWidget(self.gridLayoutWidget)
self.treeWidget.setObjectName("treeWidget")
self.gridLayout.addWidget(self.treeWidget, 3, 4, 1, 1)
```

添加头部（模板变量列和数据源列）

```python
self.treeWidget.headerItem().setText(0, _translate("MainWindow", "模板变量"))
self.treeWidget.headerItem().setText(1, _translate("MainWindow", "数据源"))
```

增加一项数据：（上面的实例化和头部可以用UI生成，item数据需要动态在代码添加）

```
child = QTreeWidgetItem(self.treeWidget)
child.setText(0, 'TEMP_COMPUTER')
child.setText(1, 'PDP-01')
```

![QTree_temp_data.png](http://image.acfuu.com/mdImages/201901/QTree_temp_data.png)

ok，还带有滚动条，这样到实际用的时候，左侧模板变量数据可以通过Word文件获取，数据源通过Excel头部数据（实际上为文本）指定，通过类似select的`Combo box`下拉框控件。

##### 2）Combo box 操作

常规操作

```
# 实例化QComBox对象
self.cb=QComboBox()
# 单个添加条目
self.cb.addItem('C')
self.cb.addItem('C++')
self.cb.addItem('Python')
# 多个添加条目
self.cb.addItems(['Java','C#','PHP'])
```

将上面的添加QTreeWidget添加项目结合起来：左侧为模板变量，右侧为`Combo  box`数据

```python
def add_qtree_item(self,  item_data):
    """ 新增item """
    child = QTreeWidgetItem(self.treeWidget)
    # 模板变量
    child.setText(0 , 'TEMP_COMPUTER')
    # 数据源Combox
    cb = QComboBox()
    cb.addItem('PDP-8')
    cb.addItem('PDP-11')
    self.treeWidget.setItemWidget(child, 1 , cb)
```

效果如下

![QTree_and_ComboBox.png](http://image.acfuu.com/mdImages/201901/QTree_and_ComboBox.png)

##### 3）结合正式数据来绑定规则

![rule1.png](http://image.acfuu.com/mdImages/201901/rule1.png)

图中读取后缀为.docx的Word文件来获取模板变量，读取后缀为.csv的Excel文件来获取头部当做数据源。

因时间关系，不打算将已选择的项加标记，只获取已选择的，再次选择时，提醒即可。但是现在这种绑定
```python
def define_combo(self):
    """ 定义combo_box """
    cb = QComboBox()
    cb.addItems(self.combo_box_item)
	
    # 存储所有的 combo box 实例
    self.all_cb.append(cb)
    # 添加一个改变的信号
    cb.currentIndexChanged.connect(MainWindow.slot_change_item)
    return cb

@staticmethod
def slot_change_item(index):
    print(index)
```
选定之后，也只会收到一个被选定的项目索引的信号（整数，比如：3）。看不出来是哪个`Combo box`实例发的信号。发现可以用lambda添加参数，直接将`cb`实例传过去：

```python
    # 添加一个改变的信号
    cb.currentIndexChanged.connect(lambda : self.slot_change_item(cb))
    return cb

def slot_change_item(self,  cb_obj):
    print(cb_obj)
    print(cb_obj.currentIndex())
    for i in self.all_cb:
        print(i)
```
输出：（第一行是激活的`cb`实例，第二行是点击的item索引，三四行为之前存储的所有`cb`实例，发现第三行和第一行是一个实例）

```
<PyQt5.QtWidgets.QComboBox object at 0x04B23DA0>
3
<PyQt5.QtWidgets.QComboBox object at 0x04B23DA0>
<PyQt5.QtWidgets.QComboBox object at 0x04B23E90>
```

至于模板变量列和数据源列的对应关系就不劳烦QTreeWidget了，自己直接处理了。

经过一番调整，终于初具雏形了

![temp_doc.png](http://image.acfuu.com/mdImages/201901/temp_doc.gif)

已存在模板的时候提醒了两次，因为是这么写的

```python
# 判断是否已有模板对应该索引，已有重置为0
if index in self.rule.values():
    self.error("已存在模板对应值，已重置，请重新选择")
    cb_obj.setCurrentIndex(0)
    return False
```

第一个为1，当前为(1,0), 修改第二个为1时，检测到 1 in (1,0), 然后置0，因0 in (1,0)再次触发，所以两次提醒：打日志`self.log(f"{index} in {self.rule.values()}")` 输出：

```
已存在模板对应值，已重置，请重新选择
1 in dict_values([1, 0])
已存在模板对应值，已重置，请重新选择
0 in dict_values([1, 0])
```

解决办法是：

```python
# 添加一个改变的信号 currentIndexChanged 和 activated

# cb.currentIndexChanged.connect(lambda : self.slot_change_item(cb))
cb.activated.connect(lambda : self.slot_change_item(cb))
```

在发送信号的时候采用`activated`而不是 ` currentIndexChanged`就好了，因为`currentIndexChanged`是**每当组合框中的当前索引通过用户交互或以编程方式更改时, 都会发送此信号**。

> user interaction or programmatically

`activated` 仅仅是**当用户在组合框中选择项目时, 将发送此信号**。



接下来就需要接入之前的处理逻辑

##### 4）接入处理Word文件逻辑

移植过来就可以了

```python
# coding:utf-8
""" word替换处理 """

from docx import Document
import os

class DocxHandle(object):

    def __init__(self, doc_file,  data,  rule, out=print):
        """ DocxHandle.
            Args: 
                doc_file: template doc file.
                data: 数据
                rule: 规则
                out: 输出重定向
        """
        self.document = Document(doc_file)  # 打开文件docx文件
        self.rule = rule
        self.data = data
        self.log = out
    
    def save(self, title):
        # 新建目录
        img_dir = './docxdata/'
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
        
        self.document.save(f"{img_dir}{title}.docx")  # 保存文档
        self.log(f"存储文件：{img_dir}{title}.docx")

    def test_rule_template(self):
        for x,y in self.rule.items():
            value = self.data[y]
            self.log(f"{x},[{value}]")

    def docx(self):
        data = self.data

        for x,y in self.rule.items():
            value = data[y]
            self.log(f"{x},[{value}]")
            self.replace_text(x, value, self.document)

    def replace_text(self, old_text, new_text, file):
        """# 传入三个参数, 旧字符串, 新字符串, 文件对象"""
        # 遍历文件对象
        for f in file.paragraphs:
            # 如果 旧字符串 在 某个段落 中
            if old_text in f.text:
                # self.log(f"替换前===>{f.text}")
                # 遍历 段落 生成 i
                for i in f.runs:
                    # 如果 旧字符串 在 i 中
                    if old_text in i.text:
                        # 替换 i.text 内文本资源
                        i.text = i.text.replace(old_text, new_text)
                # self.log(f"替换后===>{f.text}")
```
#### 2.5 最终结果

注意，遇到一个模板变量被拆分，看不出来。但是在Word分段解析的时候，会拆分开数据，导致不能替换。

![bug_word_text.png](http://image.acfuu.com/mdImages/201901/bug_word_text.png)

所以如果有未检测出来的模板变量，则报错。

最终效果：![combine_doc.gif](http://image.acfuu.com/mdImages/201901/combine_doc.gif)

在打包之前多加了一个生成文档模式功能：参考邮件合并。（合并文档当模板有非默认字体时，得注意样式问题）

![combine_doc_info.png](http://image.acfuu.com/mdImages/201901/combine_doc_info.png)

最后，需要打包exe文件：`pyinstaller`不支持3.7，需要下载  [pyinstaller](https://github.com/pyinstaller)。有奇怪报错，最后采用`cx_Freeze`来打包:

只需要编写文件`install.py`

```python
from cx_Freeze import setup, Executable
 
setup(  name = "Combine_docx",
        version = "1.0",
        description = "类似Word邮件合并功能",
        executables = [Executable("./mainwindow.py")])

```

运行`python install.py build`则打包成功。



#### 3. 其他错误

##### 1）打包之后导入csv文件会报错

```
Traceback (most recent call last):
  File "./mainwindow.py", line 78, in slot_open_excel_file
  File "D:\Software\python3\lib\codecs.py", line 322, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
```

先获取到文件编码，再次使用编码打开csv文件

```
# 获取文件编码
en_code = 'utf-8'
with open(self.excel_file, 'rb') as f:
	en_code = chardet.detect(f.read())['encoding']
            
with open(self.excel_file, encoding=en_code) as f:
	# 解析csv文件
	data = list(csv.reader(f))
```

##### 2）设置程序图标

设置程序图标有多种方式，感觉用不到Designer建qrc资源文件，直接用

```
self.setWindowIcon(QIcon('combine.ico'))  # 设置图标
```

用python直接运行程序是可以有的，生成exe运行就无图标了。

cx_freeze 加参数`icon`只会在缩略图中有，程序左上角还是没有，够用了。



终于完整的完成了一个小GUI工具 :) 虽然实际用起来一般般，特别是数据多的时候，模板变量得从前往后打，以避免在docx角度看到的模板变量是拆分的，但这只是一个开始。

**参考**

- [安装python-docx](https://blog.csdn.net/huijiaaa1/article/details/80616842)

- [xlrd](https://www.cnblogs.com/linyfeng/p/7123423.html)

- [excel读取小数](https://www.cnblogs.com/wanglei-xiaoshitou1/p/9401261.html)

- [<自动化办公> Python 操控 Word](https://www.jianshu.com/p/4af54a9b3576)

- [pip使用本地缓存文件来安装包](https://blog.csdn.net/davidsu33/article/details/52980231)

- [Word邮件合并](http://www.wordlm.com/html/6515.html) [Word邮件合并2](http://www.wordlm.com/html/6616.html)

- [QTreeWidget、右键菜单、动态改变comboBox、QTreeWidgetItem的对应列的文字编辑](https://blog.csdn.net/qq_19528953/article/details/52270129)

- [PyQt--QTreeWidget](https://www.cnblogs.com/fuqia/p/9023836.html) 

- [PyQt5基本控件详解之QComboBox(九)](https://blog.csdn.net/jia666666/article/details/81534260)

- [PyQt: How to connect QComboBox to function with Arguments](https://stackoverflow.com/questions/23116763/pyqt-how-to-connect-qcombobox-to-function-with-arguments)

- [PyQt5学习笔记16----PyQt信号和槽传递额外参数](https://blog.csdn.net/a359680405/article/details/45246605)

- [[python，字典中如何根据value值取对应的key值](https://segmentfault.com/q/1010000008277059)](https://segmentfault.com/q/1010000008277059?_ea=1601652)

- [【记录】用PyInstaller把Python代码打包成单个独立的exe可执行文件](https://www.crifan.com/use_pyinstaller_to_package_python_to_single_executable_exe/)

- cx_Freeze打包 
  - [【记录】用cx_Freeze把Python代码打包成单个独立的exe可执行文件](https://www.crifan.com/use_cx_freeze_to_package_python_to_single_executable_exe/)
  - [PyQt5环境搭建及cx_freeze打包exe](https://www.cnblogs.com/asis/p/pyqt5-cx_freeze.html)
  - [利用cx_freeze打包python程序](https://www.jianshu.com/p/e47d9be6fa96)

- 解码csv [UnicodeDecodeError: ('utf-8' codec) while reading a csv file duplicate](https://stackoverflow.com/questions/33819557/unicodedecodeerror-utf-8-codec-while-reading-a-csv-file)

  