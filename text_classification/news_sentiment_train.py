from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import sys
sys.path.append('../')
from config.functions import *

category_config = get_news_sentiment_config()

# 提取人工标注好的 dataset 文件夹下的数据集
def get_dataset_bunch():

    # 训练集路径
    train_data_path = category_config["load_files_path"]
    # 训练集对应的标签
    categories = category_config["categories"]

    train_data = load_files(train_data_path,categories=categories)

    return train_data

# 建立 tfidf 模型 作为朴素贝叶斯训练器的输入
def build_tfidf_model(train_data):

    # 单词计数
    stopword_list = read_file("./hlt_stop_words.txt").splitlines()
    count_vect = CountVectorizer(stop_words=stopword_list,max_df=0.5)
    X_train_counts = count_vect.fit_transform(train_data.data)

    print("训练数据共有{0}篇,词汇计数为{1}个".format(X_train_counts.shape[0],X_train_counts.shape[1]))
    print("'海事'出现的次数为:{0}".format(count_vect.vocabulary_.get('海事')))

    # 建立 tfidf 提取文本特征

    #TF-IDF提取文本特征
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    print(X_train_tfidf.shape)

    # 保存模型
    write_bunch_obj(category_config["count_vect_path"], count_vect)
    write_bunch_obj(category_config["tfidf_path"], tfidf_transformer)
    print("计数模型、TFIDF模型 保存完毕……")

    return X_train_tfidf


def train_news_sentiment_model(X_train_tfidf,train_data):

    clf = MultinomialNB(alpha=0.01)
    clf = clf.fit(X_train_tfidf,train_data.target)
    print("分类器训练完毕")
    joblib.dump(clf, category_config["save_model_path"])
    print("训练模型保存成功")

    return clf


def predict_news_sentiment(text):

    count_vetc_path = category_config["count_vect_path"]
    tfidf_path = category_config["tfidf_path"]

    # 训练集对应的标签
    categories = category_config["categories"]

    news_sentiment_tfidf = get_tfidf_model([text],count_vect_path=count_vetc_path,tfidf_path=tfidf_path)

    clf = joblib.load(category_config["save_model_path"])
    result = clf.predict(news_sentiment_tfidf)

    predicted_result = categories[result[0]]

    return predicted_result


def predict_news_sentiment_proba(text):

    count_vetc_path = category_config["count_vect_path"]
    tfidf_path = category_config["tfidf_path"]

    # 训练集对应的标签
    categories = category_config["categories"]

    news_sentiment_tfidf = get_tfidf_model([text],count_vect_path=count_vetc_path,tfidf_path=tfidf_path)

    clf = joblib.load(category_config["save_model_path"])
    result = clf.predict_proba(news_sentiment_tfidf)

    return result



if __name__ == '__main__':

    # print("开始训练模型")

    # train_data = get_dataset_bunch()
    # X_train_tfidf = build_tfidf_model(train_data)
    # clf = train_news_sentiment_model(X_train_tfidf,train_data)

    result = predict_news_sentiment("考生作弊被开除学籍")
    print(result)

    ################################################################
    # # 判断准确率
    ################################################################
    # correct = 0
    # wrong = 0

    # dirname = "dataset_test/news_sentiment_dataset/"
    # for d2 in os.listdir(dirname):
    #     d2 = dirname + d2 + "/"
    #     for sub_file in os.listdir(d2):
    #         sub_file = d2 + sub_file
    #         with open(sub_file, "r") as f:
    #             line = f.readline().strip().replace(" ", "")
    #             res = predict_news_sentiment(line)
    #             real_res = ""
    #             for category in ["/-1", "/0", "/1"]:
    #                 if category in d2:
    #                     real_res = category
    #                     break
    #             print(predict_news_sentiment_proba(line))
    #             print("real=" + real_res + "," + "res=" + res)
    #             if res in real_res:
    #                 correct += 1
    #             else:
    #                 wrong += 1
    # print(correct/(correct+wrong))
    ################################################################


