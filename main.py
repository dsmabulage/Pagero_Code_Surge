import subprocess
import json
import os

os.chdir('reactscraper')
subprocess.run(['python', 'reactscraper.py'], check=True)

os.chdir('../awsscraper')
subprocess.run(['scrapy', 'crawl', 'awslearnspider', '-O', '../aws.json'], check=True)

try:
    os.chdir('..')

    with open('react.json', 'r', encoding='utf-8') as file1, open('aws.json', 'r', encoding='utf-8') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    data1.extend(data2)

    with open('combined.json', 'w', encoding='utf-8') as outfile:
        json.dump(data1, outfile, indent=2, ensure_ascii=False)

except Exception as e:
     print(f"Error combining JSON files: {e}")
     raise