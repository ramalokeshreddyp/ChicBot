<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/Llama_3.2-3B_Params-7C3AED?style=for-the-badge&logo=meta&logoColor=white" alt="Llama 3.2">
  <img src="https://img.shields.io/badge/Status-Production_Ready-00C853?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge" alt="License">
</p>

<h1 align="center">🛍️ Chic Boutique — Offline Customer Support Chatbot</h1>

<p align="center">
  <strong>A privacy-first, fully offline AI chatbot for e-commerce customer support</strong><br>
  <em>Powered by Ollama × Meta Llama 3.2 (3B) — Zero data leaves your network</em>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-key-findings">Key Findings</a> •
  <a href="#-documentation">Documentation</a>
</p>

---

## 📋 Project Overview

**Chic Boutique Offline Chatbot** is a fully functional, privacy-compliant customer support chatbot built for a fictional e-commerce store. It runs **entirely on local hardware** using [Ollama](https://ollama.com) to serve Meta's **Llama 3.2 (3B)** model — ensuring **zero customer data** ever leaves the company's network.

This project evaluates two fundamental prompt engineering strategies — **Zero-Shot** and **One-Shot** prompting — across 20 real-world e-commerce queries adapted from the **Ubuntu Dialogue Corpus**.

### 🎯 Core Objectives

| Objective | Description |
|---|---|
| 🔒 **Data Privacy** | Run LLMs locally to comply with GDPR, CCPA, and DPDP Act |
| 🧪 **Prompt Engineering** | Compare Zero-Shot vs. One-Shot prompting effectiveness |
| 📊 **Performance Evaluation** | Score model outputs on Relevance, Coherence, and Helpfulness |
| 🏭 **Feasibility Study** | Assess if a 3B-parameter model is viable for customer support |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM Engine** | Meta Llama 3.2 (3B) | Instruction-tuned language model for text generation |
| **Model Server** | Ollama | Local REST API server for LLM inference |
| **Application** | Python 3.8+ | Script orchestration, API calls, result logging |
| **HTTP Client** | `requests` | Communication with Ollama's REST endpoint |
| **Data Source** | Ubuntu Dialogue Corpus | Source of customer queries (via HuggingFace `datasets`) |
| **Output** | Markdown | Structured evaluation results and reporting |

---

## 🏗️ Architecture

### High-Level System Architecture

```mermaid
graph TB
    subgraph LOCAL_MACHINE["🖥️ Local Machine (Fully Offline)"]
        subgraph PYTHON_APP["📦 Python Application"]
            A["chatbot.py"] --> B["Load Prompt Templates"]
            B --> C["Format Prompts<br>(Zero-Shot & One-Shot)"]
            C --> D["HTTP POST Request"]
        end

        subgraph OLLAMA_SERVER["⚙️ Ollama Server (localhost:11434)"]
            E["REST API Endpoint<br>/api/generate"]
            F["Llama 3.2 (3B)<br>Quantized Model"]
            E --> F
            F --> G["Generated Response"]
            G --> E
        end

        subgraph OUTPUT["📄 Output Layer"]
            H["eval/results.md<br>(Scored Results)"]
            I["Console Progress<br>(Real-time Logging)"]
        end

        D --> E
        E --> J["JSON Response"]
        J --> K["Parse & Sanitize"]
        K --> H
        K --> I
    end

    style LOCAL_MACHINE fill:#1a1a2e,stroke:#16213e,color:#e94560
    style PYTHON_APP fill:#0f3460,stroke:#533483,color:#e2e2e2
    style OLLAMA_SERVER fill:#533483,stroke:#e94560,color:#e2e2e2
    style OUTPUT fill:#16213e,stroke:#0f3460,color:#e2e2e2
```

### Prompt Processing Pipeline

```mermaid
flowchart LR
    Q["📝 Customer Query"] --> ZS["Zero-Shot Template"]
    Q --> OS["One-Shot Template"]

    ZS --> |"Role + Query"| API1["Ollama API"]
    OS --> |"Role + Example + Query"| API2["Ollama API"]

    API1 --> R1["Response A"]
    API2 --> R2["Response B"]

    R1 --> EVAL["📊 Scoring<br>Relevance • Coherence • Helpfulness"]
    R2 --> EVAL

    EVAL --> LOG["📋 eval/results.md"]

    style Q fill:#6C63FF,stroke:#333,color:#fff
    style ZS fill:#E91E63,stroke:#333,color:#fff
    style OS fill:#00BCD4,stroke:#333,color:#fff
    style EVAL fill:#FF9800,stroke:#333,color:#fff
    style LOG fill:#4CAF50,stroke:#333,color:#fff
```

---

## 📁 Code Structure

```
offline-customer-support-chatbot/
│
├── 📄 chatbot.py                         # Main script — queries Ollama API
│       ├── query_ollama()                # Sends prompts, handles errors
│       ├── load_template()               # Reads prompt templates from disk
│       ├── sanitize_for_markdown_table() # Cleans responses for MD tables
│       └── main()                        # Orchestrates the full pipeline
│
├── 📂 prompts/                           # Prompt engineering templates
│   ├── zero_shot_template.txt            # Instruction-only template
│   └── one_shot_template.txt             # Instruction + one example
│
├── 📂 eval/                              # Evaluation outputs
│   └── results.md                        # Scored results (40 rows)
│
├── 📄 report.md                          # Detailed analysis & findings
├── 📄 architecture.md                    # System architecture documentation
├── 📄 projectdocumentation.md            # Complete project documentation
├── 📄 setup.md                           # Environment setup guide
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .gitignore                         # Git ignore rules
└── 📄 README.md                          # This file
```

---

## 🔄 Workflow

### End-to-End Execution Flow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant S as 📜 chatbot.py
    participant T as 📄 Templates
    participant O as ⚙️ Ollama Server
    participant M as 🧠 Llama 3.2
    participant R as 📊 results.md

    U->>S: python chatbot.py
    S->>T: Load zero_shot_template.txt
    S->>T: Load one_shot_template.txt

    loop For each of 20 queries
        S->>S: Format Zero-Shot prompt
        S->>O: POST /api/generate (Zero-Shot)
        O->>M: Forward prompt
        M->>O: Generated text
        O->>S: JSON response
        S->>R: Log response + empty scores

        S->>S: Format One-Shot prompt
        S->>O: POST /api/generate (One-Shot)
        O->>M: Forward prompt
        M->>O: Generated text
        O->>S: JSON response
        S->>R: Log response + empty scores
    end

    S->>U: "Done! Results saved to eval/results.md"
    U->>R: Manually score all 40 responses
```

### Data Adaptation Pipeline

```mermaid
graph LR
    subgraph SOURCE["📦 Ubuntu Dialogue Corpus"]
        A1["'My wifi driver is not working<br>after the latest update.'"]
        A2["'How do I check the logs<br>for the apache server?'"]
        A3["'I can't change the<br>permissions on the directory.'"]
    end

    subgraph ADAPT["🔄 Manual Adaptation"]
        B["Domain Shift:<br>Technical → E-commerce<br>Intent Preserved"]
    end

    subgraph TARGET["🛍️ Chic Boutique Queries"]
        C1["'How do I track the shipping<br>status of my recent order?'"]
        C2["'My discount code is not<br>working at checkout.'"]
        C3["'Can I change my shipping<br>address after placing an order?'"]
    end

    A1 --> B
    A2 --> B
    A3 --> B
    B --> C1
    B --> C2
    B --> C3

    style SOURCE fill:#E3F2FD,stroke:#1565C0,color:#1565C0
    style ADAPT fill:#FFF3E0,stroke:#E65100,color:#E65100
    style TARGET fill:#E8F5E9,stroke:#2E7D32,color:#2E7D32
```

---

## 📊 Key Findings

### Quantitative Results

| Metric | Zero-Shot Avg | One-Shot Avg | Δ Improvement |
|---|---|---|---|
| 🎯 **Relevance** | 4.50 | 4.90 | **+8.9%** ⬆️ |
| 📝 **Coherence** | 5.00 | 5.00 | 0.0% ➡️ |
| 💡 **Helpfulness** | 4.20 | 4.85 | **+15.5%** ⬆️ |
| ⭐ **Overall** | 4.57 | 4.92 | **+7.7%** ⬆️ |

### Score Distribution

```mermaid
pie title Zero-Shot Relevance Distribution
    "Score 5 (55%)" : 11
    "Score 4 (40%)" : 8
    "Score 3 (5%)" : 1
```

```mermaid
pie title One-Shot Relevance Distribution
    "Score 5 (90%)" : 18
    "Score 4 (10%)" : 2
```

### Key Insight

> **One-Shot prompting** delivers a **+15.5% improvement in Helpfulness** — the most business-critical metric for customer support. The single example acts as a powerful "style guide" that improves tone, format, and actionability.

### Example Comparison

| | Zero-Shot | One-Shot |
|---|---|---|
| **Query** | *"My discount code is not working at checkout."* | *Same query* |
| **Response** | "Please ensure that the code is entered correctly and has not expired. Also, check if the items in your cart are eligible for the discount." | "I'm sorry to hear that! Please double-check the spelling and expiration date. Some codes only apply to specific items. If it still fails, feel free to reach out!" |
| **Score** | R:4 C:5 H:4 | R:5 C:5 H:5 |
| **Analysis** | ❌ Reads like a FAQ entry | ✅ Empathetic, actionable, invites follow-up |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** — [python.org](https://www.python.org/downloads/)
- **Ollama** — [ollama.com](https://ollama.com)
- **~2 GB** free disk space for model weights

### Installation

```bash
# 1. Install Ollama and pull the model
ollama pull llama3.2:3b

# 2. Clone this repository
git clone https://github.com/ramalokeshreddyp/ChicBot.git
cd ChicBot

# 3. Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the Chatbot

```bash
# Ensure Ollama is running
ollama serve

# Execute the chatbot
python chatbot.py
```

### Running Tests

```bash
pytest -q
```

### Expected Output

```
============================================================
  Chic Boutique — Offline Customer Support Chatbot
  Model : llama3.2:3b
  Server: http://localhost:11434/api/generate
  Queries: 20
============================================================

[1/20] "How do I track the shipping status of my recent order?"
  Zero-Shot (3.2s): You can track your order by logging into your account...
  One-Shot  (2.8s): Hi there! You can easily track your order by visiting...

[2/20] "My discount code is not working at checkout."
  ...

============================================================
  Done! 20 queries × 2 methods = 40 responses
  Total time: 124.5s
  Results saved to: eval/results.md
============================================================
```

---

## 🌐 GitHub Pages Deployment

This repository now includes an automated GitHub Pages deployment pipeline.

### What was added

- **Workflow**: `.github/workflows/deploy-pages.yml`
- **Published site entry**: `docs/index.html`

### How deployment works

1. Push to `main` (or manually trigger the workflow from Actions).
2. GitHub Actions publishes the `docs/` folder to the `gh-pages` branch.
3. GitHub Pages serves content from the `gh-pages` branch root.

### One-time repository setup

1. Open your repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Choose **Branch: `gh-pages`** and **Folder: `/ (root)`**.
4. Push your latest commit containing the workflow.

### Site URL format

- `https://<your-username>.github.io/<your-repo-name>/`

The landing page links to key project artifacts: `README.md`, `architecture.md`, `projectdocumentation.md`, and `report.md`.

---

## 📚 Documentation

| Document | Description |
|---|---|
| 📖 [**report.md**](report.md) | Detailed analysis comparing Zero-Shot vs. One-Shot prompting |
| 🏗️ [**architecture.md**](architecture.md) | System architecture, design decisions, and component details |
| 📋 [**projectdocumentation.md**](projectdocumentation.md) | Complete project documentation covering all aspects |
| ⚙️ [**setup.md**](setup.md) | Step-by-step environment setup with troubleshooting |
| 📊 [**eval/results.md**](eval/results.md) | Full evaluation results with scores for all 40 responses |

---

## ⚠️ Limitations & Future Work

| Limitation | Proposed Solution |
|---|---|
| No real-time data access | Implement **RAG** with vector database (ChromaDB/FAISS) |
| Potential hallucinations | Add **output guardrails** and fact-checking layers |
| Single-turn only | Implement **conversation history** management |
| CPU-bound inference (~5s) | Deploy on **GPU hardware** for sub-second latency |
| No knowledge base | **Fine-tune** model on actual company policies |

---

<p align="center">
  <strong>Built with ❤️ for privacy-first AI</strong><br>
  <em>Llama 3.2 × Ollama × Python</em>
</p>
