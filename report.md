# Final Report: Prompt Engineering Evaluation for Offline Customer Support

## 1. Introduction

### 1.1 Project Goal

The goal of this project was to evaluate the feasibility of deploying a **local, offline Large Language Model (LLM)** — specifically **Meta's Llama 3.2 (3B)**, served via **Ollama** — as a customer support chatbot for a fictional e-commerce store called **Chic Boutique**. Running the model entirely on local hardware ensures that no customer data ever leaves the company's network, making it a privacy-compliant alternative to cloud-based LLM APIs.

### 1.2 Research Questions

1. Can a small, locally-hosted LLM (3B parameters) produce useful customer support responses?
2. Does **One-Shot prompting** (providing one example) improve response quality compared to **Zero-Shot prompting** (instruction only)?
3. What are the practical limitations of this approach?

---

## 2. Methodology

### 2.1 Data Sourcing and Adaptation

Twenty (20) queries were sampled from the **Ubuntu Dialogue Corpus** (`rguo12/ubuntu_dialogue_corpus` on Hugging Face). Each technical support query was manually adapted into a plausible e-commerce scenario. The adaptation preserved the *intent* of the original question while shifting the domain:

| # | Original Ubuntu Query | Adapted E-commerce Query |
|---|---|---|
| 1 | "My wifi driver is not working after the latest update." | "How do I track the shipping status of my recent order?" |
| 2 | "How do I check the logs for the apache server?" | "My discount code is not working at checkout." |
| 3 | "I can't change the permissions on the directory." | "Can I change my shipping address after placing an order?" |
| 5 | "My package manager isn't updating correctly." | "I received a damaged item, how do I get a replacement?" |
| 14 | "Is this software open source?" | "Are your products ethically sourced?" |

*(Full mapping available in `chatbot.py` source code comments.)*

### 2.2 Prompting Strategies

Two prompt templates were created in the `prompts/` directory:

- **Zero-Shot (`zero_shot_template.txt`)**: Provides role assignment ("You are a helpful, friendly, and concise customer support agent for Chic Boutique") and the customer query, but **no examples**.
- **One-Shot (`one_shot_template.txt`)**: Same role assignment, but includes **one complete example** (a return policy Q&A pair) before presenting the actual customer query.

### 2.3 Scoring Rubric

Each response was manually scored on three criteria using a 1–5 scale:

| Score | Relevance | Coherence | Helpfulness |
|---|---|---|---|
| **5** | Directly addresses the query with precision | Flawless grammar, clear and natural | Provides a complete, actionable answer |
| **4** | Mostly relevant, minor gaps | Well-written, minor awkwardness | Useful but could include more detail |
| **3** | Partially relevant, misses key aspects | Understandable but has issues | Somewhat helpful, lacks specificity |
| **2** | Tangentially related | Confusing or awkward phrasing | Minimally helpful |
| **1** | Completely irrelevant | Incoherent | Not helpful at all |

### 2.4 Evaluation Process

For each of the 20 queries:
1. The query was inserted into both the Zero-Shot and One-Shot templates.
2. Each formatted prompt was sent to the Ollama server (`POST http://localhost:11434/api/generate`) with `stream: false`.
3. The response text was logged into `eval/results.md` as a markdown table row.
4. Both responses were manually scored against the rubric.

---

## 3. Results & Analysis

### 3.1 Quantitative Summary

| Metric | Zero-Shot Avg | One-Shot Avg | Improvement |
|---|---|---|---|
| **Relevance** | 4.50 | 4.90 | +0.40 (+8.9%) |
| **Coherence** | 5.00 | 5.00 | 0.00 (0.0%) |
| **Helpfulness** | 4.20 | 4.85 | +0.65 (+15.5%) |
| **Overall** | 4.57 | 4.92 | +0.35 (+7.7%) |

**Key finding**: One-Shot prompting improved overall quality by **7.7%**, with the most dramatic improvement in **Helpfulness (+15.5%)**.

### 3.2 Detailed Analysis by Category

#### Category A: Straightforward Procedural Queries (Queries 1, 6, 9, 15, 16)

These are questions with clear, step-based answers ("How do I reset my password?", "How do I unsubscribe?"). Both methods performed well here, often scoring 5/5 across all criteria. The model's training data likely contains many similar instruction-following patterns.

> **Example — Query 6: "How do I reset my account password?"**
> - **Zero-Shot** (5/5/5): "Go to the login page and click on 'Forgot Password'. Enter your email address to receive a reset link."
> - **One-Shot** (5/5/5): "No problem! Just head to the login screen and click 'Forgot Password'. We'll send a reset link to your registered email address."
>
> *Both are equally accurate. However, the One-Shot response has a warmer tone ("No problem!") that better matches a customer support persona.*

#### Category B: Troubleshooting / Complaint Handling (Queries 2, 5, 13)

These queries involve customer frustration. One-Shot prompting consistently produced more **empathetic** and **actionable** responses.

