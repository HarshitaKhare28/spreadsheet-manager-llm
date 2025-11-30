from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global variable to track the current active file
current_file_path = None

def load_current_file():
    """Load the currently active uploaded file."""
    global current_file_path
    if not current_file_path or not os.path.exists(current_file_path):
        return None, None
    
    if current_file_path.endswith('.csv'):
        df = pd.read_csv(current_file_path)
    else:
        df = pd.read_excel(current_file_path)
    return df, current_file_path


@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload and summarize spreadsheet."""
    global current_file_path
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Set this as the current active file
    current_file_path = filepath

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        columns = df.columns.tolist()
        rows = len(df)

        # Basic summary instead of using heavy model
        summary = f"Uploaded spreadsheet with {rows} rows and {len(columns)} columns: {', '.join(columns[:5])}"
        if len(columns) > 5:
            summary += f" and {len(columns)-5} more"

        return jsonify({
            "columns": columns,
            "rows": rows,
            "summary": summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/query', methods=['POST'])
def query_data():
    """Smart query handling with enhanced rule-based system."""
    data = request.json
    query = data.get("query", "").lower().strip()

    df, path = load_current_file()
    if df is None:
        return jsonify({"error": "No uploaded file found"}), 400

    try:
        return handle_query_with_rules(df, query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_query_with_rules(df, query):
    """Enhanced rule-based query handler with SQL-like filtering."""
    clean_query = re.sub(r'[^a-z0-9\s]', '', query)
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(exclude='number').columns.tolist()
    all_cols = df.columns.tolist()
    
    # Convert numeric columns safely
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # === ROW COUNT ===
    if any(k in clean_query for k in ["how many rows", "number of rows", "row count", "count rows"]):
        return jsonify({"query": query, "answer": f"{len(df)} rows", "type": "count"})
    
    # === FILTERING QUERIES (SQL-like) ===
    # Example: "how many people with name starting with a"
    filter_df = df.copy()
    filtered = False
    
    # Check for "starting with" or "begins with"
    if "starting with" in query or "begins with" in query or "starts with" in query:
        match = re.search(r'(starting|starts|begins)\s+with\s+([a-z])', query)
        if match:
            letter = match.group(2).upper()
            # Find text columns
            for col in categorical_cols:
                if df[col].dtype == 'object':
                    filter_df = df[df[col].astype(str).str.upper().str.startswith(letter)]
                    filtered = True
                    break
            
            if filtered:
                count = len(filter_df)
                return jsonify({
                    "query": query,
                    "answer": f"{count} rows found where {categorical_cols[0] if categorical_cols else 'column'} starts with '{letter}'",
                    "type": "filter",
                    "count": count,
                    "details": filter_df.to_dict(orient='records')[:10]  # Limit to 10 rows
                })
    
    # Check for "containing" or "with"
    if "containing" in query or " with " in query:
        words = query.split()
        for i, word in enumerate(words):
            if word in ["containing", "with"] and i + 1 < len(words):
                search_term = words[i + 1]
                for col in categorical_cols:
                    if df[col].dtype == 'object':
                        filter_df = df[df[col].astype(str).str.contains(search_term, case=False, na=False)]
                        filtered = True
                        break
                
                if filtered:
                    count = len(filter_df)
                    return jsonify({
                        "query": query,
                        "answer": f"{count} rows found containing '{search_term}'",
                        "type": "filter",
                        "count": count,
                        "details": filter_df.to_dict(orient='records')[:10]
                    })
    
    # Try to detect column name in query
    matched_col = None
    for col in all_cols:
        if col.lower() in clean_query:
            matched_col = col
            break
    
    # Default to first numeric column if none matched
    num_col = matched_col if matched_col in numeric_cols else (numeric_cols[0] if numeric_cols else None)
    
    # === SUM / TOTAL ===
    if any(k in clean_query for k in ["total", "sum"]):
        if num_col:
            total = df[num_col].sum()
            return jsonify({"query": query, "answer": f"Total {num_col}: {total}", "type": "sum"})
        return jsonify({"query": query, "answer": "No numeric column found for sum."})
    
    # === AVERAGE / MEAN ===
    if any(k in clean_query for k in ["average", "avg", "mean"]):
        if num_col:
            avg = df[num_col].mean()
            return jsonify({"query": query, "answer": f"Average {num_col}: {round(avg, 2)}", "type": "average"})
        return jsonify({"query": query, "answer": "No numeric column found for average."})
    
    # === MAX / HIGHEST ===
    if any(k in clean_query for k in ["highest", "maximum", "max", "largest"]):
        if num_col:
            max_value = df[num_col].max()
            rows_with_max = df[df[num_col] == max_value]
            
            label_col = categorical_cols[0] if categorical_cols else None
            if label_col:
                labels = rows_with_max[label_col].tolist()
                answer = f"{label_col}(s) {labels} have highest {num_col} = {max_value}"
            else:
                answer = f"Highest {num_col} = {max_value}"
            
            return jsonify({
                "query": query,
                "answer": answer,
                "details": rows_with_max.to_dict(orient='records'),
                "type": "max"
            })
        return jsonify({"query": query, "answer": "No numeric column found for maximum."})
    
    # === MIN / LOWEST ===
    if any(k in clean_query for k in ["lowest", "minimum", "min", "smallest"]):
        if num_col:
            min_value = df[num_col].min()
            rows_with_min = df[df[num_col] == min_value]
            
            label_col = categorical_cols[0] if categorical_cols else None
            if label_col:
                labels = rows_with_min[label_col].tolist()
                answer = f"{label_col}(s) {labels} have lowest {num_col} = {min_value}"
            else:
                answer = f"Lowest {num_col} = {min_value}"
            
            return jsonify({
                "query": query,
                "answer": answer,
                "details": rows_with_min.to_dict(orient='records'),
                "type": "min"
            })
        return jsonify({"query": query, "answer": "No numeric column found for minimum."})
    
    # === COUNT / HOW MANY ===
    if any(k in clean_query for k in ["how many", "count", "number of"]):
        # If asking about specific value
        for col in categorical_cols:
            unique_vals = df[col].unique()
            for val in unique_vals:
                if str(val).lower() in query:
                    count = len(df[df[col] == val])
                    return jsonify({
                        "query": query,
                        "answer": f"{count} rows with {col} = {val}",
                        "type": "count"
                    })
        
        # General count
        return jsonify({"query": query, "answer": f"Total rows: {len(df)}", "type": "count"})
    
    # === FALLBACK ===
    return jsonify({
        "query": query,
        "answer": f"I understand your question but couldn't find a match. Available columns: {', '.join(all_cols)}. Try: 'how many rows', 'sum of {num_col}', 'average {num_col}', 'highest {num_col}', 'count rows starting with A'",
        "type": "help"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)