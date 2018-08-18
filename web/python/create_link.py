import os


# 创建模型的硬链接到当前文件夹下
if __name__ == "__main__":
    try:
        os.makedirs("models")
    except BaseException:
        pass
    
    for fn in os.listdir('../../text_classification/models/'):
        os.link('../../text_classification/models/' + fn, './models/' + fn)