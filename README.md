e# Samarth AI  
### A Smart Chatbot for Government Scheme Assistance  

<img src="https://img.shields.io/badge/Team-Xeno-blue" alt="Team Badge">  
<img src="https://img.shields.io/badge/Project-Chatbot%20for%20Government%20Schemes-green" alt="Project Badge">  

## Team Name  
**Xeno**  

## Problem Statement  
Chatbot for suggesting government schemes and financial aid  

## Project Description  
Samarth AI is an intelligent chatbot that helps users discover relevant government schemes and financial aid programs using **Retrieval-Augmented Generation (RAG)**. The system:

1. Uses **IBM watsonx.ai's IBM_SLATE_30M_ENG** model to generate embeddings of scheme data
2. Stores vectors in **FAISS** for efficient similarity search
3. Retrieves relevant schemes based on user queries (e.g., "Educational support for girls")
4. Generates natural language responses using **Granite-13b-instruct-v2** LLM

## Technologies Used  
| Component          | Technology Stack              |
|--------------------|-------------------------------|
| **Embeddings**     | IBM watsonx.ai (SLATE-30M-ENG)|
| **Vector Store**   | FAISS                         |
| **LLM**           | Granite-13b-instruct-v2       |
| **Backend**       | Flask                         |
| **Frontend**      | React.js                      |
| **Data Storage**  | JSON                          |

## Setup & Installation

### Prerequisites
- Python ≥ 3.8
- Node.js ≥ 16.x
- IBM watsonx.ai API credentials

### Backend Setup
```bash
# Clone repository
git clone https://github.com/SarthakArora7/xeno-Samarth.git

# Install dependencies
pip install -r requirements.txt

# Configure environment
IBM_API_KEY = "YOUR_API_KEY"
PROJECT_ID = "YOUR_PROJECT_ID"
IBM_URL = "YOUR_REGION_IBM_CLOUD_URL"
# Edit .env with your credentials

# Run Flask server
cd backend.py
python app.py

```
### Frontend Setup Guide (Vite + React)

## Prerequisites
- Node.js ≥ 16.14.0
- npm ≥ 8.5.0 or yarn ≥ 1.22.0
- Backend server running (Flask API)

## Installation
```bash
# Clone repository (if not already done)
git clone https://github.com/SarthakArora7/xeno-Samarth.git
cd frontend

# Install dependencies
npm install
or
npm i

# Run React Server
npm run dev

```
## Video
### Drive Link: https://drive.google.com/file/d/1uFkST2Ywc6lxUA54Woko5gBqQT27306C/view?usp=sharing 
