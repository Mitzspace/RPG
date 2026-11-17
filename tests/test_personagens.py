import pytest

from tests.auxiliares import Boneco
from rpg.entidades.personagens import (
    ESPECIALIDADES, EnergiaInsuficienteError, EngenheiroCivil, EngenheiroMecanico,
    EngenheiroQuimico, Personagem,
)
from rpg.habilidades.habilidades import GolpePoderoso
from rpg.itens import itens


def test_personagem_e_abstrato():
    with pytest.raises(TypeError):
        Personagem("X", 10, 1, 1, 10, [])


@pytest.mark.parametrize("classe", ESPECIALIDADES)
def test_especialidades_tem_duas_habilidades(classe):
    jogador = classe()
    assert jogador.nome == "Michael"
    assert jogador.especialidade.startswith("Engenheiro")
    assert len(jogador.habilidades) == 2
    assert jogador.energia == jogador.energia_maxima


def test_perfis_das_especialidades():
    mec, qui, civ = EngenheiroMecanico(), EngenheiroQuimico(), EngenheiroCivil()
    assert mec.vida_maxima > civ.vida_maxima > qui.vida_maxima  # guerreiro aguenta mais
    assert qui.ataque > civ.ataque > mec.ataque                 # mago bate mais forte
    assert mec.defesa > civ.defesa > qui.defesa


def test_usar_habilidade_gasta_energia():
    jogador = EngenheiroMecanico()
    alavanca = jogador.habilidades[0]
    jogador.usar_habilidade(alavanca, Boneco(vida=500))
    assert jogador.energia == jogador.energia_maxima - alavanca.custo_energia


def test_sem_energia_lanca_erro():
    jogador = EngenheiroMecanico()
    alvo = Boneco(vida=500)
    for _ in range(3):
        jogador.usar_habilidade(jogador.habilidades[0], alvo)
    assert jogador.habilidades[0] not in jogador.habilidades_disponiveis()
    with pytest.raises(EnergiaInsuficienteError):
        jogador.usar_habilidade(jogador.habilidades[0], alvo)


def test_habilidade_desconhecida():
    with pytest.raises(ValueError):
        EngenheiroMecanico().usar_habilidade(GolpePoderoso("Outra", "", 0, 2), Boneco())


def test_equipamentos_somam_bonus():
    jogador = EngenheiroMecanico()
    assert jogador.equipar(itens.florete_de_aco()) is None
    jogador.equipar(itens.gibao_de_couro())
    assert jogador.ataque == 14 + 4
    assert jogador.defesa == 8 + 3


def test_armadura_reduz_dano_recebido():
    jogador = EngenheiroQuimico()
    jogador.equipar(itens.gibao_de_couro())
    assert jogador.receber_dano(10) == 10 - (3 + 3)


def test_equipar_troca_e_devolve_o_anterior():
    from rpg.itens.itens import Arma
    jogador = EngenheiroCivil()
    florete = itens.florete_de_aco()
    jogador.equipar(florete)
    assert jogador.equipar(Arma("Rapieira", "", 6)) is florete
    assert jogador.ataque == 17 + 6


def test_equipar_consumivel_falha():
    with pytest.raises(TypeError):
        EngenheiroCivil().equipar(itens.elixir())


def test_descansar_restaura_tudo():
    jogador = EngenheiroQuimico()
    jogador.receber_dano(50)
    jogador.usar_habilidade(jogador.habilidades[0], Boneco(vida=500))
    jogador.descansar()
    assert jogador.vida == jogador.vida_maxima
    assert jogador.energia == jogador.energia_maxima


def test_sem_controlador_nao_escolhe_acao():
    with pytest.raises(RuntimeError):
        EngenheiroMecanico().escolher_acao(Boneco())
