# 📊 Spreadsheet Manager with AI Query System

An intelligent spreadsheet management application that allows users to upload CSV/Excel files, generate comprehensive analytics dashboards, and query data using natural language. Built with Flask backend and React frontend.

## ✨ Features

### 📊 Static Dashboard Generation
- **Automated Analytics**: Upload any Excel/CSV file and get instant visual analytics
- **Summary Cards**: Display total rows, columns, numeric fields, and text fields
- **Numeric Statistics**: Comprehensive statistics table showing min, max, mean, median, and sum for all numeric columns
- **Interactive Charts**: Auto-generated Bar, Pie, and Line charts using Chart.js
- **Data Preview**: View first 10 rows of your dataset
- **PDF Export**: Download complete dashboard as PDF with all charts and statistics

### 🤖 Natural Language Query System
- **Aggregation Queries**: Sum, average, min, max, count operations
- **Conditional Filtering**: WHERE clause support with comparison operators (>, <, =)
- **Simple SELECT Queries**: Column-specific queries with intelligent column detection
- **Text Pattern Matching**: Filter data by text patterns (starts with, contains, etc.)
- **Chat-like Interface**: View all previous questions and answers
- **Real-time Results**: Instant responses with detailed data tables

## 🚀 Tech Stack

### Backend
- Python 3.12
- Flask 3.1.2
- Flask-CORS
- Pandas 2.3.3
- ReportLab (PDF generation)
- Pillow (Image processing)
- openpyxl

### Frontend
- React 19
- Vite
- Axios
- Tailwind CSS v4
- Chart.js & react-chartjs-2
- html-to-image

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
3. **Generate Dashboard**: Click "Dashboard" to create comprehensive analytics with charts
4. **Export to PDF**: Download the complete dashboard with all visualizations as PDF
5. **Ask Questions**: Type your question in natural language and press Enter or click Ask
6. **View Results**: Answers appear below with relevant data tables

### Example Queries

#### Aggregation Queries
- "How many rows are there?"
- "Sum of Sales column"
- "What is the average CGPA?"
- "Show me the highest Total score"
- "What's the minimum age?"

#### Conditional/Filter Queries
- "Give me fullName where Codolio score is greater than 800"
- "Show names where age is less than 25"
- "Find students where CGPA > 8.5"

#### Text Pattern Queries
- "Give me names starting with letter A"
- "Show fullName starting with L"
- "Count rows with Purpose = Shopping"

## 🎯 Query Types Supported

- **Row Count**: "how many rows", "total rows"
- **Sum/Total**: "total amount", "sum of sales"
- **Average**: "average salary", "mean CGPA"
- **Maximum**: "highest score", "max Total"
- **Minimum**: "lowest price", "min amount"
- **Conditional WHERE**: "column where other_column > value"
- **Text Filtering**: "starting with A", "names beginning with letter L"
- **Pattern Matching**: Intelligent column name detection and matching

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
│   │   │   ├── Dashboard.jsx      # Analytics dashboard
│   │   │   ├── SummaryCard.jsx    # Summary statistics cards
│   │   │   ├── ChartCard.jsx      # Chart visualization component
│   │   │   └── ResultTable.jsx    # Data table display
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── README.md
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
