from multiprocessing import Process
import os
import time
import spider_geonames
import spider_g2r
import sys
import spider_img

def multi_process(function_name, file_list):
    arglist = [(file,) for file in file_list]
    for arg in arglist:
        print(arg)
        process = Process(target=function_name, args=arg)
        process.start()
        time.sleep(3)


if __name__ == '__main__':
    target = spider_geonames.spider_file
    # target = spider_img.spider_file
    file_list = [
        "AI",
        "blockchain",
        "computer science",
        "data mining",
        "genetics",
        "machine learning",
    ]

    # for i in range(1, len(sys.argv)):
    #     file_list.append(sys.argv[i])

    multi_process(function_name=target, file_list=file_list)