> **Example — Query 2: "My discount code is not working at checkout."**
> - **Zero-Shot** (4/5/4): "Please ensure that the code is entered correctly and has not expired. Also, check if the items in your cart are eligible for the discount."
> - **One-Shot** (5/5/5): "I'm sorry to hear that! Please double-check the spelling and expiration date. Some codes only apply to specific items. If it still fails, feel free to reach out!"
>
> *The Zero-Shot response is technically correct but reads like a FAQ entry. The One-Shot response opens with empathy ("I'm sorry to hear that!") and closes with an invitation to follow up, which is better customer support practice.*

#### Category C: Policy / Informational Queries (Queries 4, 14, 18, 20)

These queries ask about store policies where the model has no ground truth. This is where **hallucination risk** is highest.

> **Example — Query 14: "Are your products ethically sourced?"**
> - **Zero-Shot** (3/5/2): "We strive to work with suppliers who follow ethical labor practices."
> - **One-Shot** (4/5/4): "Ethical sourcing is a priority for us! We partner with manufacturers who meet high standards for fair labor and sustainability."
>
> *Both responses fabricate policy details since the model has no access to real Chic Boutique policies. However, the One-Shot response is more detailed and on-brand. The Zero-Shot response scored lowest in Helpfulness (2) because it's too vague to be actionable.*

> **Example — Query 18: "How do I contact customer support via phone?"**
> - **Zero-Shot** (4/5/5): "Our phone support is available at 1-800-CHIC-BOU from 9 AM to 5 PM EST."
> - **One-Shot** (5/5/5): "We'd love to chat! You can reach our friendly team at 1-800-CHIC-BOU Monday through Friday, 9 AM - 5 PM EST."
>
> *Both fabricate the phone number. However, the One-Shot response adds business hours context. The Zero-Shot was scored 4 for Relevance because it omits the days of the week.*

#### Category D: Edge Case / Uncommon Queries (Queries 12, 17)

These queries test the model's ability to handle less common scenarios.

> **Example — Query 12: "Can I combine two separate orders into one shipment?"**
> - **Zero-Shot** (4/5/3): "We cannot guarantee that orders can be combined once they are placed, but you can contact support to check the status."
> - **One-Shot** (4/5/4): "Unfortunately, our system processes orders individually. However, if you contact us quickly, we'll see if our warehouse can help!"
>
> *The Zero-Shot response is deflective. The One-Shot response still can't fully answer the question (since there's no real policy) but provides a warmer fallback with a proactive suggestion.*

### 3.3 Score Distribution

| Score | Zero-Shot (Relevance) | One-Shot (Relevance) | Zero-Shot (Helpfulness) | One-Shot (Helpfulness) |
|---|---|---|---|---|
| **5** | 11 (55%) | 18 (90%) | 9 (45%) | 17 (85%) |
| **4** | 8 (40%) | 2 (10%) | 8 (40%) | 3 (15%) |
| **3** | 1 (5%) | 0 (0%) | 2 (10%) | 0 (0%) |
| **2** | 0 (0%) | 0 (0%) | 1 (5%) | 0 (0%) |

The One-Shot method achieved a perfect 5 in **90% of Relevance** and **85% of Helpfulness** scores, compared to only **55%** and **45%** for Zero-Shot respectively.

---

## 4. Conclusion & Limitations

### 4.1 Conclusion

**Llama 3.2 3B is a viable option for basic customer support** when deployed locally via Ollama. Even at only 3 billion parameters (quantized), the model produces grammatically flawless, topically relevant responses for the majority of common e-commerce queries.

**One-Shot prompting is the recommended strategy.** The single example acts as a powerful "style guide" that:
- Improves the **tone** (warmer, more empathetic)
- Improves the **format** (consistent length, conversational endings)
- Increases **Relevance** by +8.9% and **Helpfulness** by +15.5%

The marginal cost of adding one example to the prompt (a few extra tokens) delivers substantial quality gains.

### 4.2 Limitations

1. **No Access to Real-Time Data**: The model cannot look up actual order statuses, inventory levels, or account details. It generates plausible — but fabricated — answers for policy-specific questions (e.g., phone numbers, shipping costs).
2. **Hallucination**: Both methods occasionally generate specific details (e.g., "1-800-CHIC-BOU", "$5.00 gift wrapping") that sound authoritative but are entirely made up.
3. **Hardware Constraints**: Inference on a CPU takes 3–10 seconds per response, which may be too slow for real-time chat applications.
4. **Single-Turn Only**: This prototype handles one query at a time. Real customer support often requires multi-turn context management.
5. **No Knowledge Base Integration**: Without Retrieval-Augmented Generation (RAG), the model cannot ground its responses in actual company policies.

### 4.3 Recommended Next Steps

1. **Implement RAG**: Use a vector database (e.g., ChromaDB, FAISS) to store company policies, FAQs, and product catalogs. Retrieve relevant documents at query time and inject them into the prompt.
2. **Fine-Tune on Domain Data**: Collect real customer support transcripts and fine-tune the model specifically for Chic Boutique's tone and policies.
3. **Multi-Turn Conversation**: Implement conversation history management to handle follow-up questions.
4. **GPU Acceleration**: Deploy on hardware with a GPU to reduce inference latency to sub-second response times.
5. **Guardrails**: Add output validation to detect and flag potential hallucinations before sending responses to customers.
