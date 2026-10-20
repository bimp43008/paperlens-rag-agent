# Toolformer: Teaching Models to Use Tools

Toolformer, from Schick et al. (2023, Meta), shows that a language model can
learn to use external tools largely on its own, without heavy human annotation.
The starting point is a plain causal language model and a small set of APIs,
such as a calculator, a question-answering system, a web search engine, a
translation service, and a weather lookup. The model is trained to decide, for
each span of text, whether calling one of these APIs would make the next part
of the sentence easier to predict, and if so, to insert the call and use its
returned value.

## Self-supervised API annotation

The clever part of Toolformer is how the training data is built. The authors
take unlabeled text and, for every candidate API call at every position, they
measure the model's perplexity with and without the call's result spliced in.
If including the tool output lowers the loss on the surrounding tokens, the
call is considered useful and is kept; otherwise it is discarded. A filtering
step removes redundant or low-quality annotations. The result is a dataset of
"this sentence would benefit from this tool call here," produced almost
entirely automatically, which the model is then fine-tuned on.

## What the model learns to produce

After training, the model emits special API-call tokens inline while generating
text, pauses to receive the tool's response, and continues generation using
that response as context. Crucially it also learns when *not* to call a tool,
because unnecessary calls were filtered out during data construction. This
gives a form of learned tool discipline: the model invokes a calculator for
arithmetic it cannot do reliably, a search engine for facts outside its
parameters, and nothing at all for trivial continuations.

## Connection to agents and RAG

Toolformer is an early and clean demonstration of the tool-use idea that later
agent frameworks generalize. Where ReAct structures tool use as an explicit
thought-action loop at inference time, Toolformer bakes the *decision* to use a
tool into the model's weights through training. Both views meet in modern
agents: a retrieval index is just another API in the toolbox, and a query
engine plays the role that Toolformer's question-answering or search tool
plays. The lesson that transfers to RAG systems is that tool use should be
selective and grounded in measurable benefit, not fired on every prompt.

## Limitations

Toolformer's gains are bounded by the quality and coverage of the APIs provided
and by the perplexity heuristic, which can keep calls that help only locally.
It also does not natively handle multi-step chains where one tool's output must
be transformed before feeding another; that compositionality is left to the
in-time reasoning layer. Still, as a proof that models can teach themselves
when a tool is worth reaching for, it remains a foundational reference for
tool-augmented and retrieval-augmented language models.