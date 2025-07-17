
# 🤖 AutoGrader — AI-Powered Notebook Evaluation

AutoGrader is a full-stack application developed at the **Vibe Hack Hackathon** to automate grading of Jupyter Notebooks using LLMs. Upload a `.zip` of `.ipynb` files and a `.txt` rubric, and receive structured feedback and scores — instantly!

### Project Built by 
[Elena Nurullina](https://github.com/ElenkaSan)

[Aryan Jain](https://github.com/aryanj10)

https://github.com/lenzlaww
---

## 🚀 Features

- 📁 Upload multiple student notebooks in `.zip` format
- 📋 Upload a grading rubric in `.txt` format
- 💬 Uses **Claude 3.5 Haiku** via Rilla API for scoring and feedback
- 📊 Generates downloadable grading report as `.csv` and detailed feedback `.txt`
- 🖥️ Frontend built in React + Axios for smooth UX
- ⚡ FastAPI backend with async inference calls

---

## 🧱 Directory Structure

### 🔧 Backend (`/backend`)
```
backend/
├── app.py                   # FastAPI server
├── graders/
│   ├── ipynb_parser.py      # Notebook parser
│   ├── rubric_processor.py  # Rubric parsing logic
│   └── grader.py            # LLM interaction and grading logic
├── test_data/               # Sample submissions
├── templates/               # (Optional) For HTML rendering
├── static/                  # Static frontend files
└── requirements.txt         # Python dependencies
```

### 🌐 Frontend (`/src`)
```
src/
├── components/
│   ├── FileUpload.js        # Upload .zip and rubric
│   ├── ResultDisplay.js     # Show results
├── services/
│   └── api.js               # Axios for API requests
├── App.js                   # Main React app
├── index.js                 # Entry point
└── styles.css               # Global styles
```

---

## 📦 API Endpoints

| Endpoint        | Method | Description |
|----------------|--------|-------------|
| `/grade/`       | POST   | Upload `.zip` + `.txt` rubric and get feedback |
| `/csv`          | GET    | Download grading results as CSV |
| `/feedback`     | GET    | Download all feedback as TXT |
| `/`             | GET    | Serves frontend (if hosted statically) |

---

## ⚙️ How It Works

1. **Upload**: Send student notebooks + rubric via form.
2. **Parse**: Extracts code cells from `.ipynb` files.
3. **Score**: Sends rubric + code to LLM (Claude 3.5 Haiku).
4. **Output**: Collects scores + feedback, saves as CSV & TXT.

---

## 🛠️ Technologies Used

- **Frontend**: React, Axios
- **Backend**: FastAPI, httpx, nbformat, pandas, matplotlib
- **LLM API**: Claude 3.5 via LiteLLM Proxy (Rilla)
- **Deployment**: (Locally hosted / ready for Dockerization)

---

## 🧪 Sample Output

**CSV:**
```
notebook,score
student1.ipynb,88
student2.ipynb,73
```

**Feedback (TXT):**
```
===== student1.ipynb =====
Final Score: 88
What is wrong:
- Did not modularize functions

What can be improved:
- Use better variable names
```

---

## 🏁 Getting Started

### 📦 Install Backend Requirements
```bash
cd backend
pip install -r requirements.txt
```

### ▶️ Run the Backend
```bash
uvicorn app:app --reload
```

### 🌐 Start Frontend (if separate)
```bash
cd src
npm install
npm start
```

---

## 🎯 Future Improvements

- 🔒 Authentication for teacher/student roles
- 📈 Visual plots per student performance
- 🧠 Auto-rubric generation from solution notebook
- 🧪 Support for multiple LLM providers

---

## 🏆 Built at Vibe Hack Hackathon

This project was developed in under 2 hours at the **Vibe Hack Hackathon**, blending GenAI and education for impact.
