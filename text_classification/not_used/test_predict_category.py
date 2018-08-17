import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense, Dropout, LSTM
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import optimizers
import numpy as np



ngram = 2
max_features = 0
num_labels = 4


def read_data(target_name):
    X = []
    Y = []
    with open("new_dataset/category_data_" + target_name + ".txt", "r") as f:
        for one_data in f:
            one_data = one_data[:-1].split(" ")
            Y.append(one_data[0])
            X_one = []
            for i in range(1, len(one_data)):
                X_one.append(one_data[i])
                if (i == 499): break
            X.append(X_one)
    return (X, Y)
        
        
def get_fitted_tokenizer(X):
    tokenizer = Tokenizer(
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~，。、？《》【】『』·！…￥\t\n',
        lower=True,split=" "
    )
    tokenizer.fit_on_texts(X)
    return tokenizer


def create_ngram(one_data, ngram_value):
	return set(zip(*[one_data[i:] for i in range(ngram_value)]))


def add_ngram(sequences, token_indice, ngram_range):
    new_sequences = []
    for sent in sequences:
        new_list = sent[:]
        for i in range(len(new_list) - ngram_range + 1):
            for ngram_value in range(2, ngram_range + 1):
                ngram = tuple(new_list[i:i + ngram_value])
                if ngram in token_indice:
                    new_list.append(token_indice[ngram])
        new_sequences.append(new_list)
    return new_sequences


def get_preprocessed_data(target_name):
    (X, Y) = read_data(target_name)
    tokenizer = get_fitted_tokenizer(X)

    X = tokenizer.texts_to_sequences(X)

    ngram_set = set()
    for one_data in X:
        for i in range(ngram, ngram+1):
            set_of_ngram = create_ngram(one_data, i)
            ngram_set.update(set_of_ngram)

    word_to_index = tokenizer.word_index

    start_index = len(word_to_index) + 2
    token_indice = {v: k + start_index for k, v in enumerate(ngram_set)} # 给n-gram词汇编码
    indice_token = {token_indice[v]: v for v in token_indice}
    max_features = np.max(list(indice_token.keys())) + 1

    X = add_ngram(X, token_indice, ngram)
    X = pad_sequences(X, maxlen=500)
    
    Y = tensorflow.keras.utils.to_categorical(Y, num_classes=4)

    return (X, Y, max_features)
    # return (X, Y, len(list(tokenizer.word_index))+1)

    


def build_fastText_model(max_features):
    model = Sequential()
    model.add(Embedding(input_dim=max_features, output_dim=50, input_length=500))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(num_labels, activation='softmax'))
    sgd = optimizers.SGD(lr=0.01)
    model.compile(
        loss='categorical_crossentropy', 
        optimizer=sgd, metrics=['accuracy']
    )

    # model = Sequential()
    # model.add(Embedding(input_dim=10000, output_dim=50))
    # model.add(LSTM(128))
    # model.add(Dropout(0.2))
    # model.add(Dense(4, activation='softmax'))

    # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    # model.compile(loss='categorical_crossentropy',
    #             optimizer=sgd,
    #             metrics=['accuracy'])
    return model



if __name__ == "__main__":
    (X_test, Y_test, max_features) = get_preprocessed_data("test")
    (X_train, Y_train, max_features) = get_preprocessed_data("train")
    model = build_fastText_model(max_features)
    model.fit(
        X_train, Y_train, 
        batch_size=1877, epochs=30,
        validation_data=(X_test, Y_test)
    )
    print(model.summary())
    print(model.predict(X_test))
