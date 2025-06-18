import React from "react";

function ResultDisplay({ results }) {
    if (!results) return null;

    const downloadCSV = () => {
        const csvContent =
            "data:text/csv;charset=utf-8," +
            ["Student Name,Score,Key Comment"]
                .concat(
                    results.students.map((student) => `${student.name},${student.score},${student.comment}`)
                )
                .join("\n");

        const link = document.createElement("a");
        link.setAttribute("href", encodeURI(csvContent));
        link.setAttribute("download", "results.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="results-container">
            <h2>Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Student Name</th>
                        <th>Score</th>
                        <th>Key Comment</th>
                    </tr>
                </thead>
                <tbody>
                    {results.students.map((student, index) => (
                        <tr key={index}>
                            <td>{student.name}</td>
                            <td>{student.score}</td>
                            <td>{student.comment}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={downloadCSV}>Download CSV</button>
            <div className="general-feedback">
                <h3>General class Feedback</h3>
                <p>{results.feedback}</p>
            </div>
        </div>
    );
}

export default ResultDisplay;




// function ResultDisplay({ results }) {
//   if (!results) return null;

//   return (
//     <div className="results-container">
//       <h2>Grading Results</h2>
//       <p><strong>Score:</strong> {results.score}</p>
//       <p><strong>Comments:</strong> {results.comments}</p>
//       <p><strong>What is wrong:</strong> {results.wrong}</p>
//       <p><strong>Suggestions for improvement:</strong> {results.improvement}</p>
//     </div>
//   );
// }

// export default ResultDisplay;

