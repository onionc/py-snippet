# coding:utf-8
import docx
import re

def read_docs(file):
    """ 读取word数据 """
    doc=docx.Document(r''+file)
    text = []
    for i in doc.paragraphs:
        text.append(i.text)
    data = '\n'.join(text)
    return data

def get_temp_var(data):
    """ 获取模板变量{{}} """
    temp_data = re.findall(r"\{\{[^\{\}]+\}\}",  data)
    return set(temp_data)

def sorted_dict_by_key(adict): 
    keys = adict.keys() 
    keys.sort() 
    return map(adict.get, keys) 
