# SMU_News_POA_Proj_WRH

大概做了这几件事情:
1. 增加了"public/report_page.html"中的四个柱状图(针对一个媒体而言,其报道的各学校新闻数).
2. 把收尾导航栏放到了一起(写在"public/nav_top.html"和"public/nav_bottom.html").
3. 增加两个接口:
    (1)"/api/medias"(返回一个数组,包含了"所有报道数大于10的媒体名称"以及"其报道的新闻总数");
    (2)"/api/universityrank"(返回某个媒体对各个学校的新闻报道数,必填参数"media"指定某个媒体,可选参数"sentiment"(不填表示查询所有可能情况)和"limit").
4. 可能还有某些小地方改过...........


2018-8-17更新：
1. 数据库NewsPOA的newslist增加到62651条.
2. 增加自学习功能，启动文件为text_classification/prediict_in_db.py，具体说明如下：
    (1) 首先读取text_classification/dataset中的数据，然后对newslist中的数据进行预测，可自行设定阈值，但预测结果大于阈值时，认为该结果是正确的，并在数据库中标记；在下一轮预测中，把text_classification/dataset以及数据库中“已经标记的数据”作为训练集，继续预测未标记的数据.
    (2) 目前以0.99的阈值运行了3轮，sentiment方面比较理想(负面3380条，中性20701，正面14902)，但是category方面，绝大部分都被分成了social（socal有50584，entrance有6240，activity有36，study为0）（不过category的分类让人分也不太好分,并且阈值设的比较高，而study本身数据就少，所以产生了这种结果，可以适当调整阈值增加结果）.
3. text_classification/news_category_train.py 和 text_classification/news_sentiment_train.py中增加了在dataset_test上的测试（不过由于目前数据便多了，每预测一条数据都要读取一次tfidf模型，所以预测很慢，有时间我再改改）.
4. 然后还有一些小细节的地方作了修改。。。也不是很记得了，应该不重要
5. text_classification/not_used文件夹 存放了一些不用的东西，但是我想放着，也许以后要参考.
6. 模型(text_classification/models)和数据(text_classification/dataset以及text_classification/dataset_test)太大了，我就先删了.