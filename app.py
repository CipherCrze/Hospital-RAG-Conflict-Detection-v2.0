"""
Hospital RAG - Conflict Detection Q&A System
Entrypoint for the FastAPI / HTML Web App
"""
import uvicorn
import os

if __name__ == "__main__":
    print("[INFO] Starting Hospital Management System API & Frontend on port 8080...")
    print("[INFO] Streamlit has been disabled. The custom HTML UI is being served at http://localhost:8080")
    
    # We run the FastAPI app defined in backend/main.py
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8080, reload=True)
