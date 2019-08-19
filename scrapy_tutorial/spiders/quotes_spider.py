import json

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"         # 此Spider的name（唯一）
    # allowed_domains = ['quotes.toscrape.com'] todo:3
    # page = 1
    # start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        # 'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        # next_page = response.css('li.next a::attr(href)').get()   # todo:5
        # if next_page is not None:
            # next_page = response.urljoin(next_page)   # todo:4
            # yield scrapy.Request(next_page, callback=self.parse)
            # yield response.follow(next_page, callback=self.parse)   # todo:4  # todo:5
            # 与scrapy.Request不同，它response.follow直接支持相对URL - 无需调用urljoin
        for a in response.css('li.next a'):
            # response.css返回类似列表的对象；a标签自动使用其href属性
            yield response.follow(a, callback=self.parse)

        # response.follow(response.css('li.next a')[0])


    # def start_requests(self):     # todo:2
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
        # 返回可迭代的Requests，这里用生成器函数

    # def parse(self, response):    # todo:3
    #     data = json.loads(response.text)
    #     for quote in data["quotes"]:
    #         yield {"quote": quote["text"]}
    #     if data["has_next"]:
    #         self.page += 1
    #         url = "http://quotes.toscrape.com/api/quotes?page={}".format(self.page)
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):    # todo:2
    #     page = response.url.split("/")[-2]      # 取出页数
    #     filename = 'quotes-%s.html' % page      # 命名：quotes-1.html
    #     with open(filename, 'wb') as f:         # 以二进制格式打开一个文件只用于写入。
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        print(response.css('.author + a::attr(href)').getall())
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))       # 使用scrapy.Request类似分页这种相对url的，用urljoin拼url


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))