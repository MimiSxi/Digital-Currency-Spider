"""
Created on 2025-04-23
---------
@summary: 摘要分析
---------
@author: zzx
"""


import xlrd
import xlwt
import subprocess
import time


def read_excel(file_name):
    global sheet_name
    workbook = xlrd.open_workbook(file_name)
    for i in workbook.sheet_names():
        sheet_name = i
        table = workbook.sheet_by_name(i)
        rows = table.nrows
        cols = table.ncols
        sheet_list = []
        for row in range(rows):
            row_value = []
            if row != 0:
                for col in range(cols):
                    data = table.cell(row, col).value
                    row_value.append(data)
                    # print(row_value)
                sheet_list.append(row_value)
        print(sheet_list)
        analysis(sheet_list)


def write_excel(sheet_list):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet(sheet_name)
    head = ['标题', '日期', '链接', '关键字', '摘要']
    for i in head:
        sheet.write(0, head.index(i), i)
    for i in range(len(sheet_list)):
        for j in range(len(sheet_list[i])):
            sheet.write(i + 1, j, sheet_list[i][j])
    book.save(excel_name)


def analysis(sheet_list):
    for i in range(0, len(sheet_list)):
        if sheet_list[i][4] == '':
            print("开始分析第" + str(i + 1) + "篇文章")
            try:
                abstract = subprocess.check_output(
                    ["python", "workflowTest.py", sheet_list[i][2]], encoding="utf-8", text=True
                ).strip()
                sheet_list[i][4] = abstract
                write_excel(sheet_list)
                print("第" + str(i + 1) + "篇文章分析完成")
                time.sleep(5)
            except Exception as e:
                print(f"error occurred:{e}")
        else:
            print("第" + str(i + 1) + "篇文章已有摘要，无需分析")


if __name__ == "__main__":
    excel_name = input("请输入要进行摘要分析的文件名（如数字人民币爬虫.xls）：")
    sheet_name = ""
    read_excel(excel_name)
    print("-------------------------摘要分析完成-------------------------")
    input("按回车键退出")
