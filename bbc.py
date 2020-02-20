import ssl
import urllib.request
from newspaper import Article
import time
ssl._create_default_https_context = ssl._create_unverified_context

url_='https://www.bbc.co.uk/search/more?page='
page_index=2
while 1:
    url=url_+str(page_index)+'&pos=2&q=a&filter=news&suggid='
    page_index+=1
    try:
        a = urllib.request.urlopen(url)
        html = a.read()
        html = html.decode("utf-8")
        oper=""
        for i in html:
            if not i==' ':
                oper+=i
        html_lis=oper.split('\n')
        for i in html_lis:
            if i[:23]=='<h1itemprop=\"headline\">':
                temp_lis=i.split('\"')
                myurl=temp_lis[3]
                print(myurl)
                try:
                    article = Article(myurl)
                    article.download()
                    article.parse()
                    time.sleep(1)
                    text = article.text

                    text_lis = text.split('\n')
                    text = ''
                    for sentence in text_lis:
                        if len(sentence) > 1:
                            sentence.strip('\n')
                            text += sentence + ' '
                    text.strip(' ')
                    if text[:5]=='Video':
                        print('video')
                        break
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
    except Exception as e:
        print(e)
