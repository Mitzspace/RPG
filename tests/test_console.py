import pytest

from tests.auxiliares import Boneco
from rpg.entidades.personagens import EngenheiroMecanico
from rpg.interface.console import InterfaceConsole


def criar(respostas):
    saida = []
    respostas = iter(respostas)
    return InterfaceConsole(entrada=lambda _: next(respostas), saida=saida.append), saida


def test_escolher_opcao_insiste_ate_valida():
    ui, saida = criar(["abc", "0", "4", " 2 "])
    assert ui.escolher_opcao("Menu", ["a", "b", "c"]) == 1
    assert sum("Opção inválida" in s for s in saida) == 3
    assert "  1) a" in saida


def test_escolher_sem_opcoes():
    ui, _ = criar([])
    with pytest.raises(ValueError):
        ui.escolher_opcao("Menu", [])


def test_status_mostra_barra_e_energia():
    ui, saida = criar([])
    jogador = EngenheiroMecanico()
    jogador.receber_dano(65)
    ui.mostrar_status(jogador)
    assert "73/130" in saida[0]
    assert "Energia 30/30" in saida[0]
    ui.mostrar_status(Boneco())
    assert "Energia" not in saida[1]


def test_barra_de_quem_esta_quase_morto():
    ui, saida = criar([])
    alvo = Boneco(vida=1000)
    alvo.receber_dano(999)
    ui.mostrar_status(alvo)
    assert "█" in saida[0]


def test_pausar_e_mensagem():
    ui, saida = criar([""])
    ui.pausar()
    ui.mostrar_mensagem("olá")
    assert saida == ["olá"]
