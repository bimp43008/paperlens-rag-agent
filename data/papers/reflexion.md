# Reflexion: Verbal Reinforcement Learning

Reflexion, introduced by Shinn et al. (2023), is a strategy for improving
language agents without updating their model weights. Instead of gradient
descent on rewards, the agent learns through language: after attempting a task
and failing, it generates a self-reflection — a written analysis of what went
wrong and what it should try differently — and stores that reflection in an
episodic memory. On the next attempt the agent reads its own past reflections
as additional context, which steers it away from repeating the same mistake.

## The actor-evaluator-self-reflection loop

Reflexion frames the agent as three cooperating roles. The actor is the policy
that produces trajectories (the actual attempts at the task). The evaluator
scores those trajectories, often with a simple heuristic or a separate model
call, deciding whether the attempt succeeded. When the signal is negative, the
self-reflection module turns that scalar judgment into rich linguistic
feedback, reasoning about the failure in natural language. This verbal signal,
rather than a numeric reward, is what gets written to memory and reused. The
loop repeats across trials until success or a budget is exhausted.

## Episodic memory as the learning mechanism

Because weights stay frozen, all "learning" lives in the memory buffer of
reflections. This buffer is short-term and task-scoped: it accumulates the
lessons from the current episode's failures and is prepended to future prompts.
The effect is that the agent exhibits a form of trial-and-error improvement
within a single session, analogous to how a person gets better at a puzzle by
remembering which moves failed, not by rewiring their brain. Memory length is a
tunable knob; too little and lessons are forgotten, too much and the context
fills with stale reflections that dilute the useful ones.

## Results and intuition

The authors reported strong gains on programming benchmarks such as HumanEval,
where Reflexion agents reached substantially higher pass rates than baseline
ReAct-style agents, and on decision-making and sequential-search tasks. The
intuition is that language is a high-bandwidth, interpretable channel for
credit assignment: a reflection like "I assumed the file existed without
checking" carries far more corrective information than a single reward of zero,
and the model can directly condition on it.

## Relation to RAG and tool use

Reflexion complements retrieval rather than replacing it. A reflection often
identifies *what evidence was missing* ("I guessed the API signature instead of
looking it up"), which is exactly the kind of insight that tells a ReAct agent
to fire a query-engine tool on the next pass. In a RAG-backed agent, episodic
reflections and retrieved documents can both be injected into context: the
retrieval supplies grounding facts, while the reflections supply procedural
lessons about how to use them. Together they push an agent toward
self-improvement across attempts without any fine-tuning step.