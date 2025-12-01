from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
import re
from playwright.sync_api import sync_playwright
import time

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


@app.route('/dashboard', methods=['POST'])
def generate_dashboard():
    """Generate dashboard analytics for the uploaded file."""
    try:
        df, path = load_current_file()
        if df is None:
            return jsonify({"error": "No uploaded file found"}), 400
        
        print(f"Loading file: {path}")
        print(f"DataFrame shape: {df.shape}")
        
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        categorical_cols = df.select_dtypes(exclude='number').columns.tolist()
        
        print(f"Numeric columns: {numeric_cols}")
        print(f"Categorical columns: {categorical_cols}")
        
        # Basic summary
        dashboard = {
            "summary": {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "numeric_columns": len(numeric_cols),
                "categorical_columns": len(categorical_cols),
                "file_name": os.path.basename(path) if path else "Unknown"
            },
            "numeric_stats": {},
            "charts": []
        }
        
        # Generate statistics for numeric columns (max 5)
        for col in numeric_cols[:5]:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                dashboard["numeric_stats"][col] = {
                    "min": float(col_data.min()),
                    "max": float(col_data.max()),
                    "mean": float(col_data.mean()),
                    "median": float(col_data.median()),
                    "sum": float(col_data.sum()),
                    "std": float(col_data.std()) if len(col_data) > 1 else 0
                }
        
        # Generate chart data for categorical columns (max 3)
        for col in categorical_cols[:3]:
            # Convert to string to handle datetime and other special types
            col_data = df[col].astype(str)
            value_counts = col_data.value_counts().head(10)
            if len(value_counts) > 0:
                dashboard["charts"].append({
                    "type": "bar",
                    "title": f"Distribution of {col}",
                    "column": col,
                    "labels": [str(x) for x in value_counts.index.tolist()],
                    "data": value_counts.values.tolist()
                })
        
        # Generate trend chart for first numeric column if exists
        if len(numeric_cols) > 0:
            first_num_col = numeric_cols[0]
            # Take first 50 rows for trend
            trend_data = df[first_num_col].head(50).tolist()
            dashboard["charts"].append({
                "type": "line",
                "title": f"Trend of {first_num_col}",
                "column": first_num_col,
                "labels": list(range(1, len(trend_data) + 1)),
                "data": trend_data
            })
        
        # Add pie chart for first categorical column
        if len(categorical_cols) > 0:
            first_cat_col = categorical_cols[0]
            # Convert to string to handle datetime and other special types
            col_data = df[first_cat_col].astype(str)
            value_counts = col_data.value_counts().head(5)
            if len(value_counts) > 0:
                dashboard["charts"].append({
                    "type": "pie",
                    "title": f"Composition of {first_cat_col}",
                    "column": first_cat_col,
                    "labels": [str(x) for x in value_counts.index.tolist()],
                    "data": value_counts.values.tolist()
                })
        
        # Add data preview - convert to string to handle NaT and other types
        preview_df = df.head(10).copy()
        # Convert all columns to string to avoid serialization issues
        for col in preview_df.columns:
            preview_df[col] = preview_df[col].astype(str)
        dashboard["preview"] = preview_df.to_dict(orient='records')
        
        print("Dashboard generated successfully")
        return jsonify(dashboard)
    
    except Exception as e:
        print(f"Error generating dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
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
    
    # === CONDITIONAL FILTERING (WHERE clause) ===
    # Examples: "give me fullName where codolio > 800", "show names where score greater than 50"
    where_patterns = [
        (r'(give|show|get|find)\s+(?:me\s+)?(\w+)\s+where\s+(\w+)\s+(?:score\s+)?(?:is\s+)?(?:greater|more|higher)\s+than\s+(\d+)', 'greater'),
        (r'(give|show|get|find)\s+(?:me\s+)?(\w+)\s+where\s+(\w+)\s+(?:score\s+)?(?:is\s+)?(?:less|lower|smaller)\s+than\s+(\d+)', 'less'),
        (r'(give|show|get|find)\s+(?:me\s+)?(\w+)\s+where\s+(\w+)\s+(?:score\s+)?(?:is\s+)?equals?\s+(\d+)', 'equal'),
        (r'(give|show|get|find)\s+(?:me\s+)?(\w+)\s+where\s+(\w+)\s*[>]\s*(\d+)', 'greater'),
        (r'(give|show|get|find)\s+(?:me\s+)?(\w+)\s+where\s+(\w+)\s*[<]\s*(\d+)', 'less'),
        (r'(give|show|get|find)\s+(?:me\s+)?(\w+)\s+where\s+(\w+)\s*=\s*(\d+)', 'equal'),
    ]
    
    for pattern, comparison in where_patterns:
        match = re.search(pattern, query)
        if match:
            select_col = match.group(2)
            filter_col = match.group(3)
            threshold = float(match.group(4))
            
            # Find matching columns (case-insensitive)
            select_column = None
            filter_column = None
            
            for col in all_cols:
                if col.lower() == select_col.lower() or select_col.lower() in col.lower():
                    select_column = col
                if col.lower() == filter_col.lower() or filter_col.lower() in col.lower():
                    filter_column = col
            
            if select_column and filter_column and filter_column in numeric_cols:
                # Apply filter
                if comparison == 'greater':
                    filter_df = df[df[filter_column] > threshold]
                elif comparison == 'less':
                    filter_df = df[df[filter_column] < threshold]
                elif comparison == 'equal':
                    filter_df = df[df[filter_column] == threshold]
                
                count = len(filter_df)
                
                # Return the selected column values
                results = filter_df[select_column].tolist()
                
                return jsonify({
                    "query": query,
                    "answer": f"{count} rows found where {filter_column} {comparison} than {threshold}",
                    "type": "conditional_filter",
                    "count": count,
                    "column": select_column,
                    "values": results[:20],  # Limit to 20 values
                    "details": filter_df[[select_column, filter_column]].to_dict(orient='records')[:10]
                })
    
    # === FILTERING QUERIES (SQL-like) ===
    # Example: "how many people with name starting with a"
    filter_df = df.copy()
    filtered = False
    
    # Check for "starting with" or "begins with"
    if "starting with" in query or "begins with" in query or "starts with" in query:
        match = re.search(r'(starting|starts|begins)\s+with\s+(?:letter\s+)?([a-z])', query)
        if match:
            letter = match.group(2).upper()
            
            # Try to identify which column the user is asking about
            target_col = None
            for col in categorical_cols:
                # Check if column name is mentioned in query
                if col.lower() in query:
                    target_col = col
                    break
            
            # If no column mentioned, look for common keywords
            if not target_col:
                if any(word in query for word in ["name", "fullname", "full name"]):
                    # Find column containing "name"
                    for col in categorical_cols:
                        if "name" in col.lower():
                            target_col = col
                            break
            
            # Default to first text column if still not found
            if not target_col and categorical_cols:
                target_col = categorical_cols[0]
            
            if target_col and df[target_col].dtype == 'object':
                filter_df = df[df[target_col].astype(str).str.upper().str.startswith(letter)]
                filtered = True
                count = len(filter_df)
                
                return jsonify({
                    "query": query,
                    "answer": f"{count} rows found where {target_col} starts with '{letter}'",
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


@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    """Generate PDF by capturing screenshot from frontend."""
    print("=== PDF Export Started ===")
    try:
        data = request.json
        screenshot_data = data.get('screenshot')
        
        if not screenshot_data:
            print("ERROR: No screenshot data provided")
            return jsonify({"error": "No screenshot data provided"}), 400
        
        df, path = load_current_file()
        if df is None:
            print("ERROR: No uploaded file found")
            return jsonify({"error": "No uploaded file found"}), 400
        
        file_name = os.path.basename(path).replace('.xlsx', '').replace('.csv', '')
        pdf_path = os.path.join(UPLOAD_FOLDER, f'dashboard-{file_name}.pdf')
        print(f"PDF will be saved to: {pdf_path}")
        
        # Remove data URL prefix
        import base64
        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas as pdf_canvas
        
        screenshot_data = screenshot_data.split(',')[1]
        screenshot_bytes = base64.b64decode(screenshot_data)
        
        # Open image from bytes
        from PIL import Image
        img = Image.open(BytesIO(screenshot_bytes))
        img_width, img_height = img.size
        
        # Save image temporarily
        temp_img_path = os.path.join(UPLOAD_FOLDER, 'temp_dashboard.png')
        img.save(temp_img_path, 'PNG')
        img.close()
        
        # Create PDF with reportlab
        c = pdf_canvas.Canvas(pdf_path, pagesize=A4)
        page_width, page_height = A4
        
        # Calculate dimensions to fit image in A4
        img_aspect = img_width / img_height
        page_aspect = page_width / page_height
        
        if img_aspect > page_aspect:
            # Image is wider
            width = page_width
            height = page_width / img_aspect
        else:
            # Image is taller
            height = page_height
            width = page_height * img_aspect
        
        # Center the image
        x = (page_width - width) / 2
        y = (page_height - height) / 2
        
        c.drawImage(temp_img_path, x, y, width, height)
        c.save()
        
        # Clean up temp image
        try:
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)
        except Exception as cleanup_error:
            print(f"Warning: Could not delete temp file: {cleanup_error}")
        
        print(f"Sending PDF file: {pdf_path}")
        return send_file(pdf_path, as_attachment=True, download_name=f'dashboard-{file_name}.pdf')
    
    except Exception as e:
        print(f"!!! ERROR generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)