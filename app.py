import streamlit as st
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv

# =========================
# Load environment variables
# =========================
load_dotenv()

# =========================
# Configure Gemini API
# =========================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Supported & stable model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="SQL LLM Application", page_icon="🧠")
st.title("🧠 SQL LLM Application")
st.write("Ask questions in English. The AI will convert them into SQL and fetch results.")

question = st.text_input("Enter your question")

# =========================
# Database execution function
# =========================
def run_sql(sql_query):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    conn.close()
    return data

# =========================
# Button action
# =========================
if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        prompt = f"""
Convert the following English question into an SQL query.

Table name: students
Columns:
- id
- name
- marks

Question: {question}

Return ONLY the SQL query. No explanation. No markdown.
"""

        try:
            # Generate SQL using Gemini
            response = model.generate_content(prompt)

            # ✅ CLEAN MARKDOWN SQL
            sql_query = response.text.strip()
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            # ✅ SAFETY CHECK (READ-ONLY)
            if not sql_query.lower().startswith("select"):
                st.error("Only SELECT queries are allowed.")
                st.stop()

            # Show generated SQL
            st.subheader("Generated SQL")
            st.code(sql_query, language="sql")

            # Execute SQL
            result = run_sql(sql_query)

            # Show result
            st.subheader("Result")
            if result:
                st.write(result)
            else:
                st.info("No records found.")

        except Exception as e:
            st.error(f"Error: {e}")