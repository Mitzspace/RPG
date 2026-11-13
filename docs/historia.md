# O Engenheiro de Verona — Documento de Design

## Premissa

**Michael** é um estudante de engenharia que, voltando da faculdade, sofre um acidente de carro.
Ao abrir os olhos, está em Verona — no corpo de **Mercúcio**, poucos dias antes da tragédia.

Michael conhece a peça: sabe que ele próprio (Mercúcio) morrerá no duelo contra Teobaldo
e que Romeu e Julieta morrerão na cripta dos Capuletos. Armado apenas com o que aprendeu
na faculdade, ele decide **evitar a tragédia**.

## Especialidade (classe do personagem)

No início do jogo, o jogador escolhe em qual área de engenharia Michael estudava.
Cada especialidade funciona como uma classe de RPG.

| Especialidade          | Papel     | Perfil                    | Habilidades                                                        |
|------------------------|-----------|---------------------------|--------------------------------------------------------------------|
| Engenheiro Mecânico    | Guerreiro | Muita vida e defesa       | *Golpe de Alavanca* (dano dobrado), *Armadura Improvisada* (recupera parte da vida) |
| Engenheiro Químico     | Mago      | Muito ataque, pouca vida  | *Pólvora Rudimentar* (dano muito alto), *Fumaça Tóxica* (dano que ignora a defesa) |
| Engenheiro Civil       | Arqueiro  | Equilibrado e preciso     | *Balestra de Precisão* (chance de dano crítico), *Armadilha de Polia* (dano 1,5x garantido) |

As habilidades consomem **Energia**, recurso recuperado com itens.
Todas as habilidades têm efeito **instantâneo** (não há efeitos que duram vários turnos),
para manter o sistema de combate simples.

## Capítulos

1. **A Briga nas Ruas** (Ato I) — Criados dos Capuletos provocam uma briga na praça. Serve de tutorial.
   - Inimigos: *Criado Capuleto*
   - Chefão: *Capanga de Teobaldo*
2. **O Duelo Fatal** (Ato III) — O momento em que Mercúcio morreria na peça.
   - Chefão: **Teobaldo**
3. **A Cripta dos Capuletos** (Ato V) — Michael precisa chegar antes de Romeu tomar o veneno.
   - Inimigos: *Guarda da Cripta*
   - Chefão final: **Conde Páris**

Vencer o capítulo 3 leva ao **final feliz**: Romeu e Julieta vivem e as famílias fazem as pazes.

## Itens

| Item                     | Tipo         | Efeito              |
|--------------------------|--------------|---------------------|
| Ervas do Frei Lourenço   | Consumível   | Recupera vida       |
| Elixir                   | Consumível   | Recupera energia    |
| Florete de Aço           | Equipamento  | Aumenta ataque      |
| Gibão de Couro           | Equipamento  | Aumenta defesa      |

Entre os capítulos, **Frei Lourenço** entrega itens a Michael.

## Derrota

Se a vida de Michael chegar a zero: *"A tragédia se repete..."* — **Game Over**.
