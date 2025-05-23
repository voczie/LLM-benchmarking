import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
import os

if os.path.exists('results/') == False:
    os.mkdir('results/')

if os.path.exists('results/with-prompt') == False:
    os.mkdir('results/with-prompt')

with open("prompt.txt", "r") as f:
    context = f.read()

# The db description
schema = '''CREATE TABLE features (
    id text,
    seqid text,
    source text,
    featuretype text,
    start int,
    end int,
    score text,
    strand text,
    frame text,
    attributes text,
    extra text,
    bin int,
    primary key (id)
    );

CREATE TABLE relations (
    parent text,
    child text,
    level int,
    primary key (parent, child, level)
    );

CREATE TABLE meta (
    dialect text,
    version text
    );

CREATE TABLE directives (
    directive text
    );

CREATE TABLE autoincrements (
    base text,
    n int,
    primary key (base)
    );

CREATE TABLE duplicates (
    idspecid text,
    newid text,
    primary key (newid)
    );'''

# LLM part
questions = [
    """How many genes and transcripts are there on chromosome 3?""",
    """How many protein-coding genes are on chromosome 12?""",
    """How many lncRNA genes are on chromosome 7?""",
    """How many pseudogenes are on the X chromosome?""",
    """How many genes for miRNA exist in chromosome 10?""",
    """Calculate the sizes of each gene locus separately: XIST, MALAT1, BRCA1, COL1A2, NFKB1, NFKB2, REL, RELA and RELB""",
    """How many transcript isoforms does the XIST gene have? Print the transcript isoform names (transcript_name) and the sizes of each.""",
    """How many exons does the XIST gene have?""",
    """How many exons does each transcript isoform of the BRCA1 gene have? Print the transcript isoform names (tr anscript_name) and the number of exons.""",
    """What is the average exon size of the BRCA1 transcript isoforms?""",
    """What is the chromosomal position of the BRCA1 gene?""",
    """On which chromosomes are the genes NFKB1, NFKB2, REL, RELA and RELB located?""",
    """Print the names of the 2 genes located immediately before and after the gene COL1A2, respectively""",
    """What is the biotype of the following genes XIST, MALAT1, BRCA1,NFKB1, NFKB2, REL, RELA, RELB and COL1A2?""",
    """What strand are the HOTAIR, HOXC11, and HOXC12 genes located on?""",
    """Which genes are located between the HOXC11 and HOXC12 genes on + and - strands?""",
    """Get the following informations about each transcript isoforms of the XIST, MALAT1, BRCA1, NFKB1, COL1A2, HOTAIR, HOXC11, and HOXC12 genes: chromosomal location and position, size, number of exons, average exon size, strand, and biotype. Organize all the information in a table and save it.""",
    """Generate a scatterplot to represent the distribution of gene sizes in the X chromosome.""",
    """Generate a stacked barplot chart to represent the proportions of protein-coding, lncRNA and miRNA genes on each chromosome separately.""",
    """Generate a boxplot to represent the comparison of protein_coding, lncRNA, and miRNA transcript sizes"""
]

models = [
    "gemma2",
    "qwen2.5:14b",
    "phi4",
    "deepseek-r1:14b"
]

current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

for model_name in models:
    model_name_path = model_name.replace(":", "-")
    if os.path.exists(f'results/with-prompt/{model_name_path}') == False:   
        os.mkdir(f'results/with-prompt/{model_name_path}')

    for ix, question in enumerate(questions):
        TEMPLATE = '''
        {context}

        ### Given a genome annotation in a GFF/GTF format and all of its data is stored in a sqlite3 database with the following SCHEMA: 
        <schema>
        {schema}
        </schema>

        <user_question>
        Guide me with a query or a walkthrough based on to answer the following question: {question}
        </user_question>
        '''

        # Instantiating the model
        llm = OllamaLLM(model=model_name,
                    temperature=0.1,
                )

        prompt = PromptTemplate(
            input_variables=["context", "schema", "question"], template=TEMPLATE
        )

        chain = prompt | llm | StrOutputParser()

        # Running
        res = chain.invoke({
            "context": context,
            "schema": schema,
            "question": questions[0]
        })

        with open(f'results/with-prompt/{model_name_path}/llm_test_question_{ix}_{current_time}.txt', 'w') as f:
            f.write(res)