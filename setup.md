# Setup Instructions

This guide explains how to set up and run the Offline Customer Support Chatbot project on your local machine.

## Prerequisites

- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **Ollama** — [Download Ollama](https://ollama.com)
- ~2 GB free disk space (for the Llama 3.2 model weights)

---

## Step 1: Install Ollama and Pull the Model

1. Download and install Ollama for your operating system from [ollama.com](https://ollama.com).

2. Verify the installation:
   ```bash
   ollama --version
   ```

3. Pull the Llama 3.2 3B model (~2 GB download):
   ```bash
   ollama pull llama3.2:3b
   ```

4. *(Optional)* Test the model interactively:
   ```bash
   ollama run llama3.2:3b
   ```
   Type a message and press Enter. Type `/bye` to exit.

## Step 2: Set Up the Python Environment

1. Clone this repository (or navigate to the project directory):
   ```bash
   git clone https://github.com/ramalokeshreddyp/ChicBot.git
   cd ChicBot
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create
   python -m venv venv

   # Activate (Windows)
   venv\Scripts\activate

   # Activate (macOS / Linux)
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `requests` — HTTP client for the Ollama REST API
   - `datasets` — Hugging Face library for loading the Ubuntu Dialogue Corpus

## Step 3: Run the Chatbot

1. Make sure the Ollama server is running. On Windows/macOS, it starts automatically when the app is launched. On Linux:
   ```bash
   ollama serve
   ```

2. Run the chatbot script:
   ```bash
   python chatbot.py
   ```

3. The script will:
   - Process all 20 queries through both Zero-Shot and One-Shot templates
   - Display progress and timing for each query
   - Save results to `eval/results.md`

## Step 4: Evaluate the Results

1. Open `eval/results.md` in a markdown viewer or text editor.
2. Review each response and assign scores (1–5) for:
   - **Relevance**: How well does the response address the query?
   - **Coherence**: Is the response grammatically correct and clear?
   - **Helpfulness**: Does the response provide an actionable answer?
3. Summarize your findings in `report.md`.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ConnectionError: Connection refused` | Ensure Ollama is running (`ollama serve` or open the Ollama app) |
| `Model not found` | Run `ollama pull llama3.2:3b` to download the model |
| Slow responses (>10s) | Normal for CPU-only inference. GPU acceleration significantly improves speed |
| `pip install` fails | Ensure you've activated the virtual environment first |
| `ModuleNotFoundError: requests` | Run `pip install -r requirements.txt` inside the activated venv |
