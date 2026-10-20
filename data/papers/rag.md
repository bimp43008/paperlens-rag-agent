# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation combines a parametric memory (the weights of a
language model) with a non-parametric memory (an external corpus of documents
that can be searched at query time). The core idea, introduced by Lewis et al.
(2020), is that a model should not have to memorize every fact inside its
parameters. Instead, when a question arrives, the system first retrieves the
most relevant passages from a knowledge source and feeds them to the generator
as additional context. The model then produces an answer grounded in those
passages rather than relying only on what it saw during training.

## Why RAG exists

Large language models are trained on enormous but fixed corpora. They do not
know private data, they cannot see information published after their training
cutoff, and they sometimes hallucinate facts that sound plausible but are wrong.
RAG addresses all three problems at once: it lets the model consult fresh or
domain-specific material, it restricts answers to retrieved evidence, and it
makes the source of each claim inspectable because the retrieved chunks travel
with the answer.

## The five stages of a RAG pipeline

A working RAG system is usually described as five stages. Loading brings raw
data (text files, PDFs, web pages, database rows) into the workflow as
document objects. Indexing converts those documents into a searchable
structure, most commonly by turning each piece of text into a numerical
embedding, which is a vector that captures its meaning. Storing persists the
index and its metadata so the expensive embedding step does not have to run
again on every query. Querying takes a user question, embeds it in the same
vector space, finds the nearest stored chunks, and passes them to the language
model to synthesize a response. Evaluation measures whether the resulting
answers are accurate, faithful to the sources, and fast enough.

## Documents, nodes, and embeddings

Inside an indexing framework the original file is represented as a Document,
while the smaller fragments it is cut into are called Nodes. Splitting matters
because retrieval works far better on focused paragraphs than on whole books:
a tight chunk has one dominant topic, so its embedding points cleanly in one
direction in vector space. An embedding model maps each node's text to a list
of numbers; two texts with similar meaning end up close together under a
distance metric such as cosine similarity. At query time the question is
embedded with the very same model, and the system returns the nodes whose
vectors sit nearest to the question vector.

## From index to query engine

Once vectors are stored in a vector database, an index object wraps them and
exposes search. The index can then be turned into different interfaces. A
retriever returns only the matched nodes with their similarity scores, which is
useful when you want raw evidence. A query engine goes one step further: it
retrieves the nodes, hands them to a language model, and returns a written
answer. A chat engine adds conversation memory on top. For agent-style systems
the query engine is the most common choice, because an agent typically needs a
single grounded answer it can act on, not an ongoing dialogue.