# -*- coding: utf-8 -*-
"""
Created on 2025-04-18 11:20:04
---------
@summary:
---------
@author: admin
"""

import feapder
from loguru import logger


class BisSpider(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        REDISDB_IP_PORTS="192.168.31.197:6379", REDISDB_USER_PASS="", REDISDB_DB=0
    )

    def start_requests(self):
        yield feapder.Request(search_url)

    def parse(self, request, response):
        global get_num
        global search_url
        global search_index
        json = response.json
        search_word = json['q']  # 查询关键字
        total = json['result']['total']  # 文章总数
        hits = json['result']['hits']
        print(hits)
        for i in hits:
            title = i['title']
            url = i['url']
            urls.append(url)
        print(search_word)
        print(total, get_num)
        if total <= get_num:
            if search_index < len(search_list) - 1:
                search_index = search_index + 1
                get_num = 200
                search_url = "https://www.bis.org/api-search/search.json?as_sitesearch=www.bis.org&num=200&&sort=date&q=" + \
                             search_list[search_index]
                yield feapder.Request(search_url)
            else:
                self.url_operate()
                for i in urls_operated:
                    yield feapder.Request(url=i, callback=self.dowload_parse)
                return
        else:
            while get_num < total:
                search_url = search_url + "&start=" + str(get_num)
                get_num = get_num + 200
                yield feapder.Request(search_url)

    def url_operate(self):
        file_groups = {}
        print(urls)
        for i in urls:
            tmp = i.rsplit('.', 1)
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

        print(urls_operated)

    def dowload_parse(self, request, response):
        if 'application/pdf' in response.headers.get('Content-Type', ''):
            try:
                file_name = response.url.split('/')[-1]
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Successful")
            except Exception as e:
                logger.error(f"Failed:{e}")
        # else:

    # # 提取网站title
    # print(response.xpath("//title/text()").extract_first())
    # # 提取网站描述
    # print(response.xpath("//meta[@name='description']/@content").extract_first())
    # print("网站地址: ", response.url)


if __name__ == "__main__":
    search_index = 0
    get_num = 200
    search_list = ['Digital+Currencie']
    search_url = "https://www.bis.org/api-search/search.json?as_sitesearch=www.bis.org&num=20&&sort=date&q=" + \
                 search_list[0]
    urls = []
    urls_operated = []
    excel_list = []
    BisSpider(redis_key="test").start()
