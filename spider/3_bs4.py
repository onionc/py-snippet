# coding:utf-8
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'lxml')
# print(soup.prettify())
# print(soup.get_text())

# 获取标题标签、标签名、标题内容
title_tag = soup.title
tag_name = soup.title.name
title = soup.title.string
print(title_tag)
print(tag_name)
print(title)

print(soup.find_all('a'))
