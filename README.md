# SMU_News_POA_Proj_WRH

大概做了这几件事情:
1. 增加了"public/report_page.html"中的四个柱状图(针对一个媒体而言,其报道的各学校新闻数).
2. 把收尾导航栏放到了一起(写在"public/nav_top.html"和"public/nav_bottom.html").
3. 增加两个接口:
    (1)"/api/medias"(返回一个数组,包含了"所有报道数大于10的媒体名称"以及"其报道的新闻总数");
    (2)"/api/universityrank"(返回某个媒体对各个学校的新闻报道数,必填参数"media"指定某个媒体,可选参数"sentiment"(不填表示查询所有可能情况)和"limit").
4. 可能还有某些小地方改过...........