# Redes semânticas por área de concentração

Período: 2021-01-01 a 2026-12-31. Modelo: `sentence-transformers/all-mpnet-base-v2`; dispositivo: `cpu`.
Classificação provisória: comparação dos vetores de título, abstract e keywords com protótipos de artigos de orientadores vinculados a uma única área. Os protótipos dão o mesmo peso a cada orientador de referência.
O vínculo exclusivo de um orientador foi usado como referência inicial, não como validação de que todos os seus artigos pertencem àquela área.
Área atribuída se cosseno ≥ 0.2 e até 0.05 abaixo da área mais próxima. Múltiplas áreas são permitidas; 16 artigos têm correção manual em `work_area_curated.csv`.
Os valores são similaridades de cosseno, não probabilidades calibradas. Verifique os artigos e a interpretação institucional das áreas antes de usar a classificação para decisões do programa.
Artigos sem área atribuída: 11; atribuídos a mais de uma área: 316. Use `review_flags` e `score_gap` para priorizar a conferência manual.
Em `work_area_curated.csv`, `supervisors` lista os orientadores do artigo; edite `areas` para corrigir (vazio exclui). Alterações manuais são preservadas; linhas automáticas são atualizadas a cada execução.
Os artigos compartilhados entre dois orientadores são excluídos apenas da comparação daquele par.

| Área | Orientadores de referência | Artigos de referência | Artigos atribuídos |
| --- | ---: | ---: | ---: |
| B | 6 | 265 | 577 |
| N | 4 | 145 | 472 |
| Q | 6 | 216 | 451 |

Um artigo pode contar em mais de uma área. Para cada área, o perfil de um orientador usa apenas os seus artigos atribuídos àquela área.

## B — Biologia na Agricultura e no Ambiente

17 orientadores vinculados; 17 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Adibe Luiz Abdalla | 36 | sim |
| Antonio Vargas de Oliveira Figueira | 25 | sim |
| Cassio Hamilton Abreu Junior | 28 | sim |
| Diego Mauricio Riaño Pachón | 26 | sim |
| Elisabete Aparecida De Nadai Fernandes | 5 | sim |
| Ernani Pinto Junior | 23 | sim |
| Flavia Vischi Winck | 16 | sim |
| Francisco Scaglia Linhares | 13 | sim |
| Helder Louvandini | 29 | sim |
| Hudson Wallace Pereira de Carvalho | 47 | sim |
| José Lavres Junior | 82 | sim |
| Kassio Ferreira Mendes | 25 | sim |
| Lucas William Mendes | 148 | sim |
| Luiz Carlos Ruiz Pessenda | 12 | sim |
| Marisa de Cassia Piccolo | 28 | sim |
| Marli de Fatima Fiore | 29 | sim |
| Tsai Siu Mui | 65 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| B1 | Adibe Luiz Abdalla; Cassio Hamilton Abreu Junior; Francisco Scaglia Linhares; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Marisa de Cassia Piccolo | soil; nutrient; efficiency; soybean; fertilization; leaf; application; uptake | A study on nickel application methods for optimizing soybean growth; Residual effects of composted sewage sludge on nitrogen cycling and plant metabolism in a no-till common bean-palisade grass-soybean rotation; Nepheline Syenite and Phonolite as Alternative Potassium Sources for Maize |
| B2 | Antonio Vargas de Oliveira Figueira; Diego Mauricio Riaño Pachón; Ernani Pinto Junior; Flavia Vischi Winck; Marli de Fatima Fiore | cyanobacteria; cyanobacterial; gene; genome; genes; amino; acids; amino acids | Genomic and secondary metabolites of the marine cyanobacterium Capilliphycus salinus ALCB114379; The experience of teaching introductory programming skills to bioscientists in Brazil; The experience of teaching introductory programming skills to bioscientists in Brazil |
| B3 | Elisabete Aparecida De Nadai Fernandes; Helder Louvandini; Lucas William Mendes; Luiz Carlos Ruiz Pessenda; Tsai Siu Mui | microbial; microbiome; communities; soil; community; bacteria; trichostrongylus; bacterial | Taxonomic and functional diversity in the fecal microbiome of beef cattle reared in Brazilian traditional and semi-intensive production systems; Taxonomy and Functional Diversity in the Fecal Microbiome of Beef Cattle Reared in Brazilian Traditional and Semi-Intensive Production Systems; Computed tomography and radioactive 32P detected phosphorus impairment in metabolism, reduced bones density and animal performance caused by mixed infection of Haemonchus contortus and Trichostrongylus colubriformis in sheep |

