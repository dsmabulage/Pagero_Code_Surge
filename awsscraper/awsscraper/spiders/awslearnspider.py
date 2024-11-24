import scrapy
import json


class AwslearnspiderSpider(scrapy.Spider):
    name = "awslearnspider"
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
        result = []

        if "contents" in data:
            contents = data["contents"]

            for item in contents:
                title = item.get("title")
                if title and title in self.aws_sections:
                    parent_url = f"{self.base_url}/{item['href']}"
                    parent_obj = {
                        "title": title,
                        "url": parent_url,
                        "source": "aws_lambda",
                        "sections": [],
                    }
                    result.append(parent_obj)

                    for sec in item.get("contents", []):
                        sec_url = f"{self.base_url}/{sec['href']}"
                        sec_obj = {
                            "title": sec["title"],
                            "url": sec_url,
                            "source": "aws_lambda",
                            "sections": [],
                        }
                        result.append(sec_obj)

            return result

    # def parse_sub_section(self, response, sec_obj):
    #     main_div = response.css("div#main-col-body")

    #     text_content = main_div.css("p::text").getall()
    #     code_snippets = main_div.css("pre::text").getall()

    #     sec_obj["sub_sections"].append({"text": " ", "code_snippets": ""})
