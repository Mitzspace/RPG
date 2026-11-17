"""Itens concretos do jogo e o catálogo dos itens da história."""

from rpg.entidades.combatente import Combatente
from rpg.itens.item import Consumivel, Encaixe, Equipavel


# ----------------------------------------------------------------------
# Consumíveis
# ----------------------------------------------------------------------
class PocaoVida(Consumivel):
    """Recupera uma quantidade fixa de vida."""

    def __init__(self, nome: str, descricao: str, cura: int) -> None:
        super().__init__(nome, descricao)
        if cura <= 0:
            raise ValueError("A cura deve ser positiva.")
        self._cura = cura

    @property
    def cura(self) -> int:
        return self._cura

    def usar(self, alvo: Combatente) -> str:
        curado = alvo.curar(self._cura)
        return f"{alvo.nome} usa {self.nome} e recupera {curado} de vida."


class PocaoEnergia(Consumivel):
    """Recupera energia. Só tem efeito em quem possui energia (o jogador)."""

    def __init__(self, nome: str, descricao: str, energia: int) -> None:
        super().__init__(nome, descricao)
        if energia <= 0:
            raise ValueError("A energia recuperada deve ser positiva.")
        self._energia = energia

    @property
    def energia(self) -> int:
        return self._energia

    def usar(self, alvo: Combatente) -> str:
        recuperar = getattr(alvo, "recuperar_energia", None)
        if recuperar is None:
            # Aceita qualquer Combatente (Liskov): em quem não tem energia, só não faz efeito.
            return f"{alvo.nome} usa {self.nome}, mas nada acontece."
        recuperado = recuperar(self._energia)
        return f"{alvo.nome} usa {self.nome} e recupera {recuperado} de energia."


# ----------------------------------------------------------------------
# Equipamentos
# ----------------------------------------------------------------------
class Arma(Equipavel):
    def __init__(self, nome: str, descricao: str, bonus_ataque: int) -> None:
        super().__init__(nome, descricao)
        if bonus_ataque < 0:
            raise ValueError("O bônus não pode ser negativo.")
        self._bonus_ataque = bonus_ataque

    @property
    def encaixe(self) -> Encaixe:
        return Encaixe.ARMA

    @property
    def bonus_ataque(self) -> int:
        return self._bonus_ataque

    @property
    def bonus_defesa(self) -> int:
        return 0


class Armadura(Equipavel):
    def __init__(self, nome: str, descricao: str, bonus_defesa: int) -> None:
        super().__init__(nome, descricao)
        if bonus_defesa < 0:
            raise ValueError("O bônus não pode ser negativo.")
        self._bonus_defesa = bonus_defesa

    @property
    def encaixe(self) -> Encaixe:
        return Encaixe.ARMADURA

    @property
    def bonus_ataque(self) -> int:
        return 0

    @property
    def bonus_defesa(self) -> int:
        return self._bonus_defesa


# ----------------------------------------------------------------------
# Catálogo: os itens da história (cada chamada cria um item novo)
# ----------------------------------------------------------------------
def ervas_frei_lourenco() -> PocaoVida:
    return PocaoVida("Ervas do Frei Lourenço", "recupera 40 de vida", cura=40)


def elixir() -> PocaoEnergia:
    return PocaoEnergia("Elixir", "recupera 20 de energia", energia=20)


def florete_de_aco() -> Arma:
    return Arma("Florete de Aço", "+4 de ataque", bonus_ataque=4)


def gibao_de_couro() -> Armadura:
    return Armadura("Gibão de Couro", "+3 de defesa", bonus_defesa=3)
