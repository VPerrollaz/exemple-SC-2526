"""Description.

Module implémentant les objets représentant le problème et sa solution.
"""

from pydantic import BaseModel, PositiveFloat, NonNegativeFloat, model_validator
from typing import Self


class ProblemeTransport(BaseModel):
    """Encode les données d'un prolème."""

    entrepots: list[PositiveFloat]
    clients: list[PositiveFloat]
    couts_unitaires: list[PositiveFloat]

    @model_validator(mode="after")
    def verifie_compatibilite(self) -> Self:
        if len(self.entrepots) == 0:
            msg = "Il faut au moins un entrepot"
            raise ValueError(msg)
        if len(self.clients) == 0:
            msg = "Il faut au moins un client"
            raise ValueError(msg)
        if len(self.clients) * len(self.entrepots) != len(self.couts_unitaires):
            msg = "il doit y avoir exactement un cout par couple entrepot/client"
            raise ValueError(msg)
        if sum(self.entrepots) < sum(self.clients):
            msg = "il doit y avoir plus de quantité disponible que de demandes"
            raise ValueError(msg)

        return self


class SolutionTransport(BaseModel):
    """Encode une solution d'un problème de transport."""

    probleme: ProblemeTransport
    solution: list[NonNegativeFloat]

    @model_validator(mode="after")
    def verifie_compatibilite(self) -> Self:
        if len(self.solution) != len(self.probleme.couts_unitaires):
            msg = "il doit y avoir exactement une quantité transportée par couple entrepot/client"
            raise ValueError(msg)
        return self
