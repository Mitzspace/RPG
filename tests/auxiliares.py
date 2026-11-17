"""Ferramentas compartilhadas pelos testes."""

import random

from rpg.combate.acoes import Acao
from rpg.combate.controladores import Controlador
from rpg.entidades.combatente import Combatente
from rpg.interface.interface_jogo import InterfaceJogo


class InterfaceFalsa(InterfaceJogo):
    """Interface de testes: responde menus com uma lista de escolhas
    pré-definidas e grava tudo o que seria exibido."""

    def __init__(self, escolhas: list[int] | None = None, padrao: int = 0) -> None:
        self.escolhas = list(escolhas or [])
        self.padrao = padrao
        self.mensagens: list[str] = []
        self.menus: list[tuple[str, list[str]]] = []
        self.pausas = 0

    def mostrar_mensagem(self, texto: str) -> None:
        self.mensagens.append(texto)

    def mostrar_status(self, combatente: Combatente) -> None:
        self.mensagens.append(f"[status] {combatente.nome} {combatente.vida}")

    def escolher_opcao(self, titulo: str, opcoes: list[str]) -> int:
        self.menus.append((titulo, list(opcoes)))
        return self.escolhas.pop(0) if self.escolhas else self.padrao

    def pausar(self) -> None:
        self.pausas += 1

    def texto(self) -> str:
        return "\n".join(self.mensagens)


class ControladorFixo(Controlador):
    """Sempre devolve ações produzidas pela fábrica recebida."""

    def __init__(self, fabrica):
        self._fabrica = fabrica

    def decidir(self, ator: Combatente, oponente: Combatente) -> Acao:
        return self._fabrica()


class Boneco(Combatente):
    """Combatente concreto mínimo, usado como alvo nos testes."""

    def __init__(self, nome="Boneco", vida=100, ataque=10, defesa=0):
        super().__init__(nome, vida, ataque, defesa)

    def escolher_acao(self, oponente):
        raise NotImplementedError


class RngFixo(random.Random):
    """Gerador "aleatório" que devolve sempre o mesmo valor."""

    def __init__(self, valor: float) -> None:
        super().__init__()
        self.valor = valor

    def random(self) -> float:
        return self.valor
