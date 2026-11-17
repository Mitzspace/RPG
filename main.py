"""Ponto de entrada: python main.py"""

import sys

from rpg.interface.console import InterfaceConsole
from rpg.jogo import Jogo


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos e símbolos no Windows

    interface = InterfaceConsole()
    try:
        while True:
            Jogo(interface).iniciar()
            if interface.escolher_opcao("Jogar novamente?", ["Sim", "Não"]) == 1:
                break
    except (KeyboardInterrupt, EOFError):
        print("\n\nAté a próxima, Mercúcio!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
