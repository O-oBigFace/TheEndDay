import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time
import json
from multiprocessing import Process
import numpy as np
import pprint
from Logger import logger


"""
only spider
"""

_HOST_GUIDE2RESEARCH = r"http://www.guide2research.com"
_GUIDE_SCIENTISTS = r"/u/{0}"
_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    }

# proxies
_PROXY_HOST = "proxy.crawlera.com"
_PROXY_POST = "8010"
_PROXY_AUTH = "020f566483124ffabffb045089a73b11:"
_PROXIES = {
    "https": "https://{0}@{1}:{2}/".format(_PROXY_AUTH, _PROXY_HOST, _PROXY_POST),
}

# requests
_SESSION = requests.Session()

# files

# RESULT
_PATH_DIR_RESULT = os.path.join(os.getcwd(), "result")


def _get_page(pagerequest):
    resp = _SESSION.get(
        pagerequest,
        headers=_HEADERS,
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
    mat = mat.iloc[:, 1].values.tolist()
    return mat


# 处理json.dumps的问题
def default_json(o):
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError


# 存储list形式的文件
def save_list_to_file(filename, list):
    with open(filename, "w", encoding="utf-8") as f:
        for l in list:
            f.write(json.dumps(l, default=default_json) + "\n")


def _parser_xlsx(file_name):
    _NAME_XLSX = file_name.replace(".xlsx", "").strip()
    _PATH_XLSX = os.path.join(os.getcwd(), "data", "{}.xlsx".format(_NAME_XLSX))
    m = pd.read_excel(_PATH_XLSX).fillna(value="")
    return m


def multi_process(function_name, begin, end, num_of_ps):
    count = end - begin
    quarter = count // num_of_ps

    arglist = [(begin + i * quarter, begin + (i + 1) * quarter) for i in range(num_of_ps)]
    print(arglist)

    for arg in arglist:
        process = Process(target=function_name, args=arg)
        process.start()
        time.sleep(3)


def search_scientist(name):
    return Scientist(name)


class Scientist(object):
    def __init__(self, __name):
        if isinstance(__name, str):
            self.__data = __name.strip("""\'\" """)
        self._filled = False

    def fill(self):
        url = _HOST_GUIDE2RESEARCH + _GUIDE_SCIENTISTS.format(self.__data.replace(" ", "-"))
        soup = _make_soup(url)
        self.name = soup.find("h1").text
        if len(self.name) < 1:
            self._filled = True
            return None

        self.affiliation, self.country = soup.select("td[valign='top'] b a[href]")
        self.affiliation = self.affiliation.text
        self.country = self.country.text

        index_table = soup.select("tr td[style]")
        if len(index_table) > 9:
            self.hindex = int(index_table[1].text.strip().replace(",", ""))
            self.citedby = int(index_table[3].text.strip().replace(",", ""))
            self.national_ranking = index_table[5].text.strip().replace(",", "")
            self.world_ranking = index_table[7].text.strip().replace(",", "")
            self.dblp = int(index_table[9].text.strip().replace(",", ""))
        else:
            self.hindex = self.citedby = self.dblp = 0
            self.world_ranking = self.national_ranking = ""

        self.achievements = {}
        b = soup.select("li b")
        i = soup.select("li i")
        for ix in range(len(b)):
            self.achievements[b[ix].text] =  i[ix].text

        self.external_link = {}
        external = soup.select("div[class='content'] li a[target='_blank']")
        for link in external:
            self.external_link[link.text] = link["href"]

        self.url_picture = soup.select("img")[1]["src"]

        self._filled = True
        return self

    def __str__(self):
        return pprint.pformat(self.__dict__)


def spider(file_name):
    file_name = file_name.strip().replace(".xlsx", "")

    # 解析xlsx文件
    m = _parser_xlsx(file_name)
    expert_id = m.iloc[:, 0]
    expert_name = m.iloc[:, 2]
    item = [(expert_id[i], expert_name[i]) for i in range(len(expert_id))]

    path_result = os.path.join(_PATH_DIR_RESULT, "_%s_%d") % (file_name, int(time.time()) % 1000)
    result_list = []

    # expert 都是从1开始编号，在文件中都从第二行开始
    for id, name in item:
        if id % 10 == 6:
            save_list_to_file(path_result, result_list)

        author = None
        max_tries = 0
        while author is None and max_tries < 6:
            try:
                author = search_scientist(name).fill()
                break
            # 如果谷歌学术中不存在该学者的信息，则记录默认值
            except Exception as e:
                max_tries += 1
                logger.error("%s | %d | %s | %s | trries: %d" % (file_name, id, name, str(e), max_tries))
                time.sleep(max_tries)
                author = None

        item = (id,)
        if author is None:
            result_list.append(item)
            logger.info("%s | %s" % (file_name, json.dumps(item, default=default_json)))
            continue
        _name = author.name
        affiliation = author.affiliation
        citedby = author.citedby
        hindex = author.hindex
        url_picture = author.url_picture
        country = author.country
        item = (id, _name, affiliation, "", "", citedby, hindex, -1, -1, -1, url_picture, country)
        result_list.append(item)
        logger.info("%s | %s" % (file_name, json.dumps(item, default=default_json)))
    else:
        save_list_to_file(path_result, result_list)


if __name__ == '__main__':
    spider("AI")