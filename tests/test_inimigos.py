import pytest

from tests.auxiliares import Boneco
from rpg.combate.acoes import Atacar, GolpeEspecial
from rpg.combate.controladores import EstrategiaChefao
from rpg.entidades import inimigos
from rpg.habilidades.habilidades import GolpePoderoso


def test_inimigo_comum_sempre_ataca():
    criado = inimigos.criado_capuleto()
    assert not criado.eh_chefao
    assert all(isinstance(criado.escolher_acao(Boneco()), Atacar) for _ in range(5))


def test_chefao_usa_especial_a_cada_tres_turnos():
    teobaldo = inimigos.teobaldo()
    assert teobaldo.eh_chefao
    acoes = [type(teobaldo.escolher_acao(Boneco())) for _ in range(6)]
    assert acoes == [Atacar, Atacar, GolpeEspecial] * 2


def test_intervalo_invalido():
    with pytest.raises(ValueError):
        EstrategiaChefao(GolpePoderoso("X", "", 0, 1), intervalo=0)


@pytest.mark.parametrize("fabrica", [
    inimigos.criado_capuleto, inimigos.capanga_de_teobaldo, inimigos.teobaldo,
    inimigos.guarda_da_cripta, inimigos.conde_paris,
])
def test_catalogo_cria_inimigos_novos(fabrica):
    a, b = fabrica(), fabrica()
    assert a is not b
    assert a.fala
    a.receber_dano(10)
    assert b.vida == b.vida_maxima


def test_paris_ignora_defesa_no_especial():
    paris = inimigos.conde_paris()
    alvo = Boneco(vida=500, defesa=100)
    for _ in range(3):
        acao = paris.escolher_acao(alvo)
    acao.executar(paris, alvo)
    assert alvo.vida == 500 - round(20 * 1.3)
