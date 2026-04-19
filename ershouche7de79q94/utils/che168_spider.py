# coding:utf-8
"""汽车之家二手车爬取 —— Selenium 版本，可绕过 JS 反爬"""

import re
import time
import random

CITY_MAP = {
    "110100": "北京", "310100": "上海", "440100": "广州", "440300": "深圳",
    "330100": "杭州", "320100": "南京", "510100": "成都", "500100": "重庆",
    "420100": "武汉", "410100": "郑州", "430100": "长沙", "370100": "济南",
    "210100": "沈阳", "220100": "长春", "230100": "哈尔滨", "120100": "天津",
    "610100": "西安", "530100": "昆明", "350100": "福州", "360100": "南昌",
    "340100": "合肥", "320500": "苏州", "330200": "宁波", "370200": "青岛",
    "441900": "东莞", "371300": "临沂", "350200": "厦门", "330300": "温州",
}


def _parse_carname(carname):
    if not carname:
        return "", ""
    m = re.match(r"^(.+?)\s+\d{4}款", carname)
    if m:
        full = m.group(1).strip()
        m2 = re.match(r"^([\u4e00-\u9fa5]+)\s*(.*)", full)
        if m2:
            return m2.group(1), m2.group(2) if m2.group(2) else full
        return full, full
    return carname, carname


def _create_driver():
    """创建无头 Chrome 浏览器"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    driver.set_page_load_timeout(20)
    return driver


def crawl_che168(max_pages=3):
    """爬取汽车之家二手车列表页，返回记录列表"""
    from lxml import etree

    results = []
    driver = _create_driver()

    try:
        for page in range(1, max_pages + 1):
            url = f"https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{page}exx0/"
            try:
                driver.get(url)
                time.sleep(random.uniform(2, 4))
            except Exception:
                continue

            html = etree.HTML(driver.page_source)
            cards = html.xpath('//li[contains(@class,"cards-li")]')

            for card in cards:
                carname = card.get("carname", "")
                price = card.get("price", "")
                milage = card.get("milage", "")
                regdate = card.get("regdate", "")
                cid = card.get("cid", "")

                if not carname or not price:
                    continue

                brand, model1 = _parse_carname(carname)
                city = CITY_MAP.get(cid, "")

                # 提取图片
                imgs = card.xpath('.//img/@src') + card.xpath('.//img/@src2')
                imgurl = ""
                for img in imgs:
                    if img and "default" not in img:
                        imgurl = img if img.startswith("http") else ("https:" + img)
                        break

                # 提取链接
                xqurl = ""
                hrefs = card.xpath('.//a[@class="carinfo"]/@href')
                if hrefs:
                    xqurl = ("https://www.che168.com" + hrefs[0]) if hrefs[0].startswith("/") else hrefs[0]

                results.append({
                    "brand": brand,
                    "model1": model1,
                    "discountprice": float(price),
                    "originalprice": 0,
                    "vehicleage": regdate.split("/")[0] if regdate else "",
                    "kilometer": float(milage) if milage else 0,
                    "imgurl": imgurl,
                    "xqurl": xqurl,
                    "city": city,
                })

            # 页间控制频率
            if page < max_pages:
                time.sleep(random.uniform(1, 2))
    finally:
        driver.quit()

    return results
