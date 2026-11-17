"""Inimigos e chefões de Verona."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rpg.combate.controladores import Controlador, EstrategiaAgressiva, EstrategiaChefao
from rpg.entidades.combatente import Combatente
from rpg.habilidades.habilidades import GolpePerfurante, GolpePoderoso

if TYPE_CHECKING:
    from rpg.combate.acoes import Acao


class Inimigo(Combatente):
    """Combatente controlado pelo computador.

    A forma de lutar não está aqui: ela vem de um Controlador (estratégia)
    recebido no construtor. Trocar a estratégia muda o comportamento sem
    alterar esta classe.
    """

    def __init__(
        self,
        nome: str,
        vida_maxima: int,
        ataque: int,
        defesa: int,
        estrategia: Controlador | None = None,
        fala: str = "",
    ) -> None:
        super().__init__(nome, vida_maxima, ataque, defesa)
        self._estrategia = estrategia or EstrategiaAgressiva()
        self._fala = fala

    @property
    def fala(self) -> str:
        """Frase dita ao entrar em combate (pode ser vazia)."""
        return self._fala

    @property
    def eh_chefao(self) -> bool:
        return False

    def escolher_acao(self, oponente: Combatente) -> Acao:
        return self._estrategia.decidir(self, oponente)


class Chefao(Inimigo):
    """Inimigo mais forte, que encerra um capítulo e tem um golpe especial."""

    def __init__(
        self,
        nome: str,
        vida_maxima: int,
        ataque: int,
        defesa: int,
        estrategia: EstrategiaChefao,
        fala: str = "",
    ) -> None:
        super().__init__(nome, vida_maxima, ataque, defesa, estrategia, fala)

    @property
    def eh_chefao(self) -> bool:
        return True


# ----------------------------------------------------------------------
# Catálogo de inimigos da história (cada chamada cria um inimigo novo)
# ----------------------------------------------------------------------
def criado_capuleto() -> Inimigo:
    return Inimigo(
        "Criado Capuleto", vida_maxima=40, ataque=11, defesa=2,
        fala="Mordes o polegar para nós, senhor?",
    )


def capanga_de_teobaldo() -> Chefao:
    especial = GolpePoderoso("Soco Pesado", "dano 1,5x", custo_energia=0, multiplicador=1.5)
    return Chefao(
        "Capanga de Teobaldo", vida_maxima=75, ataque=14, defesa=4,
        estrategia=EstrategiaChefao(especial, intervalo=3),
        fala="O senhor Teobaldo mandou lembranças, Mercúcio!",
    )


def teobaldo() -> Chefao:
    especial = GolpePoderoso("Estocada Furiosa", "dano 1,8x", custo_energia=0, multiplicador=1.8)
    return Chefao(
        "Teobaldo", vida_maxima=140, ataque=18, defesa=6,
        estrategia=EstrategiaChefao(especial, intervalo=3),
        fala="Mercúcio, tu andas em companhia de Romeu... Defende-te!",
    )


def guarda_da_cripta() -> Inimigo:
    return Inimigo(
        "Guarda da Cripta", vida_maxima=60, ataque=15, defesa=5,
        fala="Ninguém perturba o descanso dos Capuletos!",
    )


def conde_paris() -> Chefao:
    especial = GolpePerfurante("Lâmina Nobre", "ignora a defesa", custo_energia=0, multiplicador=1.3)
    return Chefao(
        "Conde Páris", vida_maxima=170, ataque=20, defesa=7,
        estrategia=EstrategiaChefao(especial, intervalo=3),
        fala="Vil Montéquio! Vens profanar o túmulo de minha noiva?",
    )
