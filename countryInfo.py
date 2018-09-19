def get_country_code():
    d = {}
    with open("countryInfo.csv", "r", encoding="utf-8") as f:
        count = 0
        for line in f.readlines():
            line = line.split(",")
            if count is 0:
                count = 1
                continue
            d[line[0]] = line[4]
    return d