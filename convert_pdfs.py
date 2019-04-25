from bs4 import BeautifulSoup
import csv, glob, os

pdf_list = glob.glob(os.path.expanduser('~/Desktop/Python/PDF/*.pdf'))

for pdf in pdf_list:
    filename = os.path.basename(pdf)
    lettertotext = 'pdftotext -layout -htmlmeta ~/Desktop/Python/PDF/{}'.format(filename)
    os.system(lettertotext)

html_list = glob.glob(os.path.expanduser('~/Desktop/Python/PDF/*.html'))

doc_info = []
for html in html_list:
    filename = os.path.basename(html)
    with open(os.path.expanduser('~/Desktop/Python/PDF/{}'.format(filename))) as f:
        soup = BeautifulSoup(f, 'html.parser')
        name = soup.title.string[:-22]
        city = 'paloalto'
        doctype = 'agenda'
        date = soup.title.string[-20:-8]
        body = soup.body.pre.string
        doc_info.append([name, city, doctype, date, body])

with open(os.path.expanduser('~/Desktop/Python/Files/db_test.csv'), 'w') as database:
    writer = csv.writer(database)
    writer.writerow(["name", "city", "doctype", "date", "body"])
    writer.writerows(doc_info)
        