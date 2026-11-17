"""O roteiro de "O Engenheiro de Verona": textos e ordem dos capítulos.

Todo o conteúdo da história fica aqui, separado das regras do jogo.
Mudar um diálogo ou acrescentar um capítulo não exige mexer no combate.
"""

from rpg.entidades import inimigos
from rpg.historia.capitulo import Capitulo
from rpg.itens import itens

TITULO = "O ENGENHEIRO DE VERONA"

PROLOGO = [
    "Chovia na volta da faculdade. Michael, estudante de engenharia, revisava de cabeça "
    "a prova de amanhã quando os faróis de um caminhão encheram o para-brisa...",
    "Ao abrir os olhos, o cheiro de asfalto molhado deu lugar ao de pão e cavalos. "
    "Ruas de pedra, gibões, espadas na cintura. Um rapaz o sacode: — Mercúcio! Acorda, homem!",
    "Michael se vê refletido numa fonte: está em Verona, no corpo de Mercúcio. "
    "Ele conhece essa história. Sabe que Mercúcio morre num duelo contra Teobaldo, "
    "e que Romeu e Julieta morrerão na cripta dos Capuletos.",
    "Desta vez vai ser diferente. Afinal, o que ele aprendeu na faculdade tem de servir para alguma coisa.",
]

PERGUNTA_ESPECIALIDADE = "Antes do acidente, qual engenharia Michael estudava?"


def criar_capitulos() -> list[Capitulo]:
    return [
        Capitulo(
            titulo="A Briga nas Ruas",
            abertura=[
                "Praça de Verona, manhã quente. Criados dos Capuletos provocam os Montéquios "
                "e as espadas começam a sair das bainhas.",
                "Dica: escolha 'Atacar' para golpes simples. Habilidades gastam Energia, "
                "e itens recuperam vida ou energia.",
            ],
            inimigos=[inimigos.criado_capuleto, inimigos.criado_capuleto, inimigos.capanga_de_teobaldo],
            desfecho=[
                "A guarda do Príncipe chega e a briga se dispersa. Romeu puxa Michael pelo braço: "
                "— Onde aprendeste a lutar assim, Mercúcio?",
                "No mosteiro, Frei Lourenço observa o rapaz com desconfiança... e simpatia. "
                "— Tens a cabeça de um estudioso. Leva isto: dias difíceis se aproximam.",
            ],
            recompensas=[itens.florete_de_aco, itens.ervas_frei_lourenco,
                         itens.ervas_frei_lourenco, itens.elixir],
        ),
        Capitulo(
            titulo="O Duelo Fatal",
            abertura=[
                "Ato III. O sol do meio-dia castiga a praça. Teobaldo procura Romeu, "
                "que acaba de se casar em segredo com Julieta.",
                "Na peça, é aqui que Mercúcio cai, amaldiçoando as duas casas. "
                "Michael respira fundo: hoje ninguém morre.",
            ],
            inimigos=[inimigos.teobaldo],
            desfecho=[
                "Teobaldo cai de joelhos, desarmado, mas vivo. Sem mortes, Romeu não é banido.",
                "Mesmo assim, os Capuletos apressam o casamento de Julieta com o Conde Páris. "
                "Frei Lourenço revela seu plano: uma poção que simula a morte. "
                "Michael gela — ele sabe como esse plano termina.",
            ],
            recompensas=[itens.gibao_de_couro, itens.ervas_frei_lourenco,
                         itens.ervas_frei_lourenco, itens.elixir],
        ),
        Capitulo(
            titulo="A Cripta dos Capuletos",
            abertura=[
                "Ato V. Noite. A carta do Frei nunca chegou a Romeu, que cavalga para Verona "
                "acreditando que Julieta está morta e com veneno no bolso.",
                "Michael corre até a cripta. Precisa chegar antes dele.",
            ],
            inimigos=[inimigos.guarda_da_cripta, inimigos.guarda_da_cripta, inimigos.conde_paris],
            desfecho=[
                "Páris recua, ferido. Romeu entra na cripta com o frasco na mão — "
                "e Michael o derruba no chão no instante exato.",
                "Julieta desperta. Romeu chora. Páris, envergonhado, embainha a espada.",
            ],
        ),
    ]


FINAL_FELIZ = [
    "Na manhã seguinte, diante do Príncipe, Montéquios e Capuletos apertam as mãos. "
    "Romeu e Julieta estão vivos, e Verona inteira comemora.",
    "Michael sente a vista escurecer... e acorda num leito de hospital, ouvindo o bip das máquinas. "
    "Na mesinha ao lado, um exemplar de 'Romeu e Julieta' que ele não se lembra de ter comprado.",
    "★ FINAL FELIZ — Obrigado por jogar O Engenheiro de Verona! ★",
]

GAME_OVER = [
    "A tragédia se repete...",
    "✝ GAME OVER ✝",
]
