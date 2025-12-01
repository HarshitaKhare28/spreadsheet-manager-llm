# 📊 Spreadsheet Manager

An intelligent spreadsheet analytics platform with **Google OAuth**, natural language queries, and automated dashboard generation. Upload CSV/Excel files, visualize data with interactive charts, and query using plain English.

## ✨ Key Features

- 🔐 **Google Sign-In** + Email/Password authentication (MongoDB + JWT)
- 📊 **Auto-generated dashboards** with charts (Bar, Pie, Line)
- 📥 **PDF export** of complete dashboard
- 🤖 **Natural language queries**: "Give me names where score > 800"
- 🔍 **Smart filtering** with WHERE clauses and pattern matching
- 📈 **Statistics** - sum, average, min, max, median for all columns

## 🚀 Tech Stack

**Backend:** Python 3.12, Flask, MongoDB, PyJWT, Google OAuth 2.0, Pandas, ReportLab  
**Frontend:** React 19, Vite, Tailwind CSS v4, Chart.js, @react-oauth/google

## 📋 Quick Start

### Prerequisites
- Python 3.12+, Node.js 16+
- MongoDB (local or Atlas)
- Google Cloud OAuth credentials ([Get here](https://console.cloud.google.com/))

### Installation

**1. Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

Edit `backend/.env`:
```env
MONGODB_URI=mongodb://localhost:27017/
GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-secret
JWT_SECRET_KEY=generate-with-secrets.token_urlsafe(32)
FLASK_SECRET_KEY=generate-with-secrets.token_urlsafe(32)
```

```bash
python app.py  # Runs on port 8000
```

**2. Frontend:**
```bash
cd frontend
npm install
```

Edit `frontend/.env`:
```env
VITE_GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
```

```bash
npm run dev  # Runs on port 5173
```

## 📖 Usage

1. **Sign in** with Google or create account
2. **Upload** CSV/Excel file
3. **View** auto-generated dashboard with charts
4. **Download PDF** of dashboard
5. **Ask queries** like:
   - "How many rows?"
   - "Average CGPA?"
   - "Give me fullName where Codolio > 800"
   - "Names starting with letter L"

## 🎯 Query Examples

- **Aggregation**: `sum of Sales`, `average age`, `highest score`
- **Filtering**: `fullName where age > 25`, `students where CGPA > 8.5`
- **Pattern matching**: `names starting with A`, `count rows with Status = Active`

## 🔒 Security

- JWT authentication with token expiration
- bcrypt password hashing
- Protected API routes
- Google OAuth 2.0
- Environment variables for credentials

## 📁 Project Structure

```
backend/
  ├── app.py          # Flask API + auth routes
  ├── auth.py         # JWT utilities
  ├── database.py     # MongoDB connection
  └── .env            # Credentials (not in git)

frontend/
  ├── src/
  │   ├── App.jsx
  │   ├── context/AuthContext.jsx
  │   └── Components/
  │       ├── Login.jsx
  │       ├── Register.jsx
  │       └── Dashboard.jsx
  └── .env            # Google Client ID (not in git)
```

## 👤 Author

**Harshita Khare** - [@HarshitaKhare28](https://github.com/HarshitaKhare28)

