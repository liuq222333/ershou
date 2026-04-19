# -*- coding: utf-8 -*-

# 数据爬取文件 —— 汽车之家二手车 (che168.com)

import scrapy
import pymysql
import pymssql
from ..items import UsedcarItem
import re
import platform


# 城市编码映射（che168 cid -> 城市名）
CITY_MAP = {
    "110100": "北京", "310100": "上海", "440100": "广州", "440300": "深圳",
    "330100": "杭州", "320100": "南京", "510100": "成都", "500100": "重庆",
    "420100": "武汉", "410100": "郑州", "430100": "长沙", "370100": "济南",
    "210100": "沈阳", "220100": "长春", "230100": "哈尔滨", "120100": "天津",
    "610100": "西安", "530100": "昆明", "350100": "福州", "360100": "南昌",
    "340100": "合肥", "320500": "苏州", "330200": "宁波", "370200": "青岛",
    "441900": "东莞", "371300": "临沂",
}

# 爬取页数（每页约20条，15页≈300条）
MAX_PAGES = 15


class UsedcarSpider(scrapy.Spider):
    name = 'usedcarSpider'
    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [400, 403],
        'RETRY_HTTP_CODES': [500, 503],
        'DOWNLOAD_DELAY': 3,
    }

    realtime = False

    def __init__(self, realtime=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime == 'true'

    def start_requests(self):
        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, 'v6yp1uu5_usedcar') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return

        for page in range(1, MAX_PAGES + 1):
            url = f'https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{page}exx0/'
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': page})

    def parse(self, response):
        cards = response.xpath('//li[contains(@class,"cards-li")]')
        for card in cards:
            fields = UsedcarItem()

            carname = card.attrib.get('carname', '')
            price = card.attrib.get('price', '')
            milage = card.attrib.get('milage', '')
            regdate = card.attrib.get('regdate', '')
            cid = card.attrib.get('cid', '')

            # 解析品牌和型号：如 "大众Q3 2024款 35 TFSI 时尚动感型"
            brand, model1 = self._parse_carname(carname)

            try:
                fields['brand'] = brand
            except Exception:
                pass
            try:
                fields['model1'] = model1
            except Exception:
                pass
            try:
                fields['discountprice'] = float(price) if price else 0
            except Exception:
                pass
            try:
                fields['originalprice'] = 0
            except Exception:
                pass
            try:
                fields['vehicleage'] = regdate.split('/')[0] if regdate else ''
            except Exception:
                pass
            try:
                fields['kilometer'] = float(milage) if milage else 0
            except Exception:
                pass
            try:
                fields['imgurl'] = card.xpath('.//img/@src').get('') or card.xpath('.//img/@src2').get('')
            except Exception:
                pass
            try:
                fields['xqurl'] = card.xpath('.//a[@class="carinfo"]/@href').get('')
            except Exception:
                pass
            try:
                fields['city'] = CITY_MAP.get(cid, cid)
            except Exception:
                pass

            if fields.get('brand'):
                yield fields

    def _parse_carname(self, carname):
        """从车名中提取品牌和车系，如 '奥迪Q3 2024款 35 TFSI' -> ('奥迪', 'Q3')"""
        if not carname:
            return '', ''
        m = re.match(r'^(.+?)\s+\d{4}款', carname)
        if m:
            full = m.group(1).strip()
            # 尝试拆分中文品牌和字母数字型号
            m2 = re.match(r'^([\u4e00-\u9fa5]+)\s*(.*)', full)
            if m2:
                return m2.group(1), m2.group(2) if m2.group(2) else full
            return full, full
        return carname, carname

    def db_connect(self):
        type = self.settings.get('TYPE', 'mysql')
        host = self.settings.get('HOST', 'localhost')
        port = int(self.settings.get('PORT', 3306))
        user = self.settings.get('USER', 'root')
        password = self.settings.get('PASSWORD', '123456')
        try:
            database = self.databaseName
        except Exception:
            database = self.settings.get('DATABASE', '')

        if type == 'mysql':
            connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password, charset='utf8mb4')
        else:
            connect = pymssql.connect(host=host, user=user, password=password, database=database)
        return connect

    def table_exists(self, cursor, table_name):
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall(r"('.*?')", str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1
        else:
            return 0

    def temp_data(self):
        connect = self.db_connect()
        cursor = connect.cursor()
        sql = '''
            insert into `usedcar`(
                id, brand, model1, discountprice, originalprice,
                vehicleage, kilometer, imgurl, xqurl, city
            )
            select
                id, brand, model1, discountprice, originalprice,
                vehicleage, kilometer, imgurl, xqurl, city
            from `v6yp1uu5_usedcar`
            where(not exists (select id from `usedcar` where `usedcar`.id=`v6yp1uu5_usedcar`.id))
            order by rand()
            limit 50;
        '''
        cursor.execute(sql)
        connect.commit()
        connect.close()
