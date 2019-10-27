from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import math

movie_score_url_base = 'https://movie.naver.com'
movie_score_url_sub = '/movie/bi/mi/pointWriteFormList.nhn?code=163788&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page='
movie_score_url_sub_num = '1'

movie_score_url = movie_score_url_base + movie_score_url_sub
#print(movie_score_url)

movie_score_html = urlopen(movie_score_url+ movie_score_url_sub_num)
movie_score_soup = BeautifulSoup(movie_score_html, "html.parser")
#print(movie_score_soup)

# 전체 건수 구하기
score_total = movie_score_soup.find(class_='score_total')
#print(type(score_total))

score_em_num = (score_total.find('em').getText()).replace(',', '').strip()
#print('score_em_num = \''+score_em_num+'\'')

# row 추출하기
# body > div > div > div.score_result > ul > li:nth-child(1) >
score_result_div = movie_score_soup.find(class_='score_result')
#print(score_result_div)
score_result_ul = score_result_div.find('ul')
score_result_lis = score_result_ul.findAll('li');

score_result = []
score_date = []
good_score = []

# roof 횟수 구하기
score_count = math.ceil(int(score_em_num) / 10)

# 전체 구하기, 1부터 시작해서 1 더해줌
for i in range(1,score_count+1) :
#for i in range(1,3) :

    #print(movie_score_url + str(i))
    movie_score_html_page = urlopen(movie_score_url + str(i))
    movie_score_soup_page = BeautifulSoup(movie_score_html_page, "html.parser")

    score_result_div = movie_score_soup_page.find(class_='score_result')
    # print(score_result_div)
    score_result_ul = score_result_div.find('ul')
    score_result_lis = score_result_ul.findAll('li');

    for score_result_li in score_result_lis:
        # 평점
        # body > div > div > div.score_result > ul > li:nth-child(1) > div.star_score > em
        star_score_div = score_result_li.find(class_='star_score')
        score_result.append(star_score_div.find('em').getText())

        # 날짜
        # body > div > div > div.score_result > ul > li:nth-child(1) > div.score_reple > dl > dt > em:nth-child(2)
        score_reple_div = score_result_li.find(class_='score_reple')
        score_date.append(score_reple_div.findAll('em')[1].getText())

        # 공감수
        # body > div > div > div.score_result > ul > li: nth - child(1) > div.btn_area > a._sympathyButton
        btn_area_div = score_result_li.find(class_='btn_area')
        btn_area_a = btn_area_div.find('a')
        good_score.append(btn_area_a.find('strong').getText())

#print(score_result)
#print(score_date)
#print(good_score)

movie_data = {'score':score_result, 'date':score_date, 'good':good_score}
movie_df = pd.DataFrame(movie_data)
#print(movie_df.head())

# 컬럼 순서 변경
movie_df = pd.DataFrame(movie_data, columns=['score','date','good'])

movie_df.to_csv('data/naver_movie_score_01.csv', sep=',', encoding='UTF-8')
