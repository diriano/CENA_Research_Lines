# Rede de similaridade temática

Período: 2021-01-01 a 2026-12-31; apenas trabalhos OpenAlex com `type = article`.
Modelo: `BAAI/bge-large-en-v1.5`. Um vetor por artigo a partir de título (0.25), abstract (0.6) e keywords (0.15); pesos dos campos presentes são renormalizados. Abstracts longos são processados em partes.
Limite de 512 tokens por segmento, incluindo tokens especiais.
Cada orientador é representado pela direção média dos vetores de seus artigos. O peso da aresta é a similaridade de cosseno entre os perfis de dois orientadores.
Artigos em coautoria entre o par de orientadores foram excluídos da comparação desse par.
A rede usa a união dos 4 vizinhos mais próximos de cada orientador (similaridade mínima 0). A matriz CSV contém todos os pares comparáveis.
Células vazias da matriz indicam ausência de artigos com texto para comparar após a exclusão.

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

## Ligações mais fortes

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
