"""Bolsa de itens consumíveis do jogador."""

from rpg.itens.item import Consumivel


class Inventario:
    """Guarda os consumíveis. Só sabe adicionar, remover e listar itens."""

    def __init__(self, itens: list[Consumivel] | None = None) -> None:
        self._itens: list[Consumivel] = list(itens or [])

    def __len__(self) -> int:
        return len(self._itens)

    @property
    def itens(self) -> tuple[Consumivel, ...]:
        return tuple(self._itens)

    def adicionar(self, item: Consumivel) -> None:
        if not isinstance(item, Consumivel):
            raise TypeError("Só itens consumíveis vão para a bolsa.")
        self._itens.append(item)

    def remover(self, item: Consumivel) -> None:
        if item not in self._itens:
            raise ValueError(f"{item.nome} não está no inventário.")
        self._itens.remove(item)

    def agrupar_consumiveis(self) -> list[tuple[Consumivel, int]]:
        """Agrupa itens de mesmo nome: [(um exemplar, quantidade), ...]."""
        grupos: dict[str, list[Consumivel]] = {}
        for item in self._itens:
            grupos.setdefault(item.nome, []).append(item)
        return [(lista[0], len(lista)) for lista in grupos.values()]
