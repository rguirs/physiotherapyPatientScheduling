import gurobipy as gp
from gurobipy import GRB

'''

Verify sets consistency -> print them and compare

create smallest instance as possible

check if it is possible to change heuristic's behaviour to fit different kinds of sessions [i.e. r-p-r could be r-r-p-p-r-p-p-r...]

check feasibility of instances

'''

def model(initialDay, planningHorizon, slots, staff, patients, N_i, N_pf, schedule, asStart = False):
    
    m = gp.Model()
    
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

    G = {}
    for i in I:
        G[i] = {}
        for p in P:
            G[i][p] = 0

        if patients[i]['researcher'] != None:
            G[i][patients[i]['researcher']] = 1
        if patients[i]['physio'] != None:
            G[i][patients[i]['physio']] = 1
    
    C_R = ['1', '10']
    C_F = ['2', '3', '4', '5', '6', '7', '8', '9']
    C = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    U = [90, 180]

    T = U + C

    ld = {}
    for i in range(len(D)):
        ld[D[i]] = (planningHorizon[i] - planningHorizon[0]).days

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
    b_min = {90: 75, 180: 165}

    set_N_i = {}
    for patient in N_i.keys():
        set_N_i[patient] = {}
        for d in D:
            set_N_i[patient][d] = {}
            for s in S:
                set_N_i[patient][d][s] = 1 if N_i[patient][d][s] else 0

    # mockPassN_I = {}
    # for patient in N_i.keys():
    #     mockPassN_I[patient] = {}
    #     for d in D:
    #         mockPassN_I[patient][d] = {}
    #         for s in S:
    #             mockPassN_I[patient][d][s] = m.addVar(vtype=GRB.BINARY, lb = 0)

    set_N_p = {}
    for worker in P:
        set_N_p[worker] = {}
        for d in D:
            set_N_p[worker][d] = {}
            for s in S:
                set_N_p[worker][d][s] = 1 if N_pf[worker][d][s] else 0

    # mockPassN_p = {}
    # for worker in P:
    #     mockPassN_p[worker] = {}
    #     for d in D:
    #         mockPassN_p[worker][d] = {}
    #         for s in S:
    #             mockPassN_p[worker][d][s] = m.addVar(vtype=GRB.INTEGER, lb = 0)

    # mockPassV = {}
    # for i in I:
    #     mockPassV[i] = {}
    #     for p in P:
    #         mockPassV[i][p] = {}
    #         for d in D:
    #             mockPassV[i][p][d] = {}
    #             for s in S:
    #                 mockPassV[i][p][d][s] = m.addVar(vtype=GRB.INTEGER, lb = 0)


    w_consultas_under = 1
    w_consultas_over = 2
    w_follow_under = 10
    w_follow_over = 10
    w_duracao = 1

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
                    x[i][t][d][s] = m.addVar(vtype=GRB.BINARY)
        for f in F:
            k_f[i][f] = m.addVar(vtype=GRB.BINARY)
        for r in R:
            k_r[i][r] = m.addVar(vtype=GRB.BINARY)

        for p in P:
            v[i][p] = {}
            for d in D:
                v[i][p][d] = {}
                for s in S:
                    v[i][p][d][s] = m.addVar(vtype=GRB.BINARY)

        for c in C:
            y_over[i][c] = m.addVar(vtype=GRB.CONTINUOUS, lb = 0)
            y_under[i][c] = m.addVar(vtype=GRB.CONTINUOUS, lb = 0)
        for u in U:
            z_over[i][u] = m.addVar(vtype=GRB.CONTINUOUS, lb = 0)
            z_under[i][u] = m.addVar(vtype=GRB.CONTINUOUS, lb = 0)
    q = m.addVar(vtype=GRB.CONTINUOUS, lb = 0)

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
        
        if not asStart:
            for t in T:
                if schedule[patient][conversionH_days[t]] != None:
                    H[patient][t][schedule[patient][conversionH_days[t]]][schedule[patient][conversionH_shifts[t]]] = 1
        else:
            for t in T:
                for d in D: 
                    for s in S:
                        x[patient][t][d][s].Start = 0

            for t in T:
                if schedule[patient][conversionH_days[t]] != None:
                    x[patient][t][schedule[patient][conversionH_days[t]]][schedule[patient][conversionH_shifts[t]]].Start = 1

    m.setObjective(sum((y_over[i][c]*w_consultas_over + y_under[i][c]*w_consultas_under) for i in I for c in C) + sum((z_over[i][u]*w_follow_over + z_under[i][u]*w_follow_under) for i in I for u in U) + q*w_duracao, GRB.MINIMIZE)
    # m.setObjective(sum(mockPassN_p[p][d][s] for p in P for d in D for s in S) + sum(mockPassN_I[i][d][s] for i in I for d in D for s in S))
    # m.setObjective(sum(mockPassN_p[p][d][s] for p in P for d in D for s in S) + sum(mockPassN_I[i][d][s] for i in I for d in D for s in S) + sum((y_over[i][c]*w_consultas_over + y_under[i][c]*w_consultas_under) for i in I for c in C) + sum((z_over[i][u]*w_follow_over + z_under[i][u]*w_follow_under) for i in I for u in U)) 

    for i in I:
        m.addConstr(sum(k_f[i][f] for f in F) >= G[i][f]) #HC1.A
        m.addConstr(sum(k_r[i][r] for r in R) >= G[i][r]) #HC1.B
        m.addConstr(sum(k_f[i][f] for f in F) == 1) #HC1.A
        m.addConstr(sum(k_r[i][r] for r in R) == 1) #HC1.B


        for t in T:
            m.addConstr(sum(x[i][t][d][s] for d in D for s in S) == 1) #HC2

            for d in D:
                for s in S:
                    m.addConstr(x[i][t][d][s] >= H[i][t][d][s]) #HC11
                if d < initialDay:
                    m.addConstr(x[i][t][d][s] <= H[i][t][d][s]) #HC11

        for f in F:
            # m.addConstr(sum(x[i][c][d][s] for c in C_F for d in D for s in S) <= len(T)*k_f[i][f]) #HC3.A
            for d in D:
                for s in S:
                    m.addConstr(sum(x[i][c][d][s] for c in C_F) + k_f[i][f] <= 1 + v[i][f][d][s]) #HC4.A
        for r in R:
            # m.addConstr(sum(x[i][c][d][s] for c in C_R for d in D for s in S) + sum(x[i][u][d][s] for u in U for d in D for s in S) <= len(T)*k_r[i][r]) #HC3.B
            for d in D:
                for s in S:
                    m.addConstr(sum(x[i][c][d][s] for c in C_R) + sum(x[i][u][d][s] for u in U) + k_r[i][r] <= 1 + v[i][r][d][s]) #HC4.B

        for d in D:
            for s in S:
                m.addConstr(sum(x[i][t][d][s] for t in T) <= set_N_i[i][d][s]) #HC6n

        for c1 in C:
            m.addConstr(a_otimo - y_under[i][c1] >= a_min) #HC9.A
            for c2 in C:
                if O[c1][c2] == 1:
                    m.addConstr(sum((x[i][c2][d][s]*ld[d]) for d in D for s in S) - sum((x[i][c1][d][s])*ld[d] for d in D for s in S) - y_over[i][c2] + y_under[i][c2] == a_otimo) #HC7
        for u in U:
            m.addConstr(sum(x[i][u][d][s]*ld[d] for d in D for s in S) - sum(x[i][c0][d][s]*ld[d] for d in D for s in S) - z_over[i][u] + z_under[i][u] == b_otimo[u]) #HC8
            m.addConstr(b_otimo[u] - z_under[i][u] >= b_min[u]) #HC9.B

    for p in P:
        for d in D:
            for s in S:
                m.addConstr(sum(v[i][p][d][s] for i in I) <= set_N_p[p][d][s]) #HC5n
                # m.addConstr(sum(v[i][p][d][s] for i in I) <= 1)

                for i in I:
                    m.addConstr(q >= v[i][p][d][s]*ld[d]) #HC10
    
    # m.setParam('SolutionLimit', 1)
    # m.setParam('MIPFocus', 3)
    m.setParam('TimeLimit', 900)
    m.optimize()
    
    if m.Status == GRB.INFEASIBLE:
        return False, None, None, None

    print(m.Status, m.ObjVal)

    for patient in patients:

        for f in F:
            if k_f[patient][f].X >= 0.5:
                patients[patient]['physio'] = f

        for r in R:
            if k_r[patient][r].X >= 0.5:
                patients[patient]['researcher'] = r

    for patient in schedule.keys():

        for t in T:

            for d in D:
                for s in S:
                    if x[patient][t][d][s].X >= 0.5:
                        schedule[patient][schedule[patient][conversionH_days[t]]] = d
                        schedule[patient][schedule[patient][conversionH_shifts[t]]] = s

    return True, patients, schedule, N_pf

    # for p in P:
    #     for d in [D[0]]:
    #         for s in S:
    #             if sum(v[i][p][d][s].X for i in I) > set_N_p[p][d][s]:
    #                 print("-", sum(v[i][p][d][s].X for i in I), p, d, s, set_N_p[p][d][s])
    #                 k = []
    #                 getI = []
    #                 for i in I:
    #                     if p in F:
    #                         k.append(k_f[i][p].X)
    #                     if p in R:
    #                         k.append(k_r[i][p].X)
    #                     if k[-1] == 1:
    #                         getI.append(i)
    #                 print("k", k)
    #                 for i in getI:
    #                     if p in F:
    #                         if sum(x[i][c][d][s].X for c in C_F) >= 1:
    #                             print("*p",sum(x[i][c][d][s].X for c in C_F))
    #                             showC = []
    #                             for c in C_F:
    #                                 showC.append(x[i][c][d][s].X)
    #                             print("cf",showC, i)
    #                     if p in R:
    #                         if sum(x[i][c][d][s].X for c in C_R) + sum(x[i][u][d][s].X for u in U) >= 1:
    #                             print("*r", sum(x[i][c][d][s].X for c in C_R), sum(x[i][u][d][s].X for u in U))
    #                             showC = []
    #                             for c in C_R:
    #                                 showC.append(x[i][c][d][s].X)
    #                             for u in U:
    #                                 showC.append(x[i][u][d][s].X)
    #                             print("cr",showC, i, sum(x[i][c_][d_][s_].X for c_ in C_R for d_ in D for s_ in S), sum(x[i][u_][d_][s_].X for u_ in U for d_ in D for s_ in S), G[i][p])

    # for i in I:
    #     for u in U:
    #         print(b_otimo[u], z_under[i][u].X, b_min[u], i, u, sum(x[i][u][d][s].X*ld[d] for d in D for s in S), sum(x[i][c0][d][s].X*ld[d] for d in D for s in S), z_over[i][u].X)
    #         for d in D:
    #             for s in S:
    #                 if H[i][u][d][s] > 0:
    #                     print(H[i][u][d][s], d, ld[d], s)

    # for i in I:
    #     for d in D:
    #         for s in S:
    #             if mockPassN_I[i][d][s].X > 0:
    #                 print("I_MOCK", i, d, s, mockPassN_I[i][d][s].X, set_N_i[i][d][s], N_i[i][d][s])

    # for p in P:
    #     for d in D:
    #         for s in S:
    #             if mockPassN_p[p][d][s].X > 0:
    #                 print("P_MOCK", p, d, s, mockPassN_p[p][d][s].X, set_N_p[p][d][s], N_pf[worker][d][s])


    # for i in I:
    #     for f in F:
    #         for d in D:
    #             for s in S:
    #                 teste = sum(x[i][c][d][s].X for c in C_F)
    #                 if teste > 1:
    #                     print("!", teste)

    # for i in I:
    #     for r in R:
    #         for d in D:
    #             for s in S:
    #                 testeA = sum(x[i][c][d][s].X for c in C_R)
    #                 testeB = sum(x[i][u][d][s].X for u in U)
    #                 if testeA + testeB > 1:
    #                     print(testeA+testeB, testeA, testeB)

    # print("==============")

    # for i in I:
    #     for p in P:
    #         for d in D:
    #             for s in S:
    #                 if v[i][p][d][s].X > 1:
    #                     print(v[i][p][d][s].X, i, p, d, s, sum(x[i][c][d][s].X for c in C_F), sum(x[i][u][d][s].X for u in U))
    