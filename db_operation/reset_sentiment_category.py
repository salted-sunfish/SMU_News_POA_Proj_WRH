'''
    清除newslist中的sentiment和category使用的程序
'''

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database_dict_info
from pymongo import MongoClient



def reset_sentiment_category():
    db_config = get_database_dict_info()
    conn = MongoClient(db_config["host"],db_config["port"])
    NewsPOA = conn.NewsPOA

    # dataset = NewsPOA["newslist"].update_many({}, {"$set": {"sentiment": None}})
    # dataset = NewsPOA["newslist"].update_many({}, {"$set": {"category": None}})



if __name__ == "__main__":
    reset_sentiment_category()

