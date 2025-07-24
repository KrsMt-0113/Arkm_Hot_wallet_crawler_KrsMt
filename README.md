# Arkm 热钱包爬虫 Arkm_Hot_Wallet_Crawler @ KrsMt.

1.安装依赖
```
pip install re
pip install time
pip install requests
pip install csv
pip install os
pip install platform
pip install tqdm
```
2.获取cURL
  - 登录 `intel.arkm.com`
  - 选择任意实体进入主页
  - F12，"网络"(`"Network"`)中选择`"Fetch/XHR"`
  - 找到`transfer`开头的 api 请求
  - 复制为`cURL`
  - 粘贴到`curl.txt`

3.运行程序
  - 输入
    - `Entity`:实体正式名称。如`OKX`,`Binance`,`Lazarus group`
    - `entity`:实体字符串。点开实体主页即可在链接后缀找到。如`okx`,`binance`,`lazarus-group`
    - `num`:查询数。越大时间越久，不建议超过1500.

4.注意事项
  - `curl`具有时效性。如发现生成的`.csv`文件空白请重新获取`curl`。
  - 使用前先检查网络，能否访问`intel.arkm.com`
