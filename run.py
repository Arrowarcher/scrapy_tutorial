from scrapy import cmdline
# print("scrapy crawl quotes".split())
# cmdline.execute("scrapy crawl quotes -a category1=electronics".split())
# cmdline.execute("scrapy crawl author -o author.json".split())

cmdline.execute("scrapy crawl toscrape-css".split())
# -a 给Spider传递参数,参数会变成Scrapy的属性
# -o 导出