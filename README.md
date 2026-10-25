# LLM-Powered Natural Language Interface for Relational Databases

Query relational databases using natural language with Large Language Models (LLMs). This project explores how users can interact with structured data through conversational queries instead of writing SQL manually.

Built with Python, Streamlit, LangChain, Llama 3, Groq, and SQLAlchemy, the application translates natural-language questions into database queries and presents the results through an interactive web interface.

## Overview

Working with relational databases often requires users to understand SQL syntax, database schemas, and query construction. This can create a barrier for users who need insights from data but lack SQL expertise.

This project aims to simplify database interaction by providing a natural-language interface that connects user questions with relational database queries.

## Features

- **Natural Language Querying:** Ask questions about database records using everyday language.
- **LLM-Powered SQL Generation:** Use Llama 3 through the Groq API to interpret questions and assist with SQL query generation.
- **Relational Database Connectivity:** Work with SQLite and MySQL databases.
- **Interactive Web Interface:** Use Streamlit to submit questions and view query results.
- **Database Query Processing:** Leverage LangChain's SQL database integration to connect language models with relational data.
- **Extensible Architecture:** Build on the existing application to explore more complex SQL queries, analytics, and conversational database interactions.

## Technology Stack

| Component            | Technologies                             |
| -------------------- | ---------------------------------------- |
| Language             | Python                                   |
| Frontend             | Streamlit                                |
| LLM                  | Llama 3 via Groq API                     |
| LLM Framework        | LangChain                                |
| Database Integration | SQLAlchemy, LangChain SQL database tools |
| Databases            | SQLite, MySQL                            |
| Configuration        | Environment variables, python-dotenv     |

## Architecture

The application follows a natural-language-to-database workflow:

1. **User Input:** The user enters a question through the Streamlit interface.
2. **Language Model Processing:** The application uses LangChain and the configured LLM to interpret the question in the context of the database.
3. **SQL Query Generation:** The model generates an SQL query intended to answer the question.
4. **Database Interaction:** The application connects to the configured relational database and processes the query.
5. **Result Presentation:** The application displays the resulting data through the web interface.

```text
User
  |
  v
Streamlit Web Interface
  |
  v
LangChain + Llama 3 (Groq API)
  |
  v
SQL Query Generation
  |
  v
SQLAlchemy / Database Integration
  |
  v
SQLite or MySQL Database
  |
  v
Query Results
  |
  v
Streamlit Interface
```

## Getting Started

### Prerequisites

Before running the application, ensure you have:

- Python installed
- Git installed
- Access to a Groq API key
- SQLite or MySQL configured for your intended use case
- The database connection details required by your application

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace the placeholders with your GitHub repository URL and project directory name.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure your Groq API key and any database credentials required by your application.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

Add other variables using the names expected by your application's code.

**Important:** Never commit your `.env` file, API keys, database passwords, or private database contents to GitHub.

### 5. Run the Application

From the project directory, run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL in your terminal. Open that URL in your browser to interact with the application.

## Example Use Cases

Depending on the database schema and the application's implemented capabilities, natural-language questions can include:

- Retrieving records that match specific conditions
- Summarizing data using aggregate functions
- Grouping records by selected attributes
- Combining related tables through joins
- Filtering grouped results using conditions

For example, against a database with the appropriate schema:

> Show the total sales for each product category.

The application can use the question and database context to generate a corresponding SQL query.

## Security Considerations

LLM-generated SQL should be treated as untrusted input. Applications that execute generated queries should apply appropriate safeguards, including:

- Restricting database permissions to the minimum required.
- Validating generated SQL before execution.
- Preventing unauthorized data access.
- Avoiding unintended destructive operations.
- Keeping API keys and database credentials outside source control.
- Handling database errors without exposing sensitive information.

These are important considerations for making natural-language database interfaces safer and more reliable. The protections available in this project depend on the implementation.

## Future Improvements

Potential areas for further development include:

- Improving SQL generation for complex joins and nested queries.
- Adding automated tests for query correctness.
- Evaluating generated queries against expected results.
- Strengthening SQL validation and execution safeguards.
- Improving error handling and user feedback.
- Expanding support for database schemas and query patterns.
- Enhancing the interface for data exploration and analytics.

## Useful Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://docs.langchain.com/)
- [Groq API Documentation](https://console.groq.com/docs/overview)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## License and Attribution

This repository is distributed under the license included in the project. If this project is derived from an existing repository, retain the original license and applicable copyright notices, and clearly document your modifications and attribution.

---

**Developed as a project exploring LLM-powered interaction with relational databases.**
