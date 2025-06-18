import React, { useState } from "react";
import axios from "../services/api";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function FileUpload({ setResults }) {
    const [file, setFile] = useState(null);
    const [rubric, setRubric] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleRubricChange = (e) => {
        setRubric(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file || !rubric) {
            toast.error("Please upload a file and provide a rubric!");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("rubric", rubric);

        try {
            const response = await axios.post("/upload", formData);
            toast.success("Grading completed!");
            setResults(response.data); // Pass results to parent
        } catch (error) {
            toast.error("Error processing the file. Please try again.");
        }
    };

    return (
        <div className="file-upload-container">
            <h2 className="title">AutoGrader AI</h2>
            <p className="subtitle">Your Classroom Assistant</p>

            <div className="step">
                <h3>Step 1 – Upload ZIP of Student Notebooks</h3>
                <div className="upload-area">
                    <input type="file" id="file" accept=".zip" onChange={handleFileChange} />
                    <label htmlFor="file" className="drop-area">
                        Drag & drop files here, or <span className="browse">Browse</span>
                    </label>
                </div>
            </div>

            <div className="step">
                <h3>Step 2 – Enter or Upload Grading Rubric</h3>
                <textarea
                    id="rubric"
                    rows="5"
                    value={rubric}
                    onChange={handleRubricChange}
                    className="rubric-input"
                    placeholder="Enter your grading rubric or upload a txt file"
                ></textarea>
            </div>

            <div className="step">
                <h3>Step 3 – Press BIG Button:</h3>
                <button className="submit-button" onClick={handleSubmit}>
                    Grade My Class
                </button>
            </div>
        </div>
    );
}

export default FileUpload;

// import React, { useState } from "react";
// import axios from "../services/api";
// import { toast } from "react-toastify";
// import "react-toastify/dist/ReactToastify.css";

// function FileUpload({ setResults }) {
//   const [file, setFile] = useState(null);
//   const [rubric, setRubric] = useState("");

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//   };

//   const handleRubricChange = (e) => {
//     setRubric(e.target.value);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!file || !rubric) {
//       toast.error("Please upload a file and provide a rubric!");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("file", file);
//     formData.append("rubric", rubric);

//     try {
//       const response = await axios.post("/upload", formData);
//       toast.success("Grading completed!");
//       setResults(response.data); // Pass results to parent
//     } catch (error) {
//       toast.error("Error processing the file. Please try again.");
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit} className="upload-form">
//       <div>
//         <label htmlFor="file">Step 1 - Upload ZIP of Student Notebooks</label>
//         <input type="file" id="file" accept=".zip" onChange={handleFileChange} />
//       </div>
//       <div>
//         <label htmlFor="rubric">Rubric (JSON format):</label>
//         <textarea
//           id="rubric"
//           rows="5"
//           onChange={handleRubricChange}
//           placeholder='{"criteria":[{"key":"correctness","weight":50}]}'
//         ></textarea>
//       </div>
//       <button type="submit">Submit</button>
//     </form>
//   );
// }

// export default FileUpload;
