"""
Offline Customer Support Chatbot for Chic Boutique
===================================================
This script queries a locally-hosted Llama 3.2 (3B) model via Ollama's REST API
to generate customer support responses using two prompting strategies:
  - Zero-Shot  (instruction only, no examples)
  - One-Shot   (instruction + one example)

All 20 customer queries were adapted from the Ubuntu Dialogue Corpus
(rguo12/ubuntu_dialogue_corpus) to fit an e-commerce context.

Usage:
    1. Ensure Ollama is running:  ollama serve
    2. Pull the model:            ollama pull llama3.2:3b
    3. Run this script:           python chatbot.py
"""

import requests
import json
import os
import time

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

# ---------------------------------------------------------------------------
# Data Preparation
# ---------------------------------------------------------------------------
# The queries below were sourced from the Ubuntu Dialogue Corpus and manually
# adapted to an e-commerce (Chic Boutique) context.
#
# To explore the original corpus yourself:
#
#   from datasets import load_dataset
#   dataset = load_dataset("rguo12/ubuntu_dialogue_corpus", "v2.0")
#   train_data = dataset['train']
#   for i in range(5):
#       print(train_data[i])
#
# Mapping of original Ubuntu queries → adapted e-commerce queries:
#  1. "My wifi driver is not working after the latest update."
#     → "How do I track the shipping status of my recent order?"
#  2. "How do I check the logs for the apache server?"
#     → "My discount code is not working at checkout."
#  3. "I can't change the permissions on the directory."
#     → "Can I change my shipping address after placing an order?"
#  4. "What's the best way to set up a VPN on Ubuntu?"
#     → "What is your policy on international shipping?"
#  5. "My package manager isn't updating correctly."
#     → "I received a damaged item, how do I get a replacement?"
#  6. "How do I reset my root password?"
#     → "How do I reset my account password?"
#  7. "Can I customize the appearance of my desktop?"
#     → "Do you offer gift wrapping services?"
#  8. "How can I stop a background service from running?"
#     → "How can I cancel my subscription?"
#  9. "What file system types does Ubuntu support?"
#     → "What payment methods do you accept?"
# 10. "Is there a GUI version of the tool?"
#     → "Is there a physical store I can visit?"
# 11. "How do I use my SSH key to log in?"
#     → "How do I use my store credit?"
# 12. "Can I merge two partitions into one?"
#     → "Can I combine two separate orders into one shipment?"
# 13. "The update says complete but nothing has changed."
#     → "What should I do if my package is marked as delivered but I haven't received it?"
# 14. "Is this software open source?"
#     → "Are your products ethically sourced?"
# 15. "How do I remove myself from the mailing list?"
#     → "How do I unsubscribe from your newsletter?"
# 16. "Where can I find the documentation for this library?"
#     → "Do you have a size guide for your clothing?"
# 17. "Can I reserve a copy of the next release?"
#     → "Can I pre-order upcoming items?"
# 18. "How do I reach a developer on IRC?"
#     → "How do I contact customer support via phone?"
# 19. "What happens if a dependency is no longer maintained?"
#     → "What happens if an item I ordered is out of stock?"
# 20. "Do you offer volume licensing for enterprises?"
#     → "Do you offer wholesale pricing for bulk orders?"

