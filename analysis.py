from bs4 import BeautifulSoup
import sys
import datetime
import json

today = datetime.date.today()
read_file_name = "content/" + str(today) + ".html"
write_file_name = str(today) + ".json"

html = ""
with open(read_file_name, "r", encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
papers = soup.dl.find_all('dt')
papers_content = soup.dl.find_all('dd')

if len(papers) != len(papers_content):
    sys.exit()

objs = []
size = len(papers)
for i in range(size):
    paper = papers[i]
    paper_content = papers_content[i]
    obj = {}
    obj['link'] = paper.span.a['href']
    title_div = paper_content.find('div', class_='list-title')
    authors_div = paper_content.find('div', class_='list-authors')
    primary_subject_span = paper_content.find('span', class_='primary-subject')
    abstract_p = paper_content.find('p')
    
    count = 0
    for str in title_div.stripped_strings:
        if count == 1:
            obj['title'] = str
        count = count + 1
    
    authors = []
    count = 0
    for str in authors_div.stripped_strings:
        if count % 2 != 0:
            authors.append(str)
        count = count + 1
    obj['authors'] = authors
    
    obj['primary_subject'] = primary_subject_span.string
    
    obj['abstract'] = abstract_p.text.strip().replace("\n", "")
    objs.append(obj)

with open(write_file_name, "w", encoding='utf-8') as f:
    json.dump(objs, f, indent = 4)