"""Description.

Tests unitaires du module data
"""

import pytest
from pydantic import ValidationError
from exemple_sc_2526.data import ProblemeTransport, SolutionTransport


def test_verifications_probleme_transport_entrepots():
    with pytest.raises(ValidationError):
        ProblemeTransport(entrepots=[], clients=[1.0], couts_unitaires=[1.0])


def test_verifications_probleme_transport_clients():
    with pytest.raises(ValidationError):
        ProblemeTransport(entrepots=[1.0], clients=[], couts_unitaires=[1.0])


def test_verifications_probleme_transport_couts():
    with pytest.raises(ValidationError):
        ProblemeTransport(entrepots=[1.0, 2.0], clients=[1.0], couts_unitaires=[1.0])


def test_verifications_probleme_transport_quantites():
    with pytest.raises(ValidationError):
        ProblemeTransport(entrepots=[1.0], clients=[2.0], couts_unitaires=[1.0])


def test_solution_transport():
    probleme = ProblemeTransport(
        entrepots=[1.0, 2.0], clients=[1.0], couts_unitaires=[1.0, 1.0]
    )
    solution = SolutionTransport(probleme=probleme, solution=[1.0, 0.0])
    assert isinstance(solution, SolutionTransport)


def test_verifications_solution_transport_dimension():
    probleme = ProblemeTransport(entrepots=[2.0], clients=[1.0], couts_unitaires=[1.0])
    with pytest.raises(ValidationError):
        SolutionTransport(probleme=probleme, solution=[1.0, 1.0])


def test_verifications_solution_transport_livraison():
    probleme = ProblemeTransport(
        entrepots=[1.0, 2.0], clients=[2.0], couts_unitaires=[1.0, 1.0]
    )
    with pytest.raises(ValidationError):
        SolutionTransport(probleme=probleme, solution=[1.0, 0.0])


def test_verifications_solution_transport_stock():
    probleme = ProblemeTransport(
        entrepots=[1.0, 2.0], clients=[2.0], couts_unitaires=[1.0, 1.0]
    )
    with pytest.raises(ValidationError):
        SolutionTransport(probleme=probleme, solution=[2.0, 0.0])
