import util
import os
import pprint

_IX  = {
    "index": 0,
    "id": 1,
    "name": 2,
    "affiliation": 3,
    "country": 4,
    "hindex": 5,
    "citedby": 6,
    "pic": 7,
}


def get_statistics(name, dir):
    return Statistics(name, dir)


# 统计csv文件中的数值
class Statistics(object):

    def __init__(self, name, dir):
        self.target_file = os.path.join(os.getcwd(), dir, "%s.csv" % name.strip().replace(".csv", ""))

    def calculate(self):
        mat = util.csv_to_path(self.target_file)
        overall =len(mat)
        self.allCount = self.affiliationCount = self.countryCount = self.hindexCount = self.citedbyCount = self.picCount = 0

        for row in mat.itertuples(index=False, name=None):
            if row[_IX["hindex"]] < 0:
                continue
            self.allCount += 1
            self.affiliationCount += 1
            self.hindexCount += 1
            self.citedbyCount += 1
            if len(row[_IX["pic"]].strip()) > 1:
                self.picCount += 1
            if len(row[_IX["country"]].strip()) > 1:
                self.countryCount += 1

            self.allRate = self.allCount / overall
            self.affiliationRate = self.affiliationCount / overall
            self.countryRate = self.countryCount / overall
            self.hindexRate = self.hindexCount / overall
            self.citedbyRate = self.citedbyCount / overall
            self.picRate = self.picCount / overall
        return self

    def __str__(self):
        return pprint.pformat(self.__dict__)


def tuple_to_str(t):
    s = ""
    for item in t:
        s += str(item) + ","
    return s.rstrip(",")

if __name__ == '__main__':
    file_list = [
        "AI",
        "blockchain",
        "computer science",
        "data mining",
        "genetics",
        "machine learning",
    ]

    rate = 0
    countryrate = 0
    for name in file_list:
        statistics = get_statistics(name, "result").calculate()
        rate += statistics.allRate
        countryrate += statistics.countryRate

    print(rate / len(file_list), countryrate/ len(file_list))
        # with open(statistics.target_file, "a", encoding="utf-8") as f:
            # f.write(tuple_to_str((
            #         "Count",
            #         str(statistics.allCount) ,
            #         "",
            #         str(statistics.affiliationCount),
            #         str(statistics.countryCount),
            #         str(statistics.hindexCount),
            #         str(statistics.citedbyCount),
            #         str(statistics.picCount),
            #         )) + "\n")
            # f.write(tuple_to_str((
            #         "Rate",
            #         str(statistics.allRate),
            #         "",
            #         str(statistics.affiliationRate),
            #         str(statistics.countryRate),
            #         str(statistics.hindexRate),
            #         str(statistics.citedbyRate),
            #         str(statistics.picRate),
            #         )) + "\n")

