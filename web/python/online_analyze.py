import sys
import os
web_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
main_folder = os.path.dirname(web_folder)
sys.path.append(web_folder)
sys.path.append(main_folder)

from config.functions import *
from sklearn.externals import joblib
import socket
import json



def read_file(path):

    f = open(path,"r",encoding="utf-8")
    content = f.read()
    f.close()
    return content



if __name__ == "__main__":

    sentiment_config = get_news_sentiment_config()
    category_config = get_news_category_config()

    sentiment_count_vect = read_bunch_obj(sentiment_config["count_vect_path"])
    sentiment_tfidf_transformer = read_bunch_obj(sentiment_config["tfidf_path"])
    sentiment_clf = joblib.load(sentiment_config["save_model_path"])

    category_count_vect = read_bunch_obj(category_config["count_vect_path"])
    category_tfidf_transformer = read_bunch_obj(category_config["tfidf_path"])
    category_clf = joblib.load(category_config["save_model_path"])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 8484))
    sock.listen(20)

    print("socket on!")

    while True:

        connection, client_address = sock.accept()

        text = connection.recv(4096).decode('utf-8')
        text = seg_chinese_text(text)

        news_sentiment_counts = sentiment_count_vect.transform([text])
        news_sentiment_tfidf = sentiment_tfidf_transformer.transform(news_sentiment_counts)
        sentiment_result = sentiment_clf.predict(news_sentiment_tfidf)

        news_category_counts = category_count_vect.transform([text])
        news_category_tfidf = category_tfidf_transformer.transform(news_category_counts)
        category_result = category_clf.predict(news_category_tfidf)


        analyze_result = {
            "sentiment": sentiment_config["categories"][sentiment_result[0]],
            "classification": category_config["categories"][category_result[0]]
        }

        connection.send(json.dumps(analyze_result).encode("utf-8"))
        
        connection.close()