import streamlit as st
import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from setup import setup
setup()
from agent import run_agent

st.set_page_config(
    page_title="Inventory Management Agent",
    page_icon="📦",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
    }
    .tech-badge {
        display: inline-block;
        background: #1e3a5f;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 3px;
        font-weight: 500;
    }
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .test-case-btn {
        width: 100%;
        text-align: left;
    }
    .section-header {
        font-size: 14px;
        font-weight: 600;
        color: #1e3a5f;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 4px;
        border-bottom: 2px solid #2d6a9f;
    }
    .chat-container {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        min-height: 400px;
        background: #fafafa;
    }
    .stChatMessage {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 2rem;">📦 Inventory Management Agent</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem;">
        Autonomous AI agent for warehouse management using natural language
    </p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_query" not in st.session_state:
    st.session_state.quick_query = None

def get_db_stats():
    try:
        conn = sqlite3.connect("data/inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(quantity * price) FROM products")
        value = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= reorder_level")
        low = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT category) FROM products")
        cats = cursor.fetchone()[0]
        conn.close()
        return total, value, low, cats
    except:
        return 0, 0, 0, 0

total, value, low, cats = get_db_stats()

st.markdown('<p class="section-header">Warehouse Overview</p>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Products", total)
with m2:
    st.metric("Inventory Value", f"${value:,.2f}")
with m3:
    st.metric("Low Stock Alerts", low, delta=f"-{low} need reorder" if low > 0 else None, delta_color="inverse")
with m4:
    st.metric("Categories", cats)

st.markdown("---")

left_col, mid_col, right_col = st.columns([1.2, 2, 1.2])

with left_col:
    st.markdown('<p class="section-header">Test Cases</p>', unsafe_allow_html=True)

    test_cases = {
        "Semantic Search (RAG)": [
            "Do we have any 220V compatible equipment?",
            "Find chemical resistant safety gear",
            "Show me heavy duty storage solutions",
            "Any equipment for electrical work?",
        ],
        "Check Stock": [
            "How many fire extinguishers do we have?",
            "Check stock for forklift battery",
            "What is the quantity of safety helmets?",
            "Check hydraulic jack inventory",
        ],
        "Inventory Updates": [
            "Add 20 units of safety helmets",
            "Remove 5 units of hydraulic jack",
            "Add 50 units of pallet wrap",
            "Remove 2 units of conveyor belt",
        ],
        "Reports & Alerts": [
            "Generate a full inventory report",
            "Which products need to be reordered?",
            "Show me all low stock items",
            "What is the total inventory value?",
        ],
        "Edge Cases": [
            "Do we have any laptops?",
            "Remove 1000 units of safety helmets",
            "Check stock for iPhone",
            "Find 500V industrial equipment",
        ],
    }

    for category, queries in test_cases.items():
        with st.expander(f"**{category}**", expanded=category == "Semantic Search (RAG)"):
            for query in queries:
                if st.button(query, key=f"test_{query}", use_container_width=True):
                    st.session_state.quick_query = query

with mid_col:
    st.markdown('<p class="section-header">Chat with Agent</p>', unsafe_allow_html=True)

    chat_container = st.container(height=480)
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style='text-align:center; padding: 3rem 1rem; color: #888;'>
                <div style='font-size: 3rem;'>📦</div>
                <p style='font-size: 1rem; margin-top: 0.5rem;'>
                    Ask me anything about your warehouse inventory!
                </p>
                <p style='font-size: 0.85rem;'>
                    Try a test case from the left panel or type your own query below.
                </p>
            </div>
            """, unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    user_input = st.chat_input("Ask about your inventory...")

    if st.session_state.quick_query:
        user_input = st.session_state.quick_query
        st.session_state.quick_query = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                with st.spinner("Agent thinking..."):
                    response = run_agent(user_input)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    if st.session_state.messages:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

with right_col:
    st.markdown('<p class="section-header">Tech Stack</p>', unsafe_allow_html=True)

    tech_stack = {
        "LLM": ("🤖", "Groq Llama 3.3 70B", "Fast free inference"),
        "Framework": ("⛓️", "LangChain", "Agent orchestration"),
        "Vector DB": ("🔍", "ChromaDB", "Semantic search"),
        "Embeddings": ("📐", "MiniLM-L6-v2", "Local embeddings"),
        "Database": ("🗄️", "SQLite", "Inventory storage"),
        "UI": ("🎨", "Streamlit", "Web interface"),
        "Container": ("🐳", "Docker Compose", "Deployment"),
        "Fine-tuning": ("🎯", "Prompt Engineering", "No GPU needed"),
    }

    for component, (icon, name, desc) in tech_stack.items():
        st.markdown(f"""
        <div style="background: #f8f9fa; border-left: 3px solid #2d6a9f;
                    border-radius: 6px; padding: 8px 12px; margin-bottom: 8px;">
            <div style="font-size: 12px; color: #888;">{component}</div>
            <div style="font-weight: 600; font-size: 14px;">{icon} {name}</div>
            <div style="font-size: 12px; color: #666;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">How It Works</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 13px; color: #444; line-height: 1.8;">
        1. Your query hits the <b>LangChain Agent</b><br>
        2. Agent picks the right <b>tool</b> to call<br>
        3. <b>RAG pipeline</b> does semantic search<br>
        4. <b>SQLite</b> handles stock operations<br>
        5. <b>Memory</b> tracks conversation context<br>
        6. Response returned in natural language
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">Available Tools</p>', unsafe_allow_html=True)
    tools_info = [
        ("check_stock", "Query stock levels"),
        ("update_inventory", "Add or remove units"),
        ("generate_report", "Full warehouse report"),
        ("semantic_search", "RAG-powered search"),
    ]
    for tool_name, tool_desc in tools_info:
        st.markdown(f"""
        <div style="margin-bottom: 6px;">
            <code style="background:#e8f0fe; color:#1e3a5f;
                         padding: 2px 6px; border-radius: 4px;
                         font-size: 12px;">{tool_name}</code>
            <span style="font-size: 12px; color: #666; margin-left: 6px;">{tool_desc}</span>
        </div>
        """, unsafe_allow_html=True)