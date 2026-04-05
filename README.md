# AI Legal Assistant using RAG

AI-powered chatbot that answers legal questions using Retrieval-Augmented Generation (RAG).

## Features

- Answers legal queries using IPC, CRPC, Constitution datasets
- Uses Contract Law PDF for additional knowledge
- Semantic search using sentence-transformers
- Vector database using ChromaDB
- Backend built with FastAPI
- Frontend chat interface using React
- AI responses generated using Google Gemini API

## Tech Stack

Python
FastAPI
React
Gemini API
Sentence Transformers
ChromaDB
SQLite

## Architecture

User Query → Vector Search → Retrieve Legal Context → Gemini → Response