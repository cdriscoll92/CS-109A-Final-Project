import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
%matplotlib inline
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

data_folder = "https://raw.githubusercontent.com/cdriscoll92/CS-109A-Final-Project/master/data/"
# local_data_folder = '/Users/poojatyagi/Dropbox (MIT)/CS 109A Final project/Data'
local_data_folder = "/Users/colleendriscoll/Dropbox/Classes/CS 109A/CS 109A Final project/data/"

def clea_clean(clea_file_name, state_abb_df):
    ## Read in data
    clea_results = pd.read_csv(clea_file_name)
    democrat_code = 180
    republican_code = 583
    election_month_int = 11
    
    ## Subsetting to only Democrats and Republicans
    clea_results = clea_results[(clea_results.pty == democrat_code) | 
                                (clea_results.pty == republican_code)]
    ## Only general elections (November)
    clea_results = clea_results[clea_results.mn == election_month_int]

    ## Extracting district number from constituency name
    ## There are some states with only one district that then don't 
    ## have a district number listed -- therefore filling those NAs with 1s
    clea_results['dist_num'] = clea_results.cst_n.str.findall('[0-9]+').\
    str[0].fillna(1)
    
    ## Lowercase state name to match CLEA listing
    state_abb_df['state_name_lower'] = state_abb_df.state_name.str.lower()

    ## Merging CLEA with state abbrevation correspondence table
    clea_merged = pd.merge(clea_results, state_abb_df,
                              how = 'right',
                              left_on = 'sub',
                              right_on = 'state_name_lower')
    
    ## Creating distict ID variable to merge on later
    clea_merged['dist_id'] = clea_merged['state_abb']+ "_" + \
    clea_merged['dist_num'].astype(str)

    ## Grouping CLEA by district-year to get the democratic share of the 
    ## two-party vote
    grouped = clea_merged.groupby(['dist_id', 'yr'])

    years = []
    dist_ids = []
    dem_shares = []

    for name, group in grouped:
        dem_share = 0
        years.append(group.yr.values[0])
        dist_ids.append(group.dist_id.values[0])

        if democrat_code in group.pty.values: ## If a Democrat ran
            total_votes = np.sum(group.cv1.values)
            dem_votes = np.sum(group.cv1[group.pty == democrat_code].values)
            dem_share = dem_votes/total_votes
        dem_shares.append(dem_share)
    
    dem_vote_share_dict = {'year': years,
                       'dist_id': dist_ids,
                       'dem_vote_share': dem_shares
                      }
    dem_vote_share = pd.DataFrame(dem_vote_share_dict)
    
    return dem_vote_share

def drop_secondary_members(nominate_df):
    ## Districts where there was more than one member of Congress serving, 
    ## assign the one who voted the most number of times to the district
    multiple_member_districts = nominate_df.dist_id\
    [nominate_df.dist_id.duplicated()]
    
    nominate_df['main_member'] = 1
    for district in multiple_member_districts:
        member_votes = nominate_df.nominate_number_of_votes\
        [nominate_df.dist_id == district]

        orders = np.argsort(member_votes)

        lowest_score_index = nominate_df['main_member']\
        [nominate_df.dist_id == district][orders == 0].index

        nominate_df.loc[lowest_score_index, 'main_member'] = 0

    ## Only keeping the main member in each district
    nominate_df = nominate_df[nominate_df.main_member == 1]
    nominate_df.drop('main_member', axis = 1, inplace = True)

    return nominate_df

def nom_scores_clean(nom_file_name, cols_keep):
    nominate_scores = pd.read_csv(nom_file_name)
    nominate_scores = nominate_scores[cols_keep]
    
    ## Dropping president
    nominate_scores = nominate_scores[nominate_scores['state_abbrev']\
                                      != "USA"]

    ## Dropping members who didn't vote (they can't provide ideology measures then)
    missing_vote_num_indices = nominate_scores.nominate_number_of_votes.isna()\
    == True
    nominate_scores = nominate_scores[~missing_vote_num_indices]

    ## District ID column
    nominate_scores['dist_id'] = nominate_scores.state_abbrev + '_' + \
    nominate_scores.district_code.astype(str)

    nominate_scores = drop_secondary_members(nominate_scores)

    nominate_scores.drop('nominate_number_of_votes', axis = 1,
                        inplace = True)

    ## Election year during which this Congress was in session (not the one that
    ## produced this Congress!)
    session_length = 2
    congress_start_year = 1788
    nominate_scores['year'] = congress_start_year + session_length*\
    nominate_scores['congress']

    return nominate_scores


#### RUN IN THIS ORDER -- READING IN THE ACTUAL FILES AND CLEANING ####

## Reading in state abbreviations file to get the correct district ID columns
state_abbs = pd.read_csv(data_folder + "state_abbreviations_correspondence_table.csv")

clea_cleaned = clea_clean(data_folder + "election_results/clea_20180507.csv",
                          state_abbs)

## 2016 Results for Milestone 3 -- update for Milestone 4 with 2018 results
results_2016 = clea_cleaned[clea_cleaned.year == 2016]
results_2016 = results_2016[['dist_id', 'dem_vote_share']]

## If Democratic vote share is >0.50, the Democrat won; else
## the Republican did
results_2016['dem_won_2016'] = np.round(results_2016.dem_vote_share, 0)
results_2016.drop('dem_vote_share', axis = 1, inplace = True)

clea_cleaned = pd.merge(clea_cleaned, results_2016,
                       on = "dist_id", how = "left")


