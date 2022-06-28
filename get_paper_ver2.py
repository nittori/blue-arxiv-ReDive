#https://pypi.org/project/arxiv/

import arxiv
import yaml
import os
import csv

def au_search(author):
  search = arxiv.Search(query ='au:"'+author+'"',max_results = 1,sort_by = arxiv.SortCriterion.SubmittedDate)
  return search

def read_config(file_dir):
    
    config_path = f'{file_dir}/authors_config.yaml' # file dir
    with open(config_path, 'r') as yml:
        authors = yaml.safe_load(yml)
        
    return authors["authors"]

def read_db(file_dir):
    db_path = f'{file_dir}/paper_database.csv'
    
    post_ids = []
    
    with open(db_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            post_ids.append(row[0])
    f.close()
    return post_ids

def write_db(file_dir,new_ids):
    db_path = f'{file_dir}/paper_database.csv'
    with open(db_path,"a",newline='') as f: 
        writer = csv.writer(f) 
        for s_id in new_ids:
            writer.writerow([s_id])
    f.close()

def check_database(file_dir,s_id):
    post_ids = read_db(file_dir)
    
    if s_id in post_ids:
        return False
    else:
        return True
        
import time
import datetime
from dateutil import tz
timefilter_threshold = 1

def time_filter(published):
    JST = tz.gettz('Asia/Tokyo')
    UTC = tz.gettz("UTC")

    now = datetime.datetime.now(JST)
    now_utc = now.astimezone(UTC)

    time_diff = now_utc - published
    
    if datetime.timedelta(days=timefilter_threshold) >= time_diff:
        return True
    else:
        return False    

def get_paper():
    
    file_abs_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_abs_path)
    
    authors = read_config(file_dir)
    
    papers = []
    new_ids = []
    
    for author in authors:
      search = au_search(author)
      for result in search.results():
          
        s_id = result.get_short_id()
        
        paper = {"author" : author,\
                 "title" : result.title,\
                 "published" : result.published,\
                 "url" : result.pdf_url }
            
        if check_database(file_dir, s_id):
            papers.append(paper)
            new_ids.append(s_id)
    if len(new_ids) == 0:
            new_ids.append("dammy")
    write_db(file_dir,new_ids)
        
    return papers

if __name__ == "__main__":
    papers = get_paper()
    
    print(len(papers))
    
    for paper in papers:
        print(paper)

