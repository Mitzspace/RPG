"""Ações que um combatente pode realizar em seu turno.

Cada ação é um objeto com um único método, `executar` (padrão Command).
A batalha não precisa saber QUAL ação foi escolhida: ela apenas chama
`executar` e mostra a mensagem devolvida (Polimorfismo + Aberto/Fechado —
uma ação nova, como "Defender", seria só mais uma subclasse).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from rpg.entidades.combatente import Combatente
from rpg.habilidades.habilidade import Habilidade
from rpg.itens.item import Consumivel

if TYPE_CHECKING:
    from rpg.entidades.personagens import Personagem
    from rpg.itens.inventario import Inventario


class Acao(ABC):
    """Algo que o `ator` faz no turno, normalmente contra o `alvo`."""

    @abstractmethod
    def executar(self, ator: Combatente, alvo: Combatente) -> str:
        """Realiza a ação e devolve uma mensagem descrevendo o resultado."""


class Atacar(Acao):
    """Ataque básico: o dano é o ataque do ator menos a defesa do alvo."""

    def executar(self, ator: Combatente, alvo: Combatente) -> str:
        dano = alvo.receber_dano(ator.ataque)
        return f"{ator.nome} ataca {alvo.nome} e causa {dano} de dano."


class UsarHabilidade(Acao):
    """O jogador usa uma habilidade, gastando energia."""

    def __init__(self, habilidade: Habilidade) -> None:
        self._habilidade = habilidade

    @property
    def habilidade(self) -> Habilidade:
        return self._habilidade

    def executar(self, ator: Personagem, alvo: Combatente) -> str:  # type: ignore[override]
        # Quem confere e gasta a energia é o Personagem (Responsabilidade Única).
        return ator.usar_habilidade(self._habilidade, alvo)


class GolpeEspecial(Acao):
    """Um inimigo usa sua habilidade especial (inimigos não têm energia)."""

    def __init__(self, habilidade: Habilidade) -> None:
        self._habilidade = habilidade

    @property
    def habilidade(self) -> Habilidade:
        return self._habilidade

    def executar(self, ator: Combatente, alvo: Combatente) -> str:
        return self._habilidade.executar(ator, alvo)


class UsarItem(Acao):
    """O ator usa um item consumível do inventário em si mesmo."""

    def __init__(self, item: Consumivel, inventario: Inventario) -> None:
        self._item = item
        self._inventario = inventario

    @property
    def item(self) -> Consumivel:
        return self._item

    def executar(self, ator: Combatente, alvo: Combatente) -> str:
        self._inventario.remover(self._item)
        return self._item.usar(ator)
