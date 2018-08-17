from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Embedding, LSTM
from tensorflow.keras.optimizers import SGD
import pandas as pd



def get_sentiment_data():
    data = pd.read_csv(
        "new_dataset/sentiment_data.txt", 
        sep=" ", names=range(501),
        engine='python'
    )
    data = data.fillna(0)
    data = data.astype("int32")
    
    return data.values


def get_category_data():
    data = pd.read_csv(
        "new_dataset/category_data.txt", 
        sep=" ", names=range(501),
        engine='python'
    )
    data = data.fillna(0)
    data = data.astype("int32")
    
    return data.values


def train_data():
    embedding_matrix = pd.read_csv(
        "300d.txt", sep=" ", header=None, 
        usecols=[i for i in range(300)]
    ).values

    print(embedding_matrix.shape)

    # # 生成虚拟数据
    # import numpy as np
    # x_train = np.random.random((10000, 20))
    # y_train = keras.utils.to_categorical(np.random.randint(4, size=(10000, 1)), num_classes=4)
    # x_test = np.random.random((10000, 20))
    # y_test = keras.utils.to_categorical(np.random.randint(4, size=(10000, 1)), num_classes=4)

    # 生成数据
    data = get_category_data()
    x_train = data[:, 1:]
    y_train = keras.utils.to_categorical(data[:, 0], num_classes=4)

    model = Sequential()
    model.add(Embedding(
        input_dim=embedding_matrix.shape[0], output_dim=embedding_matrix.shape[1], 
        embeddings_initializer=keras.initializers.Constant(value=embedding_matrix)
    ))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(4, activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
                optimizer=sgd,
                metrics=['accuracy'])

    model.fit(x_train, y_train, batch_size=64, epochs=10)
    # score = model.evaluate(x_test, y_test, batch_size=16)
    


if __name__ == "__main__":
    get_category_data()
