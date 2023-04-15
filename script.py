import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

companies = ['dfinity', 'aptoslabs', 'CircleCI']  # Add the company names or links here

for company in companies:
    page_link = requests.get(f'https://boards.greenhouse.io/{company}')
    webpage = bs(page_link.content, 'html.parser')
    links = webpage.find_all(class_='opening')
    job = []
    for link in links:
        job_apply_url = "https://boards.greenhouse.io/" + link.a['href']
        try:
            job_category = link.find_previous_sibling('h2').get_text().strip()
        except AttributeError:
            job_category = None
        individual_job = requests.get(job_apply_url)
        job_page = bs(individual_job.content, "html.parser")

        job_title = job_page.find("h1").get_text().strip()
        job_location = job_page.find(class_="location").get_text().strip()
        job_description = job_page.find(id='content').get_text().strip()
        
        job_full = [job_title, job_location, job_category, job_description, job_apply_url]

        job.append(job_full)

    df = pd.DataFrame(job, columns=['job_title', 'job_location', 'job_category', 'job_description',
                                        'job_apply_url'])
    
    # Strip any extra whitespace from the job titles, job locations, and job descriptions
    df['job_title'] = df['job_title'].str.strip()
    df['job_location'] = df['job_location'].str.strip()
    df['job_description'] = df['job_description'].str.strip()
    
    df.to_csv(f'{company}_jobs.csv', index=False)  # Save each company's job listings as a separate CSV file
