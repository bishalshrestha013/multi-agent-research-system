from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StructuredOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1st agent = web search agent
def build_search_aagent():
  return create_agent(
    model=llm,
    tools=[web_search],
  )

# 2nd agent = web reader agent
def build_reader_agent():
  return create_agent(
    model=llm,
    tools=[scrape_url],
  )