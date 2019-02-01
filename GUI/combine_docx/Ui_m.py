# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\py\testPyQt5\hello-world\m.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(904, 437)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 431, 411))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.docNameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.docNameLabel.setObjectName("docNameLabel")
        self.gridLayout.addWidget(self.docNameLabel, 1, 4, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 1, 6, 1, 1)
        self.toolButton_3 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout.addWidget(self.toolButton_3, 2, 6, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1, QtCore.Qt.AlignRight)
        self.excelNameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.excelNameLabel.setObjectName("excelNameLabel")
        self.gridLayout.addWidget(self.excelNameLabel, 2, 4, 1, 1)
        self.treeWidget = QtWidgets.QTreeWidget(self.gridLayoutWidget)
        self.treeWidget.setMaximumSize(QtCore.QSize(400, 300))
        self.treeWidget.setObjectName("treeWidget")
        self.gridLayout.addWidget(self.treeWidget, 3, 4, 1, 1)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setMaximumSize(QtCore.QSize(37, 16777215))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_9.addWidget(self.pushButton_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMaximumSize(QtCore.QSize(37, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_9.addWidget(self.pushButton_2)
        self.runButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.runButton.setEnabled(False)
        self.runButton.setMaximumSize(QtCore.QSize(37, 16777215))
        self.runButton.setObjectName("runButton")
        self.verticalLayout_9.addWidget(self.runButton)
        self.gridLayout.addLayout(self.verticalLayout_9, 3, 6, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1, QtCore.Qt.AlignRight)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 1, 1, 1, QtCore.Qt.AlignRight)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButtonMultiple = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButtonMultiple.setChecked(True)
        self.radioButtonMultiple.setObjectName("radioButtonMultiple")
        self.horizontalLayout.addWidget(self.radioButtonMultiple)
        self.radioButtonSingle = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.radioButtonSingle.setObjectName("radioButtonSingle")
        self.horizontalLayout.addWidget(self.radioButtonSingle)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 4, 1)
        spacerItem1 = QtWidgets.QSpacerItem(13, 86, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 3, 4, 1)
        spacerItem2 = QtWidgets.QSpacerItem(13, 86, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 5, 4, 1)
        self.logBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.logBrowser.setGeometry(QtCore.QRect(460, 20, 431, 401))
        self.logBrowser.setObjectName("logBrowser")
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setGeometry(QtCore.QRect(440, 20, 20, 401))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.toolButton.clicked.connect(MainWindow.slot_open_word_file)
        self.pushButton_2.clicked.connect(MainWindow.slot_test_rule)
        self.runButton.clicked.connect(MainWindow.slot_run)
        self.toolButton_3.clicked.connect(MainWindow.slot_open_excel_file)
        self.pushButton_4.clicked.connect(MainWindow.slot_fill_data)
        self.radioButtonMultiple.toggled['bool'].connect(MainWindow.slot_build_type)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "数据合并"))
        self.docNameLabel.setText(_translate("MainWindow", "请选择 .Docx 文件"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.toolButton_3.setText(_translate("MainWindow", "..."))
        self.label_4.setText(_translate("MainWindow", "Excel 数据"))
        self.excelNameLabel.setText(_translate("MainWindow", "请选择 .csv 文件"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "模板变量"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "数据源"))
        self.pushButton_4.setText(_translate("MainWindow", "填充"))
        self.pushButton_2.setText(_translate("MainWindow", "测试"))
        self.runButton.setText(_translate("MainWindow", "运行"))
        self.label_2.setText(_translate("MainWindow", "Word 模板"))
        self.label_3.setText(_translate("MainWindow", "规则"))
        self.label.setText(_translate("MainWindow", "生成模式"))
        self.radioButtonMultiple.setText(_translate("MainWindow", "生成不同的文档"))
        self.radioButtonSingle.setText(_translate("MainWindow", "合并为一个文档"))
        self.logBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:600;\">Word数据合并</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; color:#505050;\">操作说明：</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; color:#505050;\">1. 将Word中需要更改的数据改为</span><span style=\" font-family:\'Courier New\'; font-weight:600; color:#505050;\">模板变量</span><span style=\" font-family:\'Courier New\'; color:#505050;\">，模板变量就是用两个大括号&quot;</span><span style=\" font-family:\'Courier New\'; font-size:12pt; font-weight:600; color:#505050;\">{{</span><span style=\" font-family:\'Courier New\'; color:#505050;\">&quot; &quot;</span><span style=\" font-family:\'Courier New\'; font-size:12pt; font-weight:600; color:#505050;\">}}</span><span style=\" font-family:\'Courier New\'; color:#505050;\">&quot;包裹的变量，比如{{name}}，名称自定义，多个数据一样，可以用同一个名字。注意：Word需为docx后缀文件，如不是，请另存为.docx格式。</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#505050;\">2. Excel另存为.csv文件，为了方便处理数据。注：如果需要处理的数据本身中含有英文逗号&quot;</span><span style=\" font-size:12pt; font-weight:600; color:#505050;\">,</span><span style=\" color:#505050;\">&quot;，则可能会有未知错误。</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#505050;\">3. 选择两个文件，点【填充】按钮，填充对应的数据，点击【测试】，如果测试成功则可运行。否则，请修改数据。</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#505050;\">4. 生成模式：【默认】分为生成不同的文档（拆分为多个文件）；合并为一个文档（只生成一个文件），注意如果有特殊字体，此方法样式会使用基本字体，请注意样式问题。文件生成在运行目录下的 docxdata 文件夹内。</span></p>\n"
"<p align=\"right\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#505050;\"> © 姜小豆 2019-1-30</span></p>\n"
"<hr />\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">运行日志</span>：</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

