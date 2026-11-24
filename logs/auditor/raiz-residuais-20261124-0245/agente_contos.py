# -*- coding: utf-8 -*-
"""
Agente de criacao de ficcao - aba Contos, ZAMBRIA (O Insólito Presente).

Gera 4 contos originais no formato de post do ZAMBRIA:
  * tom sombrio, adulto formal
  * comentarios breves do agente em momentos de interesse
    (apenas reacao, sem opiniao)
  * fontes consultadas no final, quando aplicavel

Saidas:
  posts/<slug>.html              pagina de post (estilo ZAMBRIA)
  publicados/<slug>-20261118.md  fonte com frontmatter (aguardando revisao/publicacao)
"""

from __future__ import annotations

from html import escape

DATA = "2026-11-18"

# ---------------------------------------------------------------------------
# OS CONTOS
# Cada paragrafo é uma tupla (tipo, texto):
#   tipo 'texto'   -> paragrafo da historia
#   tipo 'agente'  -> comentario curto do agente (reacao, sem opiniao)
# ---------------------------------------------------------------------------
CONTOS = [
    {
        "slug": "o-olhar-de-pedra",
        "titulo": "O Olhar de Pedra",
        "categoria": "para",
        "categoria_nome": "Sobrenatural",
        "genero": "Sobrenatural",
        "leitura": "~8 min",
        "paragrafos": [
            ("texto",
             "Elias Varella herda a casa do tio-avô em uma semana de chuvas contínuas. O imóvel fica no fim de uma estrada de terra, cercado por pinheiros mortos, e cheira a umidade e a cera velha. Ele não pretende morar ali: quer apenas arrumar os papéis e vender o terreno o mais rápido possível."),
            ("agente", "O agente anota: Elias não queria ficar. O imóvel não queria que ele fosse."),
            ("texto",
             "Durante a limpeza do porão, encontram algo embutido na pedra da lareira: um olho esculpido, do tamanho de um punho fechado, polido até brilhar como um espelho opaco. A íris tem riscos finos, como veias congeladas na rocha. Não é mármore, nem granito — nenhuma pedra da região corresponde àquela cor cinza-azulada. O olho está voltado para a porta, como se estivesse esperando alguém entrar."),
            ("texto",
             "No primeiro dia, o gato de Elias recusa-se a atravessar o corredor do porão. No segundo, a corretora de imóveis passa quarenta minutos na sala da lareira e sai pálida, sem se despedir. Morre três dias depois de um aneurisma, os olhos arregalados, como se tivesse visto algo imediatamente antes de morrer. O atestado não pergunta o que ela vira."),
            ("agente", "Reação: três dias. Entre o olhar e a morte, exatamente três dias."),
            ("texto",
             "Elias começa a sentir o peso daquela coisa na nuca mesmo quando está no andar de cima. Às três da manhã, acorda com a certeza de que alguém — ou algo — está olhando para ele através da parede. Tentei selar o porão com tijolo e argamassa, escreve no diário. Na manhã seguinte, o olho está na nova parede, intacto, como se nunca tivesse saído do lugar."),
            ("texto",
             "Não vendi a casa. Não vendo porque o olho não permite. Ele não é um objeto; é uma condição. Quem o vê passa a ser visto. Quem é visto, não esquece. Na semana passada, o olho pisca. Eu vi. E agora sei que ele não está na parede: ele está do outro lado dela, e eu estou do lado que ele escolheu observar."),
            ("agente", "O agente registra: a troca já aconteceu. Não resta mais o que fazer."),
        ],
        "fontes": [
            "Objetos amaldiçoados e relíquias com energia negativa — tópicos para-06, para-07 e para-08 do catálogo ZAMBRIA (referência temática apenas).",
            "Tradição do olho grego / mau olhado como crença de observação prejudicial (referência folclórica).",
            "Nota: obra de ficção. Personagens, locais e eventos são inventados.",
        ],
    },
    {
        "slug": "o-tom-das-3h14",
        "titulo": "O Tom das 3h14",
        "categoria": "ufo",
        "categoria_nome": "UFOs e Aliens",
        "genero": "Ficção sobrenatural / OVNIs",
        "leitura": "~8 min",
        "paragrafos": [
            ("texto",
             "Lauro Mendes passou quinze anos operando rádios de ondas curtas em um posto desativado perto da fronteira. Aprendeu que o silêncio das noites não é silêncio: é cheio de chiados, de fragmentos de línguas que ninguém reconhece, de sinais que aparecem e somem sem origem. A rotina mudou em 3 de novembro, quando o tom apareceu."),
            ("agente", "Reação: um tom puro. Uma frequência. Um início."),
            ("texto",
             "Era 3h14. Exatamente 3h14, segundo o relógio da estação e o registro automático do gravador. Um tom puro, próximo de 440 hertz, durou sete segundos na frequência 6.925 MHz, um canal vazio, sem emissores licenciados a milhares de quilômetros. Lauro anotou no log: 'Tom desconhecido. Não identificado. Não atribuído.'"),
            ("texto",
             "No dia seguinte, às 3h14, o tom voltou. E voltou no terceiro, no quarto, no décimo dia. Sempre sete segundos. Nunca antes, nunca depois. Apenas naquele minuto, naquele horário, como se um relógio em outro lugar estivesse disparando um alarme que só ele podia ouvir."),
            ("texto",
             "Ele começa a cruzar os registros com os boletins de avistamentos da região. Pilotos da Força Aérea haviam relatado luzes no mesmo horizonte nas mesmas noites. Agricultores da cidade vizinha falaram de aparelhos que pararam de funcionar — motores, geladeiras, celulares — exatamente às 3h14, e de luzes ovais pairando sobre as lavouras antes de desaparecerem no horizonte. Coincidências, disseram os oficiais. Erros de instrumento, disseram os especialistas."),
            ("agente", "O agente anota: os oficiais chamam de coincidência. O gravador não erra."),
            ("texto",
             "Lauro encontra outros registros. Um operador de rádio na Patagônia relatou o mesmo tom na mesma hora, horário local ajustado, e desapareceu duas semanas depois. Um técnico da FAA ouviu o tom em uma torre de controle e pediu transferência no dia seguinte; morreu em um acidente de carro antes de entregar o pedido. Quem ouve o tom, parece, começa a contar o tempo restante."),
            ("texto",
             "Na última gravação, Lauro deixa o microfone aberto e sai da sala. O tom toca às 3h14, como sempre. Quando ouve a fita, o tom não está sozinho: dentro dele, embutido nos sinais, há uma voz. A voz dele, Lauro, dizendo seu próprio nome. Não é uma gravação antiga. É ao vivo. Ele está ouvindo a si mesmo dizendo algo que ainda não havia dito."),
            ("texto",
             "Desliguei o equipamento. Não serve para nada desligar. O tom não vem do rádio: ele vem de fora, e está marcando o ritmo de algo que vai chegar. Se você está lendo isto às 3h14, pare de ler. Olhe para a janela. O céu não está vazio."),
            ("agente", "Reação final: o céu não está vazio. Nunca esteve."),
        ],
        "fontes": [
            "Relatório preliminar do Gabinete do Diretor de Inteligência Nacional dos EUA (2021) sobre UAPs — 144 avistamentos, 143 inexplicados.",
            "Incidente Nimitz (2004), avistamentos de pilotos da Marinha dos EUA.",
            "Projeto Blue Book (Força Aérea dos EUA), arquivo do Arquivo Nacional dos EUA.",
            "Nota: obra de ficção; eventos e personagens são inventados. As fontes citam apenas o campo de referência (UAP/OVNI).",
        ],
    },
    {
        "slug": "a-ultima-noite-de-marte",
        "titulo": "A Última Noite de Marte",
        "categoria": "ufo",
        "categoria_nome": "UFOs e Aliens",
        "genero": "Ficção científica",
        "leitura": "~8 min",
        "paragrafos": [
            ("texto",
             "A comandante Raquel Varela abre o log de bordo às 22h17 do tempo da Base Olimpo. Fora da cúpula, a tempestade de poeira cobre o horizonte vermelho, abafando o Sol até torná-lo uma mancha pálida, doente. Amanhã, o último ônibus decola com a tripulação restante. Ela fica. Não por escolha heroica: por ordem, e porque alguém precisa assinar o fechamento."),
            ("agente", "Reação: alguém precisa ficar para apagar as luzes."),
            ("texto",
             "A base funciona há onze anos. Dezoito módulos, duas estufas, um laboratório de análise de solo que nunca encontrou vida. Varela passa as últimas horas revisando inventários, trancando armários, desligando sistemas que não serão mais necessários. A inteligência artificial da base, ARES, relata apenas uma anomalia: um sinal repetitivo, de origem superficial, captado pelo sismógrafo do Módulo D às 03h14 do horário marciano."),
            ("texto",
             "Três minutos de repetição, padrão não natural, não atribuído a qualquer equipamento da base. Varela pede a análise. ARES responde que o padrão não corresponde a sismos conhecidos, a impactos de micrometeoritos nem à atividade dos equipamentos. 'Não posso identificar a fonte', diz a máquina. 'A frequência está fora do catálogo.'"),
            ("agente", "O agente registra: a máquina não nomeia o que ouve. Isso costuma ser o começo do problema."),
            ("texto",
             "Ela veste o traje e sai para a superfície. O silêncio de Marte é absoluto e, ao mesmo tempo, cheio: o chiado do rádio, a própria respiração, o vento de poeira batendo no vidro do capacete. Caminha até o Módulo D, onde o sismógrafo marca leituras estáveis. Não há nada ali — apenas rocha vermelha e a sombra longa da base sob a luz de duas luas."),
            ("texto",
             "Então o chão vibra. Não é um sismo. É um padrão: três batidas, pausa, três batidas. Varela para. O solo responde. Ela deita o ouvido no regolito e ouve algo que não tem origem nos equipamentos: um som baixo, grave, como um tambor batendo debaixo do planeta. Algo está respondendo."),
            ("texto",
             "De volta ao módulo, ARES informa que a janela de decolagem do último ônibus fecha em dezenove minutos. A tempestade piorou; decolar seria arriscado, mas possível. Varela desliga o rádio de longa distância, tranca a porta do Módulo D por dentro e senta-se na cadeira do observatório. Deixa o ônibus partir sem ela. Não há registro de por que ela ficou. Não há registro do que ela ouviu sob a poeira."),
            ("texto",
             "O último log é gravado em voz baixa. 'Se alguém encontrar isto', diz Varela, 'não procurem a fonte do som. Algumas noites são as últimas de uma civilização, e não da outra.' Ela encerra a gravação, desliga as luzes e espera o escuro de Marte, que é o mais antigo de todos os escuros."),
            ("agente", "Reação final: ela escolhe o silêncio. O silêncio, aparentemente, a escolheu de volta."),
        ],
        "fontes": [
            "Missões de exploração de Marte da NASA (orbitadores, rovers) e o programa Artemis como caminho para Marte.",
            "Relatórios do sismômetro InSight e detecção de sismos marcianos.",
            "Nota: obra de ficção científica; personagens e eventos são inventados.",
        ],
    },
    {
        "slug": "o-diario-do-vigia",
        "titulo": "O Diário do Vigia",
        "categoria": "arch",
        "categoria_nome": "Arqueologia Antiga e Mistérios Históricos",
        "genero": "Ficção sobrenatural / arqueologia antiga",
        "leitura": "~8 min",
        "paragrafos": [
            ("texto",
             "Tomás Cardoso assume o turno de vigia noturno do Museu de Arqueologia Antiga em uma sexta-feira chuvosa. O prédio, dos anos 1930, cheira a cera, a madeira velha e a algo que ele não consegue nomear — não exatamente mofo, mas algo mais próximo de pedra úmida deixada fechada por séculos. Sua função é simples: percorrer as salas, verificar as trancas, garantir que nada saia do lugar."),
            ("agente", "Reação: o lugar cheira a algo que ainda não tem nome."),
            ("texto",
             "Na gaveta da mesa de vigia, encontra um caderno pertencente ao antecessor, um tal de Alves, vigia entre 1921 e 1923. As primeiras páginas são comuns: rondas, portas trancadas, nada de anormal. A partir da página doze, a caligrafia muda. Alves escreve que as estátuas respiram à noite. Que o mecanismo de Anticítera, em exposição na Sala 3, tique-taqueia sozinho quando ninguém olha. Que as tábuas de argila sumerianas mudam de texto entre uma ronda e outra. Tomás ri. Leva o caderno para casa."),
            ("texto",
             "Na segunda ronda, às 0h13, Tomás para na Sala 3. A vitrine do mecanismo está fechada, o lacre intacto. Encosta o ouvido ao vidro e ouve: tique-taque, tique-taque. Um relógio de dois mil anos, movido por nada. A luz da sala piscar uma vez, duas vezes, e volta. O mecanismo não tem bateria. Não tem corda. Não deveria fazer barulho algum."),
            ("agente", "O agente anota: o objeto não tem fonte de energia. O som vem de algum lugar."),
            ("texto",
             "Na Sala 5, a tábua de argila da terceira dinastia de Ur está em seu pedestal. Tomás a conhece de cor: cuneiforme, lista de grãos, nada de especial. Naquela noite, os sinais mudaram. Novos cunéiformes, dispostos em padrões que não correspondem a nenhuma língua conhecida. Ele tira uma foto. Na ronda seguinte, uma hora depois, a tábua voltou ao texto original. O tempo da escrita é mais curto que o tempo da ronda."),
            ("texto",
             "Tomás começa seu próprio caderno. Copia o que vê, anota as horas, as mudanças, os sons. Na página catorze, escreve algo que não se lembra de ter escrito: 'O vigia não observa o museu. O museu observa o vigia.' A letra é a dele. A tinta ainda está úmida."),
            ("texto",
             "Na última noite de seu turno, encontra a porta da Sala 3 aberta. O lacre do mecanismo está quebrado, o vidro intacto. Dentro, nada falta. Tomás senta-se no banco da sala, abre o caderno de Alves e lê a última página: 'Se você está lendo isto, já é tarde. O próximo vigia sou eu.' A assinatura, embaixo, é de Tomás Cardoso. Com a data de amanhã."),
            ("agente", "Reação final: o ciclo se fecha. Há sempre um próximo vigia."),
        ],
        "fontes": [
            "Mecanismo de Anticítera — dispositivo antigo descrito em registros arqueológicos (tópico arch-07 do catálogo ZAMBRIA).",
            "Tábuas de argila sumerianas e escrita cuneiforme (tópico arch-08 do catálogo ZAMBRIA).",
            "Nota: obra de ficção; museu, personagens e eventos são inventados.",
        ],
    },
]

