# coding:utf-8
"""
逻辑处理
"""

import sys
import os
import csv
from Ui_m import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,  QApplication,  QFileDialog,  \
    QMessageBox,  QTreeWidgetItem,  QComboBox
from func import read_docs,  get_temp_var
from handle import DocxHandle, MergeDocx
from PyQt5.QtGui import QIcon
import chardet


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.word_file = ''  # word 文件地址
        self.excel_file = ''  # excel 文件地址
        self.excel_data = ''  # excel数据
        self.rule = {}  # 规则 (模板 : 数据源)
        self.combo_box_item = []  # combo box‘s item, 即csv头部，数据源
        self.tree_widget_column_map={}  # 存储QtreeWidget列的映射关系  (模板 : 数据源对象)
        self.build_type_multiple = True  # 生成文档类型（多个/单个）：默认多个
        self.merge_docx_handle = None
        
        self.setWindowIcon(QIcon('combine.ico'))  # 设置图标
        
    def open_file(self):
        """ 打开文件 """
        fname = QFileDialog.getOpenFileName(self,"open file")
        return fname[0] if fname[0] else False
    
    def slot_open_word_file(self):
        """ 打开Word """
        file = self.open_file()
        if file:
            self.log(f'打开文件：{file}')
            suffix=os.path.splitext(file)[1]
            if suffix.lower() != '.docx':
                self.error("请选择以docx后缀的Word文件")
                return 

            self.word_file = file

            # 置label
            self.docNameLabel.setText(file)

            # 获取模板变量
            temp_var = get_temp_var(read_docs(file))
            self.log(f"模板变量:<b>{'</b>,<b>'.join(temp_var)}<b>")
            temp_var = sorted(temp_var)
            self.rule = {v:0 for v in temp_var}
            self.log(f"规则初始化:{self.rule}")
    
    def slot_open_excel_file(self):
        """ 读取excel数据 """
        file = self.open_file()
        if file:
            self.log(f'打开文件：{file}')
            suffix=os.path.splitext(file)[1]
            if suffix.lower() != '.csv':
                self.error("请选择以csv后缀的Excel文件")
                return
            
            self.excel_file = file
            
            # 置label
            self.excelNameLabel.setText(file)
            
            # 获取csv文件编码
            en_code = 'UTF-8'
            with open(self.excel_file, 'rb') as f:
                en_code = chardet.detect(f.read())['encoding']  # or readline if the file is large
                if en_code.upper()=='GB2312':
                    en_code = 'GBK'
            
            # 获取头部数据
            with open(self.excel_file, encoding=en_code) as f:
                
                # 解析csv文件
                data = list(csv.reader(f))
                
                # 内容和头部，头部赋值给combo下拉框
                self.excel_data = data[1:]
                self.combo_box_item = [ str(i) for i in data[0]]
    
    def slot_fill_data(self):
        """ 填充数据 """
        if not self.word_file:
            self.error('Word 文件无效')
            return False
        if not self.excel_file:
            self.error('Excel 文件无效')
            return False
        if not self.rule:
            self.error('Word 模板变量不存在')
            return False
        if not self.combo_box_item:
            self.error('Excel 头部数据不存在')
            return False
        
        self.log('清空规则数据')
        self.treeWidget.clear()
        
        self.log("数据填充：")
        for v in self.rule:
            cb = self.define_combo()
            self.add_qtree_item(v, cb)
            self.log(f"{v}: -")
            
            # 添加对应关系，(模板 : 数据源对象)
            self.tree_widget_column_map[v] = cb
            
        self.log("请选择模板对应数据...")
        return True
    
    def slot_test_rule(self):
        """ 测试规则 """
        self.log("测试一条数据并生成一个文件...")
        flag = self.slot_run(test=True)
        if flag:
            self.log("测试成功")
            self.runButton.setEnabled(True)
        else:
            self.log("测试失败")

    def slot_run(self, test=False):
        """ 运行 """
        
        i, count = 0, len(self.excel_data)
        for line_data in self.excel_data:
            i+=1
            self.log(f"{i}/{count}: {line_data}")
            docx_handle = DocxHandle(
                self.word_file, 
                line_data, 
                self.rule, 
                out = self.log, 
                err = self.error
            )
            
            if test:
                # 测试
                return docx_handle.test_rule_template()
            else:
                # 运行保存
                temp_doc_obj = docx_handle.run()
                if self.build_type_multiple:
                    # 多个文件
                    docx_handle.save(f"{line_data[0]}_{i}")
                else:
                    # 单文件
                    self.merge_docx_handle.append(temp_doc_obj)
            
        if self.merge_docx_handle:
            del self.merge_docx_handle
        self.log(f"恭喜，转换完成，共{i}份数据！")
                

    def add_qtree_item(self,  temp_value,  cb):
        """ 新增qtree的item，模板变量和下拉数据源 """
        self.log('新增item')
        child = QTreeWidgetItem(self.treeWidget)
        # 模板变量
        child.setText(0 , temp_value)
        # 数据源Combox
        self.treeWidget.setItemWidget(child, 1 , cb)
    
    def define_combo(self):
        """ 定义combo_box """
        cb = QComboBox()
        cb.addItems(self.combo_box_item)
        
        # 添加一个改变的信号 currentIndexChanged 和 activated
        cb.activated.connect(lambda : self.slot_change_item(cb))
        return cb
        
    def slot_change_item(self,  cb_obj):
        """ combo box 改变选项时触发 """
        if not cb_obj:
            return False
        # 选定的项目索引
        index = cb_obj.currentIndex()
        
        # 取cb_obj对象对应的模板变量
        temp_v = MainWindow.get_dict_key_by_value(self.tree_widget_column_map,  cb_obj)
        
        # 判断是否已有模板对应该索引，已有重置为0
        if index in self.rule.values():
            self.error("已存在模板对应值，已重置，请重新选择")
            cb_obj.setCurrentIndex(0)
            return False
        
        # 设置规则
        self.rule[temp_v] = index
        self.log(f"规则：<pre style='color:red'>{'<br>'.join([k+':&nbsp;&nbsp;&nbsp;&nbsp;'+self.combo_box_item[v] for k,v in self.rule.items()])}</pre>")
        
    def head_data(self):
        """ 头部数据运行解析 """
        text = self.headData.text()
        text = text.split('\t')
        self.log('头部数据运行')
        self.log(text)
        
        # 待生成item
        self.combo_box_item = text
    
    
    def error(self,  message):
        """ 错误提醒 """
        self.log(message)
        QMessageBox.warning(self,  "提醒",  message,  QMessageBox.Yes)
        

    def log(self,  string):
        """ 运行日志 """
        self.logBrowser.append(str(string))
    
    @staticmethod
    def get_dict_key_by_value(d, value):
        return list(d.keys())[list(d.values()).index(value)]
    
    def slot_build_type(self, multiple=True):
        """ 生成文档的类型，多个/单个 """
        self.log("改变生成文档的类型为：" + ("多个" if multiple else "单个") )
        self.build_type_multiple = multiple
        
        if not self.build_type_multiple:
            # 初始化docx合并对象
            self.merge_docx_handle = MergeDocx(log=self.log)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window_obj = MainWindow()
    main_window_obj.show()
    sys.exit(app.exec_())
