import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
from main.backend.utils.modelhelper_code_alignment import aligner
from main.backend.utils.modelhelper_docstring_gen import generating_docstring
from pathlib import Path
import os
logo_path = os.path.join(Path(__file__).parts[0], "resources" , "logo.png")
# Page config
st.set_page_config(page_title="DocuMentor",page_icon= logo_path)

# Load logo (ensure it's in correct path)

if os.path.exists(logo_path):
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image(logo_path, width=100)
    with col_title:
        st.markdown("<h1 style='padding-top: 12px; margin-left: -20px;font-size: 5rem;'>DocuMentor</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1>DocuMentor</h1>", unsafe_allow_html=True)

# Upload Section
st.markdown("Upload Your Python Code")
uploaded_file = st.file_uploader(
    "Drag and drop or browse to upload your .py file",
    type=["py"],
    label_visibility= 'collapsed'
)
# Action Buttons
if uploaded_file:
    with open('file.py', 'wb') as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)
    with col1:
        alignment = st.button("🔍 Code Comment Alignment", use_container_width=True)

    with col2:
        doc = st.button("📄 Docstring Generator", use_container_width=True)

    if alignment:
        df = aligner('file.py')
        st.markdown("<h2 style='text-align: center;'>🔍 Code-Comment Alignment Results</h2>", unsafe_allow_html=True)
        st.markdown("---")

        if df is not None:
            for i, row in df.iterrows():
                with st.expander(f"🔹 Function {int(i) + 1}", expanded=False):
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.markdown("**🧠 Code:**")
                        st.code(row['Code'], language='python')

                    with col2:
                        st.markdown("**💬 Comment:**")
                        st.markdown(f"`{row['Comment']}`")

                    # Alignment Status
                    status = row['Labels']
                    if status == "Aligned":
                        st.badge(f"**Status:** {status}", color='green')
                    else:
                        st.badge(f"**Status:** {status}", color='red')
            os.remove('file.py')
        else:
            st.markdown("<h2 style='text-align: center;'>No Code-Comment Pair Found</h2>", unsafe_allow_html=True)
    elif doc:
        df = generating_docstring('file.py')
        st.subheader("📂 Function Viewer")
        for i, row in df.iterrows():
            with st.container():
                tab1, tab2 = st.tabs(["🧠 Code", "📄 Docstring"])
                with tab1:
                    st.code(row['Code'], language='python')
                with tab2:
                    st.markdown(f"```python\n{row['DocString']}\n```")
        os.remove('file.py')




else:
    st.info("Please upload a `.py` file to get started.")




