#!/usr/bin/python
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable
#import sys
#base = 'WIN32GUI' if sys.platform == "win32" else None

setup(  name = "Combine_docx",
#        opeions = {
#            'build_exe':{
#                'packages':[], 
#                'include_files': ['combine.ico']
#            }
#        }, 
        version = "1.0",
        description = "类似Word邮件合并功能，将Word模板用数据填充生成多份。",
        executables = [Executable("./mainwindow.py",  icon="combine.ico")])
