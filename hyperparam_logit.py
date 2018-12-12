drop_cols1 = ['nokken_poole_dim1','nokken_poole_dim2']
drop_cols2 = ['nominate_dim1', 'nominate_dim2']
drop_cols = [drop_cols1, drop_cols2]

poly_degree_max = 20
poly_degrees = range(1, poly_degree_max)
L2_penalties = [10**i for i in range(0,7,2)]

hyperparams = list(itertools.product(\
    *[L2_penalties,
      drop_cols,
     poly_degrees]))

def get_design_mats(df, dropped_columns,
                    binary_columns, poly_degree):
    df_reduced = df.drop(dropped_columns, axis = 1,
                                  inplace = False)
    
    continuous_cols = [x for x in df_reduced.columns.values if \
                      x not in binary_columns]
    
    df_power = add_power_terms(df_reduced,
                               continuous_cols,
                               poly_degree)

    df_to_fit = add_interaction_terms(df_power,
                                      continuous_cols)
    return(df_to_fit)

def run_logit(x_train, x_val, y_train, y_val,
              hyperparams, binary_cols):
    
    C_i = hyperparams[0]
    dropped_cols = hyperparams[1]
    poly_degree = hyperparams[2]
    
    x_train_to_fit = get_design_mats(x_train, dropped_cols,
                                     binary_cols,
                                   poly_degree)
    x_val_to_fit = get_design_mats(x_val, dropped_cols,
                                   binary_cols,
                                   poly_degree)
    
    logit_obj = LogisticRegression(C=C_i)
    logit_obj.fit(x_train_to_fit,y_train)
    
    train_score = logit_obj.score(x_train_to_fit, y_train)
    val_score = logit_obj.score(x_val_to_fit, y_val)
    
    return(logit_obj, train_score, val_score)

logit_objects = []
train_scores = []
val_scores = []
for hp in hyperparams:
    logit_i = run_logit(x_train_scaled, x_val_scaled,
                        y_train, y_val,
                        hp, binary_cols = ['dem_incumbent'])
    logit_objects.append(logit_i[0])
    train_scores.append(logit_i[1])
    val_scores.append(logit_i[2])
            