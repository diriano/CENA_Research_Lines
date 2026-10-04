# Redes semânticas por divisão científica

Período: 2021-01-01 a 2026-12-31. Modelo: `BAAI/bge-large-en-v1.5`; dispositivo: `cpu`.
Limite de 512 tokens por segmento, incluindo tokens especiais.
Classificação provisória: comparação dos vetores de título, abstract e keywords com protótipos de artigos de orientadores vinculados a uma única área. Os protótipos dão o mesmo peso a cada orientador de referência.
O vínculo exclusivo de um orientador foi usado como referência inicial, não como validação de que todos os seus artigos pertencem àquela área.
Área atribuída se cosseno ≥ 0.2 e até 0.05 abaixo da área mais próxima. Múltiplas áreas são permitidas; 0 artigos têm correção manual em `work_area_curated.csv`.
Os valores são similaridades de cosseno, não probabilidades calibradas. Verifique os artigos e a interpretação institucional das áreas antes de usar a classificação para decisões do programa.
Artigos sem área atribuída: 0; atribuídos a mais de uma área: 1048. Use `review_flags` e `score_gap` para priorizar a conferência manual.
Em `work_area_curated.csv`, `supervisors` lista os orientadores do artigo; edite `areas` para corrigir (vazio exclui). Alterações manuais são preservadas; linhas automáticas são atualizadas a cada execução.
Os artigos compartilhados entre dois orientadores são excluídos apenas da comparação daquele par.

| Área | Orientadores de referência | Artigos de referência | Artigos atribuídos |
| --- | ---: | ---: | ---: |
| P | 15 | 477 | 974 |
| E | 14 | 417 | 1042 |
| T | 13 | 296 | 1027 |

Um artigo pode contar em mais de uma área. Para cada área, o perfil de um orientador usa apenas os seus artigos atribuídos àquela área.

## P — Divisão de Produtividade Agroindustrial e Alimentos

15 orientadores vinculados; 15 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Adibe Luiz Abdalla | 80 | sim |
| Adriana Pinheiro Martinelli | 29 | sim |
| Antonio Vargas de Oliveira Figueira | 27 | sim |
| Augusto Tulmann Neto | 3 | sim |
| Cassio Hamilton Abreu Junior | 34 | sim |
| Diego Mauricio Riaño Pachón | 28 | sim |
| Flavia Vischi Winck | 17 | sim |
| Francisco Scaglia Linhares | 13 | sim |
| Helder Louvandini | 61 | sim |
| Lucas William Mendes | 147 | sim |
| Thiago de Araújo Mastrangelo | 13 | sim |
| Marli de Fatima Fiore | 32 | sim |
| Valter Arthur | 41 | sim |
| Tsai Siu Mui | 63 | sim |
| Victor Alexandre Vitorello | 2 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| P1 | Adibe Luiz Abdalla; Augusto Tulmann Neto; Helder Louvandini; Thiago de Araújo Mastrangelo; Valter Arthur | gamma; irradiation; gamma irradiation; sheep; dose; radiation; feed; germination | Response of melon accessions to doses of Co60 gamma rays and their effects on the morphology of the M1 generation; Phenotypic variability in the M1 population of Citrullus lanatus (Thunb.) Matsum. & Nakai ‘Sugar Baby’ irradiated with Cobalt-60 gamma rays; Hormetic effects of low-dose gamma rays in soybean seeds and seedlings: A detection technique using optical sensors |
| P2 | Adriana Pinheiro Martinelli; Antonio Vargas de Oliveira Figueira; Cassio Hamilton Abreu Junior; Francisco Scaglia Linhares; Victor Alexandre Vitorello | leaf; pollen; fertilization; accumulation; development; sugarcane; plants; species | Molybdenum sources and incorporation methods into urea granules: impacts on 15N-fertilizer recovery, photosynthesis-related parameters, and sugarcane growth; Low pH-induced cell wall disturbances in Arabidopsis thaliana roots lead to a pattern-specific programmed cell death in the different root zones and arrested elongation in late elongation zone; Synergistic interaction of calcium and boron: enhancing root nodule anatomy, nitrogenase activity, leaf ultrastructure adjustments, and growth in soybean plants |
| P3 | Diego Mauricio Riaño Pachón; Flavia Vischi Winck; Lucas William Mendes; Marli de Fatima Fiore; Tsai Siu Mui | microbial; communities; soil; bacterial; cyanobacteria; gene; cyanobacterial; microbiome | The experience of teaching introductory programming skills to bioscientists in Brazil; The experience of teaching introductory programming skills to bioscientists in Brazil; Linking soil microbial genomic features to forest-to-pasture conversion in the Amazon |

