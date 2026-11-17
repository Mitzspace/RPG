from tests.auxiliares import Boneco, ControladorFixo, InterfaceFalsa
from rpg.combate.acoes import Atacar, UsarHabilidade, UsarItem
from rpg.combate.batalha import Batalha, ResultadoBatalha
from rpg.combate.controladores import ControladorJogador
from rpg.entidades.inimigos import Inimigo
from rpg.entidades.personagens import EngenheiroMecanico, EngenheiroQuimico
from rpg.itens import itens
from rpg.itens.inventario import Inventario

ATACAR, HABILIDADE, ITEM = 0, 1, 2


def test_acao_atacar():
    atacante, alvo = Boneco(ataque=10), Boneco(vida=50, defesa=3)
    assert "7 de dano" in Atacar().executar(atacante, alvo)


def test_acao_usar_item_remove_do_inventario():
    erva = itens.ervas_frei_lourenco()
    jogador = EngenheiroMecanico(inventario=Inventario([erva]))
    jogador.receber_dano(60, ignorar_defesa=True)
    UsarItem(erva, jogador.inventario).executar(jogador, Boneco())
    assert len(jogador.inventario) == 0
    assert jogador.vida == jogador.vida_maxima - 60 + 40


# ----------------------------------------------------------------------
# Controlador do jogador (menus)
# ----------------------------------------------------------------------
def test_jogador_escolhe_atacar():
    acao = ControladorJogador(InterfaceFalsa([ATACAR])).decidir(EngenheiroMecanico(), Boneco())
    assert isinstance(acao, Atacar)


def test_jogador_escolhe_habilidade():
    jogador = EngenheiroMecanico()
    acao = ControladorJogador(InterfaceFalsa([HABILIDADE, 1])).decidir(jogador, Boneco())
    assert isinstance(acao, UsarHabilidade)
    assert acao.habilidade is jogador.habilidades[1]


def test_voltar_do_menu_de_habilidades():
    ui = InterfaceFalsa([HABILIDADE, 2, ATACAR])  # 2 = "Voltar"
    assert isinstance(ControladorJogador(ui).decidir(EngenheiroMecanico(), Boneco()), Atacar)
    assert len(ui.menus) == 3


def test_habilidade_sem_energia_volta_ao_menu():
    jogador = EngenheiroMecanico()
    for _ in range(3):
        jogador.usar_habilidade(jogador.habilidades[0], Boneco(vida=999))
    ui = InterfaceFalsa([HABILIDADE, 0, ATACAR])
    assert isinstance(ControladorJogador(ui).decidir(jogador, Boneco()), Atacar)
    assert "Energia insuficiente" in ui.texto()
    assert "[sem energia]" in ui.menus[1][1][0]


def test_jogador_usa_item():
    jogador = EngenheiroMecanico(inventario=Inventario([itens.elixir(), itens.elixir()]))
    ui = InterfaceFalsa([ITEM, 0])
    acao = ControladorJogador(ui).decidir(jogador, Boneco())
    assert isinstance(acao, UsarItem)
    assert "Elixir x2" in ui.menus[1][1][0]


def test_bolsa_vazia():
    ui = InterfaceFalsa([ITEM, ATACAR])
    assert isinstance(ControladorJogador(ui).decidir(EngenheiroMecanico(), Boneco()), Atacar)
    assert "bolsa está vazia" in ui.texto()


# ----------------------------------------------------------------------
# Batalha
# ----------------------------------------------------------------------
def test_vitoria():
    ui = InterfaceFalsa()
    jogador = EngenheiroQuimico(controlador=ControladorFixo(Atacar))
    inimigo = Inimigo("Saco de Pancada", vida_maxima=30, ataque=0, defesa=0, fala="Oi!")
    batalha = Batalha(jogador, inimigo, ui)
    assert batalha.executar() is ResultadoBatalha.VITORIA
    assert batalha.turno == 2  # 20 de dano por turno -> 2 turnos
    assert 'Saco de Pancada: "Oi!"' in ui.texto()


def test_derrota():
    jogador = EngenheiroQuimico(controlador=ControladorFixo(Atacar))
    inimigo = Inimigo("Gigante", vida_maxima=999, ataque=200, defesa=0)
    assert Batalha(jogador, inimigo, InterfaceFalsa()).executar() is ResultadoBatalha.DERROTA
    assert not jogador.esta_vivo()


def test_inimigo_morto_nao_contra_ataca():
    jogador = EngenheiroQuimico(controlador=ControladorFixo(Atacar))
    inimigo = Inimigo("Frágil", vida_maxima=1, ataque=50, defesa=0)
    Batalha(jogador, inimigo, InterfaceFalsa()).executar()
    assert jogador.vida == jogador.vida_maxima
