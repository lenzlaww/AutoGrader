from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os, zipfile, tempfile, nbformat, httpx
import pandas as pd
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import re
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# LiteLLM API setup (Rilla's server)
API_URL = "https://litellm.rillavoice.com/v1/chat/completions"
API_KEY = "sk-rilla-vibes"
LLM_MODEL = "llama-4-maverick-17b-instruct"

# Util: unzip and extract notebook code cells
def extract_notebooks(zip_bytes) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "upload.zip")
        with open(zip_path, "wb") as f:
            f.write(zip_bytes)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        notebooks = {}
        for root, _, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".ipynb"):
                    nb_path = os.path.join(root, file)
                    with open(nb_path, 'r', encoding='utf-8') as f:
                        nb = nbformat.read(f, as_version=4)
                        code_cells = [c['source'] for c in nb.cells if c.cell_type == 'code']
                        notebooks[file] = "\n\n".join(code_cells)
        return notebooks

# Util: parse rubric txt file
def parse_rubric(rubric_bytes) -> str:
    return rubric_bytes.decode("utf-8")


# Util: call Rilla LLM


async def get_llm_feedback(rubric: str, code: str) -> dict:
    prompt = f"""You are an auto-grader. Based on the rubric below, score and comment on the student's code.

Rubric:
{rubric}

Student Code:
{code}

Your response must follow this format exactly:

Final Score: <a number between 0 and 100>

What is wrong:
- point 1
- point 2

What can be improved:
- suggestion 1
- suggestion 2
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-5-haiku",
        "messages": [{"role": "user", "content": prompt}]
    }

    timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        res = await client.post(API_URL, json=payload, headers=headers)
        res.raise_for_status()
        message = res.json()["choices"][0]["message"]["content"]

    # Extract score from message
    match = re.search(r"Final Score:\s*(\d{1,3})", message)
    score = int(match.group(1)) if match else None

    return {
        "score": score,
        "feedback": message
    }


# === Main Endpoint ===
@app.post("/grade/")
async def grade_submission(zipfile: UploadFile = File(...), rubricfile: UploadFile = File(...)):
    zip_bytes = await zipfile.read()
    rubric_bytes = await rubricfile.read()

    rubric = parse_rubric(rubric_bytes)
    notebooks = extract_notebooks(zip_bytes)

    results = []
    for filename, code in notebooks.items():
        result = await get_llm_feedback(rubric, code)
        results.append({
            "notebook": filename,
            "score": result["score"],
            "feedback": result["feedback"]
        })


    # ✅ Save as CSV
    df = pd.DataFrame(results)
    csv_path = os.path.join(OUTPUT_DIR, "grading_results.csv")
    df.to_csv(csv_path, index=False)

    # Save Feedback TXT
    feedback_text = ""
    for row in results:
        feedback_text += f"\n\n===== {row['notebook']} =====\n{row['feedback']}\n"
    txt_path = os.path.join(OUTPUT_DIR, "grading_feedback.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(feedback_text)

    # Just return a success message
    return JSONResponse(content={"message": "Grading complete. Files ready at /csv, /feedback, /plot."})


@app.get("/csv")
def get_csv():
    csv_path = os.path.join(OUTPUT_DIR, "grading_results.csv")
    return FileResponse(csv_path, media_type="text/csv", filename="grading_results.csv")


@app.get("/feedback")
def get_feedback():
    txt_path = os.path.join(OUTPUT_DIR, "grading_feedback.txt")
    return FileResponse(txt_path, media_type="text/plain", filename="grading_feedback.txt")


@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join("static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()
