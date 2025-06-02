import os
import warnings
import json
import streamlit as st
import PyPDF2
import pandas as pd

from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.memory_manager import MemoryManager

# Suppress warnings and errors
os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"
warnings.filterwarnings("ignore", category=UserWarning)

st.title("Intelligent Document Routing System")

uploaded_file = st.file_uploader("Upload a document (PDF / JSON / Email)", type=["txt", "json", "pdf"])

if uploaded_file:
    file_name = uploaded_file.name
    file_ext = file_name.split(".")[-1].lower()

    # Save original uploaded file to data/input
    os.makedirs("data/input", exist_ok=True)
    with open(os.path.join("data/input", file_name), "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read file content
    if file_ext == "pdf":
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            file_content = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            st.error(f"❌ Error reading PDF: {e}")
            st.stop()
    else:
        try:
            file_content = uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            st.error("❌ File is not UTF-8 decodable.")
            st.stop()

    # Instantiate memory and agents
    memory = MemoryManager()
    classifier = ClassifierAgent(memory)
    email_agent = EmailAgent(memory)
    json_agent = JSONAgent(memory)

    # Classify format and intent
    format_type, intent = classifier.classify_and_route(file_content, file_ext, file_name)

    st.write(f"**Detected Format:** {format_type}")
    st.write(f"**Detected Intent:** {intent}")

    # Process with correct agent
    result = {}
    if format_type == "Email":
        result = email_agent.process_email(file_content, file_name)
        st.subheader("Extracted Email Metadata")
        st.json(result)

    elif format_type == "JSON":
        result = json_agent.process_json(file_content, file_name)
        st.subheader("Parsed JSON Content")
        st.json(result)

    # Save processed output to data/output
    os.makedirs("data/output", exist_ok=True)
    output_path = os.path.join("data/output", f"{file_name}.out.json")
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, indent=4)

    # Show memory log
    st.subheader("Memory Log")
    st.json(memory.get_memory())

    st.success("✅ Document processed successfully!")

    # Show download button for CSV memory log
    if os.path.exists("memory/memory_export.csv"):
        df = pd.read_csv("memory/memory_export.csv")
        st.download_button("📥 Download Memory Log (CSV)", df.to_csv(index=False), file_name="memory_log.csv")
        st.success("Memory log is ready for download.")
    else:
        st.warning("No memory log available for download yet. Process a document first.")

else:
    st.info("📂 Please upload a document to get started.")
