from mip import Model, minimize, xsum, CBC, BINARY, INTEGER

'''

Verify sets consistency -> print them and compare

'''

def model(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule):
    
    D = list(planningHorizon)
    S = slots.keys()
    I = patients.keys()
    F = [] #role B
    R = [] #role A
    P = []
    for member in staff.keys():
        P.append(member)
        if staff[member]['Role'] == 'A':
            R.append(member)
        else:
            F.append(member)
    
    C_R = ['1', '10']
    C_F = ['2', '3', '4', '5', '6', '7', '8', '9']
    C = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    U = [90, 180]

    T = U + C

    ld = {}
    i = 0
    for d in D:
        ld[d] = i
        i += 1

    O = {}
    for c1 in C:
        O[c1] = {}
        for c2 in C:
            O[c1][c2] = 0
            if int(c2) == int(c1)+1:
                O[c1][c2] = 1

    c0 = '1'

    a_otimo = 7
    a_min = 4

    b_otimo = {90: 90, 180: 180}
    b_min = {90: 80, 180: 160}

    H = {}
    ####this is due to how schedule was defined
    conversionH_days = {'1': 'SD00', '2': 'SD01','3': 'SD02', '4': 'SD03', '5': 'SD04', '6': 'SD05', '7': 'SD06', '8': 'SD07', '9': 'SD08', '10': 'SD09', 90: 'FD00', 180: 'FD01'}
    conversionH_shifts = {'1': 'SH00', '2': 'SH01', '3': 'SH02', '4': 'SH03', '5': 'SH04', '6': 'SH05','7': 'SH06', '8': 'SH07', '9': 'SH08', '10': 'SH09', 90: 'FH00', 180: 'FH01'}
    for patient in schedule.keys():
        H[patient] = {}
        for t in T:
            H[patient][t] = {}
            for d in D: 
                H[patient][t][d] = {}
                for s in S:
                    H[patient][t][d][s] = 0

        
        
        for t in T:
            if schedule[patient][conversionH_days[t]] != None:
                H[patient][t][schedule[patient][conversionH_days[t]]][schedule[patient][conversionH_shifts[t]]] = 1

    set_N_i = {}
    for patient in N_i.keys():
        set_N_i[patient] = {}
        for d in D:
            set_N_i[patient][d] = {}
            for s in S:
                set_N_i[patient][d][s] = 1 if N_i[patient][d][s] else 0

    set_N_p = {}
    for worker in P:
        set_N_p[worker] = {}
        for d in D:
            set_N_p[worker][d] = {}
            for s in S:
                set_N_p[worker][d][s] = 1 if N_pf[worker][d][s] else 0


    w_consultas_under = 1
    w_consultas_over = 2
    w_follow_under = 10
    w_follow_over = 10
    
    m = Model(solver_name=CBC)

    x = {}
    k_r = {}
    k_f = {}
    v = {}
    y_over = {}
    y_under = {}
    z_over = {}
    z_under = {}
    for i in I:
        x[i] = {}
        k_r[i] = {}
        k_f[i] = {}
        v[i] = {}
        y_over[i] = {}
        y_under[i] = {}
        z_over[i] = {}
        z_under[i] = {}
        for t in T:
            x[i][t] = {}
            for d in D:
                x[i][t][d] = {}
                for s in S:
                    x[i][t][d][s] = m.add_var(var_type=BINARY)
        for f in F:
            k_f[i][f] = m.add_var(var_type=BINARY)
        for r in R:
            k_r[i][r] = m.add_var(var_type=BINARY)

        for p in P:
            v[i][p] = {}
            for d in D:
                v[i][p][d] = {}
                for s in S:
                    v[i][p][d][s] = m.add_var(var_type=BINARY)

        for c in C:
            y_over[i][c] = m.add_var(var_type=INTEGER, lb = 0)
            y_under[i][c] = m.add_var(var_type=INTEGER, lb = 0)
        for u in U:
            z_over[i][u] = m.add_var(var_type=INTEGER, lb = 0)
            z_under[i][u] = m.add_var(var_type=INTEGER, lb = 0)

    m.objective = minimize(xsum((y_over[i][c]*w_consultas_over + y_under[i][c]*w_consultas_under) for i in I for c in C) + xsum((z_over[i][u]*w_follow_over + z_under[i][u]*w_follow_under) for i in I for u in U))

    for i in I:
        m.add_constr(xsum(k_f[i][f] for f in F) == 1) #HC1.A
        m.add_constr(xsum(k_r[i][r] for r in R) == 1) #HC1.B


        for t in T:
            m.add_constr(xsum(x[i][t][d][s] for d in D for s in S) == 1) #HC2

            for d in D:
                for s in S:
                    m.add_constr(x[i][t][d][s] >= H[i][t][d][s]) #HC7

        for f in F:
            m.add_constr(xsum(x[i][c][d][s] for c in C_F for d in D for s in S) <= len(T)*k_f[i][f]) #HC3.A
            for d in D:
                for s in S:
                    m.add_constr(xsum(x[i][c][d][s] for c in C_F) + k_f[i][f] <= 2*v[i][f][d][s]) #HC4.A
        for r in R:
            m.add_constr(xsum(x[i][c][d][s] for c in C_R for d in D for s in S) + xsum(x[i][u][d][s] for u in U for d in D for s in S) <= len(T)*k_r[i][r]) #HC3.B
            for d in D:
                for s in S:
                    m.add_constr(xsum(x[i][c][d][s] for c in C_R) + xsum(x[i][u][d][s] for u in U) + k_r[i][r] <= 2*v[i][r][d][s]) #HC4.B

        for d in D:
            for s in S:
                m.add_constr(xsum(x[i][t][d][s] for t in T) <= set_N_i[i][d][s]) #HC5

        for c1 in C:
            m.add_constr(y_under[i][c] <= a_min) #HC10.A
            for c2 in C:
                if O[c1][c2] == 1:
                    m.add_constr(xsum((x[i][c2][d][s]*ld[d]) for d in D for s in S) - xsum((x[i][c1][d][s])*ld[d] for d in D for s in S) - y_over[i][c2] + y_under[i][c2] == a_otimo) #HC8
        for u in U:
            m.add_constr(xsum(x[i][u][d][s]*ld[d] for d in D for s in S) - xsum(x[i][c0][d][s]*ld[d] for d in D for s in S) - z_over[i][u] + z_under[i][u] == b_otimo[u]) #HC9
            m.add_constr(z_under[i][u] <= b_min[u]) #HC10.B

    for p in P:
        for d in D:
            for s in S:
                m.add_constr(xsum(v[i][p][d][s] for i in I) <= set_N_p[p][d][s]) #HC6
    
    status = m.optimize(max_seconds = 60)
    print(status, m.objective_value)
    
    exit()
    