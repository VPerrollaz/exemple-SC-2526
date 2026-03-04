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
        for indice_entrepot in ...:
            expedition = sum(
                self[indice_entrepot, indice_client] for indice_client in ...
            )
            if expedition > self.probleme.entrepots[indice_entrepot]:
                msg = f"Trop expédié depuis l'entrepot d'indice {indice_entrepot}"
                raise ValueError(msg)
        for indice_client in ...:
            reception = sum(
                self[indice_entrepot, indice_client] for indice_entrepot in ...
            )
            if reception != self.probleme.clients[indice_client]:
                msg = f"Le client d'indice {indice_client} n'a pas reçu la bonne quantité de marchandise"
                raise ValueError(msg)
        return self

    def __getitem__(self, indice: tuple[int, int]) -> NonNegativeFloat:
        i, j = indice
        return self.solution[i * len(self.probleme.clients) + j]
