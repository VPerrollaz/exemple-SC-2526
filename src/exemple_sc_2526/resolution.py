"""Description.

Implémentation de la résolution d'un problème de transport.
"""
from scipy import optimize
import numpy as np
from .data import ProblemeTransport, SolutionTransport

def resolution(probleme: ProblemeTransport) -> SolutionTransport:
    c = np.array(probleme.couts_unitaires)
    n, m = len(probleme.entrepots), len(probleme.clients)
    Aeq = np.fromfunction(
        lambda (i,k): 1. if (1 <= (k - (i-1) * m) <= m) else 0., 
        shape=(m, m * n)
    )
    beq = np.array(probleme.clients)
    Aub = np.fromfunction(
        lambda (j,k): 1. if 1 <= (1 + (k - j) // m) <=n else 0., 
        shape=(n, n * m)
    )
    bub = np.array(probleme.entrepots)
    solution_abstraite = optimize.linprog(
        c=c, A_eq=Aeq, b_eq=beq, A_ub=Aub, b_ub=bub, bounds=(0, None)
    )
    ...
