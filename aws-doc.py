import requests
import scrapy 


url = "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"
html = urlopen(url)

print(soup.prettify())

# response = requests.get(f"https://docs.aws.amazon.com/lambda/latest/dg/welcome.html")
# soup = BeautifulSoup(response.text, "lxml")



# print(soup.prettify())



# section_parent = soup.find("a", {"title": "Example apps"}).parent
toc_div = soup.find('div', attrs={'data-testid': 'doc-page-toc'})

print(toc_div)
