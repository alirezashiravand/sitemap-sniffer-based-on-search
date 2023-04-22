import httplib2
import streamlit as st
import pandas as pd
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import pandas as pd
import re
from urllib.parse import urlparse
import advertools as adv
def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    # css_identifier_text = "lEBKkf"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            # 'text': result.find(css_identifier_text, first=True).text
        }
        
        output.append(item)
        
    return output

def google_search(query):
    response = get_results(query)
    return parse_results(response)


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response 
    except requests.exceptions.RequestException as e:
        print(e)

query=st.text_input(label="your query",placeholder='please insert query in this input')
getResults_Btn_submit=st.button(label='get results')
SERP_Results=''
if getResults_Btn_submit:
    SERP_Results=google_search(query)
    results_df = pd.DataFrame(SERP_Results)
    results_df
    st.dataframe(results_df)


# find robots .txt 
# don't forget to check trail slashing and just keep domain name
def find_Domain():
    results_df['link']=results_df['link'].apply(lambda x: urlparse(str(x)).netloc)
    results_df['link']=results_df['link'].apply(lambda x: x if x.endswith('/') else x+'/')
    results_df['link']=results_df['link'].apply(lambda x: 'https://'+str(x))
    
def Robots_Finder():
    robots_link_df=results_df
    # robots_link_df=results_df['link']+'robots.txt'
    robots_link_df['link'] = robots_link_df['link'].astype(str)+'robots.txt'
    # robots_link_df['link']=robots_link_df['link'].apply(lambda x: f"str{x}robots.txt")
    return robots_link_df


# this section uses advertools

def Sitemap_Finder():
    df_temp=robots_link_df
    temp_list=[]
    value1=[]
    value2=[]
    sitemap_url_df=[]
    index_finder=int

    for item in robots_link_df['link']:
        try:
            print(item)
            value1=adv.robotstxt_to_df(item)
            value2=value1.groupby(['directive'])['content'].apply(', '.join).reset_index()
            sitemap_url_df=value2.loc[value2['directive'] == 'Sitemap']
            index_finder=sitemap_url_df.index[0]
            temp_list.append({
                'url':item,
                'sitemaps':sitemap_url_df.at[index_finder,'content']
            })
        except:
            temp_list.append({
            'url':item,
            'sitemaps':''
        })
    

final=pd.DataFrame(temp_list)
final



st.write('now you can export all sitemaps')
robots_sitemaps_btn=st.button(label='find me sitemaps')

    






