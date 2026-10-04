# Análise das linhas de pesquisa do CENA/USP

## Autor

- [Diego Mauricio Riaño Pachón](https://labbces.cena.usp.br/author/diego-mauricio-riano-pachon/)

## Justificativa

Esta metodologia foi desenvolvida para examinar a produção científica dos docentes do [CENA/USP](https://www.cena.usp.br/). 

## Resultados

### Rede de coautoria

O grafo resultante está em [coauthorship.graphml](data/coauthorship.graphml) e pode ser aberto no Cytoscape. A tabela abaixo resume o número de artigos atribuído a cada orientador no conjunto analisado, no periodo de 2021 a 2026, com base nos registros do OpenAlex. Divisão: P = DVPROD, E = DVECO e T = DVTEC.

| Orientador | Divisão | Número de artigos |
| --- | --- | ---: |
| Adibe Luiz Abdalla | P | 82 |
| Adriana Pinheiro Martinelli | P | 29 |
| Antonio Vargas de Oliveira Figueira | P | 27 |
| Augusto Tulmann Neto | P | 3 |
| Cassio Hamilton Abreu Junior | P | 35 |
| Diego Mauricio Riaño Pachón | P | 28 |
| Flavia Vischi Winck | P | 17 |
| Francisco Scaglia Linhares | P | 13 |
| Helder Louvandini | P | 61 |
| Lucas William Mendes | P | 155 |
| Thiago de Araújo Mastrangelo | P | 14 |
| Marli de Fatima Fiore | P | 32 |
| Valter Arthur | P | 42 |
| Alex Vladimir Krusche | E | 9 |
| Ernani Pinto Junior | E | 59 |
| Kassio Ferreira Mendes | E | 76 |
| Luiz Antonio Martinelli | E | 48 |
| Quirijn de Jong van Lier | E | 46 |
| Giuliano Maselli Locosselli | E | 33 |
| Marcelo Zacharias Moreira | E | 29 |
| Maria Gabriella da Silva Araújo | E | 15 |
| Maria Victoria Ramos Ballester | E | 8 |
| Marília Campos | T | 23 |
| Mauricio Cruz Mantoani | E | 22 |
| Paulo César Ocheuze Trivelin | T | 14 |
| Plínio Barbosa de Camargo | E | 95 |
| Rafael Silva Santos | E | 17 |
| Samara Soares | T | 17 |
| Thaís Nascimento Pessoa | E | 13 |
| Tsai Siu Mui | P | 73 |
| Victor Alexandre Vitorello | P | 2 |
| Valdemar Luiz Tornisielo | E | 35 |
| Fabio Rodrigo Piovezani Rocha | T | 45 |
| Deoclecio Jardim Amorim | T | 15 |
| Eduardo Mariano | T | 27 |
| Elias Ayres Guidetti Zagatto | T | 8 |
| Boaventura Freire dos Reis | T | 4 |
| Luiz Carlos Ruiz Pessenda | T | 37 |
| Elisabete Aparecida De Nadai Fernandes | T | 20 |
| Alex Virgilio | T | 14 |
| Hudson Wallace Pereira de Carvalho | T | 80 |
| José Lavres Junior | T | 91 |

No Cytoscape, os nós foram coloridos assim:

| Divisão | Cor usada | Código hexadecimal |
| --- | --- | ---: |
| DVPROD (P) | Laranja | #FEBD2A |
| DVECO (E) | Verde | #4CC26C | 
| DVTEC (T) | Roxo | #8B0AA5 | 

![Rede de coautoria dos docentes CENA/USP](Figs/coauthorship.png)

**Figura 1. Rede de coautoria dos docentes do CENA/USP (2021–2026).**
Os nós representam os docentes presentes em [candidates.json](data/candidates.json). Uma aresta indica ao menos um artigo compartilhado no OpenAlex; sua espessura corresponde ao número de artigos distintos em coautoria. As cores mostram as divisões científicas.

### Rede de similaridade semântica

##### Tabela de docentes e número de artigos com título, abstract e keywords incluidos na rede semântica

| Orientador | Áreas | Artigos | Com texto | Com abstract | Com keywords |
| --- | --- | ---: | ---: | ---: | ---: |
| Adibe Luiz Abdalla | P | 82 | 82 | 58 | 82 |
| Adriana Pinheiro Martinelli | P | 29 | 29 | 21 | 28 |
| Antonio Vargas de Oliveira Figueira | P | 27 | 27 | 22 | 27 |
| Augusto Tulmann Neto | P | 3 | 3 | 2 | 3 |
| Cassio Hamilton Abreu Junior | P | 35 | 35 | 26 | 35 |
| Diego Mauricio Riaño Pachón | P | 28 | 28 | 26 | 28 |
| Flavia Vischi Winck | P | 17 | 17 | 15 | 17 |
| Francisco Scaglia Linhares | P | 13 | 13 | 10 | 13 |
| Helder Louvandini | P | 61 | 61 | 35 | 61 |
| Lucas William Mendes | P | 155 | 155 | 77 | 155 |
| Thiago de Araújo Mastrangelo | P | 14 | 14 | 12 | 14 |
| Marli de Fatima Fiore | P | 32 | 32 | 24 | 30 |
| Valter Arthur | P | 42 | 42 | 40 | 42 |
| Alex Vladimir Krusche | E | 9 | 9 | 6 | 9 |
| Ernani Pinto Junior | E | 59 | 59 | 41 | 58 |
| Kassio Ferreira Mendes | E | 76 | 76 | 63 | 76 |
| Luiz Antonio Martinelli | E | 48 | 48 | 29 | 48 |
| Quirijn de Jong van Lier | E | 46 | 46 | 32 | 46 |
| Giuliano Maselli Locosselli | E | 33 | 33 | 20 | 33 |
| Marcelo Zacharias Moreira | E | 29 | 29 | 16 | 29 |
| Maria Gabriella da Silva Araújo | E | 15 | 15 | 10 | 15 |
| Maria Victoria Ramos Ballester | E | 8 | 8 | 7 | 8 |
| Marília Campos | T | 23 | 23 | 9 | 23 |
| Mauricio Cruz Mantoani | E | 22 | 22 | 17 | 22 |
| Paulo César Ocheuze Trivelin | T | 14 | 14 | 8 | 14 |
| Plínio Barbosa de Camargo | E | 95 | 95 | 53 | 95 |
| Rafael Silva Santos | E | 17 | 17 | 6 | 17 |
| Samara Soares | T | 17 | 17 | 5 | 17 |
| Thaís Nascimento Pessoa | E | 13 | 13 | 6 | 13 |
| Tsai Siu Mui | P | 73 | 73 | 50 | 73 |
| Victor Alexandre Vitorello | P | 2 | 2 | 2 | 2 |
| Valdemar Luiz Tornisielo | E | 35 | 35 | 25 | 35 |
| Fabio Rodrigo Piovezani Rocha | T | 45 | 45 | 22 | 45 |
| Deoclecio Jardim Amorim | T | 15 | 15 | 12 | 15 |
| Eduardo Mariano | T | 27 | 27 | 16 | 27 |
| Elias Ayres Guidetti Zagatto | T | 8 | 8 | 6 | 8 |
| Boaventura Freire dos Reis | T | 4 | 4 | 3 | 4 |
| Luiz Carlos Ruiz Pessenda | T | 37 | 37 | 19 | 37 |
| Elisabete Aparecida De Nadai Fernandes | T | 20 | 20 | 10 | 20 |
| Alex Virgilio | T | 14 | 14 | 10 | 14 |
| Hudson Wallace Pereira de Carvalho | T | 80 | 80 | 50 | 80 |
| José Lavres Junior | T | 91 | 91 | 58 | 91 |

##### Ligações mais fortes de acordo com a similaridade semântica entre orientadores (2021–2026)

| Orientador 1 | Orientador 2 | Similaridade | Artigos compartilhados |
| --- | --- | ---: | ---: |
| Luiz Antonio Martinelli | Plínio Barbosa de Camargo | 0.972827 | 13 |
| Kassio Ferreira Mendes | Valdemar Luiz Tornisielo | 0.969086 | 14 |
| Luiz Antonio Martinelli | Marcelo Zacharias Moreira | 0.968995 | 4 |
| Hudson Wallace Pereira de Carvalho | José Lavres Junior | 0.966935 | 14 |
| Maria Gabriella da Silva Araújo | Plínio Barbosa de Camargo | 0.966906 | 3 |
| Cassio Hamilton Abreu Junior | José Lavres Junior | 0.963781 | 5 |
| Lucas William Mendes | Tsai Siu Mui | 0.962672 | 22 |
| Paulo César Ocheuze Trivelin | Eduardo Mariano | 0.960274 | 3 |
| Cassio Hamilton Abreu Junior | Hudson Wallace Pereira de Carvalho | 0.958170 | 1 |
| Eduardo Mariano | José Lavres Junior | 0.955692 | 5 |
| Cassio Hamilton Abreu Junior | Eduardo Mariano | 0.954282 | 1 |
| Marcelo Zacharias Moreira | Plínio Barbosa de Camargo | 0.952268 | 4 |
| Plínio Barbosa de Camargo | Rafael Silva Santos | 0.950232 | 0 |
| Paulo César Ocheuze Trivelin | José Lavres Junior | 0.947837 | 0 |
| Marcelo Zacharias Moreira | Maria Gabriella da Silva Araújo | 0.946419 | 2 |
| Plínio Barbosa de Camargo | Luiz Carlos Ruiz Pessenda | 0.946386 | 0 |
| Plínio Barbosa de Camargo | Deoclecio Jardim Amorim | 0.945170 | 0 |
| Giuliano Maselli Locosselli | Plínio Barbosa de Camargo | 0.944615 | 0 |
| Mauricio Cruz Mantoani | Plínio Barbosa de Camargo | 0.944567 | 0 |
| Maria Victoria Ramos Ballester | Rafael Silva Santos | 0.943360 | 0 |


![Rede de similaridade semântica global CENA/USP](Figs/semantic_similarity.png)
**Figura 2. Rede semântica global.**

### Rede de similaridade semântica por divisão científica

As saídas em `data/` incluem [area_semantic.graphml](data/area_semantic.graphml) (que pode ser visualizado em Cytoscape) e os arquivos [area_semantic_P.graphml](data/area_semantic_P.graphml), [area_semantic_E.graphml](data/area_semantic_E.graphml) e [area_semantic_T.graphml](data/area_semantic_T.graphml); [area_semantic_nodes.csv](data/area_semantic_nodes.csv) e [area_semantic_edges.csv](data/area_semantic_edges.csv) descrevem seus nós e arestas. [area_semantic_matrix_P.csv](data/area_semantic_matrix_P.csv), [area_semantic_matrix_E.csv](data/area_semantic_matrix_E.csv) e [area_semantic_matrix_T.csv](data/area_semantic_matrix_T.csv) preservam os pares comparáveis que não aparecem nas redes. [area_semantic_coverage.csv](data/area_semantic_coverage.csv) mostra quantos artigos de cada docentes foram aproveitados em cada divisão. Os vetores dos artigos ficam em cache em [area_semantic_embeddings.npz](data/area_semantic_embeddings.npz), de modo que uma nova execução após a curadoria no arquivo ([work_area_curated.csv](data/work_area_curated.csv)) pode reutilizá-los.

| Área | Orientadores de referência | Artigos de referência | Artigos atribuídos |
| --- | ---: | ---: | ---: |
| B | 6 | 266 | 967 |
| N | 4 | 145 | 957 |
| Q | 6 | 216 | 837 |

Para discutir novas linhas de pesquisa, a rede global pode indicar aproximações amplas; as redes por área mostram **quais dessas aproximações persistem** quando os artigos são filtrados. A interpretação final deve considerar cobertura desigual de publicações, qualidade da atribuição dos artigos às áreas, termos e artigos representativos, além das prioridades do programa.


![Rede de similaridade semântica por divisão CENA/USP](Figs/area_semantic.png)
**Figura 3. Redes semânticas por divisão científica.**
A imagem apresenta três conjuntos separados: DVPROD (P), à esquerda; Química (Q), na região superior direita; e Energia Nuclear (N), abaixo. Cada nó corresponde à atuação de um orientador naquela área, identificada pelo prefixo B::, N:: ou Q::. Por isso, orientadores vinculados a várias áreas podem aparecer mais de uma vez em diferentes conjuntos. As linhas verdes ligam pares de orientadores dentro da mesma área. A separação entre B, N e Q decorre da construção da rede, que não inclui arestas entre áreas. As posições dos nós também dependem do algoritmo de disposição e não devem ser interpretadas como uma escala numérica de similaridade. As cores dos nós correspondem ás comunidades detectadas pelo algoritmo de Louvain. A espessura das arestas indica a similaridade semantica entre os orientadores, calculada com base em títulos, resumos e palavras-chave dos artigos.

### Proposta de linhas de pesquisa por área

#### Biologia na agricultura e no ambiente (B)

| Grupo | Título representativo |
| --- | --- |
| B1 | Nutrição vegetal, fertilidade do solo e contaminantes |
| B2 | Biologia integrativa, genômica e biotecnologia |
| B3 | Ecologia de ecossistemas, microbiomas e mudanças ambientais |
| B4 | Nutrição animal, saúde e emissões de gases de efeito estufa |

#### Energia Nuclear na agricultura e no ambiente (N)

| Grupo | Título representativo |
| --- | --- | 
| N1 | Aplicações da radiação na produção animal |
| N2 | Ciclos biogeoquímicos e dinâmica ambiental |
| N3 | Fertilidade do solo, nutrição vegetal e comportamento de herbicidas |

#### Química na agricultura e no ambiente (Q)

| Grupo | Título representativo |
| --- | --- |
| Q1 | Química ambiental e biogeoquímica de solos e ecossistemas |
| Q2 | Química analítica e compostos bioativos |

## Limitações e possibilidades de aprimoramento

Um orientador pode estar vinculado a B, N e Q, mas sua produção não se distribui necessariamente da mesma forma entre essas áreas. Na rede global, todos os seus artigos elegíveis contribuem para um único perfil temático. Na análise por área, o orientador pode aparecer nas três redes, porém cada artigo é primeiro classificado: ele contribui apenas para as áreas que lhe foram atribuídas, e pode contribuir para mais de uma. Assim, o script não replica automaticamente todos os artigos do orientador em todas as suas áreas. A separação obtida depende, contudo, da qualidade dessa atribuição.
A classificação automática usa como referências publicações de orientadores vinculados a uma única área, descartando das referências os artigos também associados a orientadores exclusivos de outra área. Esse procedimento oferece um ponto de partida, mas o vínculo institucional exclusivo de um orientador não garante que cada um de seus artigos seja tematicamente exclusivo daquela área. Por isso, work_area_curated.csv permite corrigir as sugestões antes de interpretar as redes e os grupos.

Uma possibilidade de aprimoramento é usar as teses e dissertações dos egressos como referências temáticas. A relação orientador → egresso → tese/dissertação permite reunir trabalhos desenvolvidos no âmbito do programa. Com o registro da área de concentração oficial de cada trabalho, títulos, resumos e palavras-chave de teses e dissertações dessa área são exemplos mais diretamente ligados às definições institucionais de B, N e Q. Para orientadores que atuam em várias áreas, essa informação ajudaria a distinguir os temas de orientação em cada uma delas. 

Essa estratégia ainda exigiria atenção à cobertura desigual de teses entre áreas, a possíveis mudanças de temas ao longo do tempo e à diferença de idioma entre dissertações em português e artigos majoritariamente em inglês. Trata-se de uma proposta metodológica futura: os scripts atuais não incorporam teses ou dissertações.

## Métodos

## Dependências

Para executar os scripts abaixo precisa das seguintes bibliotecas de python3 instaladas:

```bash
git clone git@github.com:labbces/CENA_Research_Lines.git
cd CENA_Research_Lines
python -m venv .venv
source .venv/bin/activate
python -m pip install openpyxl numpy sentence-transformers scipy scikit-learn networkx
```

### Seleção dos orientadores

A lista de orientadores credenciados no programa em agosto de 2026 e suas áreas de concentração foi registrada em [supervisors.json](data/supervisors.json). Neste documento, **B** corresponde a Biologia na Agricultura e no Ambiente; **N**, a Energia Nuclear na Agricultura e no Ambiente; e **Q**, a Química na Agricultura e no Ambiente. Um orientador pode estar vinculado a mais de uma área.

Os perfis dos orientadores foram procurados no [OpenAlex](https://openalex.org/) por meio de sua [API](https://api.openalex.org), usando [collect.py](scripts/collect.py):

```bash
python3 ./scripts/collect.py ../CENA_Research_Lines/
```

Os resultados dessa busca foram conferidos manualmente para eliminar homônimos e manter os perfis validados com ORCID. Os identificadores selecionados estão em [candidates.json](data/candidates.json). Essa revisão é importante porque um perfil atribuído ao orientador errado contaminaria todas as etapas seguintes. Todos os orientadores credenciados estão presentes em [candidates.json](data/candidates.json).

### Recuperação das publicações

A consulta ao OpenAlex ocorreu em **1º de outubro de 2026**. O [works.py](scripts/works.py) disponível neste projeto solicita trabalhos publicados de **1º de janeiro de 2021 a 31 de dezembro de 2026**. O script consulta os perfis selecionados em `candidates.json` e guarda as respostas da API em arquivos JSON separados por identificador de autor.

Os arquivos de trabalhos são gravados em sua subpasta `data/raw/`.

```bash
python3 ./scripts/works.py ../CENA_Research_Lines/
```

O script [works_to_excel.py](scripts/works_to_excel.py), gera uma [planilha de publicações](data/candidate_publications.xlsx) com os detalhes das publicações dos orientadores. Foram identificados **1.732 registros** de publicações de diferentes tipos, incluindo artigos, livros, capítulos e preprints. A planilha contém título, DOI, lista de autores, orientador associado, ano, tipo de publicação e ID do trabalho no OpenAlex. Um mesmo trabalho pode aparecer em mais de uma linha se estiver associado a mais de um orientador; portanto, o número de registros não representa necessariamente 1.732 publicações distintas. Os resumos e as palavras-chave permanecem nos arquivos JSON usados na análise semântica, mas não são exportados por esta versão de `works_to_excel.py`.

### Rede de coautoria

O script [coauthorship.py](scripts/coauthorship.py) constrói uma rede somente com os orientadores de `candidates.json`, considerando registros do OpenAlex com `type = article`. Cada nó representa um orientador. Dois nós são ligados quando os respectivos orientadores aparecem associados ao **mesmo ID de trabalho do OpenAlex**; o peso da aresta é o número de artigos distintos compartilhados. Um artigo é contado apenas uma vez por orientador, mesmo quando há identificadores de autor duplicados ou registros repetidos nos arquivos de entrada.

```bash
python3 ./scripts/coauthorship.py ../CENA_Research_Lines/
```

### Similaridade semântica entre orientadores

O script [semantic_similarity.py](scripts/semantic_similarity.py) utiliza títulos, resumos (*abstracts*) e palavras-chave (*keywords*) dos artigos para estimar a proximidade temática entre orientadores. Ele usa um modelo da biblioteca [Sentence Transformers](https://www.sbert.net/) para transformar textos em **embeddings**: vetores numéricos cujas posições procuram representar relações de significado aprendidas durante o treinamento. Neste estudo, a semelhança entre vetores é usada como aproximação da semelhança entre os temas dos textos; não é uma classificação definitiva das linhas de pesquisa.

#### Como o transformer produz um embedding

1. **Divisão em tokens.** O texto é separado em unidades menores, chamadas *tokens*. Elas podem corresponder a palavras inteiras ou a partes de palavras. Os tokens são convertidos em identificadores numéricos de entrada do modelo.
2. **Representação contextual.** O transformer processa os tokens em conjunto. Pelo mecanismo de *[atenção](https://doi.org/10.48550/arXiv.1706.03762)*, a representação de cada token é ajustada com base nos demais tokens do mesmo trecho. Por isso, uma palavra pode contribuir de formas diferentes conforme o contexto em que aparece. Essa representação é aprendida pelo modelo durante o treinamento; o script não atribui manualmente um valor a cada palavra.
3. **Agregação dos tokens.** Para obter um único vetor por trecho de texto, o modelo Sentence Transformers combina as representações contextualizadas dos tokens por uma operação chamada *pooling*. Nos dois modelos mencionados abaixo, a operação configurada é a média dos tokens válidos, desconsiderando o preenchimento usado nos lotes. O resultado é um vetor denso: **768 dimensões** com `all-mpnet-base-v2` ou **384 dimensões** com `paraphrase-multilingual-MiniLM-L12-v2`. Cada dimensão participa da representação aprendida; ela não deve ser interpretada isoladamente como um tema específico.
4. **Normalização.** O script normaliza esses vetores para comprimento unitário antes de combiná-los. Dessa forma, a comparação posterior se concentra na direção dos vetores, e não em sua magnitude.

Essas etapas descrevem a codificação **de um trecho de texto**. O script ainda precisa combinar trechos, campos e artigos:

1. **Trechos de texto:** antes de enviar um campo ao modelo, o script o divide em blocos de até 112 tokens de texto por padrão, respeitando o limite do modelo e reservando espaço para seus tokens especiais. A opção `--max-tokens N` muda o limite total de cada trecho, **incluindo** os tokens especiais; por exemplo, com `--max-tokens 512`, um modelo que usa dois tokens especiais recebe no máximo 510 tokens do texto. Um valor acima do limite do modelo produz um erro explícito. Isso evita descartar o fim de resumos longos. Se houver vários blocos, calcula a média de seus vetores e normaliza o resultado. A média preserva informação dos blocos, mas não representa as relações de ordem entre blocos distantes.
2. **Campos de um artigo:** combina separadamente os vetores do título, do resumo e das palavras-chave. Com os valores padrão, seus pesos relativos são, respectivamente, **25%, 60% e 15%**. Se faltar um campo, os pesos dos campos presentes são redistribuídos proporcionalmente. O vetor final do artigo é normalizado. Esses pesos são escolhas metodológicas do script, não parâmetros aprendidos pelo transformer, e podem ser alterados por opções de linha de comando.
3. **Artigos de um orientador:** combina os vetores dos artigos do orientador, dando o mesmo peso a cada artigo, e normaliza o perfil resultante. O script trabalha apenas com registros `type = article` e usa o intervalo de datas indicado na execução.
4. **Comparação entre dois orientadores:** por padrão, retira dos **dois perfis daquele par** os artigos que ambos assinaram. Isso evita que um mesmo trabalho compartilhado aumente diretamente a similaridade do par. Os perfis usados nessa comparação, portanto, podem variar conforme o par; se um orientador ficar sem artigos após a exclusão, não há valor de similaridade para esse par. A opção `--include-shared` mantém os artigos compartilhados.
5. **Similaridade e rede:** calcula o **cosseno** entre os dois perfis normalizados, equivalente ao produto escalar de seus vetores. O valor matemático está entre −1 e 1; valores maiores indicam direções mais próximas, mas **não são porcentagens de temas em comum nem probabilidades**. O parâmetro `--top-k` escolhe os *k* vizinhos comparáveis mais próximos de cada orientador. A rede contém a **união** dessas escolhas: uma ligação entra se for escolhida por pelo menos um dos dois nós, de modo que um nó pode terminar com mais de *k* ligações. A matriz CSV guarda também as comparações que não viraram arestas.

#### Resultados da análise da rede semântica

Nesta análise foi escolhido o modelo [BAAI/bge-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5), outras alternativas mais baratas computacionalmente são [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) para textos majoritariamente em inglês, e [paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2), uma alternativa quando os textos incluem vários idiomas (este último é o **padrão do script**). São modelos de uso geral para embeddings de frases e parágrafos; nesta análise não houve ajuste adicional do modelo para o vocabulário específico do PPG-Ciências. A escolha do modelo afeta os vetores e, portanto, pode alterar as similaridades e as arestas. A base para a seleção do modelo foi um [benchmark recente](http://dx.doi.org/10.30970/eli.30.4) que avaliou varios modelos de embeddings em tarefas de similaridade semântica, classificação e recuperação de informação. O modelo BGE Large obteve o melhor na captura de relações semânticas, seguido por all-mpnet-base-v2 e paraphrase-multilingual-MiniLM-L12-v2. (Resultados com all-mpnet-base-v2 estão disponiveis em [data/semantic_similarity_all-mpnet-base-v2](data/semantic_similarity_all-mpnet-base-v2).)

```bash
python3 scripts/semantic_similarity.py ../CENA_Research_Lines/ \
  --model BAAI/bge-large-en-v1.5 \
  --max-tokens 512 \
  --device cpu \
  --top-k 4
```

Com essa execução, o script lê os arquivos em `PROJECT_ROOT/data/`, usa por padrão artigos de 2021 a 2026 **que estejam presentes nos arquivos JSON** e grava a rede em [semantic_similarity.graphml](data/semantic_similarity.graphml) (que pode ser visualizada em Cytoscape), além da [tabela de nós](data/semantic_similarity_nodes.csv), da [lista de arestas](data/semantic_similarity_edges.csv) e da [matriz completa de similaridade](data/semantic_similarity_matrix.csv). Os resultados descrevem proximidade no espaço vetorial do modelo e devem ser interpretados junto com os textos dos artigos e com a avaliação dos orientadores.

A rede gerada por `semantic_similarity.py` reúne todos os orientadores em uma única comparação. Ela ajuda a reconhecer afinidades temáticas que atravessam as áreas de concentração e a localizar pares cuja produção merece leitura mais atenta. Para interpretar seus resultados, convém distinguir os arquivos produzidos:

| Arquivo em `data/` | O que permite examinar |
| --- | --- |
| `semantic_similarity_nodes.csv` | Orientadores, áreas de concentração e número de artigos com texto utilizável. |
| `semantic_similarity_edges.csv` | Pares exibidos na rede, cosseno em `weight` e número de artigos que o par assinou em conjunto. |
| `semantic_similarity_matrix.csv` | Similaridade de todos os pares comparáveis, inclusive daqueles que ficaram fora da rede após a seleção dos vizinhos. |
| `semantic_similarity.graphml` | Rede para exploração visual no Cytoscape. |

Uma aresta forte sugere que os artigos **não compartilhados** daquele par tratam de assuntos próximos no espaço vetorial do modelo. A ausência de aresta **não** significa necessariamente baixa similaridade: o par pode simplesmente não ter sido escolhido entre os quatro vizinhos mais próximos de nenhum dos orientadores. Para conferir isso, consulte a matriz completa. Uma célula vazia indica que não foi possível calcular a similaridade do par, por exemplo, quando não restam artigos com texto após a exclusão dos trabalhos em coautoria. Os escores devem ser confrontados com títulos e resumos; sozinhos, não identificam linhas de pesquisa nem explicam a causa da proximidade.

### Da rede global às análises por área de concentração

O script [area_semantic.py](scripts/area_semantic.py) responde a uma pergunta mais específica: **quais orientadores se aproximam quando consideramos apenas os artigos pertinentes a uma determinada área de concentração?** Ele importa funções de `semantic_similarity.py` para ler os dados, gerar embeddings e calcular comparações, mas **não lê** `semantic_similarity.graphml`, a lista de arestas ou a matriz CSV da rede global. Pode, portanto, ser executado diretamente sobre `candidates.json`, `supervisors.json` e os JSON de artigos em `data/raw/`. Para comparar as duas análises, use o mesmo modelo, os mesmos pesos dos campos e o mesmo intervalo de datas.

O processamento por área ocorre em etapas:

1. **Classificação provisória dos artigos.** O script usa como referências iniciais artigos de orientadores vinculados a uma única área, deixando de fora das sementes os artigos também associados a orientadores exclusivos de outra área. Calcula um vetor médio para cada orientador de referência e, depois, um protótipo para B, N e Q. Cada artigo é comparado com esses três protótipos pelo cosseno. Com os parâmetros padrão, uma área é sugerida quando seu escore é pelo menos `0,20` e está a no máximo `0,05` do maior escore do artigo. Um artigo pode receber mais de uma área ou nenhuma. Os protótipos são referências automáticas, não definições oficiais das áreas.
2. **Conferência e curadoria.** `work_area_suggestions.csv` traz os escores `score_B`, `score_N` e `score_Q`, a distância entre os dois maiores escores (`score_gap`) e sinalizadores úteis para revisão, como ausência de resumo e atribuição a várias áreas. `work_area_curated.csv` lista cada artigo e os orientadores associados. Para corrigir uma área, edite a coluna `areas` com `B`, `N`, `Q` ou combinações como `B+N`; deixe-a vazia para excluir o artigo. O script preserva as alterações manuais e informa na tela quantos artigos receberam curadoria manual. Uma classificação incerta merece inspeção do texto original, mesmo quando o cosseno é alto.
3. **Perfis e redes específicos de B, N e Q.** Em cada área, o perfil de um orientador inclui somente seus artigos atribuídos àquela área, desde que ele seja vinculado a ela em `supervisors.json`. Artigos atribuídos a duas áreas podem contribuir para ambas. O script recalcula as similaridades entre os orientadores elegíveis de cada área, excluindo por padrão os artigos compartilhados na comparação de cada par. Por isso, uma ligação presente na rede global pode desaparecer na rede de uma área, ou um par pode ganhar destaque dentro dela: mudou o conjunto de artigos comparados e também o conjunto de vizinhos possíveis.
4. **Comunidades e temas propostos.** Em cada rede, o algoritmo de [Louvain](https://doi.org/10.1088/1742-5468/2008/10/P10008) identifica comunidades sem impor previamente sua quantidade. Separadamente, um agrupamento hierárquico propõe **três grupos por área** com `--groups 3`, quando há orientadores suficientes. Esse agrupamento combina, por padrão, 75% de similaridade semântica e 25% de proximidade lexical calculada por [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) sobre os textos da própria área; se não há escore semântico para um par, usa sua proximidade lexical. Os termos distintivos e títulos representativos ajudam a descrever cada grupo, mas são rótulos exploratórios, não nomes apropriados para linhas de pesquisa.

Um orientador vinculado a mais de uma área pode aparecer uma vez em **cada rede na qual tenha artigos classificados suficientes** (`--min-area-papers`, cujo padrão é 1): por exemplo, `B::Nome` e `N::Nome` são nós diferentes no GraphML combinado. As ligações conectam apenas orientadores da mesma área. Assim, é possível examinar se a atuação temática do mesmo orientador difere entre B e N, sem misturar seus artigos das duas áreas no perfil local.

Para atribuir os artigos as áreas, o script calcula a similaridade de cada artigo com protótipos de B, N e Q. A classificação provisória é registrada em [work_area_suggestions.csv](data/work_area_suggestions.csv). O arquivo [work_area_curated.csv](data/work_area_curated.csv) permite corrigir manualmente a área de cada artigo. O script lê esse arquivo e gera as redes por área.

```bash
python3 scripts/area_semantic.py ../CENA_Research_Lines/ \
  --model BAAI/bge-large-en-v1.5 \
  --max-tokens 512 \
  --device cpu \
  --top-k 4  \
  --groups 3
```