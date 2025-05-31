from gurobipy import Model, GRB, quicksum

def solve(M, N, slices):
    model = Model("pizza")
    model.Params.OutputFlag = 0  # silenzia l'output

    # variabili binarie: x[i] = 1 se prendo la pizza i, altrimenti 0
    x = model.addVars(N, vtype=GRB.BINARY, name="x")

    # vincolo: somma delle fette selezionate ≤ M
    model.addConstr(quicksum(slices[i] * x[i] for i in range(N)) <= M, name="capacity")

    # funzione obiettivo: massimizzare il numero di fette
    model.setObjective(quicksum(slices[i] * x[i] for i in range(N)), GRB.MAXIMIZE)

    # risoluzione
    model.setParam("TimeLimit", 180)     # limite di tempo a 180 secondi
    model.optimize()

    # recupera soluzione
    if model.SolCount > 0:
        # somma delle fette selezionate
        total_slices = sum(slices[i] for i in range(N) if x[i].X > 0.5)
        return total_slices
    else:
        return 0  # nessuna soluzione trovata
