def generate_dataframe(input_file):
    
    '''
    Takes the results extracted from NEOS and get them in a dataframe format:
        Input:
                input_file (str) : file with the results from NEOS in txt format.
        Output:
                sol : dataframe with NEOS solutions.
    '''
           
    import numpy as np
    import pandas as pd
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    f = open(input_file,'r');
    Lines =f.readlines()

    objective = []
    gamma = []
    demand = []
    mu = []
    p_pub_x = []
    p_priv_x = []
    p_pub_y = []
    p_priv_y = []
    q_pub_x = []
    q_priv_x = []
    q_pub_y = []
    q_priv_y = []
    z=[]
    PubCost = []
    K_x = []
    K_y = []
    P_x = []
    P_y = []

    for i in range(len(Lines)):
        if Lines[i][0:5] == 'gamma':
            gamma = np.append(gamma, float(Lines[i][8:]))
            if Lines[i-1][0:9] != 'Objective':
                objective = np.append(objective,'Not feasible')
            else:
                objective = np.append(objective,float(Lines[i-1][9:]))
        elif Lines[i][0:6] == 'demand':
            demand = np.append(demand, float(Lines[i][8:]))
        elif Lines[i][0:2] == 'mu':
            mu = np.append(mu, float(Lines[i][4:]))
        elif Lines[i][0:5] == 'price':
            p_pub_x = np.append(p_pub_x, float(Lines[i+1][10:]))
            p_priv_x = np.append(p_priv_x, float(Lines[i+3][10:]))
            p_pub_y = np.append(p_pub_y, float(Lines[i+2][10:]))
            p_priv_y = np.append(p_priv_y, float(Lines[i+4][10:]))
        elif Lines[i][0:5] == 'quant':
            q_pub_x = np.append(q_pub_x, float(Lines[i+1][10:]))
            q_priv_x = np.append(q_priv_x, float(Lines[i+3][10:]))
            q_pub_y = np.append(q_pub_y, float(Lines[i+2][10:]))
            q_priv_y = np.append(q_priv_y, float(Lines[i+4][10:]))
        elif Lines[i][0] == 'K':
            K_x = np.append(K_x, float(Lines[i+1][2:]))
            K_y = np.append(K_y, float(Lines[i+2][2:]))
        elif Lines[i][0:2] == 'P ':
            P_x = np.append(P_x, float(Lines[i+1][2:]))
            P_y = np.append(P_y, float(Lines[i+2][2:]))

        elif Lines[i][0] == 'z':
            z = np.append(z, float(Lines[i][4:]))
        elif Lines[i][0:7] == 'PubCost':
            PubCost = np.append(PubCost, float(Lines[i][10:]))

    min_n_data = min(len(objective),len(gamma),len(demand),len(mu), len(p_pub_x), len(p_priv_x), len(p_pub_y), len(p_priv_y), \
               len(q_pub_x), len(q_priv_x), len(q_pub_y), len(q_priv_y), len(z), len(PubCost), len(K_x), len(K_y), \
               len(P_x), len(P_y))


    solutions = pd.DataFrame()
    solutions['value_obj_func'] = objective[-min_n_data:]
    solutions['gamma'] = gamma[-min_n_data:]
    solutions['demand'] = demand[-min_n_data:]
    solutions['mu'] = mu[-min_n_data:]
    solutions['K_infanrix'] = K_x[-min_n_data:]
    solutions['K_daptacel'] = K_y[-min_n_data:]
    solutions['P_infanrix'] = P_x[-min_n_data:]
    solutions['P_daptacel'] = P_y[-min_n_data:]
    solutions['pub_p_infanrix'] = p_pub_x[-min_n_data:]
    solutions['priv_p_infanrix'] = p_priv_x[-min_n_data:]
    solutions['pub_p_daptacel'] = p_pub_y[-min_n_data:]
    solutions['priv_p_daptacel'] = p_priv_y[-min_n_data:]
    solutions['pub_q_infanrix'] = q_pub_x[-min_n_data:]
    solutions['priv_q_infanrix'] = q_priv_x[-min_n_data:]
    solutions['pub_q_daptacel'] = q_pub_y[-min_n_data:]
    solutions['priv_q_daptacel'] = q_priv_y[-min_n_data:] 
    solutions['z'] = z[-min_n_data:]
    solutions['PubCost'] = PubCost[-min_n_data:]
    solutions = solutions[1:]
    
    return solutions