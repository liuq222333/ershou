# 数据容器文件

import scrapy

class SpiderItem(scrapy.Item):
    pass

class UsedcarItem(scrapy.Item):
    # 品牌
    brand = scrapy.Field()
    # 型号
    model1 = scrapy.Field()
    # 现价
    discountprice = scrapy.Field()
    # 已减
    originalprice = scrapy.Field()
    # 年份
    vehicleage = scrapy.Field()
    # 行驶里程
    kilometer = scrapy.Field()
    # 图片
    imgurl = scrapy.Field()
    # 链接
    xqurl = scrapy.Field()
    # 所在城市
    city = scrapy.Field()

