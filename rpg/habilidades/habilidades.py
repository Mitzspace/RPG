"""Habilidades concretas.

São poucas classes GENÉRICAS (um tipo de efeito cada), configuradas por
parâmetros. As habilidades com nome da história ("Golpe de Alavanca",
"Fumaça Tóxica"...) são apenas instâncias dessas classes, criadas pelos
personagens e pelos chefões.
"""

import random

from rpg.entidades.combatente import Combatente
from rpg.habilidades.habilidade import Habilidade


class GolpePoderoso(Habilidade):
    """Ataque com o dano multiplicado (a defesa do alvo ainda reduz)."""

    def __init__(self, nome: str, descricao: str, custo_energia: int, multiplicador: float) -> None:
        super().__init__(nome, descricao, custo_energia)
        if multiplicador <= 0:
            raise ValueError("O multiplicador deve ser positivo.")
        self._multiplicador = multiplicador

    @property
    def multiplicador(self) -> float:
        return self._multiplicador

    def executar(self, usuario: Combatente, alvo: Combatente) -> str:
        dano = alvo.receber_dano(round(usuario.ataque * self._multiplicador))
        return f"{usuario.nome} usa {self.nome}! {alvo.nome} sofre {dano} de dano."


class GolpePerfurante(GolpePoderoso):
    """Como o GolpePoderoso, mas o dano ignora a defesa do alvo."""

    def executar(self, usuario: Combatente, alvo: Combatente) -> str:
        dano = alvo.receber_dano(round(usuario.ataque * self.multiplicador), ignorar_defesa=True)
        return (
            f"{usuario.nome} usa {self.nome}! A defesa de {alvo.nome} não adianta: "
            f"{dano} de dano."
        )


class GolpeCritico(Habilidade):
    """Ataque com chance de acerto crítico.

    O gerador de números aleatórios é recebido no construtor (Inversão de
    Dependência): no jogo é aleatório, nos testes é previsível.
    """

    def __init__(
        self,
        nome: str,
        descricao: str,
        custo_energia: int,
        chance_critico: float,
        multiplicador_critico: float,
        multiplicador_normal: float = 1.0,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(nome, descricao, custo_energia)
        if not 0 <= chance_critico <= 1:
            raise ValueError("A chance de crítico deve estar entre 0 e 1.")
        self._chance = chance_critico
        self._mult_critico = multiplicador_critico
        self._mult_normal = multiplicador_normal
        self._rng = rng or random.Random()

    def executar(self, usuario: Combatente, alvo: Combatente) -> str:
        critico = self._rng.random() < self._chance
        multiplicador = self._mult_critico if critico else self._mult_normal
        dano = alvo.receber_dano(round(usuario.ataque * multiplicador))
        if critico:
            return f"{usuario.nome} usa {self.nome}... ACERTO CRÍTICO! {alvo.nome} sofre {dano} de dano."
        return f"{usuario.nome} usa {self.nome}. {alvo.nome} sofre {dano} de dano."


class Reparo(Habilidade):
    """Recupera uma porcentagem da vida máxima de quem usa."""

    def __init__(self, nome: str, descricao: str, custo_energia: int, percentual: float) -> None:
        super().__init__(nome, descricao, custo_energia)
        if not 0 < percentual <= 1:
            raise ValueError("O percentual deve estar entre 0 e 1.")
        self._percentual = percentual

    def executar(self, usuario: Combatente, alvo: Combatente) -> str:
        curado = usuario.curar(round(usuario.vida_maxima * self._percentual))
        return f"{usuario.nome} usa {self.nome} e recupera {curado} de vida."