### Proposta de até 2 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| P1 | Adibe Luiz Abdalla; Adriana Pinheiro Martinelli; Antonio Vargas de Oliveira Figueira; Cassio Hamilton Abreu Junior; Diego Mauricio Riaño Pachón; Flavia Vischi Winck; Francisco Scaglia Linhares; Helder Louvandini; Lucas William Mendes; Marli de Fatima Fiore; Tsai Siu Mui; Victor Alexandre Vitorello | soil; nitrogen; gene; microbial; methane; plant; species; metabolism | Molybdenum sources and incorporation methods into urea granules: impacts on 15N-fertilizer recovery, photosynthesis-related parameters, and sugarcane growth; Tithonia diversifolia Improves In Vitro Rumen Microbial Synthesis of Sheep Diets without Changes in Total Gas and Methane Production; Low pH-induced cell wall disturbances in Arabidopsis thaliana roots lead to a pattern-specific programmed cell death in the different root zones and arrested elongation in late elongation zone |
| P2 | Augusto Tulmann Neto; Thiago de Araújo Mastrangelo; Valter Arthur | gamma; irradiation; gamma irradiation; dose; radiation; germination; doses; seeds | Response of melon accessions to doses of Co60 gamma rays and their effects on the morphology of the M1 generation; Phenotypic variability in the M1 population of Citrullus lanatus (Thunb.) Matsum. & Nakai ‘Sugar Baby’ irradiated with Cobalt-60 gamma rays; Hormetic effects of low-dose gamma rays in soybean seeds and seedlings: A detection technique using optical sensors |

## E — Divisão de  Funcionamento de Ecossistemas Tropicais

14 orientadores vinculados; 14 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Alex Vladimir Krusche | 9 | sim |
| Ernani Pinto Junior | 51 | sim |
| Kassio Ferreira Mendes | 75 | sim |
| Luiz Antonio Martinelli | 48 | sim |
| Quirijn de Jong van Lier | 46 | sim |
| Giuliano Maselli Locosselli | 33 | sim |
| Marcelo Zacharias Moreira | 29 | sim |
| Maria Gabriella da Silva Araújo | 15 | sim |
| Maria Victoria Ramos Ballester | 8 | sim |
| Mauricio Cruz Mantoani | 22 | sim |
| Plínio Barbosa de Camargo | 95 | sim |
| Rafael Silva Santos | 17 | sim |
| Thaís Nascimento Pessoa | 13 | sim |
| Valdemar Luiz Tornisielo | 35 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| E1 | Ernani Pinto Junior; Kassio Ferreira Mendes; Luiz Antonio Martinelli; Giuliano Maselli Locosselli; Mauricio Cruz Mantoani; Valdemar Luiz Tornisielo | herbicide; control; urban; contamination; weed; glyphosate; cyanobacterial; herbicides | Can soil type interfere in sorption-desorption, mobility, leaching, degradation, and microbial activity of the 14C-tebuthiuron herbicide?; Does Microplastic Contamination in Agricultural Soils Decrease the Efficiency of Herbicides for Weed Control?; Occurrence and ecological risk assessment of pesticides in the waters of the Tietê River, São Paulo, Brazil |
| E2 | Quirijn de Jong van Lier; Maria Victoria Ramos Ballester; Plínio Barbosa de Camargo; Rafael Silva Santos; Thaís Nascimento Pessoa | soil; hydraulic; soil water; soil organic; organic; properties; carbon; water | Influence of intensive cropping of vegetables on physical and hydraulic properties and functions of an Oxisol in the Brazilian Cerrado; Consequences of land-use change in Brazil’s new agricultural frontier: A soil physical health assessment; Changes in soil organic matter fractions induced by cropland and pasture expansion in Brazil's new agricultural frontier |
| E3 | Alex Vladimir Krusche; Marcelo Zacharias Moreira; Maria Gabriella da Silva Araújo | dissolved; nitrogen; river; tocantins; tocantins river; carbon; isotopes; dissolved organic | Composition and Flux of Dissolved and Particulate Carbon and Nitrogen in the Lower Tocantins River; Composition and Flux of Dissolved and Particulate Carbon and Nitrogen in the Lower Tocantins River; Composition and Flux of Dissolved and Particulate Carbon and Nitrogen in the Lower Tocantins River |