QUERIES = [
    "How do I track the shipping status of my recent order?",
    "My discount code is not working at checkout.",
    "Can I change my shipping address after placing an order?",
    "What is your policy on international shipping?",
    "I received a damaged item, how do I get a replacement?",
    "How do I reset my account password?",
    "Do you offer gift wrapping services?",
    "How can I cancel my subscription?",
    "What payment methods do you accept?",
    "Is there a physical store I can visit?",
    "How do I use my store credit?",
    "Can I combine two separate orders into one shipment?",
    "What should I do if my package is marked as delivered but I haven't received it?",
    "Are your products ethically sourced?",
    "How do I unsubscribe from your newsletter?",
    "Do you have a size guide for your clothing?",
    "Can I pre-order upcoming items?",
    "How do I contact customer support via phone?",
    "What happens if an item I ordered is out of stock?",
    "Do you offer wholesale pricing for bulk orders?",
]


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def query_ollama(prompt: str) -> str:
    """
    Sends a prompt to the local Ollama server and returns the model response.

    Args:
        prompt: The fully-formatted prompt string.

    Returns:
        The model's generated text, or an error message on failure.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,  # We want the full response at once
    }
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=120)
        response.raise_for_status()
        return json.loads(response.text).get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print("  ✗ Connection refused — is Ollama running? (ollama serve)")
        return "Error: Could not connect to the Ollama server."
    except requests.exceptions.Timeout:
        print("  ✗ Request timed out after 120 seconds.")
        return "Error: Request timed out."
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error querying Ollama: {e}")
        return "Error: Could not get a response from the model."


def load_template(filepath: str) -> str:
    """Reads a prompt template from disk."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def sanitize_for_markdown_table(text: str) -> str:
    """
    Cleans a response string so it can safely be inserted into a single
    markdown table cell (no pipes, no newlines).
    """
    text = text.replace("|", "\\|")
    text = text.replace("\n", " ")
    text = text.replace("\r", "")
    # Collapse multiple spaces
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # Load prompt templates
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        zero_shot_tmpl = load_template(
            os.path.join(script_dir, "prompts", "zero_shot_template.txt")
        )
        one_shot_tmpl = load_template(
            os.path.join(script_dir, "prompts", "one_shot_template.txt")
        )
    except FileNotFoundError as e:
        print(f"Error: Prompt template not found — {e}")
        return

    # Ensure eval/ directory exists
    eval_dir = os.path.join(script_dir, "eval")
    os.makedirs(eval_dir, exist_ok=True)

    results_path = os.path.join(eval_dir, "results.md")

    print("=" * 60)
    print("  Chic Boutique — Offline Customer Support Chatbot")
    print(f"  Model : {MODEL_NAME}")
    print(f"  Server: {OLLAMA_ENDPOINT}")
    print(f"  Queries: {len(QUERIES)}")
    print("=" * 60)

    with open(results_path, "w", encoding="utf-8") as f:
        # Write header
        f.write("# Evaluation Results\n\n")
        f.write("## Scoring Rubric\n\n")
        f.write(
            "- **Relevance (1-5)**: How well does the response address "
            "the customer's query? (1 = Irrelevant, 5 = Perfectly relevant)\n"
        )
        f.write(
            "- **Coherence (1-5)**: Is the response grammatically correct "
            "and easy to understand? (1 = Incoherent, 5 = Flawless)\n"
        )
        f.write(
            "- **Helpfulness (1-5)**: Does the response provide a useful, "
            "actionable answer? (1 = Not helpful, 5 = Very helpful)\n\n"
        )

        # Table header
        f.write(
            "| Query # | Customer Query | Prompting Method | Response "
            "| Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |\n"
        )
        f.write("|---|---|---|---|---|---|---|\n")

        total_start = time.time()

        for idx, query in enumerate(QUERIES, start=1):
            print(f"\n[{idx}/{len(QUERIES)}] \"{query}\"")

            # ---- Zero-Shot ----
            zs_prompt = zero_shot_tmpl.replace("{query}", query)
            t0 = time.time()
            zs_response = query_ollama(zs_prompt)
            zs_time = time.time() - t0
            zs_clean = sanitize_for_markdown_table(zs_response)
            print(f"  Zero-Shot ({zs_time:.1f}s): {zs_clean[:80]}...")
            f.write(
                f'| {idx} | "{query}" | Zero-Shot | {zs_clean} '
                f"| | | |\n"
            )

            # ---- One-Shot ----
            os_prompt = one_shot_tmpl.replace("{query}", query)
            t0 = time.time()
            os_response = query_ollama(os_prompt)
            os_time = time.time() - t0
            os_clean = sanitize_for_markdown_table(os_response)
            print(f"  One-Shot  ({os_time:.1f}s): {os_clean[:80]}...")
            f.write(
                f'| {idx} | "{query}" | One-Shot | {os_clean} '
                f"| | | |\n"
            )

        total_elapsed = time.time() - total_start
        print(f"\n{'=' * 60}")
        print(f"  Done! {len(QUERIES)} queries × 2 methods = {len(QUERIES)*2} responses")
        print(f"  Total time: {total_elapsed:.1f}s")
        print(f"  Results saved to: {results_path}")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
