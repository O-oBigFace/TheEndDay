import requests
import hashlib
import random
from bs4 import BeautifulSoup
from Logger import logger
import os
import pandas as pd
import time
import json
from multiprocessing import Process
import scholar
from countryInfo import get_country_code
import sys

"""
only spider
"""

# host
# _HOST = 'http://maps.googleapis.com/maps/api/geocode/json'
# _GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
# _COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}

# _GEONAMES_USER = "huan2018"
_GEONAMES_USER = ["bigface", "huan2018"]
_HOST_GEONAMES = "http://api.geonames.org/wikipediaSearchJSON?q={0}&maxRows=10&username=" + random.choice(_GEONAMES_USER)
_HEADERS_GEONAMES = {
    # 'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    # 'accept': 'text/html,application/xhtml+xml,application/xml'
    }

# proxies
_PROXY_HOST = "proxy.crawlera.com"
_PROXY_POST = "8010"
# _PROXY_AUTH = "c3dad299d5bb46b785fda38e8322c5e4:"
# August
_PROXY_AUTH = "020f566483124ffabffb045089a73b11:"
_PROXIES = {
    "https": "https://{0}@{1}:{2}/".format(_PROXY_AUTH, _PROXY_HOST, _PROXY_POST),
    # "http": "http://{0}@{1}:{2}/".format(_PROXY_AUTH, _PROXY_HOST, _PROXY_POST)
}
# _PROXIES = {
#     "http": "socks5://127.0.0.1:1080",
#     "https": "socks5://127.0.0.1:1080",
# }

# requests
_SESSION = requests.Session()

# files

# RESULT
_PATH_DIR_RESULT = os.path.join(os.getcwd(), "result")


# CSV
# import csv

# # XLSX
# import openpyxl
# _NAME_XLSX = "AI"
# _PATH_XLSX = os.path.join(os.getcwd(), "data", "{}.xlsx".format(_NAME_CSV))


def _get_page(pagerequest):
    resp = _SESSION.get(
        pagerequest,
        headers=_HEADERS_GEONAMES,
        # cookies=_COOKIES,
        proxies=_PROXIES,
        verify=False,
    )
    resp.encoding = "utf-8"
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


def _make_soup(pagerequest):
    html = _get_page(pagerequest)
    return BeautifulSoup(html, "lxml")


def _csv_to(name):
    _NAME_CSV = name
    _PATH_CSV = os.path.join(os.getcwd(), "data", "{}.csv".format(_NAME_CSV))

    mat = pd.read_csv(_PATH_CSV)

    # To do.
    mat = mat.fillna(value="")
    mat = mat.iloc[: , 1].values.tolist()
    return mat


def save_list_to_file(filename, list):
    with open(filename, "w", encoding="utf-8") as f:
        for l in list:
            f.write(json.dumps(l) + "\n")


# This Project.
def spider_geonames(csv_name, begin, end):
    affiliation = _csv_to(csv_name)
    print("%d | %d" % (begin, end))
    # To do.
    path_result = os.path.join(_PATH_DIR_RESULT, "%d_%d") % (begin, int(time.time()) % 1000)

    result_list = []
    for i in range(begin, end):
        # save file
        if i % 10 == 0:
            save_list_to_file(path_result, result_list)

        if len(affiliation) < 1:
            result_list.append((i, ""))

        js = None
        times = 0
        url = _HOST_GEONAMES.format(requests.utils.quote(affiliation[i]))
        while js is None and times < 5:
            if times > 0:
                time.sleep(times)
            times += 1

            try:
                js = _get_page(url)
            except Exception as e:
                logger.error("%d | %s" % (i, str(e)))
                js = None
        logger.info("%d | %s" % (i, json.dumps(js)))
        result_list.append((i, js))

    else:
        save_list_to_file(path_result, result_list)


def multi_process(function_name, begin, end, num_of_ps):
    count = end - begin
    quarter = count // num_of_ps

    arglist = [(begin + i * quarter, begin + (i + 1) * quarter) for i in range(num_of_ps)]
    print(arglist)

    for arg in arglist:
        process = Process(target=function_name, args=arg)
        process.start()
        time.sleep(3)


def _parser_xlsx(file_name):
    _NAME_XLSX = file_name.replace(".xlsx", "").strip()
    _PATH_XLSX = os.path.join(os.getcwd(), "data", "{}.xlsx".format(_NAME_XLSX))
    m = pd.read_excel(_PATH_XLSX).fillna(value="")
    return m


def get_country(affiliation):
    if len(affiliation) < 1:
        return ""
    d = get_country_code()
    js = None
    times = 0
    url = _HOST_GEONAMES.format(requests.utils.quote(affiliation))
    while js is None and times <= 6:
        if times > 0:
            time.sleep(times)
        times += 1
        try:
            js = _get_page(url)
            break
        except Exception as e:
            logger.error("%d | %s" % (affiliation, str(e)))
            js = None
    data = json.loads(js).setdefault("geonames", "")
    if len(data) < 1:
        return ""
    return d.setdefault(data[0].setdefault("countryCode", ""), "")


def spider_file(file_name):
    file_name = file_name.strip().replace(".xlsx", "")
    m = _parser_xlsx(file_name)
    expert_id = m.iloc[:, 0]
    expert_name = m.iloc[:, 2]
    item = [(expert_id[i], expert_name[i]) for i in range(len(expert_id))]

    path_result = os.path.join(_PATH_DIR_RESULT, "%s_%d") % (file_name, int(time.time()) % 1000)
    result_list = []

    # expert 都是从1开始编号，在文件中都从第二行开始
    for id, name in item:
        if id % 10 == 0:
            save_list_to_file(path_result, result_list)

        author = None
        max_tries = 0
        while author is None and max_tries < 6:
            try:
                author = next(scholar.search_author(name)).fill()
                break
            # 如果谷歌学术中不存在该学者的信息，则记录默认值
            except Exception as e:
                max_tries += 1
                logger.error("%s | %d | %s | %s | trries: %d" % (file_name, id, name, str(e), max_tries))
                time.sleep(max_tries)
                author = None
        if author is None:
            result_list.append((id,))
            continue
        logger.info("%d | %s" % (id, str(author)))
        _name = author.name
        affiliation = author.affiliation
        email = author.email
        citedby = author.citedby
        hindex = author.hindex
        hindex5y = author.hindex5y
        i10index = author.i10index
        i10index5y = author.i10index5y
        url_picture = author.url_picture
        country = get_country(affiliation)
        result_list.append((_name, affiliation, email, citedby, hindex, hindex5y,i10index, i10index5y, url_picture, country))
    else:
        save_list_to_file(path_result, result_list)


if __name__ == '__main__':
    file_name = sys.argv[1]
    spider_file(file_name)



