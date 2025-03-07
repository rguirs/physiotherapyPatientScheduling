from mip import Model, minimize, xsum, CBC, BINARY, INTEGER

'''

Review how data is plugged -> migrate from dict to matrix
Review mathematical model
Finish the implementation of the model
Join as much loops as possible
Use "sum variables" if possible and correct

'''

def model(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule):
    
    D = len(planningHorizon)
    S = len(slots)
    S_itr = [slot for slot in slots.keys()]
    I = len(patients)
    I_itr = [patient for patient in patients.keys()]
    N_i_ds = N_i
    
    all_researchers = []
    all_physio = []
    N_f_ds = []
    N_p_ds = []
    for staffMember in staff:
        if staff[staffMember]["Role"] == "A":
            all_researchers.append(staffMember)
            N_p_ds.append(N_pf[staffMember])
        else:
            all_physio.append(staffMember)
            N_f_ds.append(N_pf[staffMember])
    P = len(all_researchers)
    F = len(all_physio)
    
    C = 10
    c0 = 0
    c1 = 1
    c8 = 8
    c9 = 9
    C_P = len([c0, c9])
    C_F = len([i for i in range(c1,c9)])
    C_x = len([i for i in range(c9)])
    a_expect = 7
    U = 2
    b_expect_u = [90, 180]
    
    m = Model(solver_name=CBC)
    m.verbose = 0

    x_pc_ids = m.add_var_tensor((P, C_P, I, D, S), "x_pc_ids")
    x_fc_ids = m.add_var_tensor((P, C_F, I, D, S), "x_fc_ids")
    x_pu_ids = m.add_var_tensor((P, U, I, D, S), "x_pu_ids")
    
    w_ip = m.add_var_tensor((I, P), "w_ip")
    w_if = m.add_var_tensor((I, F), "w_if")
    
    k_ids = m.add_var_tensor((I, D, S), "k_ids")
    k_pds = m.add_var_tensor((P, D, S), "k_pds")
    k_fds = m.add_var_tensor((F, D, S), "k_fds")
    
    y_ic = m.add_var_tensor((I, C_x), "y_ic")
    y_iu = m.add_var_tensor((I, U), "y_iu")
    z_ic = m.add_var_tensor((I, C_x), "z_ic")
    z_iu = m.add_var_tensor((I, U), "z_iu")
    
    v_ipf = m.add_var_tensor((I, P, F), "v_ipf")
    
    #Objective
    print("obj")
    m.objective = minimize(xsum(y_ic[i][c] for i in range(I) for c in range(C_x)) + xsum(y_iu[i][u] for i in range(I) for u in range(U)) + xsum(z_ic[i][c] for i in range(I) for c in range(C_x)) + xsum(z_iu[i][u] for i in range(I) for u in range(U)))
    
    print("l1")
    for i in range(I):
        m.add_constr(xsum(w_ip[i][p] for p in range(P)) == 1)
        m.add_constr(xsum(w_if[i][f] for f in range(F)) == 1)
        
        for p in range(P):
            for f in range(F):
                m.add_constr(w_ip[i][p] + w_if[i][f] <= 1 + v_ipf[i][p][f])
                
            for c in range(C_P):
                m.add_constr(xsum(x_pc_ids[p][c][i][d][s] for d in range(D) for s in range(S)) == w_ip[i][p])
            for u in range(U):
                m.add_constr(xsum(x_pu_ids[p][u][i][d][s] for d in range(D) for s in range(S)) == w_ip[i][p])
            for c in range(C_F):
                m.add_constr(xsum(x_fc_ids[p][c][i][d][s] for d in range(D) for s in range(S)) == w_ip[i][p])
                
    print("l2")
    for d in range(D):
        for s in range(S):
            for p in range(P):
                m.add_constr(k_pds[p][d][s] == xsum(x_pc_ids[p][c][i][d][s] for i in range(I) for c in range(C_P)) + xsum(x_pu_ids[p][u][i][d][s] for i in range(I) for u in range(U)))
            for f in range(F):
                m.add_constr(k_fds[f][d][s] == xsum(x_fc_ids[p][c][i][d][s] for i in range(I) for c in range(C_F)))
            for i in range(I):
                m.add_constr(k_ids[i][d][s] == xsum(x_pc_ids[p][c][i][d][s] for i in range(I) for c in range(C_P)) + xsum(x_fc_ids[f][c][i][d][s] for i in range(I) for c in range(C_F)) + xsum(x_pu_ids[p][u][i][d][s] for i in range(I) for u in range(U)))
                
            for i in range(I):
                if not N_i_ds[I_itr[i]][planningHorizon[d]][S_itr[s]]:
                    m.add_constr(k_ids[i][d][s] == 0)
            for p in range(P):
                if not N_p_ds[p][planningHorizon[d]][S_itr[s]]:
                    m.add_constr(k_pds[p][d][s] == 0)
            for f in range(F):
                if not N_f_ds[f][planningHorizon[d]][S_itr[s]]:
                    m.add_constr(k_fds[f][d][s] == 0)
                    
    print("l3")
    # for i in range(I):
        # for f in range(F):
            # for c in range(C_F):
                # m.add_constr(xsum(x_fc_ids[f][c+1][i][d][s]))
    
    print("Done")
    
    exit()
    