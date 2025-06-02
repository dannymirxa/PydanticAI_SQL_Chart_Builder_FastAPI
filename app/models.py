from pydantic import BaseModel, Field
from typing import Annotated
from typing_extensions import TypeAlias, Union, Optional
from annotated_types import MinLen
from openai import AsyncAzureOpenAI, AzureOpenAI
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.providers.openai import OpenAIProvider

from dotenv import load_dotenv
import os

load_dotenv('/mnt/c/Projects/PydanticAI_SQL_Chart_Builder/.env')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

# GEMINI_MODEL = GeminiModel('gemini-2.0-flash', provider=GoogleGLAProvider(api_key=GEMINI_API_KEY))

async_client = AsyncAzureOpenAI(
    azure_endpoint = "https://llmcoechangemateopenai2.openai.azure.com/",
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-10-21",
    azure_deployment='gpt-4o'
)

OPENAI_MODEL = OpenAIModel(
    'gpt-4o-dev',
    provider=OpenAIProvider(openai_client=async_client),
)

class Request(BaseModel):
    query: Annotated[str, MinLen(1)]

class SQLSuccess(BaseModel):
    sql_query: Annotated[str, MinLen(1)]
    detail: str = Field(alias='Detail', description='Explanation of the SQL query, steps taken, the result of the query (JSON), and chart generation summary if applicable, as markdown')
    chart_insights: Optional[Annotated[str, MinLen(1)]] = Field(None, description="Insights from the dataset and graph, if a chart was generated.")
    chart_python_code: Optional[Annotated[str, MinLen(1)]] = Field(None, description='Python code to plot the graph, as markdown, if a chart was generated.')

class InvalidRequest(BaseModel):
    error_message: str

SQLResponse: TypeAlias = Union[SQLSuccess, InvalidRequest]

class ChartResponses(BaseModel):
    insights: Annotated[str, MinLen(1), Field(alias='insights', description="insights from the dataset and graph")]
    python_code: Annotated[str, MinLen(1), Field(alias='python_code',description='Python code to plot the graph, as markdown')]
