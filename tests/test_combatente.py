import pytest

from tests.auxiliares import Boneco
from rpg.entidades.combatente import Combatente


def test_combatente_e_abstrato():
    with pytest.raises(TypeError):
        Combatente("X", 10, 1, 1)


@pytest.mark.parametrize("vida, ataque, defesa", [(0, 1, 1), (-5, 1, 1), (10, -1, 0), (10, 0, -1)])
def test_valores_invalidos(vida, ataque, defesa):
    with pytest.raises(ValueError):
        Boneco(vida=vida, ataque=ataque, defesa=defesa)


def test_defesa_reduz_dano():
    alvo = Boneco(vida=50, defesa=4)
    assert alvo.receber_dano(10) == 6
    assert alvo.vida == 44


def test_dano_minimo_e_um():
    alvo = Boneco(vida=50, defesa=20)
    assert alvo.receber_dano(5) == 1


def test_ignorar_defesa():
    alvo = Boneco(vida=50, defesa=20)
    assert alvo.receber_dano(10, ignorar_defesa=True) == 10


def test_vida_nunca_fica_negativa():
    alvo = Boneco(vida=5)
    assert alvo.receber_dano(100) == 5
    assert alvo.vida == 0
    assert not alvo.esta_vivo()


def test_dano_negativo_e_rejeitado():
    with pytest.raises(ValueError):
        Boneco().receber_dano(-1)


def test_cura_nao_passa_do_maximo():
    alvo = Boneco(vida=50)
    alvo.receber_dano(10)
    assert alvo.curar(100) == 10
    assert alvo.vida == 50
    with pytest.raises(ValueError):
        alvo.curar(-1)


def test_atributos_sao_somente_leitura():
    alvo = Boneco()
    with pytest.raises(AttributeError):
        alvo.vida = 999
