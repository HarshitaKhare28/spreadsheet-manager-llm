# 📊 Spreadsheet Manager with Natural Language Query

An intelligent spreadsheet management application that allows users to upload CSV/Excel files and query data using natural language. Built with Flask backend and React frontend.

## ✨ Features

- **File Upload**: Support for CSV and Excel (.xlsx) files
- **Natural Language Queries**: Ask questions in plain English
- **Multiple Query Support**: Ask unlimited questions about your data
- **Smart Filtering**: Filter data by values, modes, purposes, etc.
- **Calculations**: Sum, average, min, max, count operations
- **Chat-like Interface**: View all previous questions and answers
- **Real-time Results**: Instant responses with detailed data tables

## 🚀 Tech Stack

### Backend
- Python 3.12
- Flask
- Flask-CORS
- Pandas
- openpyxl

### Frontend
- React
- Vite
- Axios
- Tailwind CSS

## 📋 Prerequisites

- Python 3.12+
- Node.js 16+
- npm or yarn

## 🛠️ Installation

### Backend Setup

1. Navigate to backend folder:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to frontend folder:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## 📖 Usage

1. **Upload a File**: Click on the file input and select a CSV or Excel file
2. **Wait for Processing**: File info will appear showing columns and row count
3. **Ask Questions**: Type your question in natural language and press Enter or click Ask
4. **View Results**: Answers appear below with relevant data tables

### Example Queries

- "How many rows are there?"
- "Give total amount from the Amt column"
- "What is the average salary?"
- "How many times have I paid in Cash mode?"
- "Show me the highest score"
- "Count rows with Purpose = Printout"
- "How many people with names starting with A?"

## 🎯 Query Types Supported

- **Row Count**: "how many rows", "total rows"
- **Sum/Total**: "total amount", "sum of sales"
- **Average**: "average salary", "mean price"
- **Maximum**: "highest score", "max value"
- **Minimum**: "lowest price", "min amount"
- **Filtering**: "paid in cash mode", "for shopping purpose"
- **Text Matching**: "starting with A", "containing keyword"

## 📁 Project Structure

```
Spreadhseetproject/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── uploads/              # Uploaded files storage
│   └── venv/                 # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── Components/
│   │   │   └── ResultTable.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔧 Configuration

### Backend Port
Default: `8000`  
To change, edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

### Frontend API URL
If you change the backend port, update `App.jsx`:
```javascript
axios.post("http://127.0.0.1:YOUR_PORT/upload", ...)
```

## 🐛 Troubleshooting

### Backend not starting
- Ensure virtual environment is activated
- Check if port 8000 is available
- Verify all dependencies are installed

### Frontend connection error
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify API endpoints in App.jsx

### Pandas version conflict
```bash
pip uninstall pandas -y
pip install pandas
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 👤 Author

**Harshita Khare**
- GitHub: [@HarshitaKhare28](https://github.com/HarshitaKhare28)
