# ⚖️ DRISHTI: Predictive Justice & Case Resolution Engine

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge)
![XGBoost](https://img.shields.io/badge/XGBoost-blue?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)

**DRISHTI** (Vision) is an intelligent backend engine designed to streamline the Indian judicial process. By leveraging statistical modeling and RAG (Retrieval-Augmented Generation), it predicts case timelines, suggests resolution pathways, and retrieves high-context precedents.

---

## 🚀 Key Features

* **⏱️ Timeline Prediction:** Uses **XGBoost** models trained on historical data to estimate case duration.
* **🧠 Intelligent RAG:** Orchestrates **Groq LLMs** and **Pinecone** to provide context-aware legal summaries.
* **🔍 Precedent Search:** Real-time integration with the **Indian Kanoon API** for surfacing relevant case law.
* **⚡ High Performance:** Built on **FastAPI** with **SQLAlchemy (Async)** and **Redis** caching for low-latency responses.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | FastAPI, Pydantic, SQLAlchemy (Async) |
| **AI/ML** | XGBoost, Pandas, Joblib, Groq (Llama 3) |
| **Vector DB** | Pinecone |
| **Database** | PostgreSQL |
| **Caching** | Redis |
| **Search** | Indian Kanoon API |

---

## 🏁 Getting Started

### 1. Clone & Environment
```bash
git clone [https://github.com/yourusername/drishti.git](https://github.com/yourusername/drishti.git)
cd drishti
