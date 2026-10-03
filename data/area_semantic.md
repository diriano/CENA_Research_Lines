# Redes semânticas por área de concentração

Período: 2021-01-01 a 2026-12-31. Modelo: `BAAI/bge-large-en-v1.5`; dispositivo: `cpu`.
Limite de 512 tokens por segmento, incluindo tokens especiais.
Classificação provisória: comparação dos vetores de título, abstract e keywords com protótipos de artigos de orientadores vinculados a uma única área. Os protótipos dão o mesmo peso a cada orientador de referência.
O vínculo exclusivo de um orientador foi usado como referência inicial, não como validação de que todos os seus artigos pertencem àquela área.
Área atribuída se cosseno ≥ 0.2 e até 0.05 abaixo da área mais próxima. Múltiplas áreas são permitidas; 16 artigos têm correção manual em `work_area_curated.csv`.
Os valores são similaridades de cosseno, não probabilidades calibradas. Verifique os artigos e a interpretação institucional das áreas antes de usar a classificação para decisões do programa.
Artigos sem área atribuída: 0; atribuídos a mais de uma área: 955. Use `review_flags` e `score_gap` para priorizar a conferência manual.
Em `work_area_curated.csv`, `supervisors` lista os orientadores do artigo; edite `areas` para corrigir (vazio exclui). Alterações manuais são preservadas; linhas automáticas são atualizadas a cada execução.
Os artigos compartilhados entre dois orientadores são excluídos apenas da comparação daquele par.

| Área | Orientadores de referência | Artigos de referência | Artigos atribuídos |
| --- | ---: | ---: | ---: |
| B | 6 | 266 | 967 |
| N | 4 | 145 | 957 |
| Q | 6 | 216 | 837 |

Um artigo pode contar em mais de uma área. Para cada área, o perfil de um orientador usa apenas os seus artigos atribuídos àquela área.

## B — Biologia na Agricultura e no Ambiente

17 orientadores vinculados; 17 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Adibe Luiz Abdalla | 79 | sim |
| Antonio Vargas de Oliveira Figueira | 27 | sim |
| Cassio Hamilton Abreu Junior | 35 | sim |
| Diego Mauricio Riaño Pachón | 28 | sim |
| Elisabete Aparecida De Nadai Fernandes | 12 | sim |
| Ernani Pinto Junior | 51 | sim |
| Flavia Vischi Winck | 17 | sim |
| Francisco Scaglia Linhares | 13 | sim |
| Helder Louvandini | 57 | sim |
| Hudson Wallace Pereira de Carvalho | 75 | sim |
| José Lavres Junior | 91 | sim |
| Kassio Ferreira Mendes | 72 | sim |
| Lucas William Mendes | 155 | sim |
| Luiz Carlos Ruiz Pessenda | 34 | sim |
| Marisa de Cassia Piccolo | 36 | sim |
| Marli de Fatima Fiore | 32 | sim |
| Tsai Siu Mui | 73 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| B1 | Cassio Hamilton Abreu Junior; Elisabete Aparecida De Nadai Fernandes; Francisco Scaglia Linhares; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes | soil; zinc; soybean; potassium; herbicide; uptake; leaf; application | A study on nickel application methods for optimizing soybean growth; Common Bean Productivity and Micronutrients in the Soil–Plant System under Residual Applications of Composted Sewage Sludge; Residual effects of composted sewage sludge on nitrogen cycling and plant metabolism in a no-till common bean-palisade grass-soybean rotation |
| B2 | Antonio Vargas de Oliveira Figueira; Diego Mauricio Riaño Pachón; Ernani Pinto Junior; Flavia Vischi Winck; Marli de Fatima Fiore | cyanobacteria; cyanobacterial; gene; genome; blooms; genes; amino; expression | The experience of teaching introductory programming skills to bioscientists in Brazil; The experience of teaching introductory programming skills to bioscientists in Brazil; Genomic and secondary metabolites of the marine cyanobacterium Capilliphycus salinus ALCB114379 |
| B3 | Lucas William Mendes; Luiz Carlos Ruiz Pessenda; Marisa de Cassia Piccolo; Tsai Siu Mui | soil; microbial; communities; carbon; forest; mangrove; bacterial; change | Long-term land use in Amazon influence the dynamic of microbial communities in soil and rhizosphere; Methanogenic communities and methane emissions from enrichments of Brazilian Amazonia soils under land-use change; From deforestation to regeneration: How do land-use changes shape soil microbes and methane-cycling genes in the Eastern Amazon? |
| B4 | Adibe Luiz Abdalla; Helder Louvandini | sheep; methane; feed; lambs; rumen; gas; ines; santa ines | Ruderal Tithonia diversifolia inclusion in sheep diets: impacts on digestibility and greenhouse gas emissions; Tithonia diversifolia Improves In Vitro Rumen Microbial Synthesis of Sheep Diets without Changes in Total Gas and Methane Production; Hematological, biochemical alterations and methane production in sheep submitted to mixed infection of Haemonchus contortus and Trichostrongylus colubriformis |

