## 简单的爬虫基础.

import requests

stockList = []
crawlSite = "http://hq.sinajs.cn/list=s_sh000001"
res = requests.get(crawlSite)
data = str(res.content)
stockList = data.split()
print(stockList)
