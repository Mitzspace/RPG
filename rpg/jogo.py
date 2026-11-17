"""Montagem do jogo: liga personagem, controlador, história e interface."""

from rpg.combate.controladores import ControladorJogador
from rpg.entidades.personagens import ESPECIALIDADES, Personagem
from rpg.historia import roteiro
from rpg.historia.capitulo import Campanha
from rpg.interface.interface_jogo import InterfaceJogo
from rpg.itens import itens
from rpg.itens.inventario import Inventario


class Jogo:
    """Ponto de montagem. Recebe a interface pronta (Inversão de Dependência)."""

    def __init__(self, interface: InterfaceJogo) -> None:
        self._interface = interface

    def iniciar(self) -> bool:
        """Joga uma partida completa. Devolve True em caso de vitória."""
        ui = self._interface
        ui.mostrar_mensagem(f"\n{'#' * 60}\n{roteiro.TITULO:^60}\n{'#' * 60}")
        for texto in roteiro.PROLOGO:
            ui.mostrar_mensagem(f"\n{texto}")
        ui.pausar()

        jogador = self.criar_jogador()
        ui.mostrar_mensagem(
            f"\nMichael era {jogador.especialidade}. "
            f"Vida {jogador.vida_maxima} | Ataque {jogador.ataque} | "
            f"Defesa {jogador.defesa} | Energia {jogador.energia_maxima}"
        )

        campanha = Campanha(
            jogador, roteiro.criar_capitulos(), ui,
            final_feliz=roteiro.FINAL_FELIZ, game_over=roteiro.GAME_OVER,
        )
        return campanha.jogar()

    def criar_jogador(self) -> Personagem:
        opcoes = []
        for classe in ESPECIALIDADES:
            exemplo = classe()
            opcoes.append(
                f"{exemplo.especialidade:<20} — Vida {exemplo.vida_maxima}, "
                f"Ataque {exemplo.ataque}, Defesa {exemplo.defesa}, Energia {exemplo.energia_maxima}"
            )
        escolha = self._interface.escolher_opcao(roteiro.PERGUNTA_ESPECIALIDADE, opcoes)

        inventario = Inventario([itens.ervas_frei_lourenco(), itens.ervas_frei_lourenco(), itens.elixir()])
        return ESPECIALIDADES[escolha](
            inventario=inventario, controlador=ControladorJogador(self._interface)
        )
