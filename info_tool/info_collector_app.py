
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="信息采集工具", layout="wide")

st.title("🏫 信息采集工具")
st.write("输入教育局或学校列表页面的链接，系统将自动提取学校名称、地址、电话和网址等信息，并可下载为 Excel 文件。")

url = st.text_input("请输入网页链接：", placeholder="例如：http://www.qdsn.gov.cn/.../index.shtml")

if st.button("开始提取"):
    if not url.strip():
        st.warning("请先输入网址！")
    else:
        try:
            st.info("正在抓取网页内容，请稍候……")
            response = requests.get(url, timeout=15)
            response.encoding = response.apparent_encoding

            if response.status_code != 200:
                st.error(f"网页访问失败，状态码：{response.status_code}")
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(" ", strip=True)

                pattern = re.compile(
                    r"([\u4e00-\u9fa5A-Za-z0-9]+学校).*?(地址[:：]?([^电话网址\s]+))?.*?(电话[:：]?(\d{3,4}[-—]?[0-9]{5,8}))?.*?(网址[:：]?(https?://[\w./-]+))?",
                    re.S)

                matches = pattern.findall(text)
                data = []
                for m in matches:
                    name = m[0].strip()
                    addr = m[2].strip() if m[2] else ""
                    phone = m[4].strip() if m[4] else ""
                    website = m[6].strip() if m[6] else ""
                    data.append([name, addr, phone, website])

                if data:
                    df = pd.DataFrame(data, columns=["学校名称", "办学地址", "联系电话", "学校网址"])
                    df.drop_duplicates(subset=["学校名称"], inplace=True)

                    st.success(f"✅ 共提取到 {len(df)} 条学校信息！")
                    st.dataframe(df, use_container_width=True)

                    excel_file = "school_info.xlsx"
                    df.to_excel(excel_file, index=False)
                    with open(excel_file, "rb") as f:
                        st.download_button(
                            label="📥 下载 Excel 文件",
                            data=f,
                            file_name="school_info.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.warning("未能提取到学校信息，请检查网页内容或更换网址。")

        except Exception as e:
            st.error(f"提取过程中出错：{e}")

st.markdown("---")
st.caption("© 2025 信息采集工具  |  支持教育局网站、学校名单公开页提取。")
