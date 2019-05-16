from bs4 import BeautifulSoup
from app import db, scheduler
from app.models import Scraper, Record
from datetime import datetime
import ast, csv, fnmatch, os, time, urllib.request, requests, glob

def first_pa_ag_2019():
    site = 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp'
    agenda = requests.get(site)
    soup = BeautifulSoup(agenda.text, 'html.parser')
    relevant_soup = soup.select('a')
    
    links = []
    for row in relevant_soup:
        if 'Agenda and Packet' in row.getText():
            if fnmatch.fnmatch(row['href'], '*://www.cityofpaloalto.org/*'):
                link = row['href']
                links.append(link)
            else:
                row['href'] = 'https://www.cityofpaloalto.org{}'.format(row['href'])
                link = row['href']
                links.append(link)
    
    retr_date = datetime.today().strftime('%d-%m-%Y')

    for link in links:
        name = link[-5:]
        urllib.request.urlretrieve(link, 'pdfs/pa_ag_2019/{}_{}.pdf'.format(name, retr_date))
        time.sleep(5)

    pdf_list = glob.glob('pdfs/pa_ag_2019/*.pdf')

    for pdf in pdf_list:
        filename = os.path.basename(pdf)
        if retr_date in filename:
            lettertotext = 'pdftotext -layout -htmlmeta pdfs/pa_ag_2019/{}'.format(filename)
            os.system(lettertotext)

    html_list = glob.glob('pdfs/pa_ag_2019/*.html')

    for html in html_list:
        filename = os.path.basename(html)
        if retr_date in filename:
            with open('pdfs/pa_ag_2019/{}'.format(filename)) as f:
                soup = BeautifulSoup(f, 'html.parser')
                name = soup.title.string[:-22]
                city = 'paloalto'
                doctype = 'agenda'
                date = soup.title.string[-20:-8]
                body = soup.body.pre.string
                r = Record(name=name, city=city, doctype=doctype, date=date, body=body)
                db.session.add(r)
                db.session.commit()

    scraper = Scraper(name='Palo Alto Agenda 2019', links=repr(links), total=len(links))
    db.session.add(scraper)
    db.session.commit()

    scheduler.add_job(id='pa_ag_2019', func=pa_ag_2019, trigger='interval', days=1, name='Palo Alto Agenda 2019')

def pa_ag_2019():
    site = 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp'
    agenda = requests.get(site)
    soup = BeautifulSoup(agenda.text, 'html.parser')
    relevant_soup = soup.select('a')
    
    links = []
    for row in relevant_soup:
        if row.getText() == 'Agenda and Packet':
            if fnmatch.fnmatch(row['href'], '*://www.cityofpaloalto.org/*'):
                link = row['href']
                links.append(link)
            else:
                row['href'] = 'https://www.cityofpaloalto.org{}'.format(row['href'])
                link = row['href']
                links.append(link)

    scraper = Scraper.query.filter_by(name='Palo Alto Agenda 2019').first()
    stored_links = ast.literal_eval(scraper.links)
    new_links = list(set(links) ^ set(stored_links))
    retr_date = datetime.today().strftime('%d-%m-%Y')

    for link in new_links:
        name = link[-5:]
        urllib.request.urlretrieve(link, 'pdfs/pa_ag_2019/{}_{}.pdf'.format(name, retr_date))
        time.sleep(5)

    pdf_list = glob.glob('pdfs/pa_ag_2019/*.pdf')

    for pdf in pdf_list:
        filename = os.path.basename(pdf)
        if retr_date in filename:
            lettertotext = 'pdftotext -layout -htmlmeta pdfs/pa_ag_2019/{}'.format(filename)
            os.system(lettertotext)

    html_list = glob.glob('pdfs/pa_ag_2019/*.html')

    for html in html_list:
        filename = os.path.basename(html)
        if retr_date in filename:
            with open('pdfs/pa_ag_2019/{}'.format(filename)) as f:
                soup = BeautifulSoup(f, 'html.parser')
                name = soup.title.string[:-22]
                city = 'paloalto'
                doctype = 'agenda'
                date = soup.title.string[-20:-8]
                body = soup.body.pre.string
                r = Record(name=name, city=city, doctype=doctype, date=date, body=body)
                db.session.add(r)
                db.session.commit()

    scraper.links = repr(links)
    scraper.total = len(links)
    db.session.commit()