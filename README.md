# Intelligent Document Routing System

## Project Overview

This project implements a **multi-agent AI system** that functions like a smart receptionist for business document handling. It receives documents in PDF, JSON, or Email formats, intelligently classifies them by format and business intent (e.g., RFQ, Invoice, Complaint), routes them to specialized agents, and logs the entire process for traceability.

> Built for real-world automation of document intake, classification, and processing workflows.

---

## System Components

### 1. **Classifier Agent**
- Detects file format (PDF / JSON / Email)
- Infers business intent using LLMs
- Routes to correct specialist agent
- Logs interactions in shared memory

### 2. **JSON Agent**
- Validates structured JSON payloads
- Extracts and reformats data to a target schema
- Flags missing fields or anomalies
- Stores results in memory

### 3. **Email Agent**
- Processes email text
- Extracts sender, urgency, and intent
- Prepares CRM-ready structured data
- Stores communication context and metadata

### 4. **Shared Memory Module**
- Stores all extracted metadata, document history, and agent outputs
- Supports Redis, SQLite, or JSON-based storage
- Enables context chaining and audit trails

---

## Project Structure
```
multi_agent_doc_system/
├── agents/
│   ├── __init__.py
│   ├── classifier_agent.py        # Detects file type + intent, routes docs
│   ├── json_agent.py              # Handles structured JSON
│   └── email_agent.py             # Processes email text (sender, urgency, etc.)
│
├── memory/
│   ├── __init__.py
│   ├── memory_manager.py          # Handles reading/writing shared memory
│   └── memory_store.json          # JSON-based memory (can upgrade to Redis/SQLite)
│
├── utils/
│   ├── __init__.py
│   └── file_loader.py             # Reads PDF, JSON, or plain text input
│
├── data/
│   ├── input/                     # Uploaded documents
│   └── output/                    # Extracted info, routing logs, audit trails
│
├── examples/                      # Ready-to-use input files for testing
│   ├── sample_email.txt
│   ├── sample_invoice.json
│   └── sample_complaint.pdf
│
├── tests/
│   └── test_agents.py             # Unit tests for each agent
│
├── streamlit_app.py              # 🎯 Streamlit-based frontend interface
├── main.py                       # Optional: CLI-based orchestrator
├── requirements.txt              # Python + Streamlit + LLM dependencies
└── README.md                     # Full project documentation

```

#### Set Up Virtual Environment
Choose the appropriate command based on your operating system:

#### For Linux
```bash
python -m venv venv
source venv/bin/activate
```

#### For Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start the Application:
    ```bash
    streamlit run streamlit_app.py
    OR
    streamlit run streamlit_app.py --global.developmentMode=false
    ```