### Proposta de até 3 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| B1 | Adibe Luiz Abdalla; Antonio Vargas de Oliveira Figueira; Cassio Hamilton Abreu Junior; Diego Mauricio Riaño Pachón; Ernani Pinto Junior; Flavia Vischi Winck; Francisco Scaglia Linhares; Helder Louvandini; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Lucas William Mendes; Marisa de Cassia Piccolo; Marli de Fatima Fiore; Tsai Siu Mui | soil; plant; efficiency; nutrient; sugarcane; biomass; water; cyanobacteria | Impact of nitrogen fertilizer sustainability on corn crop yield: the role of beneficial microbial inoculation interactions; Unveiling the aluminum tolerance by Tithonia diversifolia grown in acid soil: Insights from morphological, anatomical, and nutritional analysis; Residual effects of composted sewage sludge on nitrogen cycling and plant metabolism in a no-till common bean-palisade grass-soybean rotation |
| B2 | Elisabete Aparecida De Nadai Fernandes | beef; beef cattle; trichostrongylus colubriformis; colubriformis; fecal microbiome; fecal; colubriformis gastrointestinal; trichostrongylus | Taxonomy and Functional Diversity in the Fecal Microbiome of Beef Cattle Reared in Brazilian Traditional and Semi-Intensive Production Systems; Taxonomic and functional diversity in the fecal microbiome of beef cattle reared in Brazilian traditional and semi-intensive production systems; Computed tomography and radioactive 32P detected phosphorus impairment in metabolism, reduced bones density and animal performance caused by mixed infection of Haemonchus contortus and Trichostrongylus colubriformis in sheep |
| B3 | Luiz Carlos Ruiz Pessenda | mangrove; avicennia; holocene; mangroves; gulf; hurricanes; climate; flats | Poleward mangrove expansion in South America coincides with MCA and CWP: A diatom, pollen, and organic geochemistry study; Late Holocene mangrove dynamics of the Doce River delta, southeastern Brazil: Implications for the understanding of mangrove resilience to sea-level changes and channel dynamics; Effects of the middle Holocene high sea‐level stand and climate on Amazonian mangroves |

## N — Energia Nuclear na Agricultura e no Ambiente

14 orientadores vinculados; 14 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Adibe Luiz Abdalla | 46 | sim |
| Cassio Hamilton Abreu Junior | 31 | sim |
| Elisabete Aparecida De Nadai Fernandes | 4 | sim |
| Helder Louvandini | 32 | sim |
| Hudson Wallace Pereira de Carvalho | 42 | sim |
| José Lavres Junior | 34 | sim |
| Kassio Ferreira Mendes | 59 | sim |
| Luiz Carlos Ruiz Pessenda | 35 | sim |
| Marli de Fatima Fiore | 2 | sim |
| Tsai Siu Mui | 19 | sim |
| Luiz Antonio Martinelli | 42 | sim |
| Quirijn de Jong van Lier | 45 | sim |
| Thiago de Araújo Mastrangelo | 14 | sim |
| Valter Arthur | 32 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| N1 | Cassio Hamilton Abreu Junior; Luiz Carlos Ruiz Pessenda; Marli de Fatima Fiore; Tsai Siu Mui; Luiz Antonio Martinelli; Quirijn de Jong van Lier | soil; water; forest; soil water; isotopes; lakes; mangrove; carbon | Molecular, morphological and ecological studies of Limnospira platensis (Cyanobacteria), from saline and alkaline lakes, Pantanal Biome, Brazil; Impacts of Forest-to-Pasture Conversion on Soil Water Retention in the Amazon Biome; Bioaccumulation and speciation of arsenic in plankton from tropical soda lakes along a salinity gradient |
| N2 | Elisabete Aparecida De Nadai Fernandes; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Thiago de Araújo Mastrangelo; Valter Arthur | x-ray; soybean; control; herbicide; fluorescence; radiation; irradiation; seeds | Hormetic effects of low-dose gamma rays in soybean seeds and seedlings: A detection technique using optical sensors; Foliar Application and Translocation of Radiolabeled Zinc Oxide Suspension vs. Zinc Sulfate Solution by Soybean Plants; Estimating plant-available nutrients with XRF sensors: Towards a versatile analysis tool for soil condition assessment |
| N3 | Adibe Luiz Abdalla; Helder Louvandini | sheep; lambs; animal; methane; trichostrongylus; emissions; feed; gas | Assessing the impact of Samanea tubulosa trees on methane emissions and its potential as a feed supplement for ruminants in silvopastoral systems; Hematological, biochemical alterations and methane production in sheep submitted to mixed infection of Haemonchus contortus and Trichostrongylus colubriformis; Trichostrongylus colubriformis infection in Santa Inês lambs: impact on feed digestibility, blood markers, and nitrogen balance |

