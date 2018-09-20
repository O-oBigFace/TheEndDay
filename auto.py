from multiprocessing import Process
import os
import time
import spider
import sys


def multi_process(function_name, file_list):
    arglist = [(file) for file in file_list]
    print(arglist)

    for arg in arglist:
        process = Process(target=function_name, args=arg)
        process.start()
        time.sleep(3)


if __name__ == '__main__':
    file_list = []

    for i in range(1, len(sys.argv)):
        file_list.append(sys.argv[i])

    multi_process(function_name=spider.spider_file, file_list=file_list)