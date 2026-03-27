# Inventory Management Agent

An autonomous AI agent that manages warehouse inventory using natural language.
Built with LangChain, Groq LLM, ChromaDB, and Streamlit.

## Architecture
```
User (Streamlit UI)
       │
       ▼
LangChain Agent (Groq Llama 3)
       │
  ┌────┴─────┐──────────────┐
  ▼          ▼              ▼
Tools      RAG Pipeline   Memory
(SQL)    (ChromaDB)    (Chat History)
  │          │
  ▼          ▼
SQLite    Sentence
Database  Transformers
```

## Features
- Natural language to SQL query translation
- Semantic product search using vector embeddings
- Real-time stock level checking and updates
- Automated low stock alerts
- Inventory report generation
- Conversation memory across queries

## Tech Stack
| Component | Technology |
|-----------|-----------|
| LLM | Groq Llama 3 8B (free) |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Framework | LangChain |
| Database | SQLite |
| UI | Streamlit |
| Container | Docker Compose |

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/aryan999444/inventory-agent.git
cd inventory-agent
```

### 2. Create virtual environment
```bash
uv python -m venv venv
.venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 5. Initialize the database and vector store
```bash
uv python data/seed.py
uv python data/ingest.py
```

### 6. Run the app
```bash
uv streamlit run app/main.py
```

### 7. Run with Docker
```bash
docker-compose up --build
```

## Design Choices

### Why Groq + Llama 3?
Free, fast inference (300+ tokens/sec), no GPU required, and excellent
tool-calling capability out of the box.

### Why ChromaDB?
Lightweight, easy to Dockerize, persistent storage, and perfect for
semantic product search at warehouse scale.

### Why SQLite?
Zero configuration, single file database, perfect for demo and
small-to-medium warehouse deployments. Can be swapped for PostgreSQL
in production.

### Why Prompt Engineering over LoRA fine-tuning?
No GPU required, faster iteration, and equally effective for
structured tool-calling tasks. The system prompt was iteratively
refined to enforce strict tool use and consistent output format.

## Sample Queries
- "Do we have any 220V power supplies?"
- "Generate a full inventory report"
- "Add 50 units of safety helmets"
- "What products need reordering?"
- "Find heavy duty tools under $200"

## Fine-tuning Approach
See `finetuning/finetune_notes.md` for full details on the prompt
engineering methodology used as the fine-tuning technique.

## Test Cases

### 1. Semantic Search (RAG)
**Query:** `do we have any heavy duty equipment compatible with 220V?`
**Expected:** Returns Heavy Duty Power Supply 220V, Industrial Motor 5HP, Industrial Fan 36inch

**Query:** `find me chemical resistant safety gear`
**Expected:** Returns Safety Gloves (chemical resistant), Safety Helmet

---

### 2. Check Stock
**Query:** `how many fire extinguishers do we have?`
**Expected:** Fire Extinguisher CO2 - 30 units, Status: OK

**Query:** `check stock for forklift battery`
**Expected:** Forklift Battery 48V - 6 units, Status: LOW STOCK - REORDER NEEDED

---

### 3. Low Stock & Reorder Alerts
**Query:** `which products need to be reordered?`
**Expected:** Full inventory report highlighting items at or below reorder level

**Query:** `generate a full inventory report`
**Expected:** Total products, inventory value, stock by category, low stock alerts

---

### 4. Update Inventory
**Query:** `add 20 units of safety helmets`
**Expected:** Previous: 200, New: 220 units, Status: OK

**Query:** `remove 5 units of hydraulic jack`
**Expected:** Previous: 15, New: 10 units, Status: OK

---

### 5. Edge Cases
**Query:** `do we have any laptops?`
**Expected:** No product found, suggests using semantic search

**Query:** `remove 1000 units of safety helmets`
**Expected:** Cannot update — would result in negative stock

---

### 6. Conversation Memory
**Query 1:** `how many conveyor belts do we have?`
**Expected:** Conveyor Belt 10m - 3 units, LOW STOCK

**Query 2 (follow-up):** `add 10 more of those`
**Expected:** Agent remembers context, updates Conveyor Belt stock from 3 to 13
