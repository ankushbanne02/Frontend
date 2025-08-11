import json
import os
import re
from dotenv import load_dotenv
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from config import ConfigData
import markdown
from dash import no_update

# === Load environment variables ===
load_dotenv()

# === Load JSON data ===
with open("FG.json") as f:
    data = json.load(f)

# === Initialize LLM ===
llm = AzureChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

# === Prompts ===
table_schema = ConfigData.TABLE_SCHEMA
schema_description = ConfigData.SCHEMA_DESCRIPTION

code_prompt = PromptTemplate(
    template="""
You are an expert Python developer working with structured JSON data.

The data is loaded in a Python list of dictionaries stored in a variable called `data`.

Your task:
- Read the user question.
- Identify the relevant fields from the schema.
- Write a **pure Python code snippet** that stores the answer in a variable named `result` and then prints it using `print(result)`.

⚠️ Constraints:
- Do NOT return any markdown (like ```python).
- Do NOT include comments or extra text.
- Your output must be **only Python code** using `result = ...` followed by `print(result)`

Table Schema:
{table_schema}

Schema Description:
{schema_description}

User Question: {user_question}
""",
    input_variables=["user_question"],
)

summary_prompt = PromptTemplate(
    template="""
You are a helpful assistant that summarizes code results in natural language.

Given:
- The user's original question
- The Python code that was generated and executed
- The value of the variable `result` after execution

You can refer following the following mapping to number to its meaning and when the filds are valid and values. you can consider only fileds that are metioned in genarted code or result to mapping 
mapping:
{schema_description}
Your task:
- Return a clear, helpful natural language answer to the user's question based on the result.
- Keep it simple structured and non-technical.

User Question:
{user_question}

Generated Code:
{code}

Execution Result (stored in variable `result`):
{result}
""",
    input_variables=["user_question", "code", "result", "schema_description"],
)

# === Bind chains ===
code_chain = code_prompt.partial(
    table_schema=table_schema,
    schema_description=schema_description,
) | llm

summary_chain = summary_prompt | llm


# === Chat UI helper ===
def format_chat(history):
    chat_bubbles = []
    for entry in history:
        role = entry["role"]
        text = entry["text"]

        if role == "bot":
            chat_bubbles.append(
                html.Div([
                    html.Strong("Assistant:", style={"color": "#28a745"}),
                    html.Div(dcc.Markdown(text, dangerously_allow_html=True))
                ], style={
                    "marginBottom": "10px",
                    "backgroundColor": "#e9f7ef",
                    "padding": "10px",
                    "borderRadius": "5px"
                })
            )
        else:
            chat_bubbles.append(
                html.Div([
                    html.Strong("You:", style={"color": "#007bff"}),
                    html.Div(text, style={"paddingLeft": "10px"})
                ], style={"marginBottom": "10px"})
            )
    return chat_bubbles


# === Layout for Chatbot Page ===
chatbot_layout = dbc.Container([
    html.H2("📦 Smart Parcel Chat Assistant", className="mt-3 mb-2 text-center text-primary"),

    dcc.Store(id="chat-history", data=[]),

    html.Div([
        html.Div(id="chat-window", style={
            "height": "70vh",
            "overflowY": "auto",
            "border": "1px solid #ddd",
            "padding": "15px",
            "borderRadius": "10px",
            "backgroundColor": "#fff",
        }),
        html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Input(
                        id="question-input",
                        placeholder="Ask a question about parcel logs...",
                        style={"width": "100%", "padding": "10px", "fontSize": "16px"},
                    )
                ], width=10),
                dbc.Col([
                    dbc.Button("Send", id="run-button", color="primary", className="w-100")
                ], width=2)
            ], className="g-2")
        ], style={
            "position": "sticky",
            "bottom": "0",
            "backgroundColor": "#f8f9fa",
            "padding": "10px",
            "zIndex": "999"
        })
    ])
], fluid=True)


# === Callback Registration ===
def register_chatbot_callbacks(app):
    @app.callback(
        Output("chat-window", "children"),
        Output("chat-history", "data"),
        Input("run-button", "n_clicks"),
        State("question-input", "value"),
        State("chat-history", "data"),
        prevent_initial_call=True
    )
    def handle_chat(n_clicks, question, history):
        if not question:
            return html.Div("❗ Please enter a question."), history

        # Step 1: Generate Python code
        code_resp = code_chain.invoke({"user_question": question})
        code = code_resp.content if hasattr(code_resp, "content") else code_resp.get("text", "")
        code = re.sub(r"```(?:python)?", "", code).strip("` \n")

        print("\n🔧 Generated Code from LLM:\n", code)

        # Step 2: Execute code
        local_vars = {"data": data}
        try:
            exec(code, {}, local_vars)
            result = local_vars.get("result")
        except Exception as e:
            history.append({"role": "user", "text": question})
            history.append({"role": "bot", "text": f"❌ Error executing code: {e}"})
            return format_chat(history), history

        # Step 3: Generate summary
        summary_resp = summary_chain.invoke({
            "user_question": question,
            "code": code,
            "result": result,
            "schema_description": schema_description
        })
        summary = summary_resp.content if hasattr(summary_resp, "content") else summary_resp.get("text", "")

        # Update history
        history.append({"role": "user", "text": question})
        history.append({"role": "bot", "text": f"💬 Summary:\n\n{summary}"})

        return format_chat(history), history
