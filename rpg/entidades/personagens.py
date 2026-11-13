"""Personagens jogáveis: Michael e suas especialidades de engenharia."""

from abc import abstractmethod

from rpg.entidades.combatente import Combatente
from rpg.habilidades.habilidade import Habilidade


class EnergiaInsuficienteError(Exception):
    """Lançada ao tentar usar uma habilidade sem energia suficiente."""


class Personagem(Combatente):
    """Combatente controlado pelo jogador.

    Herança:    Personagem É UM Combatente (ganha vida, ataque, defesa...).
    Composição: Personagem TEM habilidades (objetos Habilidade guardados numa lista).
    """

    def __init__(
        self,
        nome: str,
        vida_maxima: int,
        ataque: int,
        defesa: int,
        energia_maxima: int,
        habilidades: list[Habilidade],
    ) -> None:
        super().__init__(nome, vida_maxima, ataque, defesa)

        if energia_maxima < 0:
            raise ValueError("A energia máxima não pode ser negativa.")

        self._energia_maxima = energia_maxima
        self._energia = energia_maxima
        self._habilidades = list(habilidades)  # cópia: a lista original não afeta o personagem

    # ------------------------------------------------------------------
    # Propriedades
    # ------------------------------------------------------------------
    @property
    @abstractmethod
    def especialidade(self) -> str:
        """Nome da especialidade de engenharia (ex.: 'Engenheiro Mecânico')."""

    @property
    def energia(self) -> int:
        return self._energia

    @property
    def energia_maxima(self) -> int:
        return self._energia_maxima

    @property
    def habilidades(self) -> tuple[Habilidade, ...]:
        """Devolve uma tupla (imutável) para que ninguém altere a lista interna."""
        return tuple(self._habilidades)

    # ------------------------------------------------------------------
    # Energia e habilidades
    # ------------------------------------------------------------------
    def recuperar_energia(self, quantidade: int) -> int:
        """Recupera energia sem passar do máximo e devolve quanto foi recuperado."""
        if quantidade < 0:
            raise ValueError("A recuperação não pode ser negativa.")

        recuperado = min(quantidade, self._energia_maxima - self._energia)
        self._energia += recuperado
        return recuperado

    def habilidades_disponiveis(self) -> list[Habilidade]:
        """Habilidades que podem ser usadas com a energia atual."""
        return [h for h in self._habilidades if h.pode_usar(self._energia)]

    def usar_habilidade(self, habilidade: Habilidade, alvo: Combatente) -> str:
        """Confere, gasta a energia e executa a habilidade. Devolve a mensagem."""
        if habilidade not in self._habilidades:
            raise ValueError(f"{self.nome} não conhece a habilidade {habilidade.nome}.")
        if not habilidade.pode_usar(self._energia):
            raise EnergiaInsuficienteError(
                f"Energia insuficiente para {habilidade.nome} "
                f"({self._energia}/{habilidade.custo_energia})."
            )

        self._energia -= habilidade.custo_energia
        return habilidade.executar(self, alvo)
