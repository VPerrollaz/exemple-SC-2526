"""Description.

Tests unitaire du module resolution
"""

import numpy as np
import pytest
from exemple_sc_2526.data import ProblemeTransport, SolutionTransport
from exemple_sc_2526.resolution import resolution, construction_matrices


def test_construction_simple():
    """Problème simplissime."""
    probleme = ProblemeTransport(
        entrepots=[2.0],
        clients=[1.0],
        couts_unitaires=[1.0],
    )
    Aeq, Aub = construction_matrices(probleme=probleme)
    assert Aeq.shape == (1, 1)
    assert Aub.shape == (1, 1)
    assert Aeq == np.array([[1.0]])
    assert Aub == np.array([[1.0]])


def test_construction_v2():
    probleme = ProblemeTransport(
        entrepots=[1.0, 1.0],
        clients=[2.0],
        couts_unitaires=[1.0, 1.0],
    )
    Aeq, Aub = construction_matrices(probleme=probleme)
    assert Aeq.shape == (1, 2)
    assert Aub.shape == (2, 2)
    assert np.array_equal(Aeq, np.array([[1.0, 1.0]]))
    assert np.array_equal(Aub, np.array([[1.0, 0.0], [0.0, 1.0]]))


def test_construction_v2_dual():
    probleme = ProblemeTransport(
        entrepots=[2.0],
        clients=[1.0, 1.0],
        couts_unitaires=[1.0, 1.0],
    )
    Aeq, Aub = construction_matrices(probleme=probleme)
    assert Aeq.shape == (2, 2)
    assert Aub.shape == (1, 2)
    assert np.array_equal(Aub, np.array([[1.0, 1.0]]))
    assert np.array_equal(Aeq, np.array([[1.0, 0.0], [0.0, 1.0]]))


def test_construction_v3():
    """Problème simplissime."""
    probleme = ProblemeTransport(
        entrepots=[1.0, 1.0],
        clients=[1.5, 0.5],
        couts_unitaires=[1.0, 1.0, 1.0, 1.0],
    )
    Aeq, Aub = construction_matrices(probleme=probleme)
    assert Aeq.shape == (2, 4)
    assert Aub.shape == (2, 4)
    assert np.array_equal(Aeq, np.array([[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0]]))
    assert np.array_equal(Aub, np.array([[1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0]]))


def test_resolution_simple():
    """Problème simplissime."""
    probleme = ProblemeTransport(
        entrepots=[2.0],
        clients=[1.0],
        couts_unitaires=[1.0],
    )
    attendue = SolutionTransport(
        probleme=probleme,
        solution=[1.0],
    )
    calculee = resolution(probleme=probleme)
    assert calculee == attendue


def test_resolution_niveau2():
    """Problème simplissime."""
    probleme = ProblemeTransport(
        entrepots=[1.0, 1.0],
        clients=[2.0],
        couts_unitaires=[1.0, 1.0],
    )
    attendue = SolutionTransport(
        probleme=probleme,
        solution=[1.0, 1.0],
    )
    calculee = resolution(probleme=probleme)
    assert calculee == attendue


def test_resolution_niveau2_dual():
    """Problème simplissime."""
    probleme = ProblemeTransport(
        entrepots=[2.0],
        clients=[1.0, 1.0],
        couts_unitaires=[1.0, 1.0],
    )
    attendue = SolutionTransport(
        probleme=probleme,
        solution=[1.0, 1.0],
    )
    calculee = resolution(probleme=probleme)
    assert calculee == attendue


def test_resolution_niveau3():
    """Problème simplissime."""
    probleme = ProblemeTransport(
        entrepots=[1.0, 1.0],
        clients=[1.0],
        couts_unitaires=[2.0, 1.0],
    )
    attendue = SolutionTransport(
        probleme=probleme,
        solution=[0.0, 1.0],
    )
    calculee = resolution(probleme=probleme)
    assert calculee == attendue
