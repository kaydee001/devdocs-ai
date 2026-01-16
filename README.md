
# DevDocs AI 🤖

A production-grade AI system that analyzes Python code, generates high-quality documentation, and evaluates its quality with actionable feedback.

**🚀 [Try Live Demo](https://devdocs-ai-jjof.onrender.com/docs)**

---

## 🎯 What It Does

Upload Python code or a `.py` file and get:
- A structured project-style README  
- Clear documentation of functions and logic  
- A quality score (0–100)  
- Concrete suggestions to improve code documentation  

**Example Flow:**
```
User uploads .py file
System parses code using AST (no execution)
System analyzes structure + semantics
System generates documentation via LLM
System evaluates quality across 6 dimensions
System returns docs + score + suggestions

```

---

## ✨ Features

✅ **AST-Based Code Analysis** – Safe parsing without executing code  
✅ **AI Documentation Generator** – README-style output using Groq + Llama 3.3  
✅ **Quality Scoring Engine** – 0–100 score with detailed feedback  
✅ **File Upload Support** – Upload `.py` files directly  
✅ **REST API** – Built with FastAPI + interactive Swagger docs  
✅ **Production Architecture** – Modular, typed, validated, and deployable  

---

## 🏗️ Architecture Overview

The system is structured into clean, single-responsibility modules:

- Code Parser (`code_parser.py`) – AST-based structural code analysis  
- LLM Service (`llm_service.py`) – Handles prompting and Groq API interaction  
- Quality Scorer (`quality_scorer.py`) – Evaluates documentation quality  
- Analysis Service (`analysis_service.py`) – Orchestrates full pipeline  
- Schemas (`responses.py`) – Type-safe API contracts using Pydantic  
- API Layer (`main.py`) – FastAPI app and routing  

---

### Data Flow

```

User Uploads Code
↓
🧠 AST Parser (structure extraction)
↓
📋 Analysis Service (orchestration)
↓
🤖 LLM Service (documentation generation)
↓
⭐ Quality Scorer (0–100 evaluation)
↓
✅ Final Output: Docs + Score + Suggestions

````

---

## 🛠️ Tech Stack

- Python 3.12  
- FastAPI  
- Groq API (Llama 3.3 70B)  
- Pydantic  
- Python AST  
- Uvicorn  
- Render (deployment)

---

## 📊 Quality Scoring System

Documentation is evaluated across 6 weighted dimensions:

| Category        | Weight | What It Evaluates |
|----------------|--------|-------------------|
| Code Quality    | 20%    | Docstrings, type hints in source |
| Completeness    | 20%    | All functions/classes covered |
| Structure       | 15%    | README sections present |
| Examples        | 15%    | Practical usage examples |
| Clarity          | 15%    | Readability and explanation |
| Coverage         | 15%    | Params, returns, behavior documented |

**Grades:**  
A (90–100) • B (80–89) • C (70–79) • D (60–69) • F (<60)

---

## 🧪 Example Usage

### API Request
```bash
curl -X POST "https://devdocs-ai-jjof.onrender.com/analyze" \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a: int, b: int) -> int:\n    return a + b"}'
````

### Python Client

```python
import requests

response = requests.post(
    "https://devdocs-ai-jjof.onrender.com/analyze",
    json={"code": "def greet(name): return f'Hello {name}'"}
)

print(response.json())
```

---

## 📡 API Endpoints

* `POST /analyze` – Analyze raw Python code
* `POST /analyze/file` – Upload and analyze `.py` file
* `GET /health` – Health check endpoint

**Validation Rules:**

* `.py` files only
* Max size: 1MB
* UTF-8 encoding
* Proper HTTP errors (400, 413, 500)

---
## 🔗 Links

* **Live API:** [https://devdocs-ai-jjof.onrender.com](https://devdocs-ai-jjof.onrender.com)

---

**Built as part of my applied AI engineering journey 🚀**


