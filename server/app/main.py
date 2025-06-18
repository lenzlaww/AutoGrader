from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os, zipfile, tempfile, nbformat, httpx

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

Return the score (0-10), what is wrong, and what can be improved.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-5-haiku",  # ✅ FASTER MODEL (optional but recommended for speed)
        "messages": [{"role": "user", "content": prompt}]
    }

    # ✅ ADD TIMEOUT (60 seconds read timeout)
    timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        res = await client.post(API_URL, json=payload, headers=headers)
        res.raise_for_status()
        response = res.json()
        return response["choices"][0]["message"]["content"]


# === Main Endpoint ===
@app.post("/grade/")
async def grade_submission(zipfile: UploadFile = File(...), rubricfile: UploadFile = File(...)):
    zip_bytes = await zipfile.read()
    rubric_bytes = await rubricfile.read()

    rubric = parse_rubric(rubric_bytes)
    notebooks = extract_notebooks(zip_bytes)

    results = {}
    for filename, code in notebooks.items():
        feedback = await get_llm_feedback(rubric, code)
        results[filename] = feedback

    return JSONResponse(content={"results": results})
