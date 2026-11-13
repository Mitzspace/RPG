"""Abstração de entrada e saída do jogo.

A batalha e a história conversam com o jogador SOMENTE por esta interface,
nunca chamando print()/input() diretamente (Inversão de Dependência).
Assim, o mesmo jogo pode rodar no console, em testes automatizados ou,
no futuro, em uma interface gráfica — basta criar outra implementação.
"""

from abc import ABC, abstractmethod

from rpg.entidades.combatente import Combatente


class InterfaceJogo(ABC):
    """Contrato que toda forma de interagir com o jogador deve cumprir."""

    @abstractmethod
    def mostrar_mensagem(self, texto: str) -> None:
        """Exibe um texto ao jogador (narração, resultado de ataque...)."""

    @abstractmethod
    def mostrar_status(self, combatente: Combatente) -> None:
        """Exibe a situação atual de um combatente (nome, vida...)."""

    @abstractmethod
    def escolher_opcao(self, titulo: str, opcoes: list[str]) -> int:
        """Apresenta um menu e devolve o ÍNDICE da opção escolhida.

        O retorno é sempre válido: um número entre 0 e len(opcoes) - 1.
        Cabe à implementação insistir até o jogador escolher algo válido.
        """

    @abstractmethod
    def pausar(self) -> None:
        """Espera o jogador antes de continuar (ex.: 'Pressione Enter')."""
