import httplib2
import streamlit as st
import pandas as pd
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import pandas as pd

# function for starting request
def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response 
    except requests.exceptions.RequestException as e:
        print(e)



# Scraping Title, Link and Text
def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    
    return response


# parse results


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


# function for getting results from serp
def google_search(query):
    response = get_results(query)
    return parse_results(response)


query=st.text_input(label='your query',placeholder='please insert your query')


results=st.button('get result',on_click=google_search(query),disabled=query)

st.success(results)


# Building the table dataset
results_df = pd.DataFrame(results)
results_df
st.dataframe(results_df)