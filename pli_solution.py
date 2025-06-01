from gurobipy import Model, GRB, quicksum
import time
import sys
import os
from contextlib import contextmanager

@contextmanager
def suppress_stdout():          # per evitare che gurobi scriva sul terminale
    with open(os.devnull, 'w') as devnull:
        old_stdout = os.dup(1)
        os.dup2(devnull.fileno(), 1)
        try:
            yield
        finally:
            os.dup2(old_stdout, 1)
            os.close(old_stdout)

def solve(M, N, slices):
    start_time = time.perf_counter()
    with suppress_stdout():
        model = Model("pizza")
        model.Params.OutputFlag = 0  # silenzia l'output

        # cerchiamo di rendere quanto più confrontabile possibile la soluzione di gurobi
        model.Params.Threads = 1 
        model.Params.MIPGap = 0.0
        model.Params.Presolve = 0
        model.Params.Heuristics = 0
        model.Params.TimeLimit = 60

        # variabili binarie: x[i] = 1 se prendo la pizza i, altrimenti 0
        x = model.addVars(N, vtype=GRB.BINARY, name="x")

        # vincolo: somma delle fette selezionate ≤ M
        model.addConstr(quicksum(slices[i] * x[i] for i in range(N)) <= M, name="capacity")

        # funzione obiettivo: massimizzare il numero di fette
        model.setObjective(quicksum(slices[i] * x[i] for i in range(N)), GRB.MAXIMIZE)

        # risoluzione
        model.optimize()

        # recupera soluzione
        if model.SolCount > 0:
            total_slices = sum(slices[i] for i in range(N) if x[i].X > 0.5) # somma delle fette selezionate
            elapsed = time.perf_counter() - start_time
            return total_slices, elapsed
        else:
            elapsed = time.perf_counter() - start_time
            return 0, elapsed  # nessuna soluzione trovata
