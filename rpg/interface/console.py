"""Implementação da InterfaceJogo para o terminal (print/input)."""

from collections.abc import Callable

from rpg.entidades.combatente import Combatente
from rpg.interface.interface_jogo import InterfaceJogo


class InterfaceConsole(InterfaceJogo):
    """Único lugar do jogo que usa print() e input().

    As funções de entrada e saída podem ser trocadas no construtor,
    o que permite testar esta classe sem um terminal de verdade.
    """

    TAMANHO_BARRA = 20

    def __init__(
        self,
        entrada: Callable[[str], str] = input,
        saida: Callable[[str], None] = print,
    ) -> None:
        self._entrada = entrada
        self._saida = saida

    def mostrar_mensagem(self, texto: str) -> None:
        self._saida(texto)

    def mostrar_status(self, combatente: Combatente) -> None:
        linha = (
            f"{combatente.nome:<22} "
            f"Vida {self._barra(combatente.vida, combatente.vida_maxima)} "
            f"{combatente.vida:>3}/{combatente.vida_maxima:<3}"
        )
        energia = getattr(combatente, "energia", None)
        if energia is not None:
            linha += f"  Energia {energia}/{getattr(combatente, 'energia_maxima', energia)}"
        self._saida(linha)

    def escolher_opcao(self, titulo: str, opcoes: list[str]) -> int:
        if not opcoes:
            raise ValueError("É preciso ao menos uma opção.")

        self._saida(f"\n{titulo}")
        for numero, opcao in enumerate(opcoes, start=1):
            self._saida(f"  {numero}) {opcao}")

        while True:
            resposta = self._entrada("> ").strip()
            if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
                return int(resposta) - 1
            self._saida(f"Opção inválida. Digite um número de 1 a {len(opcoes)}.")

    def pausar(self) -> None:
        self._entrada("(pressione Enter para continuar)")

    def _barra(self, atual: int, maximo: int) -> str:
        cheios = round(self.TAMANHO_BARRA * atual / maximo) if maximo else 0
        if atual > 0:
            cheios = max(1, cheios)  # quem está vivo sempre aparece com um pedacinho
        return "[" + "█" * cheios + "·" * (self.TAMANHO_BARRA - cheios) + "]"
