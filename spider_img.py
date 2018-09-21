import scholar
import util
import os
from Logger import logger
import time


def spider_file(file_name):
    file_name = file_name.strip().replace(".xlsx", "")

    # 解析xlsx文件
    m = util.csv_to(file_name, dir="result")
    expert_id = m.iloc[:, 1]
    expert_pic = m.iloc[:, 7]
    item = [(expert_id[i], expert_pic[i]) for i in range(len(expert_id))]

    # expert 都是从1开始编号，在文件中都从第二行开始
    for id, pic in item:
        if len(pic) < 1 or "user=&" in pic or "cleardot" in pic or "avatar_scholar" in pic:
            continue

        path_result = os.path.join(util.PATH_DIR_RESULT, "img", "%s_%s.jpg") % (file_name, str(id))
        pic = "https://scholar.google.com" + pic if pic[0] is "/" else pic

        data = None
        max_tries = 0
        while data is None and max_tries < 6:
            try:
                data = scholar._get_page_content(pic)
                break
            except Exception as e:
                max_tries += 1
                logger.error("%s | %d | %s | trries: %d" % (file_name, int(id), str(e), max_tries))
                time.sleep(max_tries)
                data = None

        if data is None:
            continue

        logger.info("Save img %s" % path_result)
        with open(path_result, "wb") as f:
            f.write(data)
