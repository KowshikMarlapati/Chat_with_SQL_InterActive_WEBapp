import os
import streamlit as st
# from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from urllib.parse import quote_plus
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
import json
from dotenv import load_dotenv
load_dotenv()



# ---------------- DATABASE CONNECTION ---------------- #

def connectDatabase(username, port, host, password, database):
    port = int(port)
    safe_password = quote_plus(password)

    mysql_uri = (
        f"mysql+mysqlconnector://{username}:{safe_password}"
        f"@{host}:{port}/{database}"
    )

    db = SQLDatabase.from_uri(mysql_uri)

    st.session_state.db = db
    st.session_state.schema = db.get_table_info()  


# ---------------- QUERY EXECUTION ---------------- #

@st.cache_data
def runQuery(query):
    return st.session_state.db.run(query) if st.session_state.db else "Please connect to database"

def extract_value(result):
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], tuple):
            return result[0][0]
    return result

def getDatabaseSchema():
    return st.session_state.schema if "schema" in st.session_state else "Please connect"


# ---------------- FAST LLM MODEL ---------------- #



llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("api_key_grok_1"),
    temperature=0
)


# ---------------- CLEAN SQL ---------------- #

import re

def clean_sql(query):
    
    query = query.replace("```sql", "")
    query = query.replace("```", "")


    query = query.replace("SQL query:", "")
    query = query.replace("SQL Query:", "")
    query = query.replace("The corrected SQL query is:", "")

    
    match = re.search(r"(SELECT .*?;|SELECT .*?$)", query, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).strip()

    return query.strip()


# ---------------- GENERATE SQL ---------------- #

def getQueryFromLLM(question):
    template = """below is the schema of MYSQL database, read the schema carefully about the table and column names. Also take care of table or column name case sensitivity.
    Finally answer user's question in the form of SQL query.

    {schema}
    
    please only provide the SQL query and nothing else
    
    

    for example:
    question: how many albums we have in database
    SQL query: SELECT COUNT(*) FROM album
    question: how many customers are from Brazil in the database ?
    SQL query: SELECT COUNT(*) FROM customer WHERE country=Brazil

    your turn :
    question: {question}
    SQL query :
    please only provide the SQL query and nothing else
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "schema": getDatabaseSchema()
    })

    query = clean_sql(response.content if hasattr(response, "content") else str(response))

    return query

def getResponseForQueryResult(question, query, result):

    template = """You are a helpful database assistant.
    Answer the user's question in clear natural language.
    Rules:
        - Do NOT mention SQL
        - Do NOT say "based on the SQL result"
        - Always respond in English only. Even if user asks in Another language .
        - Only give the final answer
    Question:{question}
    Result:{result}
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "query": query,
        "result": result
    })

    return response.content

# ---------------- STREAMLIT PAGE ---------------- #

st.set_page_config(
    page_icon="🤖",
    page_title="Chat with MYSQL DB",
    layout="centered"
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
        min-width: 240px;
        max-width: 240px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("""
    <style>
    [data-testid="stChatMessage"]{
        font-size:24px;
    }

    [data-testid="stMarkdownContainer"] p{
    f   ont-size:24px;
    }
    
    code{
        font-size:18px !important;
    }

    </style>
    """, unsafe_allow_html=True
)

st.title("🤖 Chat with MySQL Database")

question = st.chat_input("Ask something about your database")


if "chat" not in st.session_state:
    st.session_state.chat = []


# ---------------- HANDLE USER QUESTION ---------------- #

if question:

    if "db" not in st.session_state:
        st.error("Please connect to the database first.")

    else:

        st.session_state.chat.append({
            "role": "user",
            "content": question
        })

        query = getQueryFromLLM(question)
        print("Generated SQL:", query)
        try:
            result = runQuery(query)
        except Exception as e:
            print("SQL Error:", e)
            fix_prompt = f"""The following SQL query produced an error.
            query:
            {query}
            Fix the SQL query.
            Return only the corrected SQL query."""

            fix_response = llm.invoke(fix_prompt)
            fixed_query = clean_sql(fix_response.content if hasattr(fix_response, "content") else str(fix_response))
            print("Fixed SQL:", fixed_query)
            result = runQuery(fixed_query)
            query = fixed_query

        print("Query Result:", result)
        
        clean_result = extract_value(result)
        nl_response = getResponseForQueryResult(question, query, clean_result)
        
        st.session_state.chat.append({
        "role": "assistant",
        "content": nl_response,
        "sql": query
        })
        
       

        

# ---------------- DISPLAY CHAT ----------------

for chat in st.session_state.chat:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        if "sql" in chat:
            st.code(chat["sql"], language="sql")

with st.sidebar:
    st.title("Connect to Database")
    st.text_input("Host", key="host", value="localhost")
    st.text_input("Port", key="port", value="3306")
    st.text_input("Username", key="username", value="root")
    st.text_input("Password", key="password", type="password")
    st.text_input("Database", key="database", value="rag_test")
    connectBtn = st.button("Connect")

if connectBtn:

    connectDatabase(
        username=st.session_state.username,
        port=st.session_state.port,
        host=st.session_state.host,
        password=st.session_state.password,
        database=st.session_state.database,
    )

    st.success("Database connected successfully")