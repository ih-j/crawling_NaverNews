import re
import requests
from bs4 import BeautifulSoup
import datetime

keyword     = "학교"
startDate   = datetime.datetime(2020, 1, 1)
endDate     = datetime.datetime(2021, 6, 1)
outputFileName = "test_crawling_0508_schoolonly_2019.csv"

startPage = 1
maxPageNum  = 4000
increment = 10
browser = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
f = open(outputFileName, "w", encoding="UTF-8")

searchFrom  = startDate
while searchFrom <= endDate:
    print(searchFrom)
    # searchTo    = searchFrom + datetime.timedelta(days=7)
    searchTo    = searchFrom + datetime.timedelta(weeks=4)
    # browser = {'User-Agent':'Mozilla/5.0'}

    for n in range(startPage, maxPageNum, increment):
        print(n)
        try:
            # raw = requests.get("https://search.naver.com/search.naver?where=news&query="+keyword+"&start="+str(n),
            #                    headers=browser)
            raw = requests.get("https://search.naver.com/search.naver?where=news&query="+keyword+"&ds="+searchFrom.strftime("%Y.%m.%d")+"&de="+searchTo.strftime("%Y.%m.%d")+"&nso=so:r,p:from"+searchFrom.strftime("%Y%m%d")+"to"+searchTo.strftime("%Y%m%d")+",a:all&start="+str(n),
                               headers=browser)
            # print("https://search.naver.com/search.naver?where=news&query="+keyword+"&ds="+searchFrom.strftime("%Y.%m.%d")+"&de="+searchTo.strftime("%Y.%m.%d")+"&nso=so:r,p:from"+searchFrom.strftime("%Y%m%d")+"to"+searchTo.strftime("%Y%m%d")+",a:all&start="+str(n))
            html = BeautifulSoup(raw.text, "html.parser")

            articles = html.select("ul.list_news > li")

            for ar in articles:
                # title = ar.select_one("a.news_tit")
                # titleText = re.sub('[^a-zA-Z0-9가-힣_]', ' ', title.text)
                # print(title.text)
                for tag in ar.find_all(string=re.compile("네이버뉴스")):
                    url = tag.parent.attrs["href"]
                    # print(url)
                    try:
                        raw_each = requests.get(url, headers=browser)
                        html_each = BeautifulSoup(raw_each.text, 'html.parser')
                        title = html_each.select_one("div.article_info > h3")
                        if title is None:
                                continue
                            # title = html_each.select_one("div.end_ct_area > h2")
                        titleText = re.sub('[^a-zA-Z0-9가-힣_]', ' ', title.text)

                        pubDate = html_each.select_one("span.t11")
                        # if pubDate is None:
                            # pubDate = html_each.select_one("span.author > em")
                        pubDateText = pubDate.text
                        # print(pubDateText+", "+titleText)
                        f.write(pubDateText+", "+titleText+",")
                        bodies = html_each.select("div._article_body_contents")
                        for body in bodies:
                            body.script.extract()
                            # print(body.script)
                            bodyText = re.sub('[^a-zA-Z0-9가-힣_]', ' ', body.text)
                            # print(bodyText)
                            f.write(bodyText)
                        f.write('\n')
                    except:
                        print('Error :'+url)
        except:
            print('Error on page#:'+str(n//increment))
    searchFrom = searchTo + datetime.timedelta(days=1)

f.close()