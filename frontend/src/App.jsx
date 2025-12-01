import { useState } from "react";
import axios from "axios";
import ResultTable from "./Components/ResultTable";
import Dashboard from "./Components/Dashboard";
import Login from "./Components/Login";
import Register from "./Components/Register";
import { useAuth } from "./context/AuthContext";

function App() {
  const { user, loading: authLoading, logout } = useAuth();
  const [showRegister, setShowRegister] = useState(false);
  const [file, setFile] = useState(null);
  const [info, setInfo] = useState(null);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [responses, setResponses] = useState([]);
  const [loadingQuery, setLoadingQuery] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [viewMode, setViewMode] = useState("dashboard"); // "dashboard" or "query"

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-purple-500 mx-auto mb-4"></div>
          <p className="text-gray-300 text-lg">Loading...</p>
        </div>
      </div>
    );
  }

  // Show login/register if not authenticated
  if (!user) {
    return showRegister ? (
      <Register onSwitchToLogin={() => setShowRegister(false)} />
    ) : (
      <Login onSwitchToRegister={() => setShowRegister(true)} />
    );
  }

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
      setResponses([]);
      
      // Auto-generate dashboard
      await generateDashboard();
    } catch (err) {
      console.error(err);
      setError("Upload failed. Check if backend is running.");
    }
  };

  const generateDashboard = async () => {
    setLoadingDashboard(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/dashboard");
      setDashboardData(res.data);
      setViewMode("dashboard");
    } catch (err) {
      console.error(err);
      setError("Failed to generate dashboard.");
    }
    setLoadingDashboard(false);
  };

  const handleQuery = async () => {
    if (!query.trim()) return;
    setLoadingQuery(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/query", { query });
      setResponses([{ question: query, ...res.data }, ...responses]);
      setQuery("");
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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 text-gray-100 font-sans">
      {/* Navigation Bar */}
      <nav className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            {/* Logo/Brand */}
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-2 rounded-xl">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h1 className="text-2xl font-bold text-white">
                Spreadsheet Manager
              </h1>
            </div>
            
            {/* User Info & Logout */}
            <div className="flex items-center gap-4">
              {/* User Profile Avatar Only */}
              <div className="relative group">
                {user.picture && user.picture !== '' ? (
                  <img 
                    src={user.picture} 
                    alt={user.name} 
                    className="w-11 h-11 rounded-full border-2 border-purple-400 shadow-lg cursor-pointer hover:border-purple-300 transition"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextElementSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                <div className={`w-11 h-11 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center border-2 border-purple-400 shadow-lg cursor-pointer hover:border-purple-300 transition ${user.picture && user.picture !== '' ? 'hidden' : ''}`}>
                  <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                </div>
                
                {/* Tooltip on hover */}
                <div className="absolute right-0 top-full mt-2 bg-gray-800 border border-gray-700 rounded-xl px-4 py-2 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                  <p className="text-white font-semibold text-sm">{user.name}</p>
                  <p className="text-gray-400 text-xs">{user.email}</p>
                </div>
              </div>
              
              {/* Logout Button */}
              <button
                onClick={logout}
                className="bg-red-500/10 hover:bg-red-500/20 border border-red-500/50 text-red-300 hover:text-red-200 font-semibold py-2.5 px-5 rounded-xl transition-all duration-200 flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Upload Section */}
        <div className="bg-gray-800/80 backdrop-blur-md rounded-3xl shadow-2xl p-6 mb-8 flex flex-col md:flex-row gap-6 items-center transition hover:shadow-purple-500/50">
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

        {/* File Info & View Toggle */}
        {info && (
          <div className="space-y-6">
            {/* View Mode Toggle */}
            <div className="flex justify-center gap-4">
              <button
                onClick={() => setViewMode("dashboard")}
                className={`py-3 px-8 rounded-xl font-semibold transition ${
                  viewMode === "dashboard"
                    ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg"
                    : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                }`}
              >
                📊 Dashboard
              </button>
              <button
                onClick={() => setViewMode("query")}
                className={`py-3 px-8 rounded-xl font-semibold transition ${
                  viewMode === "query"
                    ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg"
                    : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                }`}
              >
                💬 Ask Questions
              </button>
            </div>

            {/* Dashboard View */}
            {viewMode === "dashboard" && (
              <div>
                {loadingDashboard ? (
                  <div className="text-center py-20">
                    <p className="text-2xl text-purple-300 animate-pulse">
                      🔄 Generating dashboard...
                    </p>
                  </div>
                ) : dashboardData ? (
                  <Dashboard data={dashboardData} />
                ) : (
                  <div className="text-center py-20">
                    <p className="text-xl text-gray-400">
                      Dashboard not available. Please try uploading again.
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Query View */}
            {viewMode === "query" && (
              <div className="bg-gray-800/80 backdrop-blur-md rounded-3xl shadow-2xl p-6 transition hover:shadow-purple-500/50">
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
                      <div
                        key={idx}
                        className="bg-gray-700/70 backdrop-blur-md p-5 rounded-2xl shadow-inner transition hover:shadow-pink-400/30"
                      >
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
        )}
      </div>
    </div>
  );
}

export default App;
