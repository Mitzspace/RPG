# O Engenheiro de Verona

> 🚧 **Projeto em desenvolvimento.** Este README será completado conforme o jogo avança.

RPG de console em Python, feito como trabalho acadêmico, que aplica os conceitos de
Orientação a Objetos (abstração, encapsulamento, herança, composição e polimorfismo)
e os cinco princípios **SOLID**.

## Sinopse

**Michael**, estudante de engenharia, sofre um acidente de carro e acorda em Verona,
no corpo de **Mercúcio**, poucos dias antes da tragédia de *Romeu e Julieta*.
Ele sabe como a história termina e usa o que aprendeu na faculdade para mudar o final.

No início do jogo, o jogador escolhe a especialidade de Michael, que funciona como a classe do RPG:

| Especialidade        | Papel     | Perfil                   |
|----------------------|-----------|--------------------------|
| Engenheiro Mecânico  | Guerreiro | Muita vida e defesa      |
| Engenheiro Químico   | Mago      | Muito ataque, pouca vida |
| Engenheiro Civil     | Arqueiro  | Equilibrado e preciso    |

O design completo (capítulos, inimigos, chefões e itens) está em [docs/historia.md](docs/historia.md).

## Andamento

- [x] Conceito e história
- [x] Arquitetura e estrutura de pastas
- [x] Abstrações base (`Combatente`, `Habilidade`, `Item`, `InterfaceJogo`)
- [ ] Personagens jogáveis *(classe base `Personagem` pronta)*
- [ ] Itens e inventário
- [ ] Inimigos e chefões
- [ ] Sistema de combate em turnos
- [ ] Interface de console
- [ ] Fluxo da história (jogo jogável)
- [ ] Testes automatizados
- [ ] Diagrama de classes
- [ ] Capturas de tela

## Requisitos e como executar

- **Python 3.12** ou superior
- O jogo não usa bibliotecas externas (os testes usarão o `pytest`)

```bash
git clone https://github.com/Mitzspace/RPG.git
cd RPG
```

> Ainda não existe um ponto de entrada jogável. Quando o `main.py` estiver pronto,
> o jogo será iniciado com `python main.py`.

## Estrutura do projeto

```
RPG/
├── docs/
│   └── historia.md            # Documento de design da história
├── rpg/
│   ├── entidades/
│   │   ├── combatente.py      # Classe abstrata Combatente
│   │   └── personagens.py     # Personagem (base do jogador)
│   ├── habilidades/
│   │   └── habilidade.py      # Classe abstrata Habilidade
│   ├── itens/
│   │   └── item.py            # Item, Consumivel, Equipavel
│   ├── interface/
│   │   └── interface_jogo.py  # Abstração de entrada e saída
│   ├── combate/               # (em breve) Batalha em turnos
│   └── historia/              # (em breve) Capítulos e campanha
└── tests/                     # (em breve) Testes automatizados
```

## Princípios SOLID

Esta seção descreve o que já está aplicado no código. Ela será ampliada a cada etapa.

### S — Responsabilidade Única
Cada classe tem um único papel. `Combatente` cuida apenas das regras de vida e dano
e **não exibe nada na tela**: métodos como `receber_dano()` devolvem valores, e quem
mostra as mensagens é a interface. Na mesma linha, `Habilidade` só descreve o efeito
e não gasta energia, porque quem controla a energia é o `Personagem`.

### O — Aberto/Fechado
`Habilidade` e `Item` são classes abstratas. Para criar uma habilidade ou um item novo,
basta escrever uma subclasse, **sem alterar nenhum código existente**.

### L — Substituição de Liskov
Habilidades e itens recebem parâmetros do tipo `Combatente` (a abstração), e não de
uma classe concreta. Qualquer subclasse, seja jogador ou inimigo, pode ocupar esse lugar
sem quebrar o comportamento.

### I — Segregação de Interfaces
Os itens são divididos em duas interfaces pequenas: `Consumivel`, com `usar()`, e
`Equipavel`, com bônus de ataque e defesa. Uma espada não é obrigada a implementar
`usar()`, e uma poção não é obrigada a ter bônus de ataque.

### D — Inversão de Dependência
O jogo vai conversar com o jogador apenas pela abstração `InterfaceJogo`, nunca
diretamente por `print()`/`input()`. A implementação de console e uma implementação
falsa para testes poderão ser trocadas sem alterar a lógica do jogo.

## Diagrama de classes

*Em breve.*

## Capturas de tela

*Em breve.*
