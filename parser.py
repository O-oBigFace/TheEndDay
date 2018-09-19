import pandas as pd
import os
import json
from countryInfo import get_country_code


def _csv(name):
    _NAME_CSV = name
    _PATH_CSV = os.path.join(os.getcwd(), "data", "{}.csv".format(_NAME_CSV))

    mat = pd.read_csv(_PATH_CSV)

    # To do.
    mat = mat.fillna(value="")

    return mat


def _parser_result_list():
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

m = _csv("remedy_0809")
l = _parser_result_list()

for id, country in l:
    m.iloc[id, 6] = country

m = m.iloc[:, 6:8]
print(m)