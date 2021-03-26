def get_data(triangular, profit, capacity, num_samples, file_name):
    
    '''Generates data to perform trials with triangular distribution,
       profit and capacity differences and store the results in txt file 
       with the required format to be input to NEOS.
       
       Input:
               triangular (binary):      Takes value 1 if triangular distribution is required,
                                                     0 otherwise
                                              
               profit (binary):          Takes value 1 if profit difference is required,
                                                     0 otherwise   
                                              
               capacity (binary):        Takes value 1 if capacity difference is required,
                                                     0 otherwise  
                                              
               num_samples (int):        Number of samples required
               
               file_name:                Name of the file with the data to be used as input to NEOS
               
                                         
       Output:
               file (txt):              File with the generated data in the format required to be input to NEOS.
                                        File directory: <current directory>/Data/<file_name>
    '''
    
    #Make sure Tri, Pro and Cap have correct values
    if triangular + profit + capacity != 1:
        return print('triangular, profit and capacity are binary and must add up to 1')
    
    elif triangular != 0 and triangular != 1:
        return print('triangular must be binary')
    
    elif profit != 0 and profit != 1:
        return print('profit must be binary')
    
    elif capacity != 0 and capacity != 1:
        return print('capacity must be binary')
    
    else:
        CAPACITY_TRIALS = capacity
        PROFIT_TRIALS = profit
        TRIANGULAR_DISTRIBUTION = triangular

        import numpy as np
        import pandas as pd
        import os
        np.random.RandomState(10)

        #-------------------------------------DATA------------------------------------------------------
        OBJ = 1e-4                  # objective function weight 
        
        DEM = [4.034e6 , 4.034e6]     # total annual US demand (public + private)
        

        GAM = [0.25,0.25]             # product similarity in [0,1], where 1=identical

        OBJ_GOVT = [1e-4, 1e-4]       # objective function weight for gov't cost


        M1_INFLATION = 18.62          #inflation constraint for infanrix
        M2_INFLATION = 18.02          #inflation constraint 


        #----------------- CAPACITY DIFERRENCE TRIALS ----------------------------
        if CAPACITY_TRIALS==1:
            
            #make sure the number of samples has an integer square root
            num_samples = (int(num_samples**(1/2)))**2

            Capacity = [2.9e6, 4.5e6]              #Upper and lower bound for capacity
            
            cap_range = np.linspace(Capacity[0],Capacity[1], int(num_samples**(1/2)))

            Profit = [42.45e6, 42.45e6]            #Constant profit in these trials

            #Capacity values    
            #Create initial list to store capacity values
            K_inf = [0]*num_samples        
            K_dap = [0]*num_samples    

            #Loop to create list with fixed values of infanrix capacity while varying daptacel capacity
            for j in range(len(cap_range)):
                for i in range(len(cap_range)):
                    K_inf[j*(len(cap_range))+i] = cap_range[j]
                    K_dap[j*(len(cap_range))+i] = cap_range[i]


            #List with constant profit
            P_inf = list(np.linspace(Profit[0],Profit[1], num_samples)) 
            P_dap = list(np.linspace(Profit[0],Profit[1], num_samples))

            #Lists with constant values of demand, gamma, objective cost weight
            D = list(np.linspace(DEM[0],DEM[1], num_samples))
            G = list(np.linspace(GAM[0],GAM[1], num_samples))
            OG = list(np.linspace(OBJ_GOVT[0],OBJ_GOVT[1], num_samples))

            #Inflation bonds - constant
            I_inf = list(np.linspace(M1_INFLATION,M1_INFLATION, num_samples))
            I_dap = list(np.linspace(M2_INFLATION,M2_INFLATION, num_samples))


        #----------------- PROFIT DIFERRENCE TRIALS ----------------------------
        if PROFIT_TRIALS==1:
            
            #make sure the number of samples has an integer square root
            num_samples = (int(num_samples**(1/2)))**2

            Capacity = [4.034e6, 4.034e6]              # Capacity remains constant

            #Profit range
            Profit = [28.45e6, 52.45e6]
            
            Profit_range = np.linspace(Profit[0],Profit[1],int((num_samples)**(1/2)))

            #List with constant capacities
            K_inf = list(np.linspace(Capacity[0],Capacity[1], num_samples))
            K_dap = list(np.linspace(Capacity[0],Capacity[1], num_samples))

            #Profit values    
            #Create initial list to store profit values
            P_inf = [0]*num_samples
            P_dap = [0]*num_samples

            #Loop to create list with fixed values of infanrix profit while varying daptacel profit
            for j in range(len(Profit_range)):
                for i in range(len(Profit_range)):
                    P_inf[j*(len(Profit_range))+i] = Profit_range[j]
                    P_dap[j*(len(Profit_range))+i] = Profit_range[i]

            #Lists with constant values of demand, gamma, objective cost weight
            D = list(np.linspace(DEM[0],DEM[1], num_samples))
            G = list(np.linspace(GAM[0],GAM[1], num_samples))
            OG = list(np.linspace(OBJ_GOVT[0],OBJ_GOVT[1], num_samples))

            #Inflation bonds - constant
            I_inf = list(np.linspace(M1_INFLATION,M1_INFLATION, num_samples))
            I_dap = list(np.linspace(M2_INFLATION,M2_INFLATION, num_samples))



        #----------------- TRIANGULAR DISTRIBUTION TRIALS ----------------------------
        if TRIANGULAR_DISTRIBUTION==1:

            # Get the values for capacity, profit, demand and gamma from triangular distribution
            K_inf = np.random.triangular(2.837e6, 4.034e6, 4.034e6, num_samples)
            K_dap = np.random.triangular(2.837e6, 4.034e6, 4.034e6, num_samples)
            P_inf = np.random.triangular(26.5e6, 39.8e6, 53e6, num_samples)
            P_dap = np.random.triangular(26.5e6, 45.1e6, 53e6, num_samples)
            D = np.random.triangular(4e6, 4.034e6, 7.832e6, num_samples)
            G = np.random.triangular(0.01, 0.25, 0.5, num_samples)
            OG = np.repeat(OBJ_GOVT[0], num_samples)

            #inflation bonds remain constant
            I_inf = np.repeat(M1_INFLATION, num_samples)
            I_dap = np.repeat(M2_INFLATION, num_samples)


        #Convert the results into a dataframe
        df = pd.DataFrame(list(zip(K_inf,K_dap,P_inf,P_dap,D,G,OG,I_inf,I_dap)))
        df.columns = ("m1_cap","m2_cap","m1_prof","m2_prof","dem","gamma",
                        "obj_govt","m1_infl","m2_infl")

        #Compute paremeters a, b and c of the model
        gamma = df.gamma
        a = [1365000+(1553000/(1+gamma)), 1030000+(2389000/(1+gamma))]      # Column 1: Infanrix, column 2: Daptacel
        b = [100000/((1+gamma)*(1-gamma)), 100000/((1+gamma)*(1-gamma))]
        c = [gamma*b[0], gamma*b[1]]

        #Add parameters a, b and c to dataframe
        df['a_pub'] = a[0]; df['a_priv'] = a[1]
        df['b_pub'] = b[0]; df['b_priv'] = b[1]
        df['c_pub'] = c[0]; df['c_priv'] = c[1]
        
        #Generates commands input for NEOS
        path = os.path.join(os.getcwd(),'commands')
        # os.chdir(path)
        file = open(os.path.join(path, file_name), 'w')

        for i in range(df.shape[0]):
            file.writelines('solve;\ndisplay gamma;\ndisplay demand;\ndisplay mu;\ndisplay K;\ndisplay P;'\
                            '\ndisplay price;\ndisplay quant;\ndisplay z;\ndisplay PubCost;\n\n')

            file.writelines('reset data price, quant, z, PubCost;\n\n')
            file.writelines('let gamma := {:.2f};\n'.format(df.gamma[i]));
            file.writelines('let demand := {:.0f};\n'.format(df.dem[i]));
            file.writelines("let a['public'] := {:.4f};\n".format(df.a_pub[i]));   
            file.writelines("let a['private'] := {:.4f};\n".format(df.a_priv[i]));
            file.writelines("let b['public'] := {:.4f};\n".format(df.b_pub[i]));   
            file.writelines("let b['private'] := {:.4f};\n".format(df.b_priv[i]));    
            file.writelines("let c['public'] := {:.4f};\n".format(df.c_pub[i]));   
            file.writelines("let c['private'] := {:.4f};\n".format(df.c_priv[i]));
            file.writelines("let K['x'] := {:.0f};\n".format(df.m1_cap[i]));   
            file.writelines("let K['y'] := {:.0f};\n".format(df.m2_cap[i]));
            file.writelines("let P['x'] := {:.0f};\n".format(df.m1_prof[i]));   
            file.writelines("let P['y'] := {:.0f};\n".format(df.m2_prof[i]));
            file.writelines("let rho['x'] := {:.2f};\n".format(df.m1_infl[i]));   
            file.writelines("let rho['y'] := {:.2f};\n\n".format(df.m2_infl[i])); 

        file.writelines('solve;\ndisplay gamma;\ndisplay demand;\ndisplay mu;\ndisplay K;\ndisplay P;'\
                            '\ndisplay price;\ndisplay quant;\ndisplay z;\ndisplay PubCost;\n\n')
        file.close()


        return
