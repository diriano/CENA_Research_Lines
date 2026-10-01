# Proposta de reorganizacao das linhas de pesquisa do PPG-Ciências CENA/USP

## Autor

- [Diego Mauricio Riaño Pachón](https://labbces.cena.usp.br/author/diego-mauricio-riano-pachon/)

## Justificativa

Está é uma metodologia proposta para agrupar as linhas de pesquisa dos orientadores do PPG-Ciencias CENA/USP. Atualmente existem 16 linhas de pesquisa. O intuito é reduzir esse número de acordo a temas mais gerais, e que agrupem varios orientadores. Atualmente existem linhas de pesquisa com um único orientador o que não é desejavel.

## Métodos

## Dependências

Para executar os scripts abaixo precisa das seguintes biobliotecas instaladas:

```bash
python -m pip install openpyxl
```

### Orientadores
Foi coletada a lista de orientadores atualmente credenciados no programa (08/2026), a informacão foi armazenada num arquivo [json](data/supervisors.json), indicando as áreas de concentracão em que atua cada orientador.

Foram identificados os perfis dos orientadores no [OpenAlex](https://openalex.org/) usando sua [API](https://api.openalex.org), usando o script [collect.py](scripts/collect.py)

```bash
python3 ./scripts/collect.py ../PPG_Ciencias_Research_Lines/
```

Essa primeira busca tem que ser curada manualmente para remover homonimos, e manter só orientadores validados com ORCID. O resultado está no arquivo [candidates.json](data/candidates.json).

### Recuperando as publicacoes dos orientadores

Foram analizadas as publicacoes desde jenaieo de 2021. Nos scripts usados as datas são controladas pelas variaveis START_DATE e END_DATE. A coleta das publicacoes foi realizada em 01/10/2026 a travez de consulta automatizada no banco de dados [OpenAlex](https://openalex.org/) usando sua [API](https://api.openalex.org), usando o script [works.py](scripts/works.py).


```bash
python3 ./scripts/works.py ../PPG_Ciencias_Research_Lines/
```
The script [works_to_excel.py](scripts/works_to_excel.py), gera uma [tabela de excel](data/candidate_publications.xlsx) com os detalhes das publicacoes dos orientadores. 

Usando as publicacoes dos orientadores gerei uma rede de co-autoria para explorar a formacao de comunidades a partir dessas intereacoes, usando o script [coauthorship.py](scripts/coauthorship.py), que gera um grafo em formato [graphml](data/coauthorship.graphml), e tam

```bash
python3 ./scripts/coauthorship.py ../PPG_Ciencias_Research_Lines/
```

Os nós foram coloridos baseados nas áreas de concentracao:

| Biologia (B) | Laranja | #FD8D3C |
| Nuclear (N) | Rosa | #FDE0DD | 
| Química (Q) | Vermelho | #EF3B2C | 
| B + N | Verde | #41AB5D | 
| B + Q | Lilas | #D0D1E6 | 
| B + N + Q | Verde claro | #99D8C9 | 

![Coauthorship network supervisors PPG-Ciencias CENA/USP](Figs/coauthorship.png)
**Figura. Rede de coautoria dos orientadores do PPG-Ciências (2021–2026).**
Cada nó representa um orientador incluído em [candidates.json](data/candidates.json). Uma aresta liga dois orientadores quando ambos são autores de pelo menos um artigo registrado no OpenAlex (identificado pelo DOI); sua espessura representa o número de artigos distintos em coautoria. As cores indicam as áreas de concentração informadas em [supervisors.json](data/supervisors.json): B = Biologia na Agricultura e no Ambiente; N = Energia Nuclear na Agricultura e no Ambiente; Q = Química na Agricultura e no Ambiente. Orientadores vinculados a mais de uma área aparecem nas categorias combinadas B+N, B+Q ou B+N+Q.