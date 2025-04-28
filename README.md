📈 Personal Investment Advice Chatbot using GenAI
A Generative AI based chatbot that provides personalized financial investment advice, combining machine learning predictions, vector search, and large language models.

✨ Features
💬 Conversational UI built with Streamlit.
🧠 GenAI Responses powered by Ollama Mistral model.
📈 Expected Returns Prediction using XGBoost ML algorithm.
🔍 Vector Embeddings to find similar user queries for better context.
🚀 FastAPI Backend for API management and orchestration.
🛡️ Privacy Focused — No sensitive user data stored unnecessarily.

🛠️ Tech Stack
Frontend --> Streamlit
Backend -->	FastAPI
GenAI Model -->	Ollama (Mistral)
Machine Learning -->	XGBoost
Vector Search	Vector embedding --> Sentence Transformers
Language -->	Python

📦 Installation
1. Install Python dependencies:
   pip install -r requirements.txt
2. Start the backend server (FastAPI):
   uvicorn app:app --reload --port 8001
3. Start the frontend UI (Streamlit):
   streamlit run UI/streamlite_ui.py

🧠 How It Works
User interacts via Streamlit UI — inputs their investment details or queries.
FastAPI receives and processes the input.
Vector embeddings search for similar historical queries for better context.
XGBoost model predicts the expected return percentage based on user profile (age, income, risk appetite, etc.).
All collected information is fed into the prompt given to the Mistral model via Ollama.
Mistral model generates and returns personalized investment advice.
