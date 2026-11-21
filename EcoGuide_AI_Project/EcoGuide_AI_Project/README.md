# EcoGuide AI
An Intelligent Waste Segregation and Recycling Assistant Using RAG and LLMs.

## Features
- Included 20-record JSON and CSV waste guidance dataset.
- TF-IDF + cosine similarity retrieval.
- Optional local Llama 3.2 3B generation through Ollama.
- Flask web interface with source links.
- Transparent fallback if Ollama is unavailable.
- Five automated retrieval tests.

## Important dataset note
This is a curated educational dataset, not an official municipal dataset. It links to government portals as starting references. Local waste rules differ by city and ward; verify instructions with your municipality. Do not treat the model's category as a legal or operational determination.

## Run in Windows VS Code
1. Extract ZIP and open `EcoGuide_AI_Project` in VS Code.
2. Terminal > New Terminal.
3. Run:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
4. Install Ollama from https://ollama.com/download.
5. In another terminal:
   ```powershell
   ollama pull llama3.2:3b
   ollama run llama3.2:3b
   ```
   Test it, then type `/bye`. Keep Ollama running in the background.
6. In the project terminal:
   ```powershell
   python app.py
   ```
7. Open http://127.0.0.1:5000 in Chrome. Stop with Ctrl+C.

If Ollama is not running, the site uses a clearly labelled knowledge-base fallback. For an actual LLM demonstration, the UI must show `Ollama LLM + RAG`.

## Test retrieval
With the virtual environment active:
```powershell
python -m unittest discover -s tests -v
```
Tests check dataset count, battery retrieval, phone retrieval, food-scrap retrieval and source presence. Run them on your computer and record actual results in your report. These tests do not evaluate legal or environmental correctness, nor do they test LLM quality.

## Main files
- `app.py`: Flask application and Ollama integration
- `retrieval.py`: TF-IDF retrieval
- `data/waste_knowledge.json` and `.csv`: included dataset
- `templates/index.html`: page
- `static/style.css`, `static/app.js`: frontend
- `tests/test_retrieval.py`: tests
- `Project_Report_EcoGuide_AI.docx` and `.pdf`: report

## Official starting references
- Swachh Bharat Mission: https://swachhbharatmission.gov.in/
- Central Pollution Control Board: https://cpcb.nic.in/
- CPCB e-waste: https://cpcb.nic.in/e-waste/
- Ministry of Environment, Forest and Climate Change: https://moef.gov.in/
- FSSAI: https://fssai.gov.in/
