# 🏗️ Architecture Documentation

## Offline Customer Support Chatbot — Chic Boutique

---

## 1. System Overview

The Chic Boutique Offline Chatbot is a **single-machine, fully offline** application that leverages a locally-hosted Large Language Model (LLM) to generate customer support responses. The system is designed with **data privacy** as the primary architectural constraint — no network calls are made to external services at any point during operation.

### Design Philosophy

| Principle | Implementation |
|---|---|
| **Privacy by Design** | All inference runs on `localhost`; no external API calls |
| **Simplicity** | Single Python script, no database, no web framework |
| **Reproducibility** | Deterministic pipeline: same queries → same prompt → logged results |
| **Separation of Concerns** | Templates, logic, and output are in separate files/directories |

---

## 2. Architecture Diagram

### 2.1 High-Level Component Architecture

```mermaid
graph TB
    subgraph USER_LAYER["👤 User Layer"]
        CLI["Command Line Interface<br>python chatbot.py"]
    end

    subgraph APPLICATION_LAYER["📦 Application Layer (chatbot.py)"]
        TL["Template Loader<br>load_template()"]
        PF["Prompt Formatter<br>str.replace('{query}', ...)"]
        QO["API Client<br>query_ollama()"]
        SN["Response Sanitizer<br>sanitize_for_markdown_table()"]
        MW["Markdown Writer<br>File I/O"]
    end

    subgraph TEMPLATE_LAYER["📄 Template Layer (prompts/)"]
        ZS["zero_shot_template.txt"]
        OS["one_shot_template.txt"]
    end

    subgraph INFERENCE_LAYER["🧠 Inference Layer (Ollama)"]
        API["REST API<br>POST /api/generate<br>localhost:11434"]
        MODEL["Llama 3.2 (3B)<br>Quantized GGUF"]
    end

    subgraph OUTPUT_LAYER["📊 Output Layer"]
        RES["eval/results.md"]
        CON["Console Output<br>(Progress + Timing)"]
    end

    CLI --> TL
    TL --> ZS
    TL --> OS
    ZS --> PF
    OS --> PF
    PF --> QO
    QO --> API
    API --> MODEL
    MODEL --> API
    API --> QO
    QO --> SN
    SN --> MW
    MW --> RES
    MW --> CON

    style USER_LAYER fill:#1B2631,stroke:#2C3E50,color:#ECF0F1
    style APPLICATION_LAYER fill:#1A237E,stroke:#283593,color:#E8EAF6
    style TEMPLATE_LAYER fill:#004D40,stroke:#00695C,color:#E0F2F1
    style INFERENCE_LAYER fill:#4A148C,stroke:#6A1B9A,color:#F3E5F5
    style OUTPUT_LAYER fill:#BF360C,stroke:#D84315,color:#FBE9E7
```

### 2.2 Request-Response Data Flow

```mermaid
sequenceDiagram
    participant Script as chatbot.py
    participant Disk as File System
    participant Ollama as Ollama Server
    participant LLM as Llama 3.2

    Note over Script: Initialization Phase
    Script->>Disk: Read zero_shot_template.txt
    Disk-->>Script: Template string with {query} placeholder
    Script->>Disk: Read one_shot_template.txt
    Disk-->>Script: Template string with {query} and example
    Script->>Disk: Create/open eval/results.md (write mode)

    Note over Script: Processing Phase (×20 queries)
    loop For each customer query
        Note over Script: Zero-Shot Pass
        Script->>Script: Replace {query} with actual question
        Script->>Ollama: POST /api/generate<br>{"model":"llama3.2:3b","prompt":"...","stream":false}
        Ollama->>LLM: Tokenize + Forward Pass
        LLM-->>Ollama: Generated tokens
        Ollama-->>Script: {"response":"...","done":true}
        Script->>Script: Sanitize response (escape pipes, strip newlines)
        Script->>Disk: Append row to results.md table

        Note over Script: One-Shot Pass
        Script->>Script: Replace {query} with actual question
        Script->>Ollama: POST /api/generate<br>{"model":"llama3.2:3b","prompt":"...","stream":false}
        Ollama->>LLM: Tokenize + Forward Pass
        LLM-->>Ollama: Generated tokens
        Ollama-->>Script: {"response":"...","done":true}
        Script->>Script: Sanitize response
        Script->>Disk: Append row to results.md table
    end

    Note over Script: Finalization
    Script->>Disk: Close results.md
    Script->>Script: Print summary (total time, response count)
```

---

## 3. Component Architecture

### 3.1 Module Breakdown

