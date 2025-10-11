import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [info, setInfo] = useState(null);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setInfo(res.data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Upload failed. Check if backend is running.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
      <div className="bg-white rounded-2xl shadow-md p-8 w-full max-w-lg">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
          📊 Spreadsheet Manager LLM
        </h1>

        <div className="flex flex-col gap-4 items-center">
          <input
            type="file"
            accept=".xlsx,.csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleUpload}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition"
          >
            Upload
          </button>
        </div>

        {error && (
          <p className="text-red-500 text-center mt-4">{error}</p>
        )}

        {info && (
          <div className="mt-6 text-center">
            <h3 className="text-lg font-semibold mb-2 text-gray-700">
              File Info
            </h3>
            <p className="text-gray-600">
              <b>Columns:</b> {info.columns.join(", ")}
            </p>
            <p className="text-gray-600">
              <b>Total Rows:</b> {info.rows}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
