# AutoGrader

## Directory Structure:

### Backend

```
backend/
├── app.py  # Main entry point
├── graders/
│   ├── ipynb_parser.py  # Extract, parse IPYNB content
│   ├── rubric_processor.py  # Interpret rubric
│   └── grader.py  # Core grading logic using OpenAI API
├── templates/  # Optional for frontend if using Flask
├── static/  # Optional for frontend assets
├── test_data/  # For testing with sample inputs
└── requirements.txt  # Dependencies

```

### Frontend

```
src/
├── components/
│   ├── FileUpload.js  # File Upload Component
│   ├── ResultDisplay.js  # Display Results Component
├── services/
│   ├── api.js  # Axios configuration for API calls
├── App.js
├── index.js
└── styles.css  # Global Styles
```
