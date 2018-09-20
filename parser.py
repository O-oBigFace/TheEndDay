import pandas as pd
import os
import json
from countryInfo import get_country_code
import openpyxl


# 特定转换任务
def _xlsx_to_csv(name_excel, name_csv):
    path = os.path.join(os.getcwd(), "data")
    path_excel = os.path.join(path, name_excel + ".xlsx")

    head_line = "id,name,country,hindex,citation"
    line = "{0},{1},{2},{3},{4}\n"
    with open(os.path.join(path, name_csv + ".csv"), "w", encoding="utf-8") as f:
        f.write(head_line + "\n")
        wb = openpyxl.load_workbook(path_excel)
        sheet = wb.active
        for i in range(2, sheet.max_row + 1):
            id = sheet["B%d" % i].value
            name = sheet["C%d" % i].value
            # interests = sheet["D%d" % i].value
            country = sheet["E%d" % i].value
            hindex = sheet["F%d" % i].value
            citations = sheet["G%d" % i].value
            f.write(line.format(id, name, country, hindex, citations))


def _csv(name):
    _NAME_CSV = name
    _PATH_CSV = os.path.join(os.getcwd(), "data", "{}.csv".format(_NAME_CSV))

    mat = pd.read_csv(_PATH_CSV)

    # To do.
    mat = mat.fillna(value="")

    return mat


def _parser_result_list_geonames():
    d = get_country_code()
    _PATH_DIR_RESULT = os.path.join(os.getcwd(), "result")

    l = []
    for name in os.listdir(_PATH_DIR_RESULT):
        path = os.path.join(_PATH_DIR_RESULT, name)
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                js = json.loads(line.strip())
                id = js[0]

                if js[1] is None:
                    continue
                js = json.loads(js[1])
                data = js.setdefault("geonames", "")
                if len(data) < 1:
                    continue
                country = d.setdefault(data[0].setdefault("countryCode", ""), "")
                l.append((id, country))
    return l


# 更新姓名
def _parser_xlsx(file_name):
    _NAME_XLSX = file_name.replace(".xlsx", "").strip()
    _PATH_XLSX = os.path.join(os.getcwd(), "data", "{}.xlsx".format(_NAME_XLSX))
    m = pd.read_excel(_PATH_XLSX).fillna(value="")
    return m


# 根据前缀找到文件名
def get_file_name(prefix, path):
    for file in os.listdir(path=path):
        name = file.split(".")[0]
        l = name.split(sep="_")
        if prefix in l:
            return file
    return ""


# 解析google scholar + gnames结果
def _parser_result_gs_gn(name):
    name = name.strip("\'\" ")
    path = os.path.join(os.getcwd(), "result", "scholar_geonames")
    filename = get_file_name(name, path)

    result_list = []
    with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
        for line in f.readlines():
            l = json.loads(line.strip())
            if 0 < len(l) < 2:
                l = [l[0], "", "", "", -1, -1, ""]
            result_list.append(list(l))

    return pd.DataFrame(result_list)


# 解析google scholar + gnames结果
def _parser_result_g2r(name):
    name = name.strip("\'\" ")
    path = os.path.join(os.getcwd(), "result", "g2r")
    filename = get_file_name(name, path)

    result_list = []
    with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
        for line in f.readlines():
            l = json.loads(line.strip())
            if 0 < len(l) < 2:
                l = [l[0], "", "", "", -1, -1, ""]
            result_list.append(list(l))

    return pd.DataFrame(result_list)


if __name__ == '__main__':
    field = "machine learning"
    #
    # mat_main = _parser_result_gs_gn(field)
    # country_main = mat_main.iloc[:, 11].values.tolist()

    # # 1. 更新国家
    # mat_com = _parser_result_g2r(field)
    # country_com = mat_com.iloc[:, 11].values.tolist()
    #
    # for i in range(len(country_main)):
    #     if len(country_com[i]) > 1:
    #         country_main[i] = country_com[i]
    #
    # mat_main.iloc[:, 11] = country_main

    # 2. 更新name, id
    # mat_row = _parser_xlsx(field)
    # print(mat_row)
    # name_row = mat_row.iloc[:, 2].values.tolist()
    # id_row = mat_row.iloc[:, 1].values.tolist()
    # mat_main.iloc[:, 0] = id_row
    # mat_main.iloc[:, 1] = name_row

    # print(mat_main)
