# -*- coding: utf-8 -*-
"""
Created on 2025-04-18 11:20:04
---------
@summary: 国际货币基金组织（IMF）爬虫
---------
@author: jlc
"""

import feapder
import xlwt
from feapder.utils import tools


class ImfSpider(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        REDISDB_IP_PORTS="192.168.31.197:6379", REDISDB_USER_PASS="", REDISDB_DB=0
    )

    def start_requests(self):
        print("---------------开始爬虫【国际货币基金组织（IMF）】---------------")
        yield feapder.Request(search_url, method="POST", params=search_params)

    def parse(self, request, response):
        global get_num
        global search_url
        global search_index
        json = response.json
        results = json["results"]
        for i in results:
            title = i["Title"]
            url = i["ClickUri"]
            time = int(i["raw"]["approvez32xdatez32xtime"])
            imfcontenttypedisplay = i["raw"]["imfcontenttypedisplay"]
            time = tools.timestamp_to_date(time / 1000.0)
            if (
                "2025-01-01 00:00:00" <= time <= "2025-12-31 00:00:00"
                and imfcontenttypedisplay != "Blogs"
            ):
                urls_init.append([title, time, url, "Digital Currencies", ""])
            else:
                break
        finish = True
        if finish:
            print("关键字" + "Digital Currencies" + "已爬完")
            if search_index < len(search_list) - 1:
                # 多关键词遍历
                search_index = search_index + 1
                # get_num = 200
                # search_url = (
                #     "https://www.bis.org/api-search/search.json?as_sitesearch=www.bis.org&num=200&&sort=date&q="
                #     + search_list[search_index]
                # )
                # yield feapder.Request(search_url)
            else:  # 全部爬完
                self.write_excel()
                print("爬虫完成，共获取" + str(len(urls_init)) + "篇文章")
                print("---------------excel已生成，程序结束---------------")
                return
        else:
            print(1)
            # 爬取数量计算
            # if get_num == 200:
            #     search_url = search_url + "&start=" + str(get_num)
            # else:
            #     search_url = search_url.replace(
            #         "start=" + str(get_num - 200), "start=" + str(get_num)
            #     )
            # get_num = get_num + 200
            # yield feapder.Request(search_url)
        # print(search_word)

    def write_excel(self):
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("国际货币基金组织（IMF）")
        head = ["标题", "日期", "链接", "关键字", "摘要"]
        for i in head:
            sheet.write(0, head.index(i), i)
        for i in range(len(urls_init)):
            for j in range(len(urls_init[i])):
                sheet.write(i + 1, j, urls_init[i][j])
        book.save("数字人民币爬虫.xls")


if __name__ == "__main__":
    config_file = "./config.ini"
    conf = tools.configparser.ConfigParser()
    conf.read(config_file)
    search = conf["search"]
    
    print(search["start_date"])
    print(search["end_date"])
    search_index = 0
    get_num = int(search["num"])
    
    search_list = search["key_word"].split(",")
    search_url = "https://www.imf.org/coveo/rest/search/v2?sitecoreItemUri=sitecore%3A%2F%2Fweb%2F%7B69D1D09E-EFFF-402D-AD91-34C2A2DAE66A%7D%3Flang%3Den%26amp%3Bver%3D8&siteName=imf"
    # todo)) 参数化
    search_params = {
        "numberOfResults": 20,
        "searchHub": "Search",
        "locale": "en",
        "q": "Digital Currencies",
        "isGuestUser": "false",
        "referrer": "https://www.imf.org/en/Search",
        "sortCriteria": "relevancy",  # 排序规则
        # "firstResult": 10   #翻页参数
    }
    urls_init = []  # 初始文章信息
    urls_operated = []  # 去重后文章信息
    # ImfSpider(redis_key="IMF").start()
