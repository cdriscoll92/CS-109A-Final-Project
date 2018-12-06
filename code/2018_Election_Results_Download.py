import pandas as pd
from bs4 import BeautifulSoup
import time
import requests

data_folder = "https://raw.githubusercontent.com/cdriscoll92/CS-109A-Final-Project/master/data/"
local_data_folder = "/Users/colleendriscoll/Dropbox/Classes/CS 109A/CS 109A Final project/data/"

politico_url_front = "https://www.politico.com/election-results/2018/"

## Reading in state abbreviations file to get the correct district ID columns
state_abbs = pd.read_csv(data_folder + "state_abbreviations_correspondence_table.csv")

## Politico site formatting for names
states = list(state_abbs.state_name.str.lower().values)
states_lower = [x.replace(" ", "-") for x in states]


def BS_html_parsed_from_html(URL):
    ## requires BeautifulSoup, time, requests
    time.sleep(2)
    bs_out = BeautifulSoup(requests.get(URL).text, "html.parser")
    return(bs_out)


## By state
## Get state page
## Figure out how many districts there are in the state
## Get district tables
## Parse district tables
## Save district tables

results_2018 = {'district': [],
               'party': [],
               'votes': []}
for i, abb in enumerate(state_abbs.state_abb):
    state_url = politico_url_front + states_lower[i]
    ## Get state page
    BS_page_state_i = BS_html_parsed_from_html(state_url)

    ## Figure out how many districts there are in the state
    district_links = BS_page_state_i.findAll("div",\
        {"class":"district-links"})

    ## At-large districts don't have links and are referenced
    ## differently from multi-district states    
    if len(district_links) >0:
        district_n = len(district_links[0].findAll("a"))
        districts_formatted = ['{num:02d}'.format(num=k) for k\
        in range(1, district_n+1)]
    else:
        districts_formatted = ['00']

    ## Get district tables
    dist_ids = [abb+"-"+dist_i for dist_i in districts_formatted]
    for district in dist_ids:
        ## Get the section on the page for this district
        district_html = BS_page_state_i.findAll("section",
                                                {"id": district})
        ## Get the table where the results are
        results_table = district_html[0].findAll("tr")
        
        ## Table composed of headers and footers; only
        ## grab candidate/vote information
        last_candidate_index = len(results_table)-2
        for j in range(1, last_candidate_index):
            ## Get party and number of votes for each cand.
            party = results_table[j].find("td",
                                          {"class":"party"})
            votes = results_table[j].find("td",
                                          {"class":"vote-count"})

            ## Add these results to the results dictionary
            results_2018['district'].append(district)
            results_2018['party'].append(party.text)
            results_2018['votes'].append(votes.text)

results_2018_df = pd.DataFrame(results_2018)

results_2018_df.votes = results_2018_df.votes.str.replace(",", "").astype(int)

results_2018_df['year'] = 2018

results_2018_df.to_csv(local_data_folder + "election_results/2018_scraped.csv")





