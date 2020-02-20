import requests
import random
import json
import time
from newspaper import Article

USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
]

Cookie = "tt_webid=6794325502510581254; __tea_sdk__user_unique_id=6794325502510581254; __tea_sdk__ssid=67815ef4-081e-410d-bd74-0f7a866f69dc; csrf-token=a8c8931a3c12944e61d7395b05158d118582c444; csrf-secret=M3coVxF3NEHLZMnf7JmQXt6W22i71dQJ"
valid_char=['1','2','3','4','5','6','7','8','9','0',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n',
            'o','p','q','r','s','t','u','v','w','x','y','z']
while 1:
    url = 'https://www.topbuzz.com/pgc/feed?content_space=bd&language=en&region=us&user_id=6794325502510581254&channel_name=foryou&classification=all&min_behot_time='+str(time.time())
    headers = {                                     
        'User-agent': random.choice(USER_AGENTS),  
        'Cookie': Cookie,
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.topbuzz.com',
        'Referer': 'https://www.topbuzz.com/'
    }
    data = {}


    req = requests.get(url, data=data, headers=headers).json()
    oper=req['data']['feed']['items']
    for i in oper:
        myurl='https://www.topbuzz.com/@'
        source=i['source']
        source = source.lower()
        title=i['title']
        title=title.lower()
        item_sid=i['item_sid']

        source_adj=''
        for x in source:
            if x in valid_char:
                source_adj+=x
        # title似乎没有用 可以不加
        title_adj = ''
        word_lis=title.split(' ')
        for x in word_lis:
            tempx=''
            for j in x:
                if j in valid_char:
                    tempx+=j
            title_adj+=tempx+'-'

        myurl=myurl+source_adj+'/'+title_adj+item_sid+'?referer=foryou'
        for cnt in range(5):
            try:
                article = Article(myurl)
                article.download()
                article.parse()
                time.sleep(2)
                text=article.text
                text_lis=text.split('\n')
                text=''
                for sentence in text_lis:
                    if len(sentence)>1:
                        sentence.strip('\n')
                        text+=sentence+' '
                text.strip(' ')
                print(article.title)
                if len(text) and len(article.title):
                    f = open("", 'a+')
                    f.write("{\"text\":\"")
                    f.write(text)
                    f.write("\",\"title\":\"")
                    f.write(article.title)
                    f.write("\",\"url\":\"")
                    f.write(article.url)
                    f.write("\"},\n")
                    f.close()
                break
            except Exception as e:
                print(e)


    time.sleep(2)
