import pytest

from tests.auxiliares import Boneco
from rpg.entidades.personagens import EngenheiroQuimico
from rpg.itens import itens
from rpg.itens.inventario import Inventario
from rpg.itens.item import Consumivel, Encaixe, Equipavel


def test_abstracoes():
    for classe in (Consumivel, Equipavel):
        with pytest.raises(TypeError):
            classe("X", "")


def test_ervas_curam():
    alvo = Boneco(vida=100)
    alvo.receber_dano(50)
    itens.ervas_frei_lourenco().usar(alvo)
    assert alvo.vida == 90


def test_elixir_recupera_energia_do_personagem():
    jogador = EngenheiroQuimico()
    jogador.usar_habilidade(jogador.habilidades[0], Boneco(vida=500))
    assert jogador.energia == 25
    itens.elixir().usar(jogador)
    assert jogador.energia == 40


def test_elixir_em_quem_nao_tem_energia_nao_quebra():
    msg = itens.elixir().usar(Boneco())
    assert "nada acontece" in msg


def test_equipamentos():
    florete, gibao = itens.florete_de_aco(), itens.gibao_de_couro()
    assert (florete.encaixe, florete.bonus_ataque, florete.bonus_defesa) == (Encaixe.ARMA, 4, 0)
    assert (gibao.encaixe, gibao.bonus_ataque, gibao.bonus_defesa) == (Encaixe.ARMADURA, 0, 3)


def test_inventario_adicionar_remover_agrupar():
    erva1, erva2, elixir = itens.ervas_frei_lourenco(), itens.ervas_frei_lourenco(), itens.elixir()
    inv = Inventario([erva1, elixir])
    inv.adicionar(erva2)
    assert len(inv) == 3
    grupos = {item.nome: qtd for item, qtd in inv.agrupar_consumiveis()}
    assert grupos == {"Ervas do Frei Lourenço": 2, "Elixir": 1}

    inv.remover(erva1)
    assert len(inv) == 2
    with pytest.raises(ValueError):
        inv.remover(erva1)


def test_inventario_so_aceita_consumiveis():
    with pytest.raises(TypeError):
        Inventario().adicionar(itens.florete_de_aco())


def test_lista_de_itens_e_imutavel_por_fora():
    inv = Inventario([itens.elixir()])
    assert isinstance(inv.itens, tuple)