### Proposta de até 3 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| B1 | Adibe Luiz Abdalla; Cassio Hamilton Abreu Junior; Elisabete Aparecida De Nadai Fernandes; Francisco Scaglia Linhares; Helder Louvandini; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Lucas William Mendes; Marisa de Cassia Piccolo; Tsai Siu Mui | soil; nutrient; soybean; soils; nitrogen; zinc; sheep; microbial | Taxonomy and Functional Diversity in the Fecal Microbiome of Beef Cattle Reared in Brazilian Traditional and Semi-Intensive Production Systems; Taxonomic and functional diversity in the fecal microbiome of beef cattle reared in Brazilian traditional and semi-intensive production systems; Impact of nitrogen fertilizer sustainability on corn crop yield: the role of beneficial microbial inoculation interactions |
| B2 | Antonio Vargas de Oliveira Figueira; Diego Mauricio Riaño Pachón; Ernani Pinto Junior; Flavia Vischi Winck; Marli de Fatima Fiore | cyanobacteria; cyanobacterial; gene; genome; blooms; genes; amino; expression | The experience of teaching introductory programming skills to bioscientists in Brazil; The experience of teaching introductory programming skills to bioscientists in Brazil; Genomic and secondary metabolites of the marine cyanobacterium Capilliphycus salinus ALCB114379 |
| B3 | Luiz Carlos Ruiz Pessenda | mangrove; holocene; mangroves; sea-level; relative sea-level; vegetation; coastal; paleoclimate | Effects of the middle Holocene high sea‐level stand and climate on Amazonian mangroves; Assessment the Impacts of Sea-Level Changes on Mangroves of Ceará-Mirim Estuary, Northeastern Brazil, during the Holocene and Anthropocene; Impacts of sea-level changes on mangroves from southeastern Brazil during the Holocene and Anthropocene using a multi-proxy approach |

## N — Energia Nuclear na Agricultura e no Ambiente

