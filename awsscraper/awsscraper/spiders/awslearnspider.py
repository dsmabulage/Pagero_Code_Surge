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
        all_titles_and_hrefs = []

        if "contents" in data:
            contents = data["contents"]

            for item in contents:
                title = item.get("title")
                if title and title in self.aws_sections:
                    all_titles_and_hrefs.extend(self.extract_titles_and_hrefs(item))

        for item in all_titles_and_hrefs:
            request = scrapy.Request(
                item["url"], callback=self.parse_content, meta={"item": item}
            )
            yield request

    def parse_content(self, response):
        item = response.meta["item"]
        main_content = response.css("div#main-col-body")

        content = {
            "title": item["title"],
            "url": item["url"],
            "source": "aws_lambda",
            "sections": [],
        }

        children = main_content.xpath("./*")
        for child in children:
            section_details = {"text": [], "code_snippets": []}
            if child.xpath(".//code"):
                code_snippets = child.xpath(".//code/text()").getall()
                section_details["code_snippets"].extend(code_snippets)
            else:
                text_content = child.xpath(".//text()").getall()
                section_details["text"].extend(text_content)

            content["sections"].append(section_details)

        return content

    def extract_titles_and_hrefs(self, data):
        if "title" in data and "href" in data:
            yield {"title": data["title"], "url": f'{self.base_url}/{data["href"]}'}

        if "contents" in data and isinstance(data["contents"], list):
            for item in data["contents"]:
                yield from self.extract_titles_and_hrefs(item)
