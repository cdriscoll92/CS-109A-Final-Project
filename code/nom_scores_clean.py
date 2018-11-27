def drop_secondary_members(nominate_df):
    ## Districts where there was more than one member of Congress serving, 
    ## assign the one who voted the most number of times to the district
    multiple_member_districts = nominate_df.dist_id[nominate_df.dist_id.duplicated()]
    
    nominate_df['main_member'] = 1
    for district in multiple_member_districts:
        member_votes = nominate_df.nominate_number_of_votes[nominate_df.dist_id == district]

        orders = np.argsort(member_votes)

        lowest_score_index = nominate_df['main_member'][nominate_df.dist_id \
                                                            == district][orders == 0].index

        nominate_df.loc[lowest_score_index, 'main_member'] = 0

    ## Only keeping the main member in each district
    nominate_df = nominate_df[nominate_df.main_member == 1]
    nominate_df.drop('main_member', axis = 1, inplace = True)

    return nominate_df

def nom_scores_clean(nom_file_name, cols_keep):
    nominate_scores = pd.read_csv(nom_file_name)
    nominate_scores = nominate_scores[cols_keep]
    
    ## Dropping president
    nominate_scores = nominate_scores[nominate_scores['state_abbrev'] != "USA"]

    ## Dropping members who didn't vote (they can't provide ideology measures then)
    missing_vote_num_indices = nominate_scores.nominate_number_of_votes.isna() == True
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
    nominate_scores['year'] = congress_start_year + session_length*nominate_scores['congress']

    return nominate_scores