14 orientadores vinculados; 14 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Adibe Luiz Abdalla | 81 | sim |
| Cassio Hamilton Abreu Junior | 34 | sim |
| Elisabete Aparecida De Nadai Fernandes | 19 | sim |
| Helder Louvandini | 61 | sim |
| Hudson Wallace Pereira de Carvalho | 77 | sim |
| José Lavres Junior | 84 | sim |
| Kassio Ferreira Mendes | 75 | sim |
| Luiz Carlos Ruiz Pessenda | 36 | sim |
| Marli de Fatima Fiore | 20 | sim |
| Tsai Siu Mui | 67 | sim |
| Luiz Antonio Martinelli | 48 | sim |
| Quirijn de Jong van Lier | 46 | sim |
| Thiago de Araújo Mastrangelo | 14 | sim |
| Valter Arthur | 42 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| N1 | Adibe Luiz Abdalla; Elisabete Aparecida De Nadai Fernandes; Helder Louvandini; Thiago de Araújo Mastrangelo; Valter Arthur | sheep; irradiation; gamma; lambs; feed; gastrointestinal; production; radiation | Taxonomy and Functional Diversity in the Fecal Microbiome of Beef Cattle Reared in Brazilian Traditional and Semi-Intensive Production Systems; Taxonomic and functional diversity in the fecal microbiome of beef cattle reared in Brazilian traditional and semi-intensive production systems; Tithonia diversifolia Improves In Vitro Rumen Microbial Synthesis of Sheep Diets without Changes in Total Gas and Methane Production |
| N2 | Luiz Carlos Ruiz Pessenda; Marli de Fatima Fiore; Tsai Siu Mui; Luiz Antonio Martinelli; Quirijn de Jong van Lier | soil; water; forest; cyanobacteria; isotopes; lakes; cyanobacterial; carbon | Methanogenic communities and methane emissions from enrichments of Brazilian Amazonia soils under land-use change; The role of microbial communities in biogeochemical cycles and greenhouse gas emissions within tropical soda lakes; From deforestation to regeneration: How do land-use changes shape soil microbes and methane-cycling genes in the Eastern Amazon? |
| N3 | Cassio Hamilton Abreu Junior; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes | soil; herbicide; application; fertilization; plant; uptake; nutrient; soybean | Residual effects of composted sewage sludge on nitrogen cycling and plant metabolism in a no-till common bean-palisade grass-soybean rotation; Common Bean Productivity and Micronutrients in the Soil–Plant System under Residual Applications of Composted Sewage Sludge; Treating Tropical Soils with Composted Sewage Sludge Reduces the Mineral Fertilizer Requirements in Sugarcane Production |

### Proposta de até 3 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| N1 | Adibe Luiz Abdalla; Cassio Hamilton Abreu Junior; Elisabete Aparecida De Nadai Fernandes; Helder Louvandini; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Tsai Siu Mui; Luiz Antonio Martinelli; Quirijn de Jong van Lier; Thiago de Araújo Mastrangelo; Valter Arthur | soil; production; quality; use; plant; control; sheep; nitrogen | Circular bioeconomy in livestock production: harnessing crop by-products in MERCOSUR/MERCOSUL; Taxonomy and Functional Diversity in the Fecal Microbiome of Beef Cattle Reared in Brazilian Traditional and Semi-Intensive Production Systems; Residual effects of composted sewage sludge on nitrogen cycling and plant metabolism in a no-till common bean-palisade grass-soybean rotation |
| N2 | Luiz Carlos Ruiz Pessenda | mangrove; holocene; sea-level; mangroves; relative sea-level; coastal; vegetation; paleoclimate | Effects of the middle Holocene high sea‐level stand and climate on Amazonian mangroves; Assessment the Impacts of Sea-Level Changes on Mangroves of Ceará-Mirim Estuary, Northeastern Brazil, during the Holocene and Anthropocene; Impacts of sea-level changes on mangroves from southeastern Brazil during the Holocene and Anthropocene using a multi-proxy approach |
| N3 | Marli de Fatima Fiore | cyanobacteria; cyanobacterial; lakes; soda; soda lakes; blooms; pantanal; cyanobacterial blooms | Phosphonate consumers potentially contributing to methane production in Brazilian soda lakes; Disentangling the lifestyle of bacterial communities in tropical soda lakes; Phylogenomic analysis of Anabaenopsis elenkinii (Nostocales, Cyanobacteria) |

## Q — Química na Agricultura e no Ambiente

