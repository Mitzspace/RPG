"""Quem decide a ação de cada combatente a cada turno.

`Combatente.escolher_acao` delega a decisão para um `Controlador`
(padrão Strategy). Assim, o mesmo Personagem poderia ser controlado por
um humano ou por um robô, e cada inimigo pode ter seu próprio "estilo"
de luta, sem alterar as classes Personagem e Inimigo.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from rpg.combate.acoes import Acao, Atacar, GolpeEspecial, UsarHabilidade, UsarItem
from rpg.entidades.combatente import Combatente
from rpg.habilidades.habilidade import Habilidade
from rpg.interface.interface_jogo import InterfaceJogo

if TYPE_CHECKING:
    from rpg.entidades.personagens import Personagem


class Controlador(ABC):
    """Contrato de qualquer "cérebro" que escolhe ações."""

    @abstractmethod
    def decidir(self, ator: Combatente, oponente: Combatente) -> Acao:
        """Devolve a ação que o `ator` vai realizar neste turno."""


# ----------------------------------------------------------------------
# Jogador humano
# ----------------------------------------------------------------------
class ControladorJogador(Controlador):
    """Pergunta ao jogador, pela InterfaceJogo, o que fazer."""

    OPCOES = ["Atacar", "Usar habilidade", "Usar item"]

    def __init__(self, interface: InterfaceJogo) -> None:
        self._interface = interface

    def decidir(self, ator: Personagem, oponente: Combatente) -> Acao:  # type: ignore[override]
        while True:
            escolha = self._interface.escolher_opcao("O que Michael vai fazer?", self.OPCOES)
            if escolha == 0:
                return Atacar()
            acao = self._escolher_habilidade(ator) if escolha == 1 else self._escolher_item(ator)
            if acao is not None:
                return acao
            # None = o jogador voltou ou não tinha o que usar: mostra o menu de novo.

    def _escolher_habilidade(self, ator: Personagem) -> Acao | None:
        habilidades = list(ator.habilidades)
        opcoes = [self._descrever_habilidade(h, ator.energia) for h in habilidades]
        opcoes.append("Voltar")

        escolha = self._interface.escolher_opcao(
            f"Habilidades (energia: {ator.energia}/{ator.energia_maxima})", opcoes
        )
        if escolha == len(habilidades):
            return None

        habilidade = habilidades[escolha]
        if not habilidade.pode_usar(ator.energia):
            self._interface.mostrar_mensagem(
                f"Energia insuficiente para {habilidade.nome}. Use um Elixir para recuperar."
            )
            return None
        return UsarHabilidade(habilidade)

    @staticmethod
    def _descrever_habilidade(habilidade: Habilidade, energia: int) -> str:
        texto = f"{habilidade.nome} ({habilidade.custo_energia} EN) — {habilidade.descricao}"
        return texto if habilidade.pode_usar(energia) else f"{texto} [sem energia]"

    def _escolher_item(self, ator: Personagem) -> Acao | None:
        grupos = ator.inventario.agrupar_consumiveis()
        if not grupos:
            self._interface.mostrar_mensagem("A bolsa está vazia: não há itens para usar.")
            return None

        opcoes = [f"{item.nome} x{qtd} — {item.descricao}" for item, qtd in grupos]
        opcoes.append("Voltar")

        escolha = self._interface.escolher_opcao("Itens", opcoes)
        if escolha == len(grupos):
            return None
        item, _ = grupos[escolha]
        return UsarItem(item, ator.inventario)


# ----------------------------------------------------------------------
# Estratégias dos inimigos ("IA")
# ----------------------------------------------------------------------
class EstrategiaAgressiva(Controlador):
    """Inimigo comum: ataca em todos os turnos."""

    def decidir(self, ator: Combatente, oponente: Combatente) -> Acao:
        return Atacar()


class EstrategiaChefao(Controlador):
    """Chefão: ataca normalmente e solta o golpe especial a cada `intervalo` turnos.

    O especial é "telegrafado" (sempre no mesmo ritmo) para que o jogador
    possa se preparar, por exemplo curando-se no turno anterior.
    """

    def __init__(self, especial: Habilidade, intervalo: int = 3) -> None:
        if intervalo < 1:
            raise ValueError("O intervalo deve ser pelo menos 1.")
        self._especial = especial
        self._intervalo = intervalo
        self._turno = 0

    @property
    def especial(self) -> Habilidade:
        return self._especial

    def decidir(self, ator: Combatente, oponente: Combatente) -> Acao:
        self._turno += 1
        if self._turno % self._intervalo == 0:
            return GolpeEspecial(self._especial)
        return Atacar()
