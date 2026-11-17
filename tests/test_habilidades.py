import pytest

from tests.auxiliares import Boneco, RngFixo
from rpg.habilidades.habilidade import Habilidade
from rpg.habilidades.habilidades import GolpeCritico, GolpePerfurante, GolpePoderoso, Reparo


def test_habilidade_e_abstrata():
    with pytest.raises(TypeError):
        Habilidade("X", "", 1)


def test_validacoes():
    with pytest.raises(ValueError):
        GolpePoderoso("", "", 1, 2)
    with pytest.raises(ValueError):
        GolpePoderoso("X", "", -1, 2)
    with pytest.raises(ValueError):
        GolpePoderoso("X", "", 1, 0)
    with pytest.raises(ValueError):
        Reparo("X", "", 1, 1.5)
    with pytest.raises(ValueError):
        GolpeCritico("X", "", 1, chance_critico=2, multiplicador_critico=2)


def test_pode_usar():
    golpe = GolpePoderoso("G", "", 10, 2)
    assert golpe.pode_usar(10)
    assert not golpe.pode_usar(9)


def test_golpe_poderoso_multiplica_e_respeita_defesa():
    usuario, alvo = Boneco(ataque=10), Boneco(vida=100, defesa=5)
    GolpePoderoso("G", "", 0, 2.0).executar(usuario, alvo)
    assert alvo.vida == 100 - (20 - 5)


def test_golpe_perfurante_ignora_defesa():
    usuario, alvo = Boneco(ataque=10), Boneco(vida=100, defesa=50)
    GolpePerfurante("F", "", 0, 1.5).executar(usuario, alvo)
    assert alvo.vida == 85


def test_golpe_critico_acerta():
    usuario, alvo = Boneco(ataque=10), Boneco(vida=100)
    msg = GolpeCritico("B", "", 0, 0.5, 3.0, 1.0, rng=RngFixo(0.1)).executar(usuario, alvo)
    assert alvo.vida == 70
    assert "CRÍTICO" in msg


def test_golpe_critico_erra():
    usuario, alvo = Boneco(ataque=10), Boneco(vida=100)
    msg = GolpeCritico("B", "", 0, 0.5, 3.0, 1.3, rng=RngFixo(0.9)).executar(usuario, alvo)
    assert alvo.vida == 87
    assert "CRÍTICO" not in msg


def test_reparo_cura_o_usuario():
    usuario = Boneco(vida=100)
    usuario.receber_dano(60)
    Reparo("R", "", 0, 0.35).executar(usuario, Boneco())
    assert usuario.vida == 75
