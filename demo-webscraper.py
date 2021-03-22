# https://www.youtube.com/watch?v=eN_3d4JrL_w&list=WL&index=42

# import csv
# from datetime import datetime
# import requests
# from bs4 import BeautifulSoup

# template = 'https://www.indeed.com/jobs?q={}&l={}'

# def get_url(position, location):
#     """Generate a URL from position and location"""
#     template = 'https://www.indeed.com/jobs?q={}&l={}'
#     url = template.format(position, location)
#     return url

# url = get_url('accountant', 'san diego ca')

# # Extract Raw HTML

# response = requests.get(url)

# soup = BeautifulSoup(response.text, 'html.parser')

# cards = soup.find_all('div', 'jobsearch-SerpJobCard')

# # Prototype the model with a single record

# card = cards[0]
# atag = card.h2.a
# job_title = atag.get('title')
# job_url = 'http://www.indeed.com' + atag.get('href')
# company = card.find('span', 'company').text.strip()
# job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
# job_summary = card.find('div', 'summary').text.strip()
# post_date = card.find('span', 'date').text
# today = datetime.today().strftime('%Y-%m-%d')
# try:
#     job_salary = card.find('span', 'salaryText').text.strip()
# except AttributeError:
#     job_salary = ''

# # Generalize the model with a function
# def get_record(card):
#     """Extract job data from single reord"""
#     atag = card.h2.a
#     job_title = atag.get('title')
#     job_url = 'http://www.indeed.com' + atag.get('href')
#     company = card.find('span', 'company').text.strip()
#     job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
#     job_summary = card.find('div', 'summary').text.strip()
#     post_date = card.find('span', 'date').text
#     today = datetime.today().strftime('%Y-%m-%d')
#     try:
#         job_salary = card.find('span', 'salaryText').text.strip()
#     except AttributeError:
#         job_salary = ''
#     record = (job_title, company, job_location, post_date, today, job_summary, job_salary, job_url )
#     return record

# records = []
# for card in cards:
#     record = get_record(card)
#     records.append(record)

# # Getting the next page
# while True:
#     try:
#         url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
#     except AttributeError:
#         break
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     cards = soup.find_all('div', 'jobsearch-SerpJobCard')

#     for card in cards:
#         record = get_record(card)
#         records.append(record)

#  import csv
# from datetime import datetime
# import requests
# from bs4 import BeautifulSoup


# def get_url(position, location):
#     """Generate url from position and location"""
#     template = 'https://www.indeed.com/jobs?q={}&l={}'
#     position = position.replace(' ', '+')
#     location = location.replace(' ', '+')
#     url = template.format(position, location)
#     return url


# def get_record(card):
#     """Extract job data from a single record"""
    
#     job_title = card.h2.a.get('title')
#     company = card.find('span', 'company').text.strip()
#     job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
#     post_date = card.find('span', 'date').text
#     today = datetime.today().strftime('%Y-%m-%d')
#     summary = card.find('div', 'summary').text.strip().replace('\n', ' ')
#     job_url = 'https://www.indeed.com' + card.h2.a.get('href')

#     # this does not exists for all jobs, so handle the exceptions
#     salary_tag = card.find('span', 'salaryText')
#     if salary_tag:
#         salary = salary_tag.text.strip()
#     else:
#         salary = ''  
        
#     record = (job_title, company, job_location, post_date, today, summary, salary, job_url)
#     return record

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(position, location):
    """Generate url from position and location"""
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url


def get_record(card):
    """Extract job data from a single record"""
    
    job_title = card.h2.a.get('title')
    company = card.find('span', 'company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    post_date = card.find('span', 'date').text
    today = datetime.today().strftime('%Y-%m-%d')
    summary = card.find('div', 'summary').text.strip().replace('\n', ' ')
    job_url = 'https://www.indeed.com' + card.h2.a.get('href')

    # this does not exists for all jobs, so handle the exceptions
    salary_tag = card.find('span', 'salaryText')
    if salary_tag:
        salary = salary_tag.text.strip()
    else:
        salary = ''  
        
    record = (job_title, company, job_location, post_date, today, summary, salary, job_url)
    return record

def main(position, location):
    """Run the main program routine"""
    records = []
    url = get_url(position, location)
    
    # extract the job data
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')
        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
        
    # save the job data
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary', 'JobUrl'])
        writer.writerows(records)

main('accountant', 'san diego ca')