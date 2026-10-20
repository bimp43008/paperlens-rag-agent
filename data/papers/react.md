# ReAct: Synergizing Reasoning and Acting

ReAct, proposed by Yao et al. (2022), is a paradigm for language-model agents
that interleaves two kinds of steps: reasoning traces (internal thoughts) and
task-specific actions (calls to external tools or environments). Rather than
planning everything silently and then acting, or acting blindly without
reflection, a ReAct agent alternates between thinking and doing. Each cycle
looks like: thought, action, observation, thought, action, observation, and so
on, until the agent decides it has enough information to answer.

## The thought-action-observation loop

A thought is free-form natural language in which the model analyzes the current
situation, breaks the goal into subgoals, or decides what to do next. An action
is a concrete operation the model emits, such as searching a knowledge base,
running a calculator, or querying an API. An observation is the result returned
by the environment after the action executes. Because observations are fed back
into the next thought, the agent can correct a mistaken assumption mid-task
instead of compounding it. This closed loop is what makes ReAct feel agentic
rather than like a single prompt.

## Why interleaving helps

Pure chain-of-thought reasoning lets a model plan in its head but leaves it
disconnected from ground truth, so it can confidently reason about facts it
never verified. Pure acting, with no explicit reasoning, gives the model no
place to plan or recover from errors. ReAct gains the benefits of both: the
reasoning traces improve interpretability and let the model decompose hard
questions, while the actions anchor those reasons to real observations from
tools and documents. On benchmarks such as HotpotQA and FEVER the authors
reported fewer hallucinations than reasoning-only baselines, and on interactive
tasks like ALFWorld and WebShop the combination beat methods that used either
component alone.

## ReAct and RAG

ReAct pairs naturally with retrieval-augmented generation. The "action" step
can simply be a query to a RAG index, and the "observation" is the retrieved
passage or the synthesized answer. In this view a query engine is just one of
the tools a ReAct agent can reach for when its internal knowledge is
insufficient. The agent's thought decides whether to search, what to search
for, and whether the returned evidence is enough to finalize the response. This
is why RAG-backed query engines are commonly registered as agent tools: the
reasoning layer supplies the when and why, and the retrieval layer supplies the
grounded what.

## Practical caveats

ReAct depends on the underlying model being able to follow a structured loop
and to emit parseable actions. Weak models drift, forget to stop, or invent
observations instead of waiting for real ones. Prompt design therefore matters:
clear separators between thought, action, and observation, plus a few worked
examples, dramatically improve reliability. Logging every step is also valuable,
because the trace itself becomes debuggable evidence of how the agent reached
its answer.