import os, requests
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from retrieval import WasteRetriever

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
retriever = WasteRetriever(ROOT / "data" / "waste_knowledge.json")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/ask", methods=["POST"])
def ask():
    question = ((request.get_json(silent=True) or {}).get("question") or "").strip()
    if not question:
        return jsonify({"error":"Please enter a waste item or question."}), 400
    docs = retriever.search(question, 3)
    if not docs:
        return jsonify({"answer":"I could not find a close match in the included knowledge base. Please check your local municipal waste-segregation instructions. Do not guess for batteries, chemicals, medicines or electronic waste.","mode":"No confident dataset match","sources":[]})
    context = "\\n\\n".join([f"Item: {d['item']}\\nCategory: {d['category']}\\nGuidance: {d['guidance']}\\nSource: {d['source']}" for d in docs])
    prompt = ("You are EcoGuide AI, an educational waste-segregation assistant for India. "
      "Use only the retrieved context. Explain the likely category and safe disposal steps in simple English. "
      "Local municipal rules can differ, so say users must verify local instructions. "
      "Do not invent recycling facilities, collection schedules or legal requirements. "
      "For batteries, e-waste, medicines and chemicals, emphasise special/authorised collection.\\n\\n"
      f"RETRIEVED CONTEXT:\\n{context}\\n\\nUSER QUESTION: {question}\\n\\nAnswer concisely.")
    try:
        response = requests.post(OLLAMA_URL, json={"model":OLLAMA_MODEL,"prompt":prompt,"stream":False}, timeout=120)
        response.raise_for_status()
        answer = response.json().get("response","").strip()
        if not answer: raise RuntimeError("Empty model response")
        mode = "Ollama LLM + RAG"
    except Exception:
        best=docs[0]
        answer=("Ollama is not connected. This is a retrieved dataset response, not an LLM-generated answer.\\n\\n"
                f"Suggested category: {best['category']}\\n{best['guidance']}")
        mode="Knowledge-base fallback"
    return jsonify({"answer":answer,"mode":mode,"matches":[{"item":d["item"],"category":d["category"],"score":round(d["score"],3),"source":d["source"]} for d in docs]})

@app.route("/api/health")
def health():
    return jsonify({"status":"ok","dataset_records":len(retriever.records),"model":OLLAMA_MODEL})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
