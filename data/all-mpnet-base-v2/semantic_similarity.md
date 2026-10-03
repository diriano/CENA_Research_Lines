# Rede de similaridade temática

Período: 2021-01-01 a 2026-12-31; apenas trabalhos OpenAlex com `type = article`.
Modelo: `sentence-transformers/all-mpnet-base-v2`. Um vetor por artigo a partir de título (0.25), abstract (0.6) e keywords (0.15); pesos dos campos presentes são renormalizados. Abstracts longos são processados em partes.
Cada orientador é representado pela direção média dos vetores de seus artigos. O peso da aresta é a similaridade de cosseno entre os perfis de dois orientadores.
Artigos em coautoria entre o par de orientadores foram excluídos da comparação desse par.
A rede usa a união dos 4 vizinhos mais próximos de cada orientador (similaridade mínima 0). A matriz CSV contém todos os pares comparáveis.
Células vazias da matriz indicam ausência de artigos com texto para comparar após a exclusão.

| Orientador | Áreas | Artigos | Com texto | Com abstract | Com keywords |
| --- | --- | ---: | ---: | ---: | ---: |
| Adibe Luiz Abdalla | B+N+Q | 83 | 83 | 59 | 83 |
| Antonio Vargas de Oliveira Figueira | B | 27 | 27 | 22 | 27 |
| Cassio Hamilton Abreu Junior | B+N+Q | 35 | 35 | 26 | 35 |
| Diego Mauricio Riaño Pachón | B | 27 | 27 | 25 | 27 |
| Elisabete Aparecida De Nadai Fernandes | B+N+Q | 20 | 20 | 10 | 20 |
| Ernani Pinto Junior | B+Q | 58 | 58 | 40 | 58 |
| Flavia Vischi Winck | B | 17 | 17 | 15 | 17 |
| Francisco Scaglia Linhares | B | 13 | 13 | 10 | 13 |
| Helder Louvandini | B+N | 62 | 62 | 36 | 62 |
| Hudson Wallace Pereira de Carvalho | B+N+Q | 80 | 80 | 50 | 80 |
| José Lavres Junior | B+N+Q | 90 | 90 | 57 | 90 |
| Kassio Ferreira Mendes | B+N+Q | 75 | 75 | 63 | 75 |
| Lucas William Mendes | B | 155 | 155 | 77 | 154 |
| Luiz Carlos Ruiz Pessenda | B+N+Q | 37 | 37 | 19 | 37 |
| Marisa de Cassia Piccolo | B | 36 | 36 | 25 | 36 |
| Marli de Fatima Fiore | B+N+Q | 32 | 32 | 24 | 31 |
| Tsai Siu Mui | B+N+Q | 73 | 73 | 50 | 73 |
| Luiz Antonio Martinelli | N | 48 | 48 | 29 | 48 |
| Quirijn de Jong van Lier | N | 46 | 46 | 32 | 46 |
| Thiago de Araújo Mastrangelo | N | 14 | 14 | 12 | 14 |
| Valter Arthur | N | 42 | 42 | 40 | 42 |
| Alex Virgilio | Q | 14 | 14 | 10 | 14 |
| Celia Regina Montes | Q | 20 | 20 | 11 | 20 |
| Fabio Rodrigo Piovezani Rocha | Q | 45 | 45 | 22 | 45 |
| Marcos Yassuo Kamogawa | Q | 5 | 5 | 4 | 5 |
| Severino Matias de Alencar | Q | 104 | 104 | 66 | 104 |
| Wanessa Melchert Mattos | Q | 35 | 35 | 16 | 35 |

## Ligações mais fortes

| Orientador 1 | Orientador 2 | Similaridade | Artigos compartilhados |
| --- | --- | ---: | ---: |
| Cassio Hamilton Abreu Junior | Marisa de Cassia Piccolo | 0.919300 | 0 |
| José Lavres Junior | Marisa de Cassia Piccolo | 0.897473 | 0 |
| Cassio Hamilton Abreu Junior | José Lavres Junior | 0.893929 | 5 |
| Hudson Wallace Pereira de Carvalho | José Lavres Junior | 0.879584 | 14 |
| Lucas William Mendes | Tsai Siu Mui | 0.872395 | 22 |
| Cassio Hamilton Abreu Junior | Hudson Wallace Pereira de Carvalho | 0.868644 | 1 |
| Fabio Rodrigo Piovezani Rocha | Wanessa Melchert Mattos | 0.860725 | 4 |
| Hudson Wallace Pereira de Carvalho | Marisa de Cassia Piccolo | 0.822415 | 0 |
| Francisco Scaglia Linhares | Hudson Wallace Pereira de Carvalho | 0.804165 | 2 |
| Elisabete Aparecida De Nadai Fernandes | Alex Virgilio | 0.797745 | 0 |
| Alex Virgilio | Fabio Rodrigo Piovezani Rocha | 0.797534 | 1 |
| Hudson Wallace Pereira de Carvalho | Marcos Yassuo Kamogawa | 0.796253 | 0 |
| Antonio Vargas de Oliveira Figueira | Diego Mauricio Riaño Pachón | 0.790779 | 2 |
| Marisa de Cassia Piccolo | Luiz Antonio Martinelli | 0.784892 | 0 |
| Ernani Pinto Junior | Marli de Fatima Fiore | 0.775284 | 7 |
| Luiz Antonio Martinelli | Celia Regina Montes | 0.772893 | 0 |
| Cassio Hamilton Abreu Junior | Marcos Yassuo Kamogawa | 0.770263 | 0 |
| Antonio Vargas de Oliveira Figueira | Francisco Scaglia Linhares | 0.768740 | 0 |
| Cassio Hamilton Abreu Junior | Kassio Ferreira Mendes | 0.768549 | 0 |
| Luiz Carlos Ruiz Pessenda | Luiz Antonio Martinelli | 0.761391 | 0 |