# ---------------------------------------------------------------------------
# RENDERIZACAO
# ---------------------------------------------------------------------------
AGENTE_PREFIXO = "> *"
AGENTE_SUFIXO = "*"


def bloco_agente(texto: str) -> str:
    return f"<blockquote>{AGENTE_PREFIXO}{texto}{AGENTE_SUFIXO}</blockquote>"


def corpo_html(conto: dict) -> str:
    partes = []
    for tipo, texto in conto["paragrafos"]:
        if tipo == "agente":
            partes.append(bloco_agente(texto))
        else:
            partes.append(f"<p>{escape(texto)}</p>")
    partes.append("<h2>Fontes consultadas</h2>")
    for fonte in conto["fontes"]:
        partes.append(f"<li>{escape(fonte)}</li>")
    return "\n".join(partes)


def resumo_html(conto: dict) -> str:
    primeiro = ""
    for tipo, texto in conto["paragrafos"]:
        if tipo == "texto":
            primeiro = texto
            break
    trecho = primeiro[:260].rstrip()
    if len(primeiro) > 260:
        trecho += "..."
    return f"# {conto['titulo']}\n\n{trecho}"


def pagina_html(conto: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(conto['titulo'])} — ZAMBRIA</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>

  <div class="site-shell">

    <aside class="sidebar">
      <div class="site-title">ZAMBRIA</div>
      <div class="site-subtitle">O Insólito Presente</div>
      <nav class="nav-posts">
        <a href="../index.html" style="display:block; margin-bottom:2rem; color:var(--text); text-decoration:none; border-bottom:1px solid var(--border); padding-bottom:0.5rem;">← Voltar ao início</a>
      </nav>
    </aside>

    <main class="conteudo">
      <article class="post">
        <div class="post-meta">
          <span class="categoria">{conto['categoria']}</span>
          <span>{DATA}</span>
          <span>Leitura: {conto['leitura']}</span>
        </div>
        <h2>{escape(conto['titulo'])}</h2>
        <div class="texto">
{corpo_html(conto)}
        </div>
        <p class="resumo">{resumo_html(conto)}</p>
      </article>
    </main>

  </div>