```mermaid
classDiagram
    class chatbot_py {
        +OLLAMA_ENDPOINT: str
        +MODEL_NAME: str
        +QUERIES: list~str~
        +query_ollama(prompt: str) str
        +load_template(filepath: str) str
        +sanitize_for_markdown_table(text: str) str
        +main() None
    }

    class zero_shot_template {
        +role_assignment: str
        +query_placeholder: str
        -examples: None
    }

    class one_shot_template {
        +role_assignment: str
        +query_placeholder: str
        +example_query: str
        +example_response: str
    }

    class results_md {
        +scoring_rubric: Section
        +data_table: MarkdownTable
        +columns: QueryNum, Query, Method, Response, R, C, H
    }

    chatbot_py --> zero_shot_template : loads
    chatbot_py --> one_shot_template : loads
    chatbot_py --> results_md : writes
```

### 3.2 Function Responsibilities

| Function | Input | Output | Responsibility |
|---|---|---|---|
| `query_ollama(prompt)` | Formatted prompt string | Model response text | HTTP POST to Ollama API, error handling, JSON parsing |
| `load_template(filepath)` | File path string | Raw template string | Reads UTF-8 text file from disk |
| `sanitize_for_markdown_table(text)` | Raw response text | Cleaned single-line text | Escapes `\|`, removes `\n`, collapses whitespace |
| `main()` | — | — | Orchestrates the full pipeline: load → format → query → log |

---

## 4. Inference Architecture

### 4.1 Ollama Server Architecture

```mermaid
graph LR
    subgraph OLLAMA["Ollama Runtime"]
        direction TB
        REST["REST API Server<br>:11434"]
        RUNNER["Model Runner<br>(llama.cpp backend)"]
        CACHE["KV Cache<br>(Context Memory)"]
        QUANT["Quantized Weights<br>~2GB GGUF file"]

        REST --> RUNNER
        RUNNER --> CACHE
        RUNNER --> QUANT
    end

    CLIENT["chatbot.py<br>requests.post()"] --> REST
    REST --> |"JSON Response"| CLIENT

    style OLLAMA fill:#2D1B69,stroke:#7C4DFF,color:#E8EAF6
    style CLIENT fill:#1B5E20,stroke:#4CAF50,color:#E8F5E9
```

### 4.2 Model Specifications

| Property | Value |
|---|---|
| **Model** | Meta Llama 3.2 |
| **Parameters** | 3 Billion |
| **Quantization** | Q4_0 (4-bit) via Ollama |
| **Model File Size** | ~2 GB |
| **Context Window** | 128K tokens |
| **Architecture** | Transformer (decoder-only) |
| **Training** | Instruction-tuned (chat-optimized) |

### 4.3 Inference Pipeline

```mermaid
flowchart LR
    A["Raw Prompt Text"] --> B["Tokenizer<br>(Text → Token IDs)"]
    B --> C["Embedding Layer<br>(Token IDs → Vectors)"]
    C --> D["32 Transformer Layers<br>(Self-Attention + FFN)"]
    D --> E["Output Head<br>(Vectors → Logits)"]
    E --> F["Sampling<br>(Logits → Token ID)"]
    F --> G["Detokenizer<br>(Token ID → Text)"]
    G --> |"Append to output"| H{"End of<br>Sequence?"}
    H --> |"No"| D
    H --> |"Yes"| I["Final Response String"]

    style A fill:#E3F2FD,stroke:#1565C0,color:#1565C0
    style D fill:#F3E5F5,stroke:#6A1B9A,color:#6A1B9A
    style I fill:#E8F5E9,stroke:#2E7D32,color:#2E7D32
```

---

## 5. Prompt Architecture

### 5.1 Template Design

```mermaid
graph TB
    subgraph ZERO_SHOT["Zero-Shot Template"]
        Z1["System Role:<br>'You are a helpful, friendly, and concise<br>customer support agent for Chic Boutique...'"]
        Z2["Query Slot:<br>Customer Query: '{query}'"]
        Z3["Response Trigger:<br>Agent Response:"]
        Z1 --> Z2 --> Z3
    end

    subgraph ONE_SHOT["One-Shot Template"]
        O1["System Role:<br>(Same as Zero-Shot)"]
        O2["Example Block:<br>--- EXAMPLE START ---<br>Q: 'What is your return policy?'<br>A: 'We offer a 30-day return...'<br>--- EXAMPLE END ---"]
        O3["Query Slot:<br>Customer Query: '{query}'"]
        O4["Response Trigger:<br>Agent Response:"]
        O1 --> O2 --> O3 --> O4
    end

    style ZERO_SHOT fill:#FFEBEE,stroke:#C62828,color:#B71C1C
    style ONE_SHOT fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
```

### 5.2 Prompt Structure Comparison

| Component | Zero-Shot | One-Shot |
|---|---|---|
| Role Assignment | ✅ Present | ✅ Present |
| Guard Rail ("Don't make up info") | ✅ Present | ✅ Present |
| Example Q&A Pair | ❌ Absent | ✅ 1 pair (return policy) |
| Query Placeholder | ✅ `{query}` | ✅ `{query}` |
| Token Count (approx.) | ~50 tokens | ~90 tokens |
| Expected Behavior | General instruction following | Style-guided generation |

---

## 6. Error Handling Architecture

