
# 信息采集工具

## 项目简介
本工具用于从教育局或学校公开网页自动提取学校信息，包括：
- 学校名称
- 办学地址
- 联系电话
- 学校网址

提取结果可直接下载为 Excel 文件。

## 使用方法
1. 打开 [Streamlit Cloud](https://streamlit.io/cloud) 并登录。
2. 新建 App，选择本仓库并选择 `info_collector_app.py` 文件。
3. 点击 Deploy，部署完成后即可在网页使用。
4. 在网页输入学校信息页面链接，点击“开始提取”，查看结果并下载 Excel。

## 依赖
请确保安装以下依赖：
```
streamlit
requests
beautifulsoup4
pandas
openpyxl
```