### Proposta de até 3 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| N1 | Cassio Hamilton Abreu Junior; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Luiz Carlos Ruiz Pessenda; Tsai Siu Mui; Luiz Antonio Martinelli; Quirijn de Jong van Lier | soil; water; soils; soil water; forest; crop; herbicide; nutrient | Composted Sewage Sludge Sustains High Maize Productivity on an Infertile Oxisol in the Brazilian Cerrado; Nutritional status of Eucalyptus plantation and chemical attributes of a Ferralsol amended with lime and copper plus zinc; Treating Tropical Soils with Composted Sewage Sludge Reduces the Mineral Fertilizer Requirements in Sugarcane Production |
| N2 | Adibe Luiz Abdalla; Elisabete Aparecida De Nadai Fernandes; Helder Louvandini; Thiago de Araújo Mastrangelo; Valter Arthur | sheep; lambs; trichostrongylus; colubriformis; trichostrongylus colubriformis; animal; infection; radiation | Computed tomography and radioactive 32P detected phosphorus impairment in metabolism, reduced bones density and animal performance caused by mixed infection of Haemonchus contortus and Trichostrongylus colubriformis in sheep; Trichostrongylus colubriformis infection damages intestine brush board cells and could negatively impact postabsorptive parameters of Santa Ines lambs; Hematological, biochemical alterations and methane production in sheep submitted to mixed infection of Haemonchus contortus and Trichostrongylus colubriformis |
| N3 | Marli de Fatima Fiore | lakes; cyanobacteria; lakes pantanal; pantanal; arsenic; platensis; limnospira; salinity gradient | Bioaccumulation and speciation of arsenic in plankton from tropical soda lakes along a salinity gradient; Molecular, morphological and ecological studies of Limnospira platensis (Cyanobacteria), from saline and alkaline lakes, Pantanal Biome, Brazil |

## Q — Química na Agricultura e no Ambiente

16 orientadores vinculados; 16 com pelo menos 1 artigo(s) classificado(s).

| Orientador | Artigos da área | Na rede |
| --- | ---: | --- |
| Adibe Luiz Abdalla | 52 | sim |
| Cassio Hamilton Abreu Junior | 8 | sim |
| Elisabete Aparecida De Nadai Fernandes | 17 | sim |
| Ernani Pinto Junior | 47 | sim |
| Hudson Wallace Pereira de Carvalho | 40 | sim |
| José Lavres Junior | 15 | sim |
| Kassio Ferreira Mendes | 29 | sim |
| Luiz Carlos Ruiz Pessenda | 3 | sim |
| Marli de Fatima Fiore | 9 | sim |
| Tsai Siu Mui | 4 | sim |
| Alex Virgilio | 12 | sim |
| Celia Regina Montes | 9 | sim |
| Fabio Rodrigo Piovezani Rocha | 44 | sim |
| Marcos Yassuo Kamogawa | 4 | sim |
| Severino Matias de Alencar | 97 | sim |
| Wanessa Melchert Mattos | 35 | sim |

### Comunidades Louvain

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| Q1 | Adibe Luiz Abdalla; Elisabete Aparecida De Nadai Fernandes; Alex Virgilio; Fabio Rodrigo Piovezani Rocha; Severino Matias de Alencar; Wanessa Melchert Mattos | green; food; analytical; chemistry; determination; trace; digestion; sample | Sample preparation and spectrometric methods for elemental analysis of milk and dairy products – A review; Evaluation of Closed-Vessel Conductively-Heated Digestion System with Diluted Acid for Analysis of Animal Feed by ICP-MS; Closed-Vessel Conductively Heated Digestion of Dry Dog Food for Spectrometric Determination of Essential Nutrients |
| Q2 | Cassio Hamilton Abreu Junior; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Marcos Yassuo Kamogawa | soil; fertilizer; herbicide; fertilizers; phosphate; zinc; urea; potassium | RELEASE OF POTASSIUM FERTILIZER COATED WITH POLYMER; Nepheline Syenite and Phonolite as Alternative Potassium Sources for Maize; Development and characterization of enhanced urea through micronutrients and established technology addition |
| Q3 | Luiz Carlos Ruiz Pessenda; Tsai Siu Mui; Celia Regina Montes | geology; lakes; pantanal; geology geology; jst; jst 京大機械翻訳; 京大機械翻訳; 化学的およひ微生物学的属性に及ほす燃焼およひ非燃焼サトウキヒ収穫システムの影響 | Determinação de mercúrio total em águas por espectrometria de absorção atômica sem chama baseada em fluxo; Flow-based determination of total mercury in waters by flameless atomic absorption spectrometry; Phosphonate consumers potentially contributing to methane production in Brazilian soda lakes |
| Q4 | Ernani Pinto Junior; Marli de Fatima Fiore | cyanobacterial; cyanobacteria; blooms; microcystis; aeruginosa; microcystis aeruginosa; cyanobacterial blooms; cyanotoxins | Effects of different cultivation conditions on the production of β-cyclocitral and β-ionone in Microcystis aeruginosa; Biosynthesis of Guanitoxin Enables Global Environmental Detection in Freshwater Cyanobacteria; Microcystins can be extracted from Microcystis aeruginosa using amino acid-derived biosurfactants |

### Proposta de até 3 temas

| ID | Orientadores | Termos distintivos | Artigos representativos |
| --- | --- | --- | --- |
| Q1 | Adibe Luiz Abdalla; Cassio Hamilton Abreu Junior; Elisabete Aparecida De Nadai Fernandes; Hudson Wallace Pereira de Carvalho; José Lavres Junior; Kassio Ferreira Mendes; Alex Virgilio; Fabio Rodrigo Piovezani Rocha; Marcos Yassuo Kamogawa; Severino Matias de Alencar; Wanessa Melchert Mattos | chemistry; soil; analytical; trace; zinc; food; green; sample | A convective heated digestion system with closed vessels: a new digestor for elemental inorganic analysis; Closed-Vessel Conductively Heated Digestion of Dry Dog Food for Spectrometric Determination of Essential Nutrients; Nepheline Syenite and Phonolite as Alternative Potassium Sources for Maize |
| Q2 | Luiz Carlos Ruiz Pessenda; Tsai Siu Mui; Celia Regina Montes | geology; lakes; pantanal; geology geology; jst; jst 京大機械翻訳; 京大機械翻訳; 化学的およひ微生物学的属性に及ほす燃焼およひ非燃焼サトウキヒ収穫システムの影響 | Determinação de mercúrio total em águas por espectrometria de absorção atômica sem chama baseada em fluxo; Flow-based determination of total mercury in waters by flameless atomic absorption spectrometry; Phosphonate consumers potentially contributing to methane production in Brazilian soda lakes |
| Q3 | Ernani Pinto Junior; Marli de Fatima Fiore | cyanobacterial; cyanobacteria; blooms; microcystis; aeruginosa; microcystis aeruginosa; cyanobacterial blooms; cyanotoxins | Effects of different cultivation conditions on the production of β-cyclocitral and β-ionone in Microcystis aeruginosa; Biosynthesis of Guanitoxin Enables Global Environmental Detection in Freshwater Cyanobacteria; Microcystins can be extracted from Microcystis aeruginosa using amino acid-derived biosurfactants |

