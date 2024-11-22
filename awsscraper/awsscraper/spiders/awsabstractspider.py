import scrapy
import json


class AwsabstractspiderSpider(scrapy.Spider):
    name = "awsabstractspider"
    allowed_domains = ["docs.aws.amazon.com"]
    headers = {}
    base_url = "https://docs.aws.amazon.com/lambda/latest/dg"
    start_urls = [f"{base_url}/welcome.html"]
    aws_sections = [
        "What is AWS Lambda?",
        "Example apps",
        "Building with TypeScript",
        "Integrating other services",
        "Code examples",
    ]

    def parse(self, response):
        url = f"{self.base_url}/toc-contents.json"
        request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)

        yield request

    def parse_api(self, response):
        data = json.loads(response.body)

        if "contents" in data:
            contents = data["contents"]

            for item in contents:
                title = item.get("title")
                if title and title in self.aws_sections:
                    parent_url = f"{self.base_url}/{item['href']}"
                    obj = {
                        "title": title,
                        "url": parent_url,
                        "source": "aws_lambda",
                        "sections": [],
                    }

                    yield obj

    def parse_sub_section(self, response, sec_obj):
        main_div = response.css("div#main")

        text_content = main_div.css("p::text").getall()
        code_snippets = main_div.css("pre::text").getall()

        sec_obj["sub_sections"].append({"text": " ", "code_snippets": ""})