16 orientadores vinculados; 16 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Adibe Luiz Abdalla | 78 | sim |
| Cassio Hamilton Abreu Junior | 33 | sim |
| Elisabete Aparecida De Nadai Fernandes | 20 | sim |
| Ernani Pinto Junior | 55 | sim |
| Hudson Wallace Pereira de Carvalho | 78 | sim |
| José Lavres Junior | 63 | sim |
| Kassio Ferreira Mendes | 70 | sim |
| Luiz Carlos Ruiz Pessenda | 23 | sim |
| Marli de Fatima Fiore | 22 | sim |
| Tsai Siu Mui | 35 | sim |
| Alex Virgilio | 13 | sim |
| Celia Regina Montes | 19 | sim |
| Fabio Rodrigo Piovezani Rocha | 45 | sim |
| Marcos Yassuo Kamogawa | 5 | sim |
| Severino Matias de Alencar | 102 | sim |
| Wanessa Melchert Mattos | 35 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| Q1 | Adibe Luiz Abdalla; Cassio Hamilton Abreu Junior; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Luiz Carlos Ruiz Pessenda; Marli de Fatima Fiore; Tsai Siu Mui; Celia Regina Montes; Marcos Yassuo Kamogawa | soil; soils; carbon; nitrogen; tropical; lakes; pantanal; microbial | Soil C and N fractions across soil depths in an ecological intensification system of maize-soybean rotation in Southern Brazil; Treating Tropical Soils with Composted Sewage Sludge Reduces the Mineral Fertilizer Requirements in Sugarcane Production; Residual effects of composted sewage sludge on nitrogen cycling and plant metabolism in a no-till common bean-palisade grass-soybean rotation |
| Q2 | Elisabete Aparecida De Nadai Fernandes; Ernani Pinto Junior; Alex Virgilio; Fabio Rodrigo Piovezani Rocha; Severino Matias de Alencar; Wanessa Melchert Mattos | green; analytical; food; compounds; determination; chemistry; digestion; sample | Sample preparation and spectrometric methods for elemental analysis of milk and dairy products – A review; Microwave-assisted extraction of total phenolic compounds from coffee; Closed-Vessel Conductively Heated Digestion of Dry Dog Food for Spectrometric Determination of Essential Nutrients |

### Proposta de até 3 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| Q1 | Adibe Luiz Abdalla; Cassio Hamilton Abreu Junior; Elisabete Aparecida De Nadai Fernandes; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Alex Virgilio; Fabio Rodrigo Piovezani Rocha; Marcos Yassuo Kamogawa; Severino Matias de Alencar; Wanessa Melchert Mattos | trace; green; determination; analytical; food; zinc; sample; digestion | A convective heated digestion system with closed vessels: a new digestor for elemental inorganic analysis; Closed-Vessel Conductively Heated Digestion of Dry Dog Food for Spectrometric Determination of Essential Nutrients; Common Bean Productivity and Micronutrients in the Soil–Plant System under Residual Applications of Composted Sewage Sludge |
| Q2 | Luiz Carlos Ruiz Pessenda; Tsai Siu Mui; Celia Regina Montes | soil; carbon; pantanal; climate; mangrove; holocene; amazonian; lakes | Climatic variations, vegetation and soils during the Holocene in the Pantanal of Mato Grosso do Sul, Brazil; Holocene limnological changes in saline and freshwater lakes, Lower Nhecolândia, Pantanal, Brazil; Molecular evidence for stimulation of methane oxidation in Amazonian floodplains by ammonia-oxidizing communities |
| Q3 | Ernani Pinto Junior; Marli de Fatima Fiore | cyanobacterial; cyanobacteria; blooms; cyanobacterial blooms; metabolites; cyanotoxins; lakes; microcystins | Biosynthesis of Guanitoxin Enables Global Environmental Detection in Freshwater Cyanobacteria; Effects of different cultivation conditions on the production of β-cyclocitral and β-ionone in Microcystis aeruginosa; Genomic and secondary metabolites of the marine cyanobacterium Capilliphycus salinus ALCB114379 |

