"""Batalha em turnos entre Michael e um inimigo."""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from rpg.interface.interface_jogo import InterfaceJogo

if TYPE_CHECKING:
    from rpg.entidades.inimigos import Inimigo
    from rpg.entidades.personagens import Personagem


class ResultadoBatalha(Enum):
    VITORIA = auto()
    DERROTA = auto()


class Batalha:
    """Conduz os turnos: o jogador age primeiro, depois o inimigo.

    A Batalha só organiza a ordem dos turnos. Ela não sabe calcular dano
    (isso é do Combatente e das ações) nem como escrever na tela (isso é
    da InterfaceJogo) — Responsabilidade Única.
    """

    LIMITE_TURNOS = 200  # trava de segurança contra laços infinitos

    def __init__(self, jogador: Personagem, inimigo: Inimigo, interface: InterfaceJogo) -> None:
        self._jogador = jogador
        self._inimigo = inimigo
        self._interface = interface
        self._turno = 0

    @property
    def turno(self) -> int:
        return self._turno

    def executar(self) -> ResultadoBatalha:
        ui = self._interface
        ui.mostrar_mensagem(f"\n⚔  {self._inimigo.nome} entra em combate!")
        if self._inimigo.fala:
            ui.mostrar_mensagem(f'{self._inimigo.nome}: "{self._inimigo.fala}"')

        while self._jogador.esta_vivo() and self._inimigo.esta_vivo():
            self._turno += 1
            if self._turno > self.LIMITE_TURNOS:
                raise RuntimeError("A batalha passou do limite de turnos.")

            ui.mostrar_mensagem(f"\n——— Turno {self._turno} ———")
            ui.mostrar_status(self._jogador)
            ui.mostrar_status(self._inimigo)

            for ator, alvo in ((self._jogador, self._inimigo), (self._inimigo, self._jogador)):
                acao = ator.escolher_acao(alvo)
                ui.mostrar_mensagem(acao.executar(ator, alvo))
                if not alvo.esta_vivo():
                    break

        if self._jogador.esta_vivo():
            ui.mostrar_mensagem(f"\n★ {self._inimigo.nome} foi derrotado!")
            return ResultadoBatalha.VITORIA

        ui.mostrar_mensagem(f"\n✝ {self._jogador.nome} caiu diante de {self._inimigo.nome}...")
        return ResultadoBatalha.DERROTA
