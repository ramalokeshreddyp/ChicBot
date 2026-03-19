# 🛒 Chic Boutique — Offline Customer Support Chatbot

> A privacy-first, offline customer support chatbot powered by **Ollama** and **Meta's Llama 3.2 (3B)** for a fictional e-commerce store.

---

## 📋 Project Overview

This project demonstrates how to build a fully **offline**, **privacy-compliant** customer support chatbot. By running the LLM entirely on local hardware via [Ollama](https://ollama.com), no customer data ever leaves the company's network — making it suitable for organizations subject to **GDPR**, **CCPA**, or **DPDP Act** regulations.

The chatbot processes 20 e-commerce customer queries (adapted from the **Ubuntu Dialogue Corpus**) using two prompting strategies and evaluates their relative effectiveness.

## 🏗️ Architecture

```
┌─────────────────────┐
│   chatbot.py        │  1. Load query + template
│   (Python Script)   │──────────────────────────┐
└─────────────────────┘                          │
                                                 ▼
                                    ┌────────────────────────┐
                                    │  HTTP POST Request     │
                                    │  localhost:11434       │
                                    └────────────┬───────────┘
                                                 │
                                                 ▼
                                    ┌────────────────────────┐
                                    │  Ollama Server         │
                                    │  + Llama 3.2 (3B)     │
                                    └────────────┬───────────┘
                                                 │
                                                 ▼
                                    ┌────────────────────────┐
                                    │  JSON Response         │
                                    └────────────┬───────────┘
                                                 │
                                                 ▼
                                    ┌────────────────────────┐
                                    │  eval/results.md       │
                                    │  (Logged + Scored)     │
                                    └────────────────────────┘
```

## 🔬 Methodology

1. **Data Sourcing**: 20 technical queries from the [Ubuntu Dialogue Corpus](https://huggingface.co/datasets/rguo12/ubuntu_dialogue_corpus) were adapted into e-commerce scenarios.
2. **Prompting**: Each query was processed twice:
   - **Zero-Shot** — Instruction only, no examples
   - **One-Shot** — Instruction + one example Q&A pair
3. **Scoring**: All 40 responses were manually scored on **Relevance**, **Coherence**, and **Helpfulness** (1–5 scale).

## 📊 Key Findings

| Metric | Zero-Shot Avg | One-Shot Avg | Improvement |
|---|---|---|---|
| Relevance | 4.50 | 4.90 | **+8.9%** |
| Coherence | 5.00 | 5.00 | 0.0% |
| Helpfulness | 4.20 | 4.85 | **+15.5%** |

**One-Shot prompting** consistently outperformed Zero-Shot, especially in tone and helpfulness. The single example acted as a powerful "style guide" for the model. See [`report.md`](report.md) for the full analysis.

## 📁 Repository Structure

```
offline-customer-support-chatbot/
├── chatbot.py                        # Main script — queries Ollama API
├── prompts/
│   ├── zero_shot_template.txt        # Zero-shot prompt template
│   └── one_shot_template.txt         # One-shot prompt template
├── eval/
│   └── results.md                    # Scored results for all 40 responses
├── report.md                         # Detailed analysis and findings
├── setup.md                          # Environment setup instructions
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## 🚀 Quick Start

```bash
# 1. Install Ollama (https://ollama.com) and pull the model
ollama pull llama3.2:3b

# 2. Clone this repository
git clone https://github.com/ramalokeshreddyp/ChicBot.git
cd ChicBot

# 3. Set up Python environment
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the chatbot
python chatbot.py
```

Results will be saved to `eval/results.md`. See [`setup.md`](setup.md) for detailed instructions.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Meta Llama 3.2 (3B parameters) |
| Model Server | Ollama (local REST API) |
| Language | Python 3.8+ |
| HTTP Client | `requests` library |
| Data Source | Ubuntu Dialogue Corpus (Hugging Face) |

## 📝 License

This project is for educational purposes as part of a course assignment.