### Proposta de até 2 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| E1 | Alex Vladimir Krusche; Luiz Antonio Martinelli; Quirijn de Jong van Lier; Giuliano Maselli Locosselli; Marcelo Zacharias Moreira; Maria Gabriella da Silva Araújo; Maria Victoria Ramos Ballester; Mauricio Cruz Mantoani; Plínio Barbosa de Camargo; Rafael Silva Santos; Thaís Nascimento Pessoa | carbon; isotopes; nitrogen; forest; stable; land; change; organic carbon | Seasonal Variation in Carbon Dynamics in the Lower Tocantins River: Influence of Discharge and Environmental Drivers; Composition and Flux of Dissolved and Particulate Carbon and Nitrogen in the Lower Tocantins River; Composition and Flux of Dissolved and Particulate Carbon and Nitrogen in the Lower Tocantins River |
| E2 | Ernani Pinto Junior; Kassio Ferreira Mendes; Valdemar Luiz Tornisielo | herbicide; weed; control; cyanobacterial; glyphosate; herbicides; weed control; contamination | Can soil type interfere in sorption-desorption, mobility, leaching, degradation, and microbial activity of the 14C-tebuthiuron herbicide?; Does Microplastic Contamination in Agricultural Soils Decrease the Efficiency of Herbicides for Weed Control?; Understanding the complexities in glyphosate and ametryn interactions: Soil retention and transformation as influenced by their applications alone and mixture |

## T — Divisão de Desenvolvimento de Métodos e Técnicas Analíticas Nucleares

13 orientadores vinculados; 13 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Marília Campos | 20 | sim |
| Paulo César Ocheuze Trivelin | 14 | sim |
| Samara Soares | 17 | sim |
| Fabio Rodrigo Piovezani Rocha | 45 | sim |
| Deoclecio Jardim Amorim | 14 | sim |
| Eduardo Mariano | 26 | sim |
| Elias Ayres Guidetti Zagatto | 8 | sim |
| Boaventura Freire dos Reis | 4 | sim |
| Luiz Carlos Ruiz Pessenda | 31 | sim |
| Elisabete Aparecida De Nadai Fernandes | 20 | sim |
| Alex Virgilio | 14 | sim |
| Hudson Wallace Pereira de Carvalho | 80 | sim |
| José Lavres Junior | 91 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| T1 | Marília Campos; Paulo César Ocheuze Trivelin; Deoclecio Jardim Amorim; Eduardo Mariano; Luiz Carlos Ruiz Pessenda; Hudson Wallace Pereira de Carvalho; José Lavres Junior | nitrogen; soil; tropical; fertilization; nutrient; efficiency; fertilizer; uptake | Can no-tillage and crop diversification sustain nutrient stocks in acidic and poorly-fertilized soils? Evidence from 32 years of real-world agricultural management in Paraguay; Genotype‐Dependent Modulation of Stomatal Function and Carbon Isotope Fractionation by Silicon in Common Bean Under Water Deficit; Molybdenum sources and incorporation methods into urea granules: impacts on 15N-fertilizer recovery, photosynthesis-related parameters, and sugarcane growth |
| T2 | Samara Soares; Fabio Rodrigo Piovezani Rocha; Elias Ayres Guidetti Zagatto; Boaventura Freire dos Reis; Elisabete Aparecida De Nadai Fernandes; Alex Virgilio | determination; flow; analytical; green; detection; analytical chemistry; chemistry; trace | Flow-based determination of lead exploiting in-syringe dispersive liquid-liquid micro-extraction in xylene and integrated spectrophotometric detection; Determination of volatile acids in sugarcane spirits exploring an air drag system and digital image photometry; Sample preparation and spectrometric methods for elemental analysis of milk and dairy products – A review |

### Proposta de até 2 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| T1 | Paulo César Ocheuze Trivelin; Samara Soares; Fabio Rodrigo Piovezani Rocha; Deoclecio Jardim Amorim; Eduardo Mariano; Elias Ayres Guidetti Zagatto; Boaventura Freire dos Reis; Elisabete Aparecida De Nadai Fernandes; Alex Virgilio; Hudson Wallace Pereira de Carvalho; José Lavres Junior | determination; nitrogen; green; analytical; detection; chemistry; analytical chemistry; flow | Determination of volatile acids in sugarcane spirits exploring an air drag system and digital image photometry; Flow-based determination of lead exploiting in-syringe dispersive liquid-liquid micro-extraction in xylene and integrated spectrophotometric detection; Sample preparation and spectrometric methods for elemental analysis of milk and dairy products – A review |
| T2 | Marília Campos; Luiz Carlos Ruiz Pessenda | holocene; south; atlantic; climate; mangrove; paleoclimate; sea-level; isotopes | Mid‐ to Late Holocene Contraction of the Intertropical Convergence Zone Over Northeastern South America; The coupling between monsoon rainfall and Sea Surface Temperature in the subtropical South Atlantic during the Last Glacial Period; Millennial- to centennial-scale Atlantic ITCZ swings during the penultimate deglaciation |

