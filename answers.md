# Questionnaire Answers

## 1. What was the most challenging aspect of designing your prompt templates, and how did you iterate on them to improve model responses?

The hardest part was balancing helpfulness with hallucination control in an offline setup. My first zero-shot drafts were too generic and sometimes sounded robotic, while early one-shot variants sometimes overfit to the example style and invented policy details. I iterated by keeping the role instruction stable, adding a clear guardrail ("Do not make up information about policies if you don't know the answer"), and then refining one high-quality example in the one-shot template to enforce tone and structure. I compared outputs across the same 20 queries and looked for improvements in empathy, actionability, and policy safety. The final one-shot prompt consistently produced better support-style responses without changing the model.

## 2. Explain the rationale behind the scoring criteria you chose for your evaluation rubric. Why were these specific metrics important for a customer support chatbot?

I used Relevance, Coherence, and Helpfulness because they map directly to customer support quality:

- Relevance checks whether the answer actually addresses the user issue.
- Coherence checks readability, grammar, and clarity, which affects trust.
- Helpfulness checks whether the response gives actionable next steps, not just generic text.

For support use cases, a response can be fluent but still fail if it is not relevant or actionable. These three metrics gave a practical balance between linguistic quality and business usefulness.

## 3. Beyond what you mentioned in your report, what are the biggest limitations of this offline chatbot? If you had more time, what is the first thing you would do to improve it?

The biggest limitations are: no real-time order/account access, no true policy grounding, and limited multi-turn memory. Even with good prompting, the model can still generate plausible but unverifiable details. If I had more time, my first improvement would be Retrieval-Augmented Generation (RAG) with a curated policy/FAQ knowledge base so responses are grounded in actual store data. That would reduce hallucinations and make answers more consistent and production-safe.

## 4. Based on your experiment, how suitable is a 3-billion-parameter model like Llama 3.2 for a production e-commerce support chatbot? Discuss the trade-offs between performance, cost, and response quality.

A 3B model is suitable for tier-1 support scenarios (common FAQs, simple policy questions, basic troubleshooting), especially when privacy and low cost are priorities. It performs well enough for structured single-turn tasks with strong prompts. Trade-offs:

- Performance/cost: excellent for local deployment, no API cost, privacy-friendly.
- Quality: good but not perfect; more prone to shallow answers or hallucinated specifics than larger models.
- Latency: acceptable for offline CPU usage, but can be slower than cloud GPU systems.

So it is good enough for a controlled support layer with guardrails and escalation, but complex cases may require larger models or human handoff.

## 5. This task used one-shot prompting. What other techniques could you have used to improve the chatbot performance without changing the model (e.g., retrieval-augmented generation)? Briefly describe one.

I would use Retrieval-Augmented Generation (RAG). For each customer query, the system would retrieve relevant documents (return policy, shipping rules, payment FAQ, escalation SOP) from a local knowledge base and inject that context into the prompt before generation. This improves factual grounding, reduces hallucinations, and keeps answers aligned with business policy, all without changing the base Llama 3.2 model.
