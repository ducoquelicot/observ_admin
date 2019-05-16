from bs4 import BeautifulSoup
import csv, glob, os

pdf_list = glob.glob('pdfs/pa_ag_2018/*.pdf')

for pdf in pdf_list:
    filename = os.path.basename(pdf)
    lettertotext = 'pdftotext -layout -htmlmeta pdfs/pa_ag_2018/{}'.format(filename)
    os.system(lettertotext)

html_list = glob.glob('pdfs/pa_ag_2018/*.html')

doc_info = []
for html in html_list:
    filename = os.path.basename(html)
    with open('pdfs/pa_ag_2018/{}'.format(filename)) as f:
        soup = BeautifulSoup(f, 'html.parser')
        name = soup.title.string[:-22]
        city = 'paloalto'
        doctype = 'agenda'
        date = soup.title.string[-20:-8]
        body = soup.body.pre.string
        doc_info.append([name, city, doctype, date, body])

with open('pa_ag_2018.csv', 'w') as database:
    writer = csv.writer(database)
    writer.writerow(["name", "city", "doctype", "date", "body"])
    writer.writerows(doc_info)
        