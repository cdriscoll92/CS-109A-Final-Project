def clea_clean(clea_file_name, state_abb_df):
    ## Read in data
    clea_results = pd.read_csv(clea_file_name)
    democrat_code = 180
    republican_code = 583
    election_month_int = 11
    
    ## Subsetting to only Democrats and Republicans
    clea_results = clea_results[(clea_results.pty == democrat_code) | (clea_results.pty == republican_code)]
    ## Only general elections (November)
    clea_results = clea_results[clea_results.mn == election_month_int]

    ## Extracting district number from constituency name
    ## There are some states with only one district that then don't 
    ## have a district number listed -- therefore filling those NAs with 1s
    clea_results['dist_num'] = clea_results.cst_n.str.findall('[0-9]+').str[0].fillna(1)
    
    ## Lowercase state name
    state_abb_df['state_name_lower'] = state_abb_df.state_name.str.lower()

    ## Merging CLEA with state abbrevation correspondence table
    clea_merged = pd.merge(clea_results, state_abb_df,
                              how = 'right',
                              left_on = 'sub',
                              right_on = 'state_name_lower')
    
    ## Creating distict ID variable to merge on later
    clea_merged['dist_id'] = clea_merged['state_abb']+ "_"+ clea_merged['dist_num'].astype(str)

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