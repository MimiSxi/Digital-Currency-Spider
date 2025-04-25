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
        global search_params
        global search_index
        global firstResult
        global key_url_num
        json = response.json
        results = json["results"]
        totalCount = int(json["totalCount"])
        print(f"=========进度{firstResult + 50 }/{totalCount}==========")
        for i in results:
            title = i["Title"]
            url = i["ClickUri"]
            time = int(i["raw"]["date"])
            time = tools.timestamp_to_date(time / 1000.0, time_format="%Y-%m-%d")
            if search["start_date"] <= time <= search["end_date"]:
                urls_init.append([title, time, url, search_list[search_index], ""])
                key_url_num = key_url_num + 1
            else:
                break
        print(f"get_num:{get_num}")
        print(f"key_url_num:{key_url_num}")
        if get_num <= key_url_num or totalCount <= (firstResult + get_num):
            print("关键字" + search_list[search_index] + "已爬完")
            if search_index < len(search_list) - 1:
                # 多关键词遍历
                search_index = search_index + 1
                firstResult = 0
                search_params["q"] = search_list[search_index]
                search_params["firstResult"] = firstResult
                key_url_num = 0
                yield feapder.Request(search_url, method="POST", params=search_params)
            else:  # 全部爬完
                self.write_excel()
                print("爬虫完成，共获取" + str(len(urls_init)) + "篇文章")
                print("---------------excel已生成，程序结束---------------")
                return
        else:
            firstResult = firstResult + 50
            search_params["firstResult"] = firstResult
            yield feapder.Request(search_url, method="POST", params=search_params)
        # print(search_word)

    # 文章链接处理，重复文章保留pdf格式
    def url_operate(self):
        file_groups = {}
        for i in urls_init:
            tmp = i[2].rsplit(".", 1)
            main_part = tmp[0]
            ext = tmp[-1]
            if main_part not in file_groups:
                file_groups[main_part] = []
            file_groups[main_part].append((ext, i))

        for main_part, files in file_groups.items():
            if len(files) == 1:
                urls_operated.append((files[0][1]))
            else:
                pdf_files = [file for ext, file in files if ext.lower() == "pdf"]
                if pdf_files:
                    urls_operated.append(pdf_files[0])

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
    key_url_num = 0
    search_index = 0
    get_num = int(search["num"])

    search_list = search["key_word"].split(",")
    search_url = "https://www.imf.org/coveo/rest/search/v2?sitecoreItemUri=sitecore%3A%2F%2Fweb%2F%7B69D1D09E-EFFF-402D-AD91-34C2A2DAE66A%7D%3Flang%3Den%26amp%3Bver%3D8&siteName=imf"
    firstResult = 0
    search_params = {
        "maximumAge": "900000",
        "filterField": "@foldingcollection",
        "filterFieldRange": "1",
        "parentField": "@foldingchild",
        "childField": "@foldingparent",
        "enableDidYouMean": "true",
        "sortCriteria": "@imfdate descending",
        "retrieveFirstSentences": "true",
        "timezone": "Asia/Shanghai",
        "enableQuerySyntax": "true",
        "enableDuplicateFiltering": "true",
        "enableCollaborativeRating": "false",
        "debug": "false",
        "allowQueriesWithoutKeywords": "true",
        "aq": '((((@imfcol<>"IMFORG-IEO" OR @syssourcetype==Web) OR @syssourcetype==Sitemap) @imfdate>1900/01/01@13:05:43) NOT @z95xtemplate==(ADB6CA4F03EF4F47B9AC9CE2BA53FF97,FE5DD82648C6436DB87A7C4210C7413B))',
        "cq": '(((@imflanguage==ENG @sysfiletype<>pdf) OR (@syslanguage==English @sysfiletype==pdf) OR @syslanguage==en)) (((@z95xlanguage==en) (@z95xlatestversion==1) (@source=="Coveo_web_index - PRD93-SITECORE-IMFORG")) OR (@source==("DATA-IMF-ORG","IMFORG-ADMINTRIB","IMFORG-AM-VIDEOS","IMFORG-FAD","IMFORG-FANDD","IMFORG-MAIN","IMFORG-SELDEC","IMFORG-SM-VIDEOS","IMFORG-STAFFPAPERS","IMFORG-SiteMap-Manual","IMFORG-DATAMAPPER")))',
        "numberOfResults": "50",
        "searchHub": "Search",
        "locale": "en",
        "q": search_list[search_index],
        "isGuestUser": "false",
        "referrer": "https://www.imf.org/en/Search",
        "sortCriteria": "@imfdate descending",  # 排序规则
        "facets": '[{"facetId":"type","field":"imfcontenttype","type":"hierarchical","injectionDepth":1000,"delimitingCharacter":"|","filterFacetCount":true,"basePath":[],"filterByBasePath":false,"currentValues":[{"value":"PUBS","state":"selected","children":[],"retrieveChildren":true,"retrieveCount":10}],"preventAutoSelect":false,"numberOfValues":1,"isFieldExpanded":false}]',
        "firstResult": firstResult,  # 翻页参数
    }
    urls_init = []  # 初始文章信息
    urls_operated = []  # 去重后文章信息
    ImfSpider(redis_key="IMF").start()
