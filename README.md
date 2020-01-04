# NSR (小說故事推薦系統架構) 以天龍八部作為範例

Novel Story Recommendation System

## NSCrawler (爬蟲)

* Scrapy (本研究使用工具，適用於小型資料開發與測試目的。學習難度：簡單。)
* Scrapy-Redis (適用於小型資料，同一個網站進行多次且不同目的之爬取，如：爬取 A 分類存到 A Collection、B 分類存到 B Collection。學習難度：簡單。)
* Scrapy-Redis-Cluster (適用於中型資料，多個網站進行多次且不同目的之爬取，但因架構較為簡單，所以不適合作為多個大網站或深度太高網站的工具。學習難度：中等。)
* Scrapy-Cluster (適用於大型資料，多個網站進行多次且不同目的之爬取。學習難度：困難。)

### Common

* settings.py：設定自動挑選 USER AGENT、遵循 robots.txt 規則、禁止遠端連線以及 Cookies

#### 將資料匯入MongoDB

* items.py： 設定 MongoDB 中 Collection 專屬的 id 欄位以及選擇要將資料匯入哪一個 Collection 的 Collection 欄位。
* pipelines.py：完成 MongoDB 的連線設定以及爬取到資料後需要對資料做什麼動作，如：Insert、Delete、Update。
* settings.py：開啟 Pipeline 設定以及設定 Mongo 的環境變數，如：連線字串以及連接資料庫。

### BFS

### DFS

* items.py：設定三種資料格式 Class、Object、Content，Class 用於儲存網站目錄架構，此例為：龍騰世紀/武俠小說/作者/書名；Object 用於儲存各書的章回；Content 則是用於儲存各書章回的內容。
* settings.py：設定使用 DFS 演算法 (DEPTH_PRIORITY = 1)、併發總數 (CONCURRENT_REQUESTS = 32)、網域最大爬取深度 (DOMAIN_DEPTHS = {'example.com': 4})
* Content.py：撰寫爬蟲，共四個，主要用到的兩個爬蟲為 AuthorSpider 以及 ChapterSpider。AuthorSpider 用來爬取網站架構，完成後會送到 Pipeline 並儲存於 MongoDB 的 Class Collection；ChapterSpider則是爬取各書的章回名稱以及內容，爬取會一樣送至 Pipeline 並儲存於 MongoDB，章回名稱儲存於 Object Collection；內容儲存於 Content Collection。由於利於 Debug 因此才將兩隻爬蟲分開來寫。

### 資料來源

* 基本書籍資訊：[博客來網路書店](https://www.books.com.tw/products/0010218098)
* 書籍內容：[龍騰世紀書庫](http://www.bwsk.net/wx/j/jingyong/tlbb/index.html)
* 相關作品：[維基百科](https://zh.wikipedia.org/wiki/%E5%A4%A9%E9%BE%99%E5%85%AB%E9%83%A8_(%E5%B0%8F%E8%AF%B4))

## NSFront (前端)

## NSAPI (API 端)

## NSBackend (後端)

### Mongo 端

### Postgres 端

## NSAI (資料分析端)

## NSVis (視覺化端)
