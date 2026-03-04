"""Description.

Tests unitaires du module data
"""

import pytest
from pydantic import ValidationError
from exemple_sc_2526.data import ProblemeTransport, SolutionTransport


def test_verifications_probleme_transport():
    with pytest.raises(ValidationError):
        ...
