"""Base abstrata para as habilidades especiais dos personagens."""

from abc import ABC, abstractmethod

from rpg.entidades.combatente import Combatente


class Habilidade(ABC):
    """Uma ação especial que consome energia (ex.: Golpe de Alavanca).

    Cada habilidade concreta herda desta classe e implementa `executar`.
    Para criar uma habilidade nova, basta criar uma nova subclasse —
    nenhum código existente precisa ser alterado (Aberto/Fechado).
    """

    def __init__(self, nome: str, descricao: str, custo_energia: int) -> None:
        if not nome:
            raise ValueError("A habilidade precisa de um nome.")
        if custo_energia < 0:
            raise ValueError("O custo de energia não pode ser negativo.")

        self._nome = nome
        self._descricao = descricao
        self._custo_energia = custo_energia

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def custo_energia(self) -> int:
        return self._custo_energia

    def pode_usar(self, energia_disponivel: int) -> bool:
        """Indica se há energia suficiente para usar a habilidade."""
        return energia_disponivel >= self._custo_energia

    @abstractmethod
    def executar(self, usuario: Combatente, alvo: Combatente) -> str:
        """Aplica o efeito da habilidade e devolve uma mensagem do que aconteceu.

        Não gasta energia: isso é responsabilidade de quem usa a habilidade
        (o Personagem), que confere `pode_usar` antes de chamar este método.
        """
