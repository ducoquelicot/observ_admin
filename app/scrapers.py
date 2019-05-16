from bs4 import BeautifulSoup
from app import db
from app.models import Scraper
import ast, csv, fnmatch, os, time, urllib.request, requests

def first_pa_ag_2019():
    site = 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp'
    agenda = requests.get(site)
    soup = BeautifulSoup(agenda.text, 'html.parser')
    relevant_soup = soup.select('a')
    
    links = []
    for row in relevant_soup:
        if relevant_soup[row].getText() == 'Agenda and Packet':
            if fnmatch.fnmatch(relevant_soup[row]['href'], '*://www.cityofpaloalto.org/*'):
                link = relevant_soup[row]['href']
                links.append(link)
            else:
                links[row]['href'] = 'https://www.cityofpaloalto.org{}'.format(links[row]['href'])
                link = relevant_soup[row]['href']
                links.append(link)

    scraper = Scraper(name='Palo Alto Agenda 2019', links=repr(links), total=len(links))
    db.session.add(scraper)
    db.session.commit()

def pa_ag_2019():
    site = 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp'
    agenda = requests.get(site)
    soup = BeautifulSoup(agenda.text, 'html.parser')
    relevant_soup = soup.select('a')
    
    links = []
    for row in relevant_soup:
        if relevant_soup[row].getText() == 'Agenda and Packet':
            if fnmatch.fnmatch(relevant_soup[row]['href'], '*://www.cityofpaloalto.org/*'):
                link = relevant_soup[row]['href']
                links.append(link)
            else:
                links[row]['href'] = 'https://www.cityofpaloalto.org{}'.format(links[row]['href'])
                link = relevant_soup[row]['href']
                links.append(link)

    scraper = Scraper.query.filter_by(name='Palo Alto Agenda 2019').first()
    stored_links = ast.literal_eval(scraper.links)


def scrape(html_link):
    # get all links within parameters from provided html
    agenda = requests.get(html_link)
    soup = BeautifulSoup(agenda.text, 'lxml')
    relevant_soup = soup.select('a')
    return relevant_soup

def get_links(links, years):
    # filter for Agenda and packet only, append to list and download pdf
    agendas = []
    for row in range(len(links)):
        if links[row].getText()== 'Agenda and Packet':
            if fnmatch.fnmatch(links[row]['href'], '*://www.cityofpaloalto.org/*'):
                agendas.append([links[row]['href']])
                time.sleep(2)

                urllib.request.urlretrieve(links[row]['href'], os.path.expanduser('~/Desktop/Python/PDF/pdfs_' +str(years) + '_' +str(row) + '.pdf'))
                time.sleep(5)
            else:
                links[row]['href'] = 'https://www.cityofpaloalto.org' + links[row]['href']
                agendas.append([links[row]['href']])
                time.sleep(2)
                urllib.request.urlretrieve(links[row]['href'], os.path.expanduser('~/Desktop/Python/PDF/pdfs_' +str(years) + '_' +str(row) + '.pdf'))
                time.sleep(5)

def main():
    pa_agenda = {2019: 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp'}
    for year in pa_agenda.keys():
        output = scrape(pa_agenda[year])
        get_links(output, year)