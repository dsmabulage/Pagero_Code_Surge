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

        print(request)

    def get_page_content(url):
        response = requests.get(url)
        return response.content

    def parse_api(self, response):
        data = json.loads(response.body)

        if "contents" in data:
            contents = data["contents"]

            for item in contents:
                title = item.get("title")
                if title and title in self.aws_sections:
                    obj = {
                        "title": title,
                        "url": f"{self.base_url}/{item['href']}",
                        "source": "aws_lambda",
                        "sections": [],
                    }

                    for sec in item.get("contents", []):
                        sec_url = f"{self.base_url}/{sec['href']}"
                        sec_obj = {
                            "title": sec["title"],
                            "url": sec_url,
                        }
                        obj["sections"].append(sec_obj)                       

                    yield obj



