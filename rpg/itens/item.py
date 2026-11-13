"""Abstrações dos itens do jogo.

A hierarquia é separada em interfaces pequenas (Segregação de Interfaces):

    Item
    ├── Consumivel   -> itens que se usam e acabam (ervas, elixir)
    └── Equipavel    -> itens que se vestem/empunham (florete, gibão)
"""

from abc import ABC, abstractmethod
from enum import Enum

from rpg.entidades.combatente import Combatente


class Item(ABC):
    """Base comum a todo item: apenas nome e descrição."""

    def __init__(self, nome: str, descricao: str) -> None:
        if not nome:
            raise ValueError("O item precisa de um nome.")
        self._nome = nome
        self._descricao = descricao

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def descricao(self) -> str:
        return self._descricao


class Consumivel(Item):
    """Item de uso único: ao ser usado, aplica um efeito e sai do inventário."""

    @abstractmethod
    def usar(self, alvo: Combatente) -> str:
        """Aplica o efeito no alvo e devolve uma mensagem do que aconteceu."""


class Encaixe(Enum):
    """Onde um equipamento é colocado. Só cabe um item por encaixe."""

    ARMA = "arma"
    ARMADURA = "armadura"


class Equipavel(Item):
    """Item que fica equipado e concede bônus enquanto estiver em uso."""

    @property
    @abstractmethod
    def encaixe(self) -> Encaixe:
        """Em qual encaixe o item é colocado (arma ou armadura)."""

    @property
    @abstractmethod
    def bonus_ataque(self) -> int:
        """Quanto de ataque o item acrescenta."""

    @property
    @abstractmethod
    def bonus_defesa(self) -> int:
        """Quanto de defesa o item acrescenta."""
