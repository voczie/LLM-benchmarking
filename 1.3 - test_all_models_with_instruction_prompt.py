import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
import os
import chromadb

collection = chromadb.PersistentClient(path="databases/").get_collection(name="questions_code_examples_python")

def get_code_examples(question_query, n = 3):
    results = collection.query(
        query_texts=[question_query],
        n_results=3,
        include=['metadatas', 'documents']
    )

    dict_results = {}
    for i, doc in enumerate(results['documents'][0]):
        dict_results.update({doc:results['metadatas'][0][i]['code_example']})

    return dict_results

if os.path.exists('results/') == False:
    os.mkdir('results/')

if os.path.exists('results/with-prompt') == False:
    os.mkdir('results/with-prompt')

with open("1.2 - prompt.md", "r") as f:
    context = f.read()

# The db description
ddl = '''table_name,field_name,field_type,field_description
features,id,text,Primary key for features. The content of this field is determined by the user and the file format at creation time
features,seqid,text,Chromosome or contig ID
features,source,text,The source of the annotation (e.g. Ensembl; GENCODE)
features,featuretype,text,The type of feature (e.g. gene; transcript; exon)
features,start,int,The start coordinate of the feature
features,end,int,The end coordinate of the feature
features,score,text,A score associated with the feature (if available)
features,strand,text,The strand of the feature (+; -; or .)
features,frame,text,The coding frame of the feature (0; 1; or 2)
features,attributes,text,A string containing semicolon-separated attribute-value pairs
features,extra,text,A JSON-serialized list of non-standard extra fields. These are sometimes added by analysis tools (e.g. BEDTools). For standard GFF/GTF this field will be empty
features,bin,int,The genomic bin according to the UCSC binning strategy
features,primary key,(id),Same as the field id. Primary key for features
relations,parent,text,Foreign key to features.id – a gene for example
relations,child,text,Foreign key to feature.id – an mRNA or an exon for example
relations,level,int,In graph terms the number of edges between child and parent. In biological terms if parent=gene and child=mRNA then level=1. If parent=gene and child=exon then level=2
relations,primary key,(parent, child, level),Composite key using the fields parent; child and level. Composed of two foreign keys and one integer
meta,dialect,text,A JSON-serialized version of the dialect empirically determined when parsing the original file
meta,version,text,The gffutils version used to create the database
directives,directive,text,String directive without the leading ##
autoincrements,base,text,By default the feature type (gene; exon; etc) but can also be the value of any GFF field or attribute (e.g. the seqid or “GENE_1” (in the case of multiple features with ID=”GENE_1”)
autoincrements,n,int,Current extent of autoincrementing – add 1 to this when autoincrementing next time
autoincrements,primary key,(base),Same as the field base. Primary key for autoincrements
duplicates,idspecid,text,ID of the identified duplicated feature
duplicates,newid,text,New ID for the duplicated feature
duplicates,primary key,(newid),Same as the field newid. Primary key for duplicates
'''

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

questions_2 = [
    """How many genes and transcripts are there on chromosome Y?""",  #1 Gene Count and Distribution by Chromosome
    """How many protein-coding transcripts are present on chromosome 1?""",        #2 Gene Count and Distribution by Chromosome
    """What are the Ensembl gene IDs and biotypes of XIST, MALAT1, BRCA1, and COL1A2?""",    #3 Specific Gene Characteristics
    """Which BRCA1 transcript has the smallest average exon size?""",              #4 Specific Gene Characteristics
    """Which gene lies directly downstream of COL1A2 on the same strand?""",           #5 Chromosomal Location
    """Which gene precedes COL1A2 and is on the same strand?""",       #6 Chromosomal Location
    """Create a table showing the number of transcripts per gene for BRCA1, MALAT1, and XIST.""",      #7 Gene and Isoform Features
    """Generate a scatterplot showing the relationship between gene length and number of exons on chromosome X."""        #8 Gene and Isoform Features                                                                                       
]

models = [
    "gemma2:9b",
    "qwen2.5:14b",
    "phi4:14b",
    "deepseek-r1:14b"
]

current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

for model_name in models:
    model_name_path = model_name.replace(":", "-")
    if os.path.exists(f'results/with-prompt/{model_name_path}') == False:   
        os.mkdir(f'results/with-prompt/{model_name_path}')

    for ix, question in enumerate(questions):
        questions_codes = get_code_examples(question)

        TEMPLATE = '''
        {context}

        ### Given a genome annotation in a GFF/GTF format, and all of its data is stored in a SQLite3 database, whose fields are described within the DDL: 
        <ddl>
        {ddl}
        </ddl>

        <user_question>
        Guide me with a query or a walkthrough based on to answer the following question: {question}
        </user_question>

        Here's some code examples in Python 3 that might help:
        <code_examples>
        {questions_codes}
        </code_examples>
        '''

        # Instantiating the model
        llm = OllamaLLM(model=model_name,
                    temperature=0.1,
                )

        prompt = PromptTemplate(
            input_variables=["context", "ddl", "question", "questions_codes"], template=TEMPLATE
        )

        chain = prompt | llm | StrOutputParser()

        # Running
        res = chain.invoke({
            "context": context,
            "ddl": ddl,
            "question": questions,
            "questions_codes": questions_codes
        })

        with open(f'results/with-prompt/{model_name_path}/llm_test_question_{ix}_{current_time}.txt', 'w') as f:
            f.write(res)