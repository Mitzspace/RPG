import pytest

from tests.auxiliares import ControladorFixo, InterfaceFalsa
from rpg.combate.acoes import Atacar
from rpg.entidades.inimigos import Inimigo
from rpg.entidades.personagens import EngenheiroMecanico, Personagem
from rpg.historia import roteiro
from rpg.historia.capitulo import Campanha, Capitulo
from rpg.itens import itens
from rpg.itens.item import Encaixe
from rpg.jogo import Jogo


class Heroi(Personagem):
    """Personagem de testes, forte o bastante para vencer tudo só atacando.
    Mostra que qualquer subclasse de Personagem funciona na campanha (Liskov)."""

    def __init__(self):
        super().__init__("Herói", 9999, 999, 999, 0, [], controlador=ControladorFixo(Atacar))

    @property
    def especialidade(self):
        return "Testador"


def capitulo_simples(recompensas=()):
    return Capitulo(
        "Teste", ["abertura"], [lambda: Inimigo("Rato", 10, 1, 0)], ["desfecho"], list(recompensas)
    )


def test_campanha_completa_com_o_roteiro_real():
    ui = InterfaceFalsa()
    heroi = Heroi()
    campanha = Campanha(heroi, roteiro.criar_capitulos(), ui, roteiro.FINAL_FELIZ, roteiro.GAME_OVER)
    assert campanha.jogar() is True
    assert campanha.capitulo_atual == 3
    texto = ui.texto()
    for nome in ("Criado Capuleto", "Teobaldo", "Guarda da Cripta", "Conde Páris"):
        assert nome in texto
    assert "FINAL FELIZ" in texto
    # recompensas do Frei Lourenço
    assert set(heroi.equipamentos) == {Encaixe.ARMA, Encaixe.ARMADURA}
    assert len(heroi.inventario) == 6


def test_derrota_mostra_game_over():
    ui = InterfaceFalsa()
    jogador = EngenheiroMecanico(controlador=ControladorFixo(Atacar))
    capitulo = Capitulo("Impossível", [], [lambda: Inimigo("Dragão", 9999, 999, 0)], [])
    campanha = Campanha(jogador, [capitulo], ui, game_over=roteiro.GAME_OVER)
    assert campanha.jogar() is False
    assert campanha.capitulo_atual == 0
    assert "A tragédia se repete..." in ui.texto()


def test_recompensas_e_troca_de_equipamento():
    from rpg.itens.itens import Arma
    ui = InterfaceFalsa()
    jogador = EngenheiroMecanico(controlador=ControladorFixo(Atacar))
    caps = [capitulo_simples([itens.florete_de_aco, itens.elixir]),
            capitulo_simples([lambda: Arma("Rapieira", "+6 de ataque", 6)])]
    assert Campanha(jogador, caps, ui).jogar()
    assert jogador.equipamentos[Encaixe.ARMA].nome == "Rapieira"
    assert "no lugar de Florete de Aço" in ui.texto()
    assert len(jogador.inventario) == 1


def test_descanso_so_entre_capitulos():
    ui = InterfaceFalsa()
    jogador = EngenheiroMecanico(controlador=ControladorFixo(Atacar))
    capitulo = Capitulo("Dor", [], [lambda: Inimigo("Espinho", 20, 30, 0)], [])
    Campanha(jogador, [capitulo, capitulo], ui).jogar()
    assert ui.texto().count("descansa no mosteiro") == 1
    assert jogador.vida < jogador.vida_maxima  # depois do último capítulo não há descanso


def test_campanha_vazia():
    with pytest.raises(ValueError):
        Campanha(Heroi(), [], InterfaceFalsa())


@pytest.mark.parametrize("escolha, especialidade", [
    (0, "Engenheiro Mecânico"), (1, "Engenheiro Químico"), (2, "Engenheiro Civil"),
])
def test_jogo_cria_jogador_escolhido(escolha, especialidade):
    jogador = Jogo(InterfaceFalsa([escolha])).criar_jogador()
    assert jogador.especialidade == especialidade
    assert len(jogador.inventario) == 3
    assert jogador.controlador is not None


def test_partida_completa_pelos_menus():
    """Joga o jogo de verdade pelos menus: Químico, sempre a Pólvora Rudimentar
    quando há energia, senão Elixir, senão ataque. Sem aleatoriedade, é determinístico."""

    class Robo(InterfaceFalsa):
        def __init__(self):
            super().__init__()
            self._plano = []

        def escolher_opcao(self, titulo, opcoes):
            self.menus.append((titulo, opcoes))
            if titulo.startswith("Antes do acidente"):
                return 1  # Engenheiro Químico
            return self._plano.pop(0) if self._plano else 0

        def mostrar_status(self, combatente):
            super().mostrar_status(combatente)
            if combatente.nome == "Michael":
                self._plano = self._planejar(combatente)

        def _planejar(self, j):
            if j.vida < j.vida_maxima * 0.35 and self._tem(j, "Ervas"):
                return [2, self._indice(j, "Ervas")]
            if j.energia >= 15:
                return [1, 0]
            if self._tem(j, "Elixir"):
                return [2, self._indice(j, "Elixir")]
            return [0]

        @staticmethod
        def _tem(j, nome):
            return any(nome in item.nome for item in j.inventario.itens)

        @staticmethod
        def _indice(j, nome):
            grupos = j.inventario.agrupar_consumiveis()
            return next(n for n, (item, _) in enumerate(grupos) if nome in item.nome)

    ui = Robo()
    assert Jogo(ui).iniciar() is True
    assert "FINAL FELIZ" in ui.texto()