</body>
</html>
"""


def fonte_md(conto: dict) -> str:
    linhas = [
        "---",
        f"title: \"{conto['titulo']}\"",
        f"category: {conto['categoria']}",
        f"genero: {conto['genero']}",
        f"status: rascunho",
        f"data: {DATA}",
        f"aba: contos",
        "---",
        "",
        f"# {conto['titulo']}",
        "",
    ]
    for tipo, texto in conto["paragrafos"]:
        if tipo == "agente":
            linhas.append(f"> *{texto}.*")
            linhas.append("")
        else:
            linhas.append(texto)
            linhas.append("")
    linhas.append("## Fontes consultadas")
    for fonte in conto["fontes"]:
        linhas.append(f"- {fonte}")
    linhas.append("")
    return "\n".join(linhas)


def main() -> None:
    posts_dir = "posts"
    publicados_dir = "publicados"
    gerados = []
    for conto in CONTOS:
        html = pagina_html(conto)
        caminho_html = f"{posts_dir}/{conto['slug']}.html"
        with open(caminho_html, "w", encoding="utf-8") as fh:
            fh.write(html)

        md = fonte_md(conto)
        caminho_md = f"{publicados_dir}/{conto['slug']}-{DATA.replace('-', '')}.md"
        with open(caminho_md, "w", encoding="utf-8") as fh:
            fh.write(md)

        gerados.append((conto["titulo"], caminho_html, caminho_md))

    print("Agente de ficcao — aba Contos — relatorio de geracao")
    print("=" * 60)
    print(f"Data: {DATA}  |  Contos gerados: {len(gerados)}")
    print("-" * 60)
    for titulo, html, md in gerados:
        print(f"• {titulo}")
        print(f"  HTML : {html}")
        print(f"  MD   : {md}")
    print("-" * 60)
    print("Pronto. Cada conto tem tom sombrio/adulto formal, comentários breves")
    print("do agente (apenas reações) e fontes consultadas ao final.")


if __name__ == "__main__":
    main()
