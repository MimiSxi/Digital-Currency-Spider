# -*- coding: utf-8 -*-
"""
Created on 2025-04-18 11:20:04
---------
@summary: BIS爬虫
---------
@author: zzx
"""

import feapder
import xlwt


class BisSpider(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        REDISDB_IP_PORTS="192.168.31.197:6379", REDISDB_USER_PASS="", REDISDB_DB=0
    )

    def start_requests(self):
        print("---------------开始爬虫【国际清算银行（BIS）】---------------")
        yield feapder.Request(search_url)

    def parse(self, request, response):
        # self.stop_spider()
        global get_num
        global search_url
        global search_index
        finish = False
        json = response.json
        search_word = json['q']  # 查询关键字
        hits = json['result']['hits']
        for i in hits:
            title = i['title']  # 文章标题
            url = i['url']  # 文章链接
            date = i['date']  # 文章日期
            # if '2024-01-01' <= date <= '2025-12-31':
            if '2025-01-01' <= date <= '2025-12-31':
                finish = False
                urls_init.append([title, date, url, search_word, ''])
            else:
                finish = True
                break
        if finish:
            print("关键字" + search_word + "已爬完")
            if search_index < len(search_list) - 1:
                search_index = search_index + 1
                get_num = 200
                search_url = "https://www.bis.org/api-search/search.json?as_sitesearch=www.bis.org&num=200&&sort=date&q=" + \
                             search_list[search_index]
                yield feapder.Request(search_url)
            else:  # 全部爬完
                self.url_operate()
                self.write_excel()
                print("爬虫完成，共获取" + str(len(urls_operated)) + "篇文章")
                print("---------------excel已生成，程序结束---------------")
                return
        else:
            if get_num == 200:
                search_url = search_url + "&start=" + str(get_num)
            else:
                search_url = search_url.replace("start=" + str(get_num - 200), "start=" + str(get_num))
            get_num = get_num + 200
            yield feapder.Request(search_url)

    # 文章链接处理，重复文章保留pdf格式
    def url_operate(self):
        file_groups = {}
        for i in urls_init[:]:
            if "/author/" in i[2] or "/country/" in i[2] or "/about/" in i[2]:
                urls_init.remove(i)
            if i[0] is not None:
                i[0] = i[0].replace('<b>', '')
                i[0] = i[0].replace('</b>', '')
        for i in urls_init:
            tmp = i[2].rsplit('.', 1)
            main_part = tmp[0]
            ext = tmp[-1]
            if main_part not in file_groups:
                file_groups[main_part] = []
            file_groups[main_part].append((ext, i))

        for main_part, files in file_groups.items():
            if len(files) == 1:
                urls_operated.append((files[0][1]))
            else:
                pdf_files = [file for ext, file in files if ext.lower() == 'pdf']
                if pdf_files:
                    urls_operated.append(pdf_files[0])

    def write_excel(self):
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet("国际清算银行（BIS）")
        head = ['标题', '日期', '链接', '关键字', '摘要']
        for i in head:
            sheet.write(0, head.index(i), i)
        for i in range(len(urls_operated)):
            for j in range(len(urls_operated[i])):
                sheet.write(i + 1, j, urls_operated[i][j])
        book.save('数字人民币爬虫.xls')


if __name__ == "__main__":
    search_index = 0  # 关键字下标
    get_num = 200  # 当前爬取文章数
    search_list = ['CBDC']  # 关键字列表
    search_url = "https://www.bis.org/api-search/search.json?as_sitesearch=www.bis.org&num=200&&sort=date&q=" + \
                 search_list[0]
    urls_init = []  # 初始文章信息
    urls_operated = []  # 去重后文章信息
    BisSpider(redis_key="test").start()
