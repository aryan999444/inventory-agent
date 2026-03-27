import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from prompts import SYSTEM_PROMPT
from tools import check_stock, update_inventory, generate_report, semantic_search

load_dotenv()

def get_api_key():
    return os.getenv("GROQ_API_KEY")

@tool
def check_stock_tool(product_name: str) -> str:
    """Check the current stock level of a product by name."""
    return check_stock(product_name)

@tool
def update_inventory_tool(product_name: str, quantity_change: int) -> str:
    """Update inventory for a product. Use positive numbers to add stock, negative to remove."""
    return update_inventory(product_name, quantity_change)

@tool
def generate_report_tool(query: str = "full") -> str:
    """Generate a full inventory status report including low stock alerts. Pass any string to trigger it."""
    return generate_report()

@tool
def semantic_search_tool(query: str) -> str:
    """Search for products using natural language. Use this for descriptive queries."""
    return semantic_search(query)

tools = [
    check_stock_tool,
    update_inventory_tool,
    generate_report_tool,
    semantic_search_tool,
]

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

_agent_executor = None

def get_agent_executor():
    global _agent_executor
    if _agent_executor is None:
        api_key = get_api_key()
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=api_key,
            temperature=0,
        )
        agent = create_tool_calling_agent(llm, tools, prompt)
        _agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            max_execution_time=30,
        )
    return _agent_executor

def run_agent(user_input: str) -> str:
    try:
        executor = get_agent_executor()
        response = executor.invoke({"input": user_input})
        output = response.get("output", "")
        if not output or "Agent stopped" in output:
            return semantic_search(user_input)
        return output
    except TypeError as e:
        if "NoneType" in str(e):
            return generate_report()
        return f"Error: {str(e)}"
    except Exception as e:
        if "Agent stopped" in str(e):
            return semantic_search(user_input)
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Inventory Agent ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = run_agent(user_input)
        print(f"\nAgent: {response}\n")