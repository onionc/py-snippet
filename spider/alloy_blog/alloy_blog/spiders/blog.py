# coding:utf-8
""" 爬取前端博客文章爬虫 """

from scrapy import Spider
from scrapy import Request
from bs4 import BeautifulSoup
import bs4
import re
import logging
from alloy_blog.items import AlloyBlogItem
import os
logging.basicConfig(level=logging.INFO)


class BlogSpider(Spider):
    name = "blog"
    allowd_domains = ["alloyteam.com"]
    start_urls = ['http://www.alloyteam.com/page/0/']

    def parse(self, response):
        """ 解析函数 """
        urls = re.findall(r'href="([^\"]*)".*blogTitle', response.text)
        for url in urls:
            yield Request(url, callback=self.parse_article)

    def parse_article(self, response):
        """ 解析博客文章 """
        url = response.url

        soup = BeautifulSoup(response.text, 'lxml')

        item = AlloyBlogItem()
        item['title'] = soup.find('a', 'blogTitle btitle').string
        item['author'] = soup.find(rel='author').string
        item['url'] = url
        item['urid'] = url.split('/')[-2]

        # 内容获取
        content = soup.select(".content_banner > .text")[0]
        md_text = self.html_to_md(content)
        md_str = '\n'.join(md_text)
        md_str = f"> [{item['title']}]({url})\n\n" + md_str
        item['content'] = md_str
        '''
        # 也可直接写入md后缀文件
        path = item['urid'] + '.md'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(md_str)
        '''

        yield item

    @staticmethod
    def html_to_md(content_tag):
        """ 文章内容html解析为md """
        _code_class = 'crayon-row'

        if not isinstance(content_tag, bs4.element.Tag):
            raise TypeError("content_tag must be bs4.element.Tag type.")
        # 防止取到此节点之后，将此文档树独立出来使用
        content_tag = content_tag.extract()
        content_text = []
        tag = content_tag

        # for tag in content_tag.next_elements:
        while True:
            try:
                tag_name = tag.name
                logging.info(f"content:{tag}  tag:{tag_name}")

                if tag_name == 'a':
                    # 链接
                    logging.debug("链接")
                    href = tag.get('href', '')
                    title = tag.string

                    # to md
                    md_img = f"[{title}]({href})"
                    content_text.append(md_img)
                    # 跳过文本
                    tag = tag.next_element

                elif tag_name == 'img':

                    # 图片
                    logging.debug("图片")
                    src = tag.get('src', '')

                    # to md
                    md_img = f"![]({src})"
                    content_text.append(md_img)

                elif tag_name == 'tr' and tag.has_attr('class') and _code_class in tag['class']:
                    logging.debug("代码块")
                    # 获取每行code，添加回车
                    temp_code = []
                    for line in tag.select('div.crayon-line')[:]:
                        line_code = line.get_text()
                        if line_code == '\xa0':
                            continue
                        temp_code.append(line_code)
                    code = '\n'.join(temp_code)
                    logging.debug(f"code={code}")

                    # to md
                    md_code = f"""
```
{code}
```
"""
                    content_text.append(md_code)

                    # 避免内容再取到，取前一个对象的兄弟标签，continue的接管必须有标签节点的变更，不然死循环
                    # tag = tag.previous_element.previous_element.next_sibling
                    tag = tag.parent.parent.next_sibling

                elif tag_name is None:
                    # 文本内容
                    logging.debug(f"other: {tag.string}")

                    if isinstance(tag, bs4.element.Comment):
                        # 注释
                        pass
                    elif tag.string == '\n':
                        pass
                    else:
                        # 追加普通内容
                        content_text.append(tag.string)
                        pass
                elif re.search(r'h\d', tag_name):
                    logging.debug("标题")
                    head_grade = int(re.sub(r"h(\d)", r"\1", tag_name))
                    md_head = f"{'#'*head_grade} {tag.string}"
                    content_text.append(md_head)
                    tag = tag.next_element

                # 下一个标签
                tag = tag.next_element
            except AttributeError as e:
                print("AttributeError:", e)
                break
            except Exception as e:
                print("Exception:", e)
                break

        return content_text
