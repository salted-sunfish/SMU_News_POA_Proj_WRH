import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.datasets import load_files
from config.database import get_database_dict_info
from pymongo import MongoClient
from config.functions import *
from text_classification import news_sentiment_train as nst
from text_classification import news_category_train as nct
import jieba



target_to_index = {
    "sentiment": {
        "-1": 0,
        "0": 1,
        "1": 2
    },
    "category": {
        "activity": 0,
        "entrance": 1,
        "social": 2,
        "study": 3
    }
}


def text_clean(text):
    for _str in ["\n", " ", "\t", "\r"]:
        text = text.replace(_str, "").strip()
    return text


def get_newslist():
    db_config = get_database_dict_info()
    conn = MongoClient(db_config["host"],db_config["port"])
    NewsPOA = conn.NewsPOA
    newslist = NewsPOA["newslist"]
    return newslist


def get_train_data(target="sentiment"):
    if target == "sentiment":
        category_config = get_news_sentiment_config()
    else:
        category_config = get_news_category_config()

    train_data_path = category_config["load_files_path"]
    categories = category_config["categories"]
    train_data = load_files(train_data_path,categories=categories)

    newslist = get_newslist()

    dataset = newslist.find({target: {"$ne": None}})

    train_data["filenames"] = list(train_data["filenames"])
    train_data["target"] = list(train_data["target"])
    
    for data in dataset:
        train_data["data"].append(
            text_clean(data["title"]) + " " 
            + text_clean(data["body"])
        )
        train_data["filenames"].append(str(data["_id"]))
        train_data["target"].append(target_to_index[target][data[target]])
        
    
    return train_data


def save_and_get_model(target="sentiment"):
    train_data = get_train_data(target)
    if target == "sentiment":
        X_train_tfidf = nst.build_tfidf_model(train_data)
        clf = nst.train_news_sentiment_model(X_train_tfidf,train_data)
    else:
        X_train_tfidf = nct.build_tfidf_model(train_data)
        clf = nct.train_news_category_model(X_train_tfidf,train_data)
    return clf


def predict_in_db(target="sentiment", threshold=0.99):
    if target == "sentiment":
        category_config = get_news_sentiment_config()
    else:
        category_config = get_news_category_config()

    newslist = get_newslist()
    dataset = newslist.find({target: None})

    count_vetc_path = category_config["count_vect_path"]
    tfidf_path = category_config["tfidf_path"]

    clf = save_and_get_model(target)

    data_to_predict = []
    ids = []
    i = 0
    dataset_size = dataset.count()
    c_all = 0
    for data in dataset:
        data_to_predict.append(
            text_clean(data["title"]) + " " 
            + text_clean(data["body"])
        )
        ids.append(data["_id"])
        i += 1
        c_all += 1
        if (i >= 500):
            i = 0
            c = 0
            tfidf_to_predict = get_tfidf_model(
                data_to_predict, 
                count_vect_path=count_vetc_path,
                tfidf_path=tfidf_path
            )
            predictions = clf.predict_proba(tfidf_to_predict)
            package = zip(predictions, ids)
            for prediction, _id in package:
                for j in range(3):
                    if (prediction[j] > threshold):
                        newslist.update_one(
                            {"_id": _id},
                            {"$set": {target: category_config["categories"][j]}}
                        )
                        c += 1
                        break
            data_to_predict.clear()
            ids.clear()
            print(
                target + "：本轮添加"+ str(c) 
                + "条,已预测" + str(c_all) 
                + "条,共" + str(dataset_size) + "条"
            )

        


if __name__ == "__main__":
    for i in range(100):
        print("第" + str(i) + "轮开始")
        predict_in_db("sentiment", 0.99)
        predict_in_db("category", 0.99)
        print("第" + str(i) + "轮结束")

