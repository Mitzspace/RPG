"""Estrutura de um capítulo e a campanha que os encadeia."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from rpg.combate.batalha import Batalha, ResultadoBatalha
from rpg.entidades.inimigos import Inimigo
from rpg.entidades.personagens import Personagem
from rpg.interface.interface_jogo import InterfaceJogo
from rpg.itens.item import Consumivel, Equipavel, Item


@dataclass
class Capitulo:
    """Dados de um capítulo. Não tem lógica: quem o joga é a Campanha.

    `inimigos` guarda FÁBRICAS (funções que criam o inimigo), para que cada
    partida comece com inimigos novos, de vida cheia.
    """

    titulo: str
    abertura: list[str]
    inimigos: list[Callable[[], Inimigo]]
    desfecho: list[str]
    recompensas: list[Callable[[], Item]] = field(default_factory=list)


class Campanha:
    """Joga os capítulos em ordem e diz se o jogador chegou ao final feliz."""

    def __init__(
        self,
        jogador: Personagem,
        capitulos: list[Capitulo],
        interface: InterfaceJogo,
        final_feliz: list[str] | None = None,
        game_over: list[str] | None = None,
    ) -> None:
        if not capitulos:
            raise ValueError("A campanha precisa de pelo menos um capítulo.")
        self._jogador = jogador
        self._capitulos = list(capitulos)
        self._interface = interface
        self._final_feliz = final_feliz or ["Fim."]
        self._game_over = game_over or ["Game Over."]
        self._capitulo_atual = 0

    @property
    def capitulo_atual(self) -> int:
        """Quantos capítulos já foram concluídos."""
        return self._capitulo_atual

    def jogar(self) -> bool:
        """Devolve True se o jogador venceu a campanha."""
        for numero, capitulo in enumerate(self._capitulos, start=1):
            if not self._jogar_capitulo(numero, capitulo):
                self._narrar(self._game_over)
                return False
            self._capitulo_atual = numero
            if numero < len(self._capitulos):
                self._jogador.descansar()
                self._interface.mostrar_mensagem(
                    "Michael descansa no mosteiro: vida e energia restauradas."
                )
                self._interface.pausar()
        self._narrar(self._final_feliz)
        return True

    def _jogar_capitulo(self, numero: int, capitulo: Capitulo) -> bool:
        ui = self._interface
        ui.mostrar_mensagem(f"\n{'=' * 60}\n  Capítulo {numero}: {capitulo.titulo}\n{'=' * 60}")
        self._narrar(capitulo.abertura)

        for fabrica in capitulo.inimigos:
            resultado = Batalha(self._jogador, fabrica(), ui).executar()
            if resultado is ResultadoBatalha.DERROTA:
                return False
            ui.pausar()

        self._narrar(capitulo.desfecho)
        self._entregar_recompensas(capitulo)
        return True

    def _entregar_recompensas(self, capitulo: Capitulo) -> None:
        if not capitulo.recompensas:
            return
        ui = self._interface
        ui.mostrar_mensagem("\nFrei Lourenço entrega a Michael:")
        for fabrica in capitulo.recompensas:
            item = fabrica()
            if isinstance(item, Equipavel):
                anterior = self._jogador.equipar(item)
                troca = f" (no lugar de {anterior.nome})" if anterior else ""
                ui.mostrar_mensagem(f"  • {item.nome} — {item.descricao}. Equipado{troca}!")
            elif isinstance(item, Consumivel):
                self._jogador.inventario.adicionar(item)
                ui.mostrar_mensagem(f"  • {item.nome} — {item.descricao}.")

    def _narrar(self, textos: list[str]) -> None:
        for texto in textos:
            self._interface.mostrar_mensagem(f"\n{texto}")
        if textos:
            self._interface.pausar()
