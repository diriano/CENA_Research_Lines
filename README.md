# Proposta de reorganizacao das linhas de pesquisa do PPG-Ciências CENA/USP

## Autor

- [Diego Mauricio Riaño Pachón](https://labbces.cena.usp.br/author/diego-mauricio-riano-pachon/)

## Justificativa

Está é uma metodologia proposta para agrupar as linhas de pesquisa dos orientadores do PPG-Ciencias CENA/USP. Atualmente existem 16 linhas de pesquisa. O intuito é reduzir esse número de acordo a temas mais gerais, e que agrupem varios orientadores. Atualmente existem linhas de pesquisa com um único orientador o que não é desejavel.

## Métodos

### Orientadores
Foi coletada a lista de orientadores atualmente credenciados no programa (08/2026), a informacão foi armazenada num arquivo [json](data/supervisors.json), indicando as áreas de concentracão em que atua cada orientador.

Foram identificados os perfis dos orientadores no [OpenAlex](https://openalex.org/) usando sua [API](https://api.openalex.org), usando o script [collect.py](scripts/collect.py)

```bash
python3 ./scripts/collect.py ../PPG_Ciencias_Research_Lines/
```

Essa primeira busca tem que ser curada manualmente para remover homonimos, e manter só orientadores validados com ORCID. O resultado está no arquivo [candidates.json](data/candidates.json).

### Recuperando as publicacoes dos orientadores

Foram analizadas as publicacoes num periodo dos 5 anos mas recentes e completos (01/01/2021 a 31/12/2025). A coleta das publicacoes foi realizada em 01/10/2026 a travez de consulta automatizada no banco de dados [OpenAlex](https://openalex.org/) usando sua [API](https://api.openalex.org), usando o script [works.py](scripts/works.py).


```bash
python3 ./scripts/works.py ../PPG_Ciencias_Research_Lines/
```

