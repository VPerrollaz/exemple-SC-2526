"""Description.

Module implémentant les objets représentant le problème et sa solution.
"""

from pydantic import BaseModel, PositiveFloat, NonNegativeFloat, model_validator
from typing import Self


class ProblemeTransport(BaseModel):
    """Encode les données d'un prolème.

    n entrepots, m clients, n*m couts unitaires de transport
    le cout unitaire de transport de l'entrepot i vers le client est stocké à la position i * m + j

    Avant la création de l'objet on vérifie que
    - le nombre d'entrepots est strictement positif
    - le nombre de clients est strictement positif
    - le nombre de couts unitaires de transport est cohérent
    - le stock est supérieur ou égal à la demande

    Exemples:

    >>> ProblemeTransport(entrepots=[], clients=[1.0], couts_unitaires=[1.0])
    Traceback (most recent call last):
    File "<python-input-2>", line 1, in <module>
        ProblemeTransport(entrepots=[], clients=[1.0], couts_unitaires=[1.0])
        ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Value error, Il faut au moins un entrepot [type=value_error, input_value={'entrepots': [], 'client...couts_unitaires': [1.0]}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.12/v/value_error
    >>> ProblemeTransport(entrepots=[1.0], clients=[], couts_unitaires=[1.0])
    Traceback (most recent call last):
    File "<python-input-3>", line 1, in <module>
        ProblemeTransport(entrepots=[1.0], clients=[], couts_unitaires=[1.0])
        ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Value error, Il faut au moins un client [type=value_error, input_value={'entrepots': [1.0], 'cli...couts_unitaires': [1.0]}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.12/v/value_error
    """

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

    @property
    def nombre_clients(self):
        return len(self.probleme.clients)

    @property
    def nombre_entrepots(self):
        return len(self.probleme.entrepots)

    @model_validator(mode="after")
    def verifie_compatibilite(self) -> Self:
        if len(self.solution) != len(self.probleme.couts_unitaires):
            msg = "il doit y avoir exactement une quantité transportée par couple entrepot/client"
            raise ValueError(msg)
        for indice_entrepot in range(self.nombre_entrepots):
            expedition = sum(
                self[indice_entrepot, indice_client]
                for indice_client in range(len(self.probleme.clients))
            )
            if expedition > self.probleme.entrepots[indice_entrepot]:
                msg = f"Trop expédié depuis l'entrepot d'indice {indice_entrepot}"
                raise ValueError(msg)
        for indice_client in range(self.nombre_clients):
            reception = sum(
                self[indice_entrepot, indice_client]
                for indice_entrepot in range(self.nombre_entrepots)
            )
            if reception != self.probleme.clients[indice_client]:
                msg = f"Le client d'indice {indice_client} n'a pas reçu la bonne quantité de marchandise"
                raise ValueError(msg)
        return self

    def __getitem__(self, indice: tuple[int, int]) -> NonNegativeFloat:
        i, j = indice
        return self.solution[i * len(self.probleme.clients) + j]
