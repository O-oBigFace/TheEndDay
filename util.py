import os
import pandas as pd
import json
import numpy as np

# RESULT
PATH_DIR_RESULT = os.path.join(os.getcwd(), "result")


def csv_to(name, dir="data"):
    _NAME_CSV = name
    _PATH_CSV = os.path.join(os.getcwd(), dir, "{}.csv".format(_NAME_CSV))

    mat = pd.read_csv(_PATH_CSV)

    # To do.
    mat = mat.fillna(value="")
    # mat = mat.iloc[:, 1].values.tolist()
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


def parser_xlsx(file_name):
    _NAME_XLSX = file_name.replace(".xlsx", "").strip()
    _PATH_XLSX = os.path.join(os.getcwd(), "data", "{}.xlsx".format(_NAME_XLSX))
    m = pd.read_excel(_PATH_XLSX).fillna(value="")
    return m