```mermaid
flowchart TD
    A["query_ollama(prompt)"] --> B{"HTTP POST<br>to Ollama"}
    B --> |"Success (200)"| C["Parse JSON<br>Extract 'response' field"]
    B --> |"ConnectionError"| D["Return error message<br>'Is Ollama running?'"]
    B --> |"Timeout (>120s)"| E["Return error message<br>'Request timed out'"]
    B --> |"Other HTTP Error"| F["response.raise_for_status()<br>→ HTTPError"]
    F --> G["Return generic error message"]
    C --> H["Return cleaned response"]

    style A fill:#1565C0,stroke:#0D47A1,color:#fff
    style C fill:#2E7D32,stroke:#1B5E20,color:#fff
    style D fill:#C62828,stroke:#B71C1C,color:#fff
    style E fill:#E65100,stroke:#BF360C,color:#fff
    style F fill:#AD1457,stroke:#880E4F,color:#fff
```

---

## 7. Output Architecture

### 7.1 Results File Structure

The `eval/results.md` file follows a strict markdown table schema:

```
# Evaluation Results

## Scoring Rubric
[Criterion definitions]

| Query # | Customer Query | Prompting Method | Response | Relevance | Coherence | Helpfulness |
|---------|---------------|-----------------|----------|-----------|-----------|-------------|
| 1       | "..."         | Zero-Shot       | "..."    | 5         | 5         | 5           |
| 1       | "..."         | One-Shot        | "..."    | 5         | 5         | 5           |
| ...     | ...           | ...             | ...      | ...       | ...       | ...         |
```

**Schema guarantees:**
- Exactly **40 rows** (20 queries × 2 methods)
- Every query appears exactly **twice** (once per method)
- Scores are integers in range **[1, 5]**
- Responses are single-line (sanitized)

---

## 8. Security & Privacy Architecture

```mermaid
graph TB
    subgraph BOUNDARY["🔒 Security Boundary (localhost only)"]
        APP["chatbot.py"]
        OLLAMA["Ollama Server<br>127.0.0.1:11434"]
        MODEL["Model Weights<br>(Local Disk)"]
        DATA["eval/results.md<br>(Local Disk)"]

        APP <--> OLLAMA
        OLLAMA <--> MODEL
        APP --> DATA
    end

    INTERNET["🌐 Internet"] -.->|"❌ No Connection"| BOUNDARY

    style BOUNDARY fill:#1B5E20,stroke:#4CAF50,color:#E8F5E9
    style INTERNET fill:#B71C1C,stroke:#F44336,color:#FFCDD2
```

| Security Feature | Implementation |
|---|---|
| **No external API calls** | Ollama runs on `localhost:11434` only |
| **No data exfiltration** | All outputs written to local filesystem |
| **No credentials stored** | No API keys, tokens, or secrets required |
| **No PII processing** | Queries are fictional; no real customer data |
| **GDPR/CCPA compliant** | Data never leaves the local machine |

---

## 9. Technology Decisions

### Why Ollama?

| Alternative | Limitation | Ollama Advantage |
|---|---|---|
| OpenAI API | Requires internet, costs money, data leaves network | Free, offline, private |
| Hugging Face Transformers | Complex setup, requires PyTorch/CUDA | Single binary, auto-quantization |
| llama.cpp (raw) | Manual compilation, no REST API out of box | Built-in REST API, model management |
| vLLM | Complex, designed for multi-GPU servers | Lightweight, runs on laptops |

### Why Llama 3.2 (3B)?

| Alternative | Trade-off |
|---|---|
| Llama 3.2 (1B) | Too small — quality degrades significantly |
| Llama 3.1 (8B) | Better quality but requires 8GB+ RAM |
| Mistral 7B | Strong alternative, but larger memory footprint |
| Llama 3.1 (70B) | Excellent quality but needs GPU server |

**The 3B model hits the sweet spot**: good enough quality for basic support, small enough to run on any modern laptop.

### Why Python + `requests`?

| Alternative | Reason Not Chosen |
|---|---|
| `ollama` Python package | Adds unnecessary dependency for simple REST calls |
| `aiohttp` (async) | Overkill — queries are sequential by design |
| `curl` / bash script | Less readable, harder to maintain |
| Node.js / `fetch` | Python is the ML ecosystem standard |

---

## 10. Scalability Considerations

While this prototype is a single-script tool, the architecture can scale:

| Scale | Approach |
|---|---|
| **Multi-model** | Add more templates and loop over multiple Ollama model names |
| **RAG Integration** | Add ChromaDB/FAISS vector store for knowledge grounding |
| **Web Interface** | Wrap `query_ollama()` in a Flask/FastAPI endpoint |
| **Batch Processing** | Current design already supports batch — just add more queries |
| **GPU Acceleration** | Ollama automatically uses GPU if available (NVIDIA CUDA, Apple Metal) |
| **Multi-turn Chat** | Switch from `/api/generate` to `/api/chat` endpoint |
