# 🛡️ CyberIntel-SLM: RAG-Augmented Multilingual Threat Intelligence

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![Model](https://img.shields.io/badge/Model-Qwen_2.5_1.5B-purple.svg)

## 📌 Project Overview
CyberIntel-SLM is an end to end, multilingual Small Language Model (SLM) pipeline designed to ingest, classify, and route chaotic cyber threat intelligence. 

Real-world security data sourced from Telegram, Twitter, and hacker forums, is notoriously noisy, often blurring the lines between colloquial internet slang, benign IT support requests, and active malicious threats. This project abandons static text classification in favor of a **Retrieval Augmented Generation (RAG) Multi-Agent Consensus Architecture** to prioritize pipeline safety and minimize catastrophic false negatives.

## 🏗️ System Architecture

The pipeline processes incoming text (English, Russian, Bengali, Hindi) through three distinct engineering phases:

1. **Representation Learning (SFT):** The base `Qwen-2.5 1.5B-Instruct` model was fine-tuned using 4-bit quantization and LoRA adapters on a highly stratified subset of 1,000 rows. This forced the model to adapt to domain-specific syntax and slang.
2. **Dynamic Boundary Injection (RAG):** Instead of static few-shot prompting, the system uses a Scikit-Learn `TfidfVectorizer` (Character N-Grams) and a K-Nearest Neighbors (KNN) database. It retrieves the exact mathematical precedent from a curated "Golden Set" and injects it into the prompt context at inference time.
3. **Multi-Agent Consensus (ChainPoll):** The generated context is passed to three distinct AI Personas (Threat Analyst, Support Tech, AI Auditor). 
4. **Confidence Routing:** A strict programmatic threshold requires unanimous agent consensus. Split decisions are automatically escalated to human analysts, preventing the model from hallucinating on contradictory data.

## 📊 Performance Metrics & The "Data Singularity"

Evaluating the pipeline on a strictly unseen, zero-leakage test set revealed critical insights into open-source dataset reliability. 

| Metric | Score | Description |
|--------|-------|-------------|
| **Zero-Shot Baseline** | **32.00%** | The base model's performance on the raw, noisy dataset. |
| **SFT Unseen Accuracy** | **55.00%** | Performance after LoRA fine-tuning (17% absolute increase). |
| **RAG Auto-Resolve Accuracy** | **59.26%** | Accuracy of the final pipeline on high confidence consensus votes. |
| **Human Escalation Rate** | **46.00%** | The percentage of data the system refused to guess on due to split agent votes. |
| **High-Confidence System Accuracy** | **60.00%** | The hard performance ceiling (59.26%) on auto resolved, unanimous  consensus votes. |

### 🛠️ Engineering Verdict
While tutorial datasets often boast 90%+ accuracy, this pipeline hit a hard 60% ceiling. Diagnostic error analysis (`Pred: 2 | Act: 1`) revealed that the underlying Kaggle dataset was fundamentally contradictory, frequently mislabeling identical IT Support requests as Malicious threats. 

Instead of forcing the model to overfit to bad data, the **Confidence Router** successfully identified the data's ambiguity, refusing to guess on 46% of the queue. This architecture reduces human analyst workload by over half (54%) while maintaining a strict safety margin against false negatives, a critical requirement for production geopolitical intelligence pipelines. 


## 🚀 Quick Start

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Download the Kaggle Dataset**
*(Note: Requires a valid `kaggle.json` API token)*
```bash
python data/download_kaggle.py
```

**3. Run the Evaluation Pipeline**
```bash
python src/consensus_router.py
```
