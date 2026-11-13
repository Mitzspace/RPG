"""Base abstrata para todos que participam de uma batalha."""

from abc import ABC, abstractmethod


class Combatente(ABC):
    """Representa qualquer ser que luta: o jogador (Michael) ou um inimigo.

    Não pode ser instanciada diretamente — serve apenas de molde para as
    subclasses concretas (Personagem, Inimigo).
    """

    DANO_MINIMO = 1

    def __init__(self, nome: str, vida_maxima: int, ataque: int, defesa: int) -> None:
        if vida_maxima <= 0:
            raise ValueError("A vida máxima deve ser maior que zero.")
        if ataque < 0 or defesa < 0:
            raise ValueError("Ataque e defesa não podem ser negativos.")

        self._nome = nome
        self._vida_maxima = vida_maxima
        self._vida = vida_maxima
        self._ataque = ataque
        self._defesa = defesa

    # ------------------------------------------------------------------
    # Propriedades (somente leitura para quem está de fora)
    # ------------------------------------------------------------------
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def vida(self) -> int:
        return self._vida

    @property
    def vida_maxima(self) -> int:
        return self._vida_maxima

    @property
    def ataque(self) -> int:
        return self._ataque

    @property
    def defesa(self) -> int:
        return self._defesa

    # ------------------------------------------------------------------
    # Comportamentos comuns a todos os combatentes
    # ------------------------------------------------------------------
    def esta_vivo(self) -> bool:
        return self._vida > 0

    def receber_dano(self, dano: int, ignorar_defesa: bool = False) -> int:
        """Aplica o dano e devolve quanto de vida foi realmente perdido."""
        if dano < 0:
            raise ValueError("O dano não pode ser negativo.")

        reducao = 0 if ignorar_defesa else self.defesa
        dano_real = max(self.DANO_MINIMO, dano - reducao)
        dano_real = min(dano_real, self._vida)  # a vida nunca fica negativa

        self._vida -= dano_real
        return dano_real

    def curar(self, quantidade: int) -> int:
        """Recupera vida sem ultrapassar o máximo e devolve quanto foi curado."""
        if quantidade < 0:
            raise ValueError("A cura não pode ser negativa.")

        curado = min(quantidade, self._vida_maxima - self._vida)
        self._vida += curado
        return curado

    # ------------------------------------------------------------------
    # Comportamento que cada tipo de combatente define do seu jeito
    # ------------------------------------------------------------------
    @abstractmethod
    def escolher_acao(self, oponente: "Combatente"):
        """Decide o que fazer no turno (atacar, usar habilidade, item...).

        - Personagem: pergunta ao jogador.
        - Inimigo: decide com base na sua estratégia ("IA").
        """
