# SideProject02-PersonalBlog
個人獨立小型專案<br>
網址: <a href='http://matt323.pythonanywhere.com/'>http://matt323.pythonanywhere.com/</a> <br>
<img src="https://github.com/r97221004/SideProject02-PersonalBlog/blob/master/PersonalBlog/static/Blog.PNG"></img>
# 介紹
這是我的第二個個人獨立小型專案。在上一個專案個人網站的基礎之下，持續學習新的技術與功能，彙整寫成一個基礎簡單的個人部落格。
個人部落格所用到的技術:
<ul>
  <li>程式語言: Python、SQL、Bash、HTML/CSS</li>
  <li>框架: Flask</li>
  <li>資料庫: MySQL</li>
  <li>版本控制與開發: Docker、Git</li>
  <li>部屬: Pythonanywhere</li>
</ul>
主要包含以下幾個功能點:
<ul>
  <li>使用工廠函數與藍本模塊化實例</li>
  <li>使用富文本编辑器</li>
  <li>文章的新增修改刪除</li>
  <li>文章的分類</li>
  <li>評論的發表與回覆</li>
  <li>Email的發送</li>
  <li>登入登出系統，用戶認證</li>
  <li>後台管理</li>
  <li>虛擬數據的生成</li>
</ul>

# 資料庫的關係圖
<img src="https://github.com/r97221004/SideProject02-PersonalBlog/blob/master/PersonalBlog/static/EM.PNG"></img>

# 使用 docker-compose 啟動
首先 git clone 將程式碼下載到你的電腦且進入 SideProject02-PersonalBlog
```
$ git clone git@github.com:r97221004/SideProject02-PersonalBlog.git
$ cd SideProject02-PersonalBlog
```
建立鏡像
```
docker-compose build
```
拉取鏡像
```
docker-compose pull
```
啟動
```
docker-compose up -d
```
進入 flask 容器的 shell 

```
docker container exec -it sideproject02-personalblog_flask_1 sh
```
建立管理員帳號密碼以及建立虛擬數據
```
flask initdb
flask forge
flask admin
```
打開瀏覽器，輸入 http://127.0.0.1:8001

# 參考資源
<ul>
  <li>Flask 入門教程, 李輝</li>
  <li>Flask Web 開發實戰, 李輝</li>
  <li>Docker容器技術入門到精通, Peng Xiao</li>
</ul>
