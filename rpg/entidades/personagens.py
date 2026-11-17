"""Personagens jogáveis: Michael e suas especialidades de engenharia."""

from __future__ import annotations

import random
from abc import abstractmethod
from typing import TYPE_CHECKING

from rpg.entidades.combatente import Combatente
from rpg.habilidades.habilidade import Habilidade
from rpg.habilidades.habilidades import GolpeCritico, GolpePerfurante, GolpePoderoso, Reparo
from rpg.itens.inventario import Inventario
from rpg.itens.item import Encaixe, Equipavel

if TYPE_CHECKING:
    from rpg.combate.acoes import Acao
    from rpg.combate.controladores import Controlador

NOME_JOGADOR = "Michael"


class EnergiaInsuficienteError(Exception):
    """Lançada ao tentar usar uma habilidade sem energia suficiente."""


class Personagem(Combatente):
    """Combatente controlado pelo jogador.

    Herança:    Personagem É UM Combatente (ganha vida, ataque, defesa...).
    Composição: Personagem TEM habilidades, um inventário e equipamentos.
    """

    def __init__(
        self,
        nome: str,
        vida_maxima: int,
        ataque: int,
        defesa: int,
        energia_maxima: int,
        habilidades: list[Habilidade],
        inventario: Inventario | None = None,
        controlador: Controlador | None = None,
    ) -> None:
        super().__init__(nome, vida_maxima, ataque, defesa)

        if energia_maxima < 0:
            raise ValueError("A energia máxima não pode ser negativa.")

        self._energia_maxima = energia_maxima
        self._energia = energia_maxima
        self._habilidades = list(habilidades)  # cópia: a lista original não afeta o personagem
        self._inventario = inventario if inventario is not None else Inventario()
        self._equipamentos: dict[Encaixe, Equipavel] = {}
        self._controlador = controlador

    # ------------------------------------------------------------------
    # Propriedades
    # ------------------------------------------------------------------
    @property
    @abstractmethod
    def especialidade(self) -> str:
        """Nome da especialidade de engenharia (ex.: 'Engenheiro Mecânico')."""

    @property
    def energia(self) -> int:
        return self._energia

    @property
    def energia_maxima(self) -> int:
        return self._energia_maxima

    @property
    def habilidades(self) -> tuple[Habilidade, ...]:
        """Devolve uma tupla (imutável) para que ninguém altere a lista interna."""
        return tuple(self._habilidades)

    @property
    def inventario(self) -> Inventario:
        return self._inventario

    @property
    def equipamentos(self) -> dict[Encaixe, Equipavel]:
        """Cópia dos equipamentos em uso, por encaixe."""
        return dict(self._equipamentos)

    @property
    def ataque(self) -> int:
        """Ataque base + bônus dos equipamentos (sobrescreve Combatente.ataque)."""
        return self._ataque + sum(e.bonus_ataque for e in self._equipamentos.values())

    @property
    def defesa(self) -> int:
        """Defesa base + bônus dos equipamentos. Como Combatente.receber_dano
        usa `self.defesa`, a armadura passa a valer automaticamente."""
        return self._defesa + sum(e.bonus_defesa for e in self._equipamentos.values())

    @property
    def controlador(self) -> Controlador | None:
        return self._controlador

    @controlador.setter
    def controlador(self, controlador: Controlador) -> None:
        self._controlador = controlador

    # ------------------------------------------------------------------
    # Turno
    # ------------------------------------------------------------------
    def escolher_acao(self, oponente: Combatente) -> Acao:
        """Delega a decisão ao controlador (normalmente, o jogador humano)."""
        if self._controlador is None:
            raise RuntimeError(f"{self.nome} não tem um controlador definido.")
        return self._controlador.decidir(self, oponente)

    # ------------------------------------------------------------------
    # Equipamentos e descanso
    # ------------------------------------------------------------------
    def equipar(self, item: Equipavel) -> Equipavel | None:
        """Equipa o item e devolve o que estava no mesmo encaixe (ou None)."""
        if not isinstance(item, Equipavel):
            raise TypeError(f"{item.nome} não pode ser equipado.")
        anterior = self._equipamentos.get(item.encaixe)
        self._equipamentos[item.encaixe] = item
        return anterior

    def descansar(self) -> None:
        """Recupera toda a vida e a energia (usado entre os capítulos)."""
        self.curar(self.vida_maxima)
        self.recuperar_energia(self.energia_maxima)

    # ------------------------------------------------------------------
    # Energia e habilidades
    # ------------------------------------------------------------------
    def recuperar_energia(self, quantidade: int) -> int:
        """Recupera energia sem passar do máximo e devolve quanto foi recuperado."""
        if quantidade < 0:
            raise ValueError("A recuperação não pode ser negativa.")

        recuperado = min(quantidade, self._energia_maxima - self._energia)
        self._energia += recuperado
        return recuperado

    def habilidades_disponiveis(self) -> list[Habilidade]:
        """Habilidades que podem ser usadas com a energia atual."""
        return [h for h in self._habilidades if h.pode_usar(self._energia)]

    def usar_habilidade(self, habilidade: Habilidade, alvo: Combatente) -> str:
        """Confere, gasta a energia e executa a habilidade. Devolve a mensagem."""
        if habilidade not in self._habilidades:
            raise ValueError(f"{self.nome} não conhece a habilidade {habilidade.nome}.")
        if not habilidade.pode_usar(self._energia):
            raise EnergiaInsuficienteError(
                f"Energia insuficiente para {habilidade.nome} "
                f"({self._energia}/{habilidade.custo_energia})."
            )

        self._energia -= habilidade.custo_energia
        return habilidade.executar(self, alvo)


