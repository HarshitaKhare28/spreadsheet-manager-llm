import { useState } from "react";
import axios from "axios";
import ResultTable from "./Components/ResultTable";

function App() {
  const [file, setFile] = useState(null);
  const [info, setInfo] = useState(null);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [responses, setResponses] = useState([]); // Changed to array for multiple Q&A
  const [loadingQuery, setLoadingQuery] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setInfo(res.data);
      setError("");
      setResponses([]); // Clear previous responses when new file uploaded
    } catch (err) {
      console.error(err);
      setError("Upload failed. Check if backend is running.");
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) return;
    setLoadingQuery(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/query", { query });
      // Add new response to the beginning of the array
      setResponses([{ question: query, ...res.data }, ...responses]);
      setQuery(""); // Clear input after asking
    } catch (err) {
      console.error(err);
      setError("Query failed. Check backend or try again.");
    }
    setLoadingQuery(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loadingQuery) {
      handleQuery();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 text-gray-100 p-6 font-sans">
      <div className="max-w-7xl mx-auto">

        {/* Header */}
        <h1 className="text-5xl font-extrabold text-center py-3 bg-clip-text text-white mb-16 drop-shadow-lg">
           Spreadsheet Manager
        </h1>

        {/* Upload Section (Form pushed down with mb-16 for spacing) */}
        <div className="bg-gray-800/80 backdrop-blur-md rounded-3xl shadow-2xl p-6 py-4 mb-8 flex flex-col md:flex-row gap-6 items-center transition hover:shadow-purple-500/50">
          <input
            type="file"
            accept=".xlsx,.csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full md:w-2/3 text-sm text-gray-200 border border-gray-600 rounded-lg cursor-pointer bg-gray-700 focus:outline-none focus:ring-2 focus:ring-purple-400 p-3"
          />
          <button
            onClick={handleUpload}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-3 px-8 rounded-2xl shadow-lg transition"
          >
            Upload
          </button>
        </div>

        {error && (
          <p className="text-red-400 text-center mb-6 font-medium animate-pulse">
            {error}
          </p>
        )}

        {/* File Info & Query */}
        {info && (
          <div className="bg-gray-800/80 backdrop-blur-md rounded-3xl shadow-2xl p-6 mb-8 transition hover:shadow-purple-500/50">
            <h2 className="text-2xl font-bold mb-4 text-pink-400">
              File Info
            </h2>
            <p className="mb-2 text-gray-200">
              <b>Columns:</b> {info.columns.join(", ")}
            </p>
            <p className="mb-4 text-gray-200">
              <b>Total Rows:</b> {info.rows}
            </p>

            {/* Query Section */}
            <div className="flex flex-col md:flex-row gap-4 mb-6">
              <input
                type="text"
                placeholder="Ask a question... (Press Enter to submit)"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="border border-gray-600 rounded-xl p-3 flex-1 bg-gray-700 text-gray-200 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-400 transition"
              />
              <button
                onClick={handleQuery}
                className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-gray-900 font-semibold py-3 px-6 rounded-xl shadow-lg transition"
                disabled={loadingQuery}
              >
                {loadingQuery ? "Processing..." : "Ask"}
              </button>
            </div>

            {/* All Query Responses (Chat-like history) */}
            {responses.length > 0 && (
              <div className="mt-6 space-y-4 max-h-[500px] overflow-y-auto">
                {responses.map((resp, idx) => (
                  <div key={idx} className="bg-gray-700/70 backdrop-blur-md p-5 rounded-2xl shadow-inner transition hover:shadow-pink-400/30">
                    <p className="text-md font-medium mb-2 text-gray-300">
                      <b>Q:</b> {resp.question}
                    </p>
                    <p className="text-lg font-semibold mb-4 text-pink-300">
                      <b>A:</b> {resp.answer}
                    </p>
                    {resp.details && (
                      <div className="overflow-x-auto">
                        <ResultTable data={resp.details} dark />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
