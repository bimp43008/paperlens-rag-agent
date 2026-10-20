# Evaluating RAG and Language Agents

A retrieval-augmented or agentic system is not finished when it runs; it is
finished when you can show that its outputs are trustworthy. Because language
models are stochastic and can phrase the same idea in countless ways, you cannot
rely on eyeballing a handful of answers. Evaluation provides objective,
repeatable measurements of quality along several independent dimensions, and it
lets you compare strategies or detect regressions when you change a chunk size,
an embedding model, or a prompt.

## The three core dimensions

Most RAG evaluation frameworks separate quality into three axes. Faithfulness
(also called groundedness) asks whether every claim in the answer is actually
supported by the retrieved context; an unfaithful answer invents details that
were never in the sources, which is the classic hallucination failure mode.
Answer relevancy asks whether the response actually addresses the question that
was asked, catching cases where the model returns true-but-off-topic material.
Correctness compares the answer against a known ground truth when one exists,
measuring factual accuracy rather than mere consistency with the context. A
system can be faithful yet irrelevant, or relevant yet wrong, which is why these
are measured separately instead of collapsed into one score.

## LLM-as-judge

Checking these dimensions by hand does not scale, so evaluators typically use a
strong language model as a judge: the question, the retrieved context, and the
generated answer are presented to the model, which returns a verdict and often a
short rationale. In LlamaIndex this is exposed through evaluator classes such as
FaithfulnessEvaluator, AnswerRelevancyEvaluator, and CorrectnessEvaluator, each
wrapping a judge LLM and producing a passing flag plus feedback. The judge
approach is convenient but imperfect: it inherits the biases and errors of the
judging model, so for high-stakes use it should be calibrated against human
labels and combined with deterministic checks where possible.

## What can go wrong in a RAG stack

Failures localize to specific stages, and good evaluation tells you which. If
retrieval is weak, the right passage never reaches the model, so even a perfect
synthesizer produces unfaithful or empty answers; this shows up as low recall in
the retrieved nodes. If chunking is bad, relevant facts are split across
fragments so no single node contains enough context, degrading faithfulness. If
the synthesizer over-generalizes, answers drift beyond the sources even when
retrieval was correct. Observability and tracing help here by recording, per
query, which nodes were fetched, what scores they had, and how the answer was
assembled, turning a vague "the bot is wrong" into a pinpoint diagnosis.

## Evaluation as a loop, not a gate

The practical value of evaluation is iterative. You establish a baseline on a
fixed set of questions, change one variable at a time (embedding model, chunk
size, response mode, prompt), re-run the suite, and keep the change only if the
metrics move in the right direction. Treating the question set as a regression
test prevents silent degradation as the system grows. For an agent that uses a
query engine as a tool, the same discipline extends upward: you also evaluate
whether the agent chose the right tool at the right time, not just whether the
final answer was grounded. Measurement is what converts a demo into a system you
can responsibly maintain.