# PydanticAI SQL Chart Builder: Comprehensive Documentation

## What is this?

The PydanticAI SQL Chart Builder is a Python application that leverages Google's Gemini (a Large Language Model) and PydanticAI to enable natural language interaction with your database. It understands your questions, generates appropriate SQL queries, executes them, and can even visualize the results as charts. This project integrates a FastAPI backend to expose these capabilities via a web API.

Think of it as a smart assistant that not only answers your database questions but also helps you visualize the data!

## Key Features

*   **Natural Language Queries**: Interact with your database using plain English questions (e.g., "How many customers are there in the USA?").
*   **Intelligent SQL Generation**: The AI agent automatically constructs and executes complex SQL queries based on your natural language input.
*   **Dynamic Chart Generation**: If your request implies a visualization (e.g., "plot", "chart", "graph"), the agent can generate various chart types (Scatter, Line, Histograph, Bargraph, Pie Chart) using Plotly Express.
*   **FastAPI Integration**: Exposes database querying and chart generation functionalities via a RESTful API.
*   **Structured Output**: Get query results in a clean, predictable JSON format, and chart insights along with the Python code used for generation.
*   **Database Agnostic (SQLAlchemy)**: Configured to work with PostgreSQL by default, but easily adaptable to other SQL databases supported by SQLAlchemy.
*   **Easy Configuration**: Uses a `.env` file for API keys.

## Core Components

The project is structured around these key Python files and directories:

*   `main.py`: The main entry point for the FastAPI application. It initializes the FastAPI app and includes the API router.
*   `app/`: This directory contains the core logic of the application.
    *   `app/controller.py`: Defines the API endpoints (`/request_insights` and `/get_chart`) that handle incoming requests and delegate to the service layer.
    *   `app/service.py`: Contains the main business logic, including the PydanticAI `SQLAgent` and `ChartAgent`. It orchestrates the flow from natural language query to SQL execution, data processing, and chart generation.
    *   `app/models.py`: Defines Pydantic models for request and response payloads (e.g., `Request`, `SQLSuccess`, `InvalidRequest`, `ChartResponses`), ensuring structured data exchange. It also handles API key loading and OpenAI model initialization.
    *   `app/sql_operations.py`: Provides utility functions for interacting directly with the database, such as `list_tables`, `describe_table`, and `run_sql_query`.
    *   `app/dataframe.py`: Contains functions (`create_dataframe_pd_json`, `create_dataframe_pd`) to convert SQL query results into Pandas DataFrames, which are then used for chart generation.
*   `sql_agent.py`: (Note: While `sql_agent.py` exists, the core agent logic has been integrated into `app/service.py` for the FastAPI application.)
*   `requirements.txt`: Lists all Python dependencies required for the project.
*   `Chinook_Sqlite.sqlite`: An example SQLite database used for demonstration purposes.
*   `chart.html`: The HTML file where generated Plotly charts are saved.
*   `index.html`: A simple HTML file that can serve as a basic frontend for interacting with the API.

## Quick Setup

1.  **Get the Code**:
    If you haven't already, clone the repository:
    ```bash
    git clone <repository-url>
    cd PydanticAI_SQL_Chart_Builder
    ```

2.  **Install Necessary Packages**:
    It's highly recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
    (The `requirements.txt` file should contain `fastapi`, `uvicorn`, `pydantic-ai`, `sqlalchemy`, `python-dotenv`, `google-generativeai`, `pandas`, `plotly`, `psycopg2-binary` (for PostgreSQL), and `openai`.)

3.  **Set Up Your API Key**:
    *   Create a file named `.env` in the root directory of the project (`PydanticAI_SQL_Chart_Builder/`).
    *   Add your Google Gemini API key or Azure OpenAI key to it like this:
        ```env
        GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
        # OR for Azure OpenAI
        AZURE_OPENAI_KEY="YOUR_ACTUAL_AZURE_OPENAI_KEY"
        ```
    *   (This file is ignored by Git, so your key stays private).

4.  **Database Setup (PostgreSQL Example)**:
    The application is configured to connect to a PostgreSQL database named `chinook_auto_increment` with user `chinook` and password `chinook` on `localhost:5433`.
    *   Ensure you have a PostgreSQL server running and a database configured as per `app/service.py` and `app/dataframe.py`.
    *   You can use the provided SQL files in `DataSources/` to set up the Chinook database in PostgreSQL. For example, to create the database and tables:
        ```bash
        # Assuming you have psql installed and access to a PostgreSQL server
        psql -h localhost -p 5433 -U postgres -c "CREATE DATABASE chinook_auto_increment;"
        psql -h localhost -p 5433 -U postgres -d chinook_auto_increment -f DataSources/Chinook_PostgreSql_AutoIncrementPKs.sql
        ```
    *   If you wish to use SQLite, you'll need to modify the `create_engine` calls in `app/service.py` and `app/dataframe.py` to point to your SQLite database file (e.g., `sqlite:///./Chinook_Sqlite.sqlite`).

## How to Use

Once everything is set up, you can run the FastAPI application:

1.  **Start the FastAPI Server**:
    From the project's root directory, run:
    ```bash
    uvicorn main:app --host 127.0.0.1 --port 9090 --reload
    ```
    This will start the server, typically accessible at `http://127.0.0.1:9090`. The `--reload` flag enables automatic reloading on code changes.

2.  **Access the API**:
    You can interact with the API using tools like `curl`, Postman, or by building a simple frontend.

    *   **Request Insights (SQL Query & Optional Chart)**:
        Send a POST request to `/request_insights` with your natural language query.
        **Endpoint**: `POST /request_insights`
        **Body (JSON)**:
        ```json
        {
            "query": "Show me the total sales for each customer in the USA, and plot this as a bar chart for the top 10."
        }
        ```
        **Example `curl` command**:
        ```bash
        curl -X POST "http://127.0.0.1:9090/request_insights" \
             -H "Content-Type: application/json" \
             -d '{ "query": "Show me the total sales for each customer in the USA, and plot this as a bar chart for the top 10." }'
        ```
        The response will be a JSON object containing the generated SQL query, the query results, and optionally chart insights and Python code.

    *   **Retrieve Generated Chart**:
        After a chart generation request, the chart will be saved as `chart.html` in the root directory. You can access it directly via a GET request.
        **Endpoint**: `GET /get_chart`
        **Example `curl` command**:
        ```bash
        curl -X GET "http://127.0.0.1:9090/get_chart" -o chart_downloaded.html
        ```
        You can then open `chart_downloaded.html` in your browser.

3.  **Using the `index.html` Frontend (Basic)**:
    If you have a simple `index.html` file that makes requests to these endpoints, you can open it directly in your browser to interact with the application. Ensure your `index.html` points to the correct API endpoint (`http://127.0.0.1:9090`).

## Chart Output

When a chart is requested and successfully generated, the Python code for the Plotly chart is executed, and the chart is saved as `chart.html` in the project's root directory. You can open this `chart.html` file directly in any web browser to view the visualization.