# ----------------------------------------------------------------------
# Especialidades (classes do RPG)
# ----------------------------------------------------------------------
class EngenheiroMecanico(Personagem):
    """Guerreiro: muita vida e defesa."""

    def __init__(self, inventario: Inventario | None = None, controlador: Controlador | None = None) -> None:
        super().__init__(
            NOME_JOGADOR, vida_maxima=130, ataque=14, defesa=8, energia_maxima=30,
            habilidades=[
                GolpePoderoso("Golpe de Alavanca", "dano dobrado", custo_energia=10, multiplicador=2.0),
                Reparo("Armadura Improvisada", "recupera 35% da vida", custo_energia=12, percentual=0.35),
            ],
            inventario=inventario, controlador=controlador,
        )

    @property
    def especialidade(self) -> str:
        return "Engenheiro Mecânico"


class EngenheiroQuimico(Personagem):
    """Mago: muito ataque, pouca vida."""

    def __init__(self, inventario: Inventario | None = None, controlador: Controlador | None = None) -> None:
        super().__init__(
            NOME_JOGADOR, vida_maxima=90, ataque=20, defesa=3, energia_maxima=40,
            habilidades=[
                GolpePoderoso("Pólvora Rudimentar", "dano muito alto (2,5x)", custo_energia=15, multiplicador=2.5),
                GolpePerfurante("Fumaça Tóxica", "dano que ignora a defesa", custo_energia=10, multiplicador=1.2),
            ],
            inventario=inventario, controlador=controlador,
        )

    @property
    def especialidade(self) -> str:
        return "Engenheiro Químico"


class EngenheiroCivil(Personagem):
    """Arqueiro: equilibrado e preciso."""

    def __init__(
        self,
        inventario: Inventario | None = None,
        controlador: Controlador | None = None,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(
            NOME_JOGADOR, vida_maxima=115, ataque=17, defesa=5, energia_maxima=35,
            habilidades=[
                GolpeCritico(
                    "Balestra de Precisão", "50% de chance de dano triplo",
                    custo_energia=10, chance_critico=0.5,
                    multiplicador_critico=3.0, multiplicador_normal=1.3, rng=rng,
                ),
                GolpePoderoso("Armadilha de Polia", "dano 1,5x garantido", custo_energia=8, multiplicador=1.5),
            ],
            inventario=inventario, controlador=controlador,
        )

    @property
    def especialidade(self) -> str:
        return "Engenheiro Civil"


# Para adicionar uma especialidade nova, basta criar a subclasse e incluí-la aqui.
ESPECIALIDADES: list[type[Personagem]] = [EngenheiroMecanico, EngenheiroQuimico, EngenheiroCivil]
