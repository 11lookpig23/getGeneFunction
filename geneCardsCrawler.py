
# coding=utf-8

import urllib.request
import requests
from requests import RequestException, Timeout
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
 

def get_page(url, timeout=40):
    """ download html according to an url """
    headers = {
        "Host": "www.genecards.org",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    }
    rsp = requests.get(url, headers=headers, timeout=timeout)
    if rsp.status_code != 200:
        raise RequestException("request failed.")
    html = rsp.content
    return html

def parse(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    funcli = soup.find_all(id="function")
    try:
        functext = funcli[0]
        functext = str(functext.dd)
    except:
        return "NO-text"
    try:
        func = re.search(r'<dd>\r\n(.*)\r\n', functext).group(1)
    except:
        return "NO-text"
    return func

def getGeneName(name = "gene.xlsx"):
    workbook=xlrd.open_workbook(name)  #文件路径
    worksheet=workbook.sheet_by_index(0)
    genelist=worksheet.col_values(0)  #获取第一列的内容
    return genelist


if __name__ == "__main__":
    genelist = getGeneName("gene.xlsx")
    funcdict = {}
    for genename in genelist[10:]:
        url1 = 'https://www.genecards.org/cgi-bin/carddisp.pl?gene='+genename
        html_doc = get_page(url1)
        functions = parse(html_doc)
        funcdict[genename] = functions
    funcPD = pd.Series(funcdict)
    funcPD.to_csv("expResult.csv")
