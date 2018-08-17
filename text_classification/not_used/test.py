import numpy as np
import jieba
import pandas as pd
import os



# def generate_words()
#     words = []
#     numbers = []
#     with open('sgns.sogounews.bigram-char', "r") as f:
#         print(f.readline())
#         for line in f:
#             line = line.split(" ")
#             words.append(line[0])

#     with open("words.txt", "w") as f:
#         for i in range(len(words)):
#             f.write(words[i])
#             f.write("\n")


# def generate_300d():
#     lines = []
#     with open('sgns.sogounews.bigram-char', "r") as f:
#         f.readline()
#         for line in f:
#             line = line.split(" ")
#             line = line[1:-1]
#             lines.append(line)
#     print("finish read")
#     with open('300d.txt', "w") as f:
#         for line in lines:
#             for e in line:
#                 f.write(e)
#                 f.write(" ")
#             f.write("\n")


def add_words_to_jieba():
    with open("words.txt", "r") as f:
        for line in f:
            jieba.add_word(line[:-1])


def reset_data(file_name):
    tmp = ""
    with open(file_name, "r") as f:
        tmp = f.readline()
        tmp = tmp.replace(" ", "")
    
    with open(file_name, "w") as f:
        f.write(tmp)


def jieba_cut(file_name):
    tmp = None
    with open(file_name, "r") as f:
        tmp = f.readline()
        tmp = [i for i in jieba.cut(tmp)]
    
    with open(file_name, "w") as f:
        for t in tmp:
            f.write(t)
            f.write(" ")


def rebuild_category_data():

    main_file = open("category_data.txt", "w")

    index_to_word = []
    word_to_index = {}
    with open("words.txt") as words_file:
        for word in words_file:
            word = word[:-1]
            word_to_index[word] = len(index_to_word)
            index_to_word.append(word)

    dirname = "dataset/news_category_dataset/"
    for d2 in os.listdir(dirname):
        d2 = dirname + d2 + "/"
        print("finish" + d2)
        for sub_file in os.listdir(d2):
            sub_file = d2 + sub_file
            with open(sub_file, "r") as f:
                line = f.readline().split(" ")


def get_word_and_index():
    index_to_word = []
    word_to_index = {}
    with open("words.txt") as f:
        for word in f:
            word = word[:-1]
            word_to_index[word] = len(index_to_word)
            index_to_word.append(word)
    return (index_to_word, word_to_index)


def get_embedding_matrix():
    a = pd.read_csv("300d.txt", sep=" ", header=None, usecols=[i for i in range(300)])
    return a.values


def get_stop_words():
    stop_words = set()

    with open("hlt_stop_words.txt", "r") as f:
        for line in f:
            line = line[:-1].split(" ")
            stop_words.add(line[0])
        stop_words.add("\n")

    return stop_words



def save_category_data(one_data, dir_name, target_name):
    y = 0
    for category in ["activity", "entrance", "social", "study"]:
        if category in dir_name:
            switch_category = {
                "activity": 0,
                "entrance": 1,
                "social": 2,
                "study": 3
            }
            y = switch_category[category]
            break

    with open("new_dataset/category_data_" + target_name + ".txt", "a") as f:
        f.write(str(y))
        i = 0
        for word in one_data:
            word = word.strip()
            f.write(" ")
            f.write(str(word))
            i += 1
            if (i>=500): break
        f.write("\n")


def save_sentiment_data(one_data, dir_name, target_name):
    y = 0
    for category in ["/-1", "/0", "/1"]:
        if category in dir_name:
            switch_category = {
                "/-1": 2,
                "/0": 0,
                "/1": 1,
            }
            y = switch_category[category]
            break

    with open("new_dataset/sentiment_data_" + target_name + ".txt", "a") as f:
        f.write(str(y))
        i = 0
        for word in one_data:
            word = word.strip()
            f.write(" ")
            f.write(str(word))
            i += 1
            if (i>=500): break
        f.write("\n")
            

        



if __name__ == "__main__":

    ##############################
    ### 重新分词
    ##############################
    # add_words_to_jieba()
    # print("finish add words")

    # main_dirname = "dataset/"

    # for dirname in os.listdir(main_dirname):
    #     dirname = main_dirname + dirname + "/"
    #     for d2 in os.listdir(dirname):
    #         d2 = dirname + d2 + "/"
    #         print("finish" + d2)
    #         for f in os.listdir(d2):
    #             f = d2 + f
    #             reset_data(f)
    #             jieba_cut(f)
    ##############################
    ### end 重新分词
    ##############################




    # line = list(filter(lambda a: a != word, line))

    # (index_to_word, word_to_index) = get_word_and_index()

    # stop_words = get_stop_words()

    # dirname = "dataset/news_category_dataset/"
    # for d2 in os.listdir(dirname):
    #     d2 = dirname + d2 + "/"
    #     for sub_file in os.listdir(d2):
    #         sub_file = d2 + sub_file
    #         with open(sub_file, "r") as f:
    #             line = f.readline().strip().split(" ")
    #             new_line = []
    #             for word in line:
    #                 if word not in stop_words:
    #                     new_line.append(word)

    #             encoded_line = []
    #             for word in new_line:
    #                 tmp = word_to_index.get(word)
    #                 if tmp is not None:
    #                     encoded_line.append(tmp)
    #             save_category_data(encoded_line, d2)

    # with open("new_dataset/category_data.txt", "r") as f:
    #     length = []
    #     for line in f:
    #         line = line.split(" ")
    #         length.append(len(line))
    #     print(sum(length)/len(length))




    # from tensorflow.keras.preprocessing.text import Tokenizer

    # title = None
    # dirname = "dataset/news_category_dataset/"
    # for d2 in os.listdir(dirname):
    #     d2 = dirname + d2 + "/"
    #     for sub_file in os.listdir(d2):
    #         sub_file = d2 + sub_file
    #         with open(sub_file, "r") as f:
    #             title = f.readline().strip().split(" ")
    #     break
                
    # tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~，。、？《》【】『』·！…￥\t\n',lower=True,split=" ")
    # tokenizer.fit_on_texts([['我是谁', '我在哪儿'],['道格斯奶茶', '有只道格']])
    # print(tokenizer.word_index)





    # def create_ngram(sent, ngram_value):
    #     print([sent[i:] for i in range(ngram_value)])
    #     for k, v in enumerate(set(zip(*[sent[i:] for i in range(ngram_value)]))):
    #         print(k)
    #         print(v)
    #     return set(zip(*[sent[i:] for i in range(ngram_value)]))

    # print(create_ngram("哈士奇哈萨基", 4))




    # from tensorflow.keras.preprocessing.sequence import pad_sequences
    # print(pad_sequences([[123,4,533,53], [123,43,14]], maxlen=10))





    stop_words = get_stop_words()

    dirname = "dataset/news_sentiment_dataset/"
    for d2 in os.listdir(dirname):
        d2 = dirname + d2 + "/"
        for sub_file in os.listdir(d2):
            new_line = []
            for word in jieba.cut(sub_file[:-4]):
                new_line.append(word)
            sub_file = d2 + sub_file
            with open(sub_file, "r") as f:
                line = f.readline().strip().split(" ")
                for word in line:
                    if word not in stop_words:
                        new_line.append(word)

                save_sentiment_data(new_line, d2, "train")