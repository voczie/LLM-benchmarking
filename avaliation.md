## OpenAI GPT-4o Mini - Avaliation


### 1 - How many genes and transcripts are there on chromosome 3?
#### No prompt
Pros:
Indica possíveis nomes para identificar genes e transcritos dentro dos arquivos GFF/GTF
Ofereceu SQL extra usando UNION que funciona, mas precisa corrigir o valor de seqid
Passa um script python FUNCIONAL para executar o SQL

Cons:
Necessário corrigir o valor de seqid de "chr3" para "3"
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada


### 2 - How many protein-coding genes are on chromosome 12?
#### No prompt
Pros:
Indica que protein-coding genes normalmente são rotulados como genes nesses arquivos
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL

Cons:
Necessário corrigir o valor de seqid de "chr12" para "12"
O modelo não processou a probabilidade da informação sobre ser protein-coding estar presente na coluna de atributos. Logo a resposta está errada.
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils
Entende que a informação sobre ser protein-coding está dentro de gene_biotype nos atributos

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada


### 3 - How many lncRNA genes are on chromosome 7?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Passa um script python FUNCIONAL para executar o SQL

Cons:
Necessário corrigir o valor de seqid de "chr7" para "7"
Necessário corrigir que a informação que o gene é lncRNA não se encontra na coluna "featuretype" e sim dentro da coluna "attributes", logo a resposta está errada.
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils
Entende que a informação sobre ser lncRNA está dentro de gene_biotype nos atributos

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada


### 4 - How many pseudogenes are on the X chromosome?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Passa um script python FUNCIONAL para executar o SQL

Cons:
Necessário corrigir que a informação que o gene é um subtipo pseudogene não se encontra na coluna "featuretype" e sim dentro da coluna "attributes", logo a resposta está errada.
Necessário corrigir o SQL, pois deve conter a clausula para verificar se o featuretype é "gene", pois só assim teremos a contagem correta.
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils
Não deu erro ao rodar o script de primeira, mas ele não retorna resposta satisfatória (retornou 0)

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada


### 5 - How many genes for miRNA exist in chromosome 10?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL

Cons:
Necessário corrigir que a informação que o gene é um miRNA não se encontra na coluna "featuretype" e sim dentro da coluna "attributes", logo a resposta está errada.
Necessário corrigir o SQL, pois deve conter a clausula para verificar se o featuretype é "gene", pois só assim teremos a contagem correta.
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils
Entende que a informação sobre ser miRNA está dentro de gene_biotype nos atributos

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada


### 6 - Calculate the sizes of each gene locus separately: XIST, MALAT1, BRCA1, COL1A2, NFKB1, NFKB2, REL, RELA and RELB
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal
Sabe que o cálculo do locus gênico é end - start + 1

Cons:
Necessário corrigir como estão escritos os valores a serem buscados na coluna de atributos. Não é possível buscar de forma precisa na primeira execução, logo a resposta está errada.
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils
Entende que a informação sobre ser XIST, MALAT1, BRCA1, COL1A2, NFKB1, NFKB2, REL, RELA ou RELB está dentro de gene_name nos atributos
Sabe calcular o tamanho do locus gênico

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada


### 7 - How many transcript isoforms does the XIST gene have? Print the transcript isoform names (transcript_name) and the sizes of each.
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Dá três códigos SQL. Os dois primeiros formam o terceiro e último código. Dessa forma, o usuário pode aprender como formar códigos SQL únicos e mais complexos.
O código final retornado é quase perfeito para resposta. Ele peca somente no cálculo do tamanho, pois esquece de somar +1 ao (end - start)

Cons:
Errou o cálculo do tamanho dos transcritos
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils
Entende que a informação sobre XIST ser um gene_name de um gene e que estaríamos querendo o tamanho dos transcritos desse gene

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils
Alucina sobre precisar calcular o tamanho dos exons dentro dos transcritos, então faz mais trabalho do que é necessário

### 8 - How many exons does the XIST gene have?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal

Cons:
Processou errado, achando que XIST era o nome do cromossomo, pois procurou pelo valor na coluna "seqid", logo o resto da resposta está todo errado.
A clausula para procurar pelo id do gene XIST na coluna de atributos está errada, teria que ser corrigido isso também.
#### With prompt
Pros:
Tenta utilizar a biblioteca gffutils

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils
Não entende a informação que XIST é um gene_name, pois gerou um código para buscar por "gene_id", que existe, mas possui outra informação


### 9 - How many exons does each transcript isoform of the BRCA1 gene have? Print the transcript isoform names (transcript_name) and the number of exons. 
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal
As queries geradas funcionam para o propósito final e ele retorna a reposta correta

Cons:
É necessário o input do usuário dos IDs dos genes retornados pela primeira query gerada, e, por mais que o modelo guie o usuário a fazer isso, não é um ponto positivo.
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Entende que a informação sobre BRCA1 ser um gene_name de um gene e que estaríamos querendo a quantidade de exons para cada transcrito desse gene

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils


### 10 - What is the average exon size of the BRCA1 transcript isoforms?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal
O código SQL gerado pelo modelo funciona e está correto. Se compararmos com o gabarito, ele erra somente na casa dos décimos (Modelo: 251.56/Gabarito: 251.83)

Cons:
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils
Não entende a informação sobre BRCA1 ser um gene_name, interpretando como se fosse um "gene_id"

### 11 - What is the chromosomal position of the BRCA1 gene?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Passa um script python FUNCIONAL para executar o SQL
O código SQL gerado retorna uma resposta satisfatória, por mais que consideravelmente excedente (existem dois genes recuperáveis a partir da clausula "attributes LIKE '%BRCA1%'", o correto seria "attributes LIKE '%BRCA1"%'")

Cons:
Retorna um gene a mais, o BRCA1P1, se não for corrigido
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Talvez funcionasse, se ele conseguisse fazer a função feature_of_type funcionar a favor dele.

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils
Não entende a informação sobre BRCA1 ser um gene_name, interpretando como se fosse um "gene_id"


### 12 - On which chromosomes are the genes NFKB1, NFKB2, REL, RELA and RELB located?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal
Os códigos SQL gerados funcionam, porém é necessário colocar, nos valores dos atributos, aspas antes do segundo símbolo de porcentagem (e para REL, é necessário colocar depois do primeiro símbolo de porcentagem)

Cons:
É necessário fazer pequenas alterações nesses valores dos atributos
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Entende que a informação sobre NFKB1, NFKB2, REL, RELA e RELB serem gene_name de um gene e que estaríamos querendo o valor de seqid

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils


### 13 - Print the names of the 2 genes located immediately before and after the gene COL1A2, respectively
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal
Os códigos SQL gerados respondem corretamente a pergunta

Cons:
Não gerou um grande SQL final para juntar os dois SQLs que respondem a pergunta
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils
Não entende a informação sobre COL1A2 ser um gene_name, interpretando como se fosse um "gene_id"


### 14 - What is the biotype of the following genes XIST, MALAT1, BRCA1,NFKB1, NFKB2, REL, RELA, RELB and COL1A2?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Passa um script python FUNCIONAL para executar o SQL

Cons:
A lógica do script não é boa suficiente para extrair, da coluna de atributos, o biotipo dos genes, por isso o modelo não foi capaz de responder a pergunta corretamente
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Entende que a informação de ser XIST, MALAT1, BRCA1,NFKB1, NFKB2, REL, RELA, RELB e COL1A2 está em gene_name na coluna de atributos e que queremos o valor em gene_biotype, também na coluna de atributos

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils


### 15 - What strand are the HOTAIR, HOXC11, and HOXC12 genes located on?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Passa um script python FUNCIONAL para executar o SQL
O código SQL gerado funciona, porém é necessário colocar, no valor do atributo "HOTAIR", aspas antes do segundo símbolo de porcentagem, para evitar pegar o gene "HOTAIRM1"

Cons:
É necessário fazer pequenas alterações nesses valores dos atributos
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Entende que a informação de ser XIST, MALAT1, BRCA1, NFKB1, NFKB2, REL, RELA, RELB e COL1A2 está em gene_name na coluna de atributos e que queremos o valor em gene_biotype, também na coluna de atributos

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils



### 16 - Which genes are located between the HOXC11 and HOXC12 genes on + and - strands?
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Se o usuário seguir o passo a passo e for bem informado em computação, ele consegue responder parcialmente

Cons:
É necessária muita intervenção do usuário, correções e a resposta ainda está incompleta/errada
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils
Não entende que a informação de ser HOXC11 and HOXC12 está em gene_name, crê que está em "gene_id" na coluna de atributos


### 17 - Get the following informations about each transcript isoforms of the XIST, MALAT1, BRCA1, NFKB1, COL1A2, HOTAIR, HOXC11, and HOXC12 genes: chromosomal location and position, size, number of exons, average exon size, strand, and biotype. Organize all the information in a table and save it.
#### No prompt
Pros:
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL

Cons:
Gerou um SQL enorme que não funciona, errou completamente
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Entende que a informação de ser XIST, MALAT1, BRCA1, NFKB1, COL1A2, HOTAIR, HOXC11, e HOXC12 está em gene_name na coluna de atributos

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils


### 18 - Generate a scatterplot to represent the distribution of gene sizes in the X chromosome.
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
O código SQL e o script python gerados funcionam de primeira, porém não geram um gráfico idêntico/parecido com o do gabarito

Cons:
Está errado
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Primeiro código gerado pelo GPT-4o Mini com contextualização que rodou e gerou um resultado satisfatório.

Cons:
Não gera um gráfico idêntico/parecido com o do gabarito

### 19 - Generate a stacked barplot chart to represent the proportions of protein-coding, lncRNA and miRNA genes on each chromosome separately.
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica para o usuário que há a possiblidade de que seja necessário ajustar as clausulas que buscam por valores na coluna de atributos, pois é uma coluna sem padronização universal
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL
Se corrigido o primeiro SQL e executado o script python gerado pelo modelo, ele cria um gráfico que mostra as proporções de CDS, Selenocysteine, exon, five_prime_utr, gene, start_codon, stop_codon, three_prime_utr e transcript em cada cromossomo

Cons:
É necessário corrigir o primeiro SQL gerado, pois o modelo pôs que as informações protein-coding, lncRNA e miRNA estariam na coluna featuretype
O gráfico gerado é errado, pois não é idêntico/parecido com o gráfico do gabarito
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils

Cons:
Necessário corrigir a chamada da função, o modelo claramente não sabe como funciona a chamada
O modelo claramente, a esse ponto, não entendeu como funciona o módulo gffutils


### 20 - Generate a boxplot to represent the comparison of protein_coding, lncRNA, and miRNA transcript sizes
#### No prompt
Pros:
Explica primeiro com um passo a passo em linguagem natural, sem entrar em detalhes técnicos de computação, como construir a lógica do SQL pra resolver a questão
Explica a query, cada pedaço dela. O que é ótimo pra quem não entende nada de SQL

Cons:
É necessário corrigir o primeiro SQL gerado, pois o modelo pôs que as informações protein-coding, lncRNA e miRNA estariam na coluna featuretype
A lógica do script não é suficiente para gerar o gráfico do gabarito, pois seria necessário utilizar o gffutils para recuperar algumas informações
#### With prompt
Pros:
Tentou utilizar a biblioteca gffutils
Segundo código gerado pelo GPT-4o Mini com contextualização que rodou e gerou um resultado satisfatório.

Cons:
Não gera um gráfico idêntico/parecido com o do gabarito


### Grandes problemas
- Os códigos gerados pelo GPT-4o Mini sempre encontravam problema com a função features_of_type(), isso faz sentido, pois, por ter amplos usos na biblioteca gffutils, é considerado complexo para a compreensão do modelo, que não foi treinado com afinco em cima do módulo python. A sugestão é que fosse feita uma melhor instrução dessa função para o modelo, caso a intenção ainda seja de fazê-lo utilizar o gffutils.