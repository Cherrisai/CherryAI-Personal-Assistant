"""
CherryAI 🍒 - Personal AI Assistant
Single-file Streamlit app for Hugging Face Spaces
"""
import streamlit as st
import os
import uuid
import tempfile
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

# ─── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="CherryAI",
    page_icon="🍒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

.stApp {
    background-color: #0f0f0f;
    color: #e8e8e8;
}

[data-testid="stSidebar"] {
    background-color: #141414;
    border-right: 1px solid #222;
}

.main .block-container {
    max-width: 820px;
    padding: 1rem 1.5rem 7rem;
    margin: 0 auto;
}

/* User message */
.user-msg {
    display: flex;
    justify-content: flex-end;
    margin: 1.2rem 0;
}
.user-bubble {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    color: #e8e8e8;
    padding: 0.85rem 1.15rem;
    border-radius: 16px 16px 3px 16px;
    max-width: 78%;
    font-size: 0.93rem;
    line-height: 1.65;
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* AI message */
.ai-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin: 1.2rem 0;
}
.cherry-logo-small {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #8b0000, #cc2200);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 3px;
    box-shadow: 0 2px 8px rgba(180,30,0,0.4);
}
.ai-content {
    color: #e8e8e8;
    font-size: 0.93rem;
    line-height: 1.75;
    max-width: 88%;
}

/* Buttons */
.stButton button {
    background: #8b0000;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    transition: all 0.2s;
}
.stButton button:hover {
    background: #b30000;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(139,0,0,0.4);
}

/* Input */
.stChatInput > div {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 14px !important;
}
.stChatInput textarea {
    color: #e8e8e8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Text inputs */
.stTextInput input, .stTextArea textarea {
    background: #1a1a1a !important;
    color: #e8e8e8 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Select */
[data-baseweb="select"] {
    background: #1a1a1a !important;
}
[data-baseweb="select"] * {
    background: #1a1a1a !important;
    color: #e8e8e8 !important;
    border-color: #2a2a2a !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #141414;
    border-radius: 10px;
    padding: 3px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    color: #888;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #8b0000 !important;
    color: white !important;
}

/* Code */
code {
    font-family: 'DM Mono', monospace !important;
    background: #1a1a1a !important;
    border-radius: 4px;
    padding: 0.15em 0.4em;
    font-size: 0.85em;
}
pre {
    background: #141414 !important;
    border: 1px solid #222 !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #141414;
    border: 2px dashed #2a2a2a;
    border-radius: 12px;
}

/* Sidebar labels */
[data-testid="stSidebar"] label {
    color: #888 !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #888;
    font-size: 0.82rem;
}

/* Download button */
.stDownloadButton button {
    background: #0d3d6e !important;
    color: white !important;
}
.stDownloadButton button:hover {
    background: #1259a0 !important;
}

/* Welcome cards */
.welcome-wrap {
    text-align: center;
    padding: 2.5rem 0 2rem;
}
.welcome-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #e8e8e8;
    letter-spacing: -0.5px;
}
.welcome-sub {
    color: #666;
    font-size: 0.9rem;
    margin-top: 0.3rem;
    margin-bottom: 2rem;
}
.sugg-btn {
    background: #141414;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: left;
    color: #aaa;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 0.5rem;
}

/* Footer */
.cherry-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0f0f0f;
    border-top: 1px solid #1a1a1a;
    padding: 0.5rem 0;
    text-align: center;
    font-size: 0.72rem;
    color: #333;
    z-index: 999;
    letter-spacing: 0.5px;
}
.cherry-footer span {
    color: #8b0000;
    font-weight: 600;
}

hr { border-color: #1e1e1e !important; }
</style>
""", unsafe_allow_html=True)


# ─── AI Providers ─────────────────────────────────────────
SYSTEM_PROMPT = """You are CherryAI, an expert personal AI assistant.

You excel at:
- Answering ANY question with depth and accuracy
- Writing perfect, working code in ANY programming language
- Fixing bugs with clear explanations
- Creating any type of file or document
- Explaining complex topics simply

Response style:
- Always clear, structured, and easy to read
- Use markdown formatting (headers, code blocks, bullet points)
- Code always inside proper ```language blocks
- Be concise yet comprehensive
- Friendly, helpful and encouraging"""


def get_available_provider():
    def is_set(k):
        v = os.getenv(k, "")
        return bool(v and "your_" not in v and len(v) > 10)
    if is_set("GROQ_API_KEY"):
        return "groq"
    if is_set("GEMINI_API_KEY"):
        return "gemini"
    if is_set("OPENAI_API_KEY"):
        return "openai"
    return "none"


def get_ai_response(message, history=None, provider=None, model=None, temperature=0.7):
    history = history or []
    if not provider or provider == "auto":
        provider = get_available_provider()

    if provider == "none":
        return ("⚠️ **No API key configured!**\n\n"
                "Add your free Groq key:\n"
                "- Get it FREE at https://console.groq.com\n"
                "- Add `GROQ_API_KEY` in HF Space secrets\n")

    try:
        if provider == "groq":
            return _groq(message, history, model, temperature)
        elif provider == "gemini":
            return _gemini(message, history, model, temperature)
        elif provider == "openai":
            return _openai(message, history, model, temperature)
    except Exception as e:
        return f"❌ Error: {str(e)}"


def _groq(message, history, model, temperature):
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = model or "llama-3.3-70b-versatile"
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.extend(history[-20:])
    msgs.append({"role": "user", "content": message})
    r = client.chat.completions.create(model=model, messages=msgs,
                                        temperature=temperature, max_tokens=4096)
    return r.choices[0].message.content


def _gemini(message, history, model, temperature):
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    m = genai.GenerativeModel(model or "gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
    hist = [{"role": "user" if h["role"] == "user" else "model",
             "parts": [h["content"]]} for h in history[-20:]]
    chat = m.start_chat(history=hist)
    r = chat.send_message(message,
                          generation_config={"temperature": temperature, "max_output_tokens": 4096})
    return r.text


def _openai(message, history, model, temperature):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.extend(history[-20:])
    msgs.append({"role": "user", "content": message})
    r = client.chat.completions.create(model=model or "gpt-4o-mini",
                                        messages=msgs, temperature=temperature, max_tokens=4096)
    return r.choices[0].message.content


# ─── Web Search ───────────────────────────────────────────
def search_web(query, max_results=5):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return ""
        out = []
        for i, r in enumerate(results, 1):
            out.append(f"[{i}] {r.get('title','')}\n{r.get('body','')}\nSource: {r.get('href','')}")
        return "\n\n".join(out)
    except Exception as e:
        return ""


# ─── File Reader ──────────────────────────────────────────
def read_file(file_obj):
    name = file_obj.name
    ext = Path(name).suffix.lower()
    try:
        if ext in [".txt", ".md", ".py", ".js", ".ts", ".html", ".css",
                   ".java", ".cpp", ".c", ".go", ".rs", ".php", ".sh",
                   ".sql", ".json", ".xml", ".yaml", ".yml", ".csv"]:
            return file_obj.read().decode("utf-8", errors="replace")
        elif ext == ".pdf":
            import PyPDF2
            reader = PyPDF2.PdfReader(file_obj)
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        elif ext in [".docx"]:
            from docx import Document
            doc = Document(file_obj)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        elif ext in [".xlsx"]:
            import openpyxl
            wb = openpyxl.load_workbook(file_obj, read_only=True, data_only=True)
            rows = []
            for ws in wb.worksheets:
                rows.append(f"=== {ws.title} ===")
                for row in ws.iter_rows(max_row=100, values_only=True):
                    rows.append(" | ".join(str(c) if c else "" for c in row))
            return "\n".join(rows)
        else:
            return f"[File: {name}] — uploaded successfully."
    except Exception as e:
        return f"Could not read file: {str(e)}"


# ─── File Generator ───────────────────────────────────────
FILE_TYPES = {
    "py": "python", "js": "javascript", "ts": "typescript",
    "jsx": "jsx", "tsx": "tsx", "html": "html", "css": "css",
    "java": "java", "cpp": "cpp", "c": "c", "cs": "csharp",
    "go": "go", "rs": "rust", "php": "php", "rb": "ruby",
    "swift": "swift", "kt": "kotlin", "sql": "sql", "sh": "bash",
    "json": "json", "xml": "xml", "yaml": "yaml", "csv": "csv",
    "md": "markdown", "txt": "text", "r": "r",
}

def generate_code_file(prompt, ext, provider=None, temperature=0.3):
    lang = FILE_TYPES.get(ext, ext)
    doc_types = ["md", "txt", "csv", "json", "xml", "yaml"]
    if ext in doc_types:
        ai_prompt = f"Create a complete {lang} file for:\n{prompt}\n\nReturn ONLY the raw content, no code blocks."
    else:
        ai_prompt = (f"Write complete, production-ready {lang} code for:\n{prompt}\n\n"
                     f"Include all imports, comments, error handling.\n"
                     f"Return ONLY the code inside a ```{lang} code block.")
    raw = get_ai_response(ai_prompt, provider=provider, temperature=temperature)
    import re
    for pat in [rf'```{lang}\n(.*?)```', r'```\w*\n(.*?)```', r'```\n(.*?)```']:
        m = re.search(pat, raw, re.DOTALL)
        if m:
            return m.group(1).strip()
    return raw.strip()


# ─── Session State ────────────────────────────────────────
def init():
    defaults = {
        "messages": [], "provider": "auto", "model": None,
        "web_search": False, "temperature": 0.7,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()


# ─── Sidebar ─────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:0.5rem 0 1.2rem;text-align:center;">
            <div style="font-size:1.4rem;font-weight:700;color:#e8e8e8;letter-spacing:-0.5px;">CherryAI</div>
            <div style="font-size:0.72rem;color:#555;margin-top:2px;">Personal AI Assistant</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown("**Settings**")

        provider_map = {
            "auto": "Auto-Select",
            "groq": "Groq (FREE)",
            "gemini": "Gemini (FREE)",
            "openai": "OpenAI (Paid)",
        }
        sel = st.selectbox("Provider", list(provider_map.keys()),
                           format_func=lambda x: provider_map[x])
        st.session_state.provider = sel

        if sel == "groq":
            m = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"])
            st.session_state.model = m
        elif sel == "gemini":
            m = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
            st.session_state.model = m
        else:
            st.session_state.model = None

        temp = st.slider("Creativity", 0.0, 1.0, st.session_state.temperature, 0.1)
        st.session_state.temperature = temp

        ws = st.toggle("Web Search", value=st.session_state.web_search,
                       help="Search web for current info")
        st.session_state.web_search = ws

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", len(st.session_state.messages))
        with col2:
            u = sum(1 for m in st.session_state.messages if m["role"] == "user")
            st.metric("Asked", u)

        st.markdown("---")
        with st.expander("API Key Setup"):
            st.markdown("""
**Free Groq Key:**
1. [console.groq.com](https://console.groq.com)
2. Sign up → Create Key
3. Add to HF Secrets:
   `GROQ_API_KEY = your_key`
            """)


# ─── Render Messages ──────────────────────────────────────
def render_msg(role, content):
    if role == "user":
        st.markdown(f'<div class="user-msg"><div class="user-bubble">{content}</div></div>',
                    unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([0.045, 0.955])
        with col1:
            st.markdown('<div class="cherry-logo-small">🍒</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(content)


# ─── Welcome Screen ───────────────────────────────────────
def welcome():
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-title">Welcome to CherryAI</div>
        <div class="welcome-sub">Ask anything. Generate any file. Fix any code.</div>
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "Write a Python Flask REST API with CRUD operations",
        "Explain how machine learning works simply",
        "Fix my code bugs and optimize performance",
        "Create a responsive HTML landing page",
        "Write a SQL query to find top customers",
        "Explain Big O notation with examples",
    ]

    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(s[:52] + ("..." if len(s) > 52 else ""),
                         use_container_width=True, key=f"s{i}"):
                st.session_state["_prefill"] = s
                st.rerun()


# ─── Chat Tab ────────────────────────────────────────────
def chat_tab():
    for m in st.session_state.messages:
        render_msg(m["role"], m["content"])

    if not st.session_state.messages:
        welcome()

    prefill = st.session_state.pop("_prefill", None)
    user_input = st.chat_input("Message CherryAI...")
    if prefill:
        user_input = prefill

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_msg("user", user_input)

        with st.spinner("Thinking..."):
            search_ctx = ""
            if st.session_state.web_search:
                search_ctx = search_web(user_input)
                if search_ctx:
                    search_ctx = f"\n\n[WEB SEARCH RESULTS]\n{search_ctx}\n[END]\n\n"

            full_msg = search_ctx + user_input
            history = st.session_state.messages[:-1]
            provider = st.session_state.provider if st.session_state.provider != "auto" else None

            response = get_ai_response(
                message=full_msg,
                history=history,
                provider=provider,
                model=st.session_state.model,
                temperature=st.session_state.temperature,
            )

        if search_ctx:
            response = "🌐 *Web search used*\n\n" + response

        st.session_state.messages.append({"role": "assistant", "content": response})
        render_msg("assistant", response)
        st.rerun()


# ─── Generate File Tab ────────────────────────────────────
def generate_tab():
    st.markdown("### Generate Any File")
    st.markdown("Describe what you want — CherryAI writes the complete file.")

    col1, col2 = st.columns([3, 1])
    with col1:
        prompt = st.text_area("Describe the file", height=110,
                               placeholder="e.g. A Python FastAPI server with JWT authentication and user CRUD")
    with col2:
        ext = st.selectbox("Type", list(FILE_TYPES.keys()))
        fname = st.text_input("Filename", placeholder=f"my_file.{ext}")

    if st.button("Generate File", use_container_width=True, type="primary"):
        if not prompt.strip():
            st.warning("Please describe what you want.")
        else:
            with st.spinner(f"Generating {ext.upper()} file..."):
                provider = st.session_state.provider if st.session_state.provider != "auto" else None
                content = generate_code_file(prompt, ext, provider=provider)
                final_name = fname if fname else f"cherryai_output.{ext}"
                if not final_name.endswith(f".{ext}"):
                    final_name += f".{ext}"

            lines = content.count('\n') + 1
            st.success(f"Generated: **{final_name}** — {lines} lines")
            st.code(content, language=FILE_TYPES.get(ext, ext))
            st.download_button(
                f"Download {final_name}",
                data=content,
                file_name=final_name,
                mime="text/plain",
                use_container_width=True,
            )


# ─── Code Tools Tab ───────────────────────────────────────
def code_tab():
    st.markdown("### Code Tools")

    col1, col2 = st.columns([4, 1])
    with col1:
        code = st.text_area("Paste your code", height=260,
                             placeholder="Paste any code here...")
    with col2:
        langs = ["python", "javascript", "typescript", "java", "cpp",
                 "c", "go", "rust", "php", "ruby", "sql", "bash", "html", "css"]
        lang = st.selectbox("Language", langs)
        task = st.selectbox("Task", ["fix", "explain", "optimize", "document"])
        labels = {"fix": "Fix all bugs", "explain": "Explain clearly",
                  "optimize": "Optimize speed", "document": "Add docs"}
        st.caption(labels[task])

    if st.button("Run", use_container_width=True, type="primary"):
        if not code.strip():
            st.warning("Paste some code first.")
        else:
            task_prompts = {
                "fix": f"Fix ALL bugs in this {lang} code. Return corrected code + explanation:\n\n```{lang}\n{code}\n```",
                "explain": f"Explain this {lang} code step-by-step clearly:\n\n```{lang}\n{code}\n```",
                "optimize": f"Optimize this {lang} code. Return improved code + what changed:\n\n```{lang}\n{code}\n```",
                "document": f"Add comprehensive comments/docstrings to this {lang} code:\n\n```{lang}\n{code}\n```",
            }
            with st.spinner("Analyzing..."):
                provider = st.session_state.provider if st.session_state.provider != "auto" else None
                result = get_ai_response(task_prompts[task], provider=provider)
            st.markdown("### Result")
            st.markdown(result)


# ─── Analyze File Tab ─────────────────────────────────────
def analyze_tab():
    st.markdown("### Analyze Any File")
    st.markdown("Upload PDF, Word, Excel, code, CSV — ask anything about it.")

    uploaded = st.file_uploader(
        "Upload a file",
        type=["pdf", "docx", "txt", "py", "js", "html", "css", "csv",
              "xlsx", "json", "xml", "yaml", "md", "java", "cpp", "sql"],
    )
    question = st.text_input("Your question", value="Summarize and analyze this file in detail.")

    if uploaded and st.button("Analyze", use_container_width=True, type="primary"):
        with st.spinner(f"Reading {uploaded.name}..."):
            content = read_file(uploaded)
            prompt = f"File: {uploaded.name}\n\nContent:\n{content[:8000]}\n\nQuestion: {question}"
            provider = st.session_state.provider if st.session_state.provider != "auto" else None
            result = get_ai_response(prompt, provider=provider)
        st.success(f"Analyzed: {uploaded.name}")
        st.markdown("### Result")
        st.markdown(result)


# ─── Footer ───────────────────────────────────────────────
def footer():
    st.markdown("""
    <div class="cherry-footer">
        🍒 &nbsp; © 2026 <span>CherryAI</span> &nbsp;·&nbsp; All rights reserved
    </div>
    """, unsafe_allow_html=True)


# ─── Main ────────────────────────────────────────────────
def main():
    sidebar()

    st.markdown("""
    <div style="text-align:center;padding:0.6rem 0 0.8rem;border-bottom:1px solid #1a1a1a;margin-bottom:1rem;">
        <span style="font-size:1rem;font-weight:600;color:#e8e8e8;letter-spacing:-0.3px;">CherryAI</span>
        <span style="font-size:0.72rem;color:#444;margin-left:0.6rem;">Personal AI Assistant</span>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["Chat", "Generate File", "Code Tools", "Analyze File"])
    with tabs[0]: chat_tab()
    with tabs[1]: generate_tab()
    with tabs[2]: code_tab()
    with tabs[3]: analyze_tab()

    footer()


if __name__ == "__main__":
    main()
