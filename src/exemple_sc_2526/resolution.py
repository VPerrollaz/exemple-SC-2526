"""Description.

Implémentation de la résolution d'un problème de transport.
"""

from scipy import optimize
import numpy as np
from .data import ProblemeTransport, SolutionTransport


def construction_matrices(
    probleme: ProblemeTransport,
) -> tuple[np.ndarray, np.ndarray]:
    """Construction des matrices de contraintes de la programmation linéaire."""
    n, m = len(probleme.entrepots), len(probleme.clients)
    Aub = np.zeros((n, m * n))
    Aeq = np.zeros((m, m * n))
    for i in range(n):
        for j in range(m):
            Aub[i, i * len(probleme.clients) + j] = 1.0
    for j in range(m):
        for i in range(n):
            Aeq[j, i * len(probleme.clients) + j] = 1.0

    return Aeq, Aub


def resolution(probleme: ProblemeTransport) -> SolutionTransport:
    c = np.array(probleme.couts_unitaires)
    beq = np.array(probleme.clients)
    bub = np.array(probleme.entrepots)
    Aeq, Aub = construction_matrices(probleme=probleme)
    solution_abstraite = optimize.linprog(
        c=c, A_eq=Aeq, b_eq=beq, A_ub=Aub, b_ub=bub, bounds=(0, None)
    )
    return SolutionTransport(
        probleme=probleme,
        solution=solution_abstraite.x,
    )
