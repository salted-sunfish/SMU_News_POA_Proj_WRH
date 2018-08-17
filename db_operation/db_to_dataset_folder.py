'''
    手动分拣数据时使用的程序
'''


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database_dict_info
from pymongo import MongoClient
import jieba
import re
import os



def db_to_dataset_folder():
    db_config = get_database_dict_info()
    conn = MongoClient(db_config["host"],db_config["port"])
    NewsPOA = conn.NewsPOA

    dataset = NewsPOA["newslist"].find(
        { 
            "$or": [ 
                { "body": { "$regex": ".*学术论坛.*" } }
            ],
        }
    )

    to_filt = "/,.<》；：‘\"[]\{\}-_=+!~`@#$%^&*()"
    for data in dataset:
        data_title = data["title"]
        data_body = data["body"]
        for c in to_filt:
            data_title = data_title.replace(c, "")
            data_body = data_body.replace(c, "")
        with open(
            "../text_classification/dataset/news_category_dataset/"
            + data_title + ".txt", "w"
        ) as f:
            data_to_save = []
            data_to_save.extend(jieba.cut(data_title))
            data_to_save.extend(jieba.cut(data_body))
            for item in data_to_save:
                if (item == "\n"):
                    continue
                f.write(item)
                f.write(" ")


def test():
    path = os.path.dirname(os.path.abspath(""))
    path += "/text_classification/dataset/news_category_dataset/"
    for f in os.listdir(path):
        if "论坛" in f:
            os.rename(path+f, path + "study/" + f)
            print("233")


if __name__ == "__main__":
    # db_to_dataset_folder()
    # test()