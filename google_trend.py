import requests
import re
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import json
import pymysql
import MySQLdb
from sqlalchemy import create_engine

#read total file path
path=pd.read_csv('/self_project/google_trend/configure.csv',encoding='utf_8_sig',index_col='name')
#read sql configure path
path=pd.read_csv(path.loc['sql_configure_path','value'],encoding='utf_8_sig',index_col='name')

def search_date(date):
    a=requests.get('https://trends.google.com/trends/api/dailytrends?hl=zh-TW&tz=-480&ed={}&geo=TW&ns=15'.format(date),
                  headers={
                      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                      'referer': 'https://trends.google.com/trends/trendingsearches/daily?geo=TW',
                      'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                  })
    temp=json.loads(re.sub(r'\)\]\}\',\n', '', a.text))
    title=[s['title']['query'] for s in temp['default']['trendingSearchesDays'][0]['trendingSearches']]
    query_number=[s['formattedTraffic'] for s in temp['default']['trendingSearchesDays'][0]['trendingSearches']]
    related_query=[';'.join([j['query'] for j in s['relatedQueries']]) for s in temp['default']['trendingSearchesDays'][0]['trendingSearches']]
    return pd.DataFrame({
        'create_time':format(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'),
        'created_at':date,
        'keyword':title,
        'hot_level':query_number,
        'related_keyword':related_query
    })


# In[ ]:


def get_sql(host,port,user,password,db_name):
    conn=pymysql.connect(host=host,
               port=int(port),
               user=user,
               password=password,
               db=db_name)
    cursor=conn.cursor()
    engine = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8mb4' %
                  (user,password,
                   host,port,db_name))
    return (conn,cursor,engine)


# In[ ]:


def main():
    conn,cursor,engine=get_sql(path.loc['ip','value'],path.loc['port','value'],path.loc['user','value'],
                               path.loc['password','value'],'google')    
    
    now=format(datetime.datetime.now(),'%Y%m%d')
    #判斷有沒有daily_word(google_daily_trend)表格
    temp=pd.read_sql_query('show tables',engine)
    if 'daily_word' not in temp['Tables_in_google'].tolist():
        cursor.execute('create table daily_word(wid int auto_increment not null,create_time datetime,created_at datetime,keyword varchar(255),hot_level varchar(255),related_keyword longtext,primary key(wid));')
        conn.commit()
    #開始爬google daily trend
    dat=search_date(now)
    for i in range(0,dat.shape[0]):
        try:
            dat.iloc[[i],:].to_sql('daily_word',engine,if_exists='append',index=0)
        except:
            pass
 
    conn.close() #關閉資料庫


# In[ ]:


if __name__ == '__main__':
    main()


