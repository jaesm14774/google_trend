# google_trend

## 目標

* https://trends.google.com/trends/trendingsearches/daily?<geo=TW>
  * geo:地理位置，可以更改國家縮寫代碼變成他國熱門搜尋關鍵字

* 收集當日最熱門的搜索趨勢，作為輿情判別依據

* :star: 可做為新字更新，高品質關鍵字字典做使用，能應對日新月異的創新字與事件名

最早可以追朔1個月前，需提早佈署，累積資料

### 注意

* 需要更改configure檔中mysql的資訊與configure的路徑位置，可參考additional_file中的sql_config.txt範例檔

* 想要抓取其他日期，可以更改main裡面的now，或是單抓取search_date function做使用
