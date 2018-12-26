# coding:utf-8
""" 爬虫练习：2018豆瓣图书榜单 json数据解析"""
import requests
import json
import sqlite3
import sys
import os
import logging
logging.basicConfig(level=logging.INFO)


class DoubanJson(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.sqlite = Sqlite()
        self.path = sys.path[0]
        self.data_path = sys.path[0]+'/data'

    def get_index(self, offset):
        """ 获取指定页数据 """
        url = f"https://book.douban.com/ithil_j/activity/book_annual2018/widget/{offset}"
        content = None
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                content = resp.text
        except Exception as e:
            logging.info(f"urlerror. {url}, {e}")

        return content

    def parse_json(self, text):
        return json.loads(text)

    def save(self, text, is_save_img=False):
        """ 保存 """
        self.sqlite = Sqlite()
        text = json.loads(text)

        subjects = text['res']['subjects']
        if subjects:
            data = {}
            # 获取分类
            data['class'] = text['res']['payload']['title']

            # 建文件夹
            dir_path = None
            if is_save_img:
                logging.info("创建文件夹")
                dir_path = self.mkdir(data['class'])
                logging.info(dir_path)

            values = []
            for k, v in enumerate(subjects):
                data['title'] = v['title']
                data['type'] = v['type']
                data['url'] = v['url']
                data['rating'] = v['rating']
                data['rating_count'] = v['rating_count']
                data['cover'] = v['cover']
                data['book_id'] = v['id']
                data['rank'] = k

                # 组装sql语句
                keys = (tuple(data.keys()))
                # occupy = tuple(['?']*len(keys))
                # occupy = str(tuple([0]*len(keys))).replace('0', '?')
                occupy = "("+("?,"*len(keys))[:-1]+")"
                sql = f"insert into books{keys} values{occupy}"
                values.append(tuple(data.values()))

                if dir_path and is_save_img:
                    self.save_img(dir_path, data['cover'], data['title'])

            sqlite.execute(sql, values)
            logging.info(f"写入分类：[{data['class']}], 条数：{len(values)}")

        else:
            logging.info('无数据')

    def save_img(self, path, img_url, img_name=None):
        """ 保存图片 """
        # 获取图片名
        suffix = img_url.split('.')[-1]
        if not img_name:
            img_name = img_url.split('/')[-1]
        else:
            img_name = img_name + "." + suffix
        local_img_url = os.path.join(path, img_name)

        imgs = requests.get(img_url, headers=self.headers)
        with open(local_img_url, "wb") as f:
            f.write(imgs.content)
        logging.info(f"{local_img_url} saved.")

    def mkdir(self, dir_name):
        """ 创建文件夹 """
        dir_path = os.path.join(self.data_path, dir_name)
        is_exists = os.path.exists(dir_path)

        if not is_exists:
            os.makedirs(dir_path)

        return dir_path


class Sqlite(object):
    """ 使用Sqlite """
    def __init__(self):
        self.conn = sqlite3.connect(sys.path[0]+'/book2018.db')
        self.cur = self.conn.cursor()

    def create(self):
        table = """
            CREATE TABLE `books` (
            `id` INTEGER primary key AUTOINCREMENT NOT NULL,
            `book_id` varchar(32) NOT NULL,
            `title` varchar(128),
            `type` varchar(32) NOT NULL,
            `class` varchar(128),
            `url` varchar(128),
            `cover` varchar(128),
            `rating` double(10,2),
            `rating_count` int,
            `rank` int,
            `status` int,
            `created` varchar(20)
            )
        """
        self.execute(table)

    def execute(self, sql, data=None):
        """ 执行SQL，返回结果 """
        result = False
        try:
            arg = sql.lstrip().upper()
            if arg.startswith("SELECT"):
                result = self.cur.execute(sql)
            elif arg.startswith("INSERT") and data:
                self.cur.executemany(sql, data)
                self.commit()
                result = True
            else:
                self.cur.execute(sql)
                result = True
        except sqlite3.Error as e:
            logging.debug(f"sql execute:{sql} \n error: {e.args[0]}\n")
        except Exception as e:
            logging.debug(e)

        return result

    def commit(self):
        self.conn.commit()

    def truncate(self, table_name=None):
        """ 清空表 """
        logging.debug(f"清空表 {table_name}")
        if not table_name:
            table_name = 'books'
        self.execute(f"delete from `{table_name}`")
        self.execute(f"update sqlite_sequence set seq=0 where name='{table_name}'")

    def __del__(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    douban = DoubanJson()
    # 创建和清空表
    sqlite = Sqlite()
    sqlite.create()
    sqlite.truncate()

    # 遍历页码
    for i in range(1, 42):
        logging.info(f"页码：{i}...")
        content = douban.get_index(i)
        douban.save(content, True)
