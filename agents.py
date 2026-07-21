from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv()

openrouter_api_key = os.getenv("OPEN_ROUTER_API_KEY")

if not openrouter_api_key:
  raise RuntimeError(
    "Missing OpenRouter credentials. Set OPEN_ROUTER_API_KEY in .env."
  )

llm = ChatOpenAI(
  model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
  api_key=openrouter_api_key,
  base_url="https://openrouter.ai/api/v1",
  temperature=0,
)

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

# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
  ("system", "You are an expert writer. Write clear, structured and insightful reports."),
  ("human", """Write a detailed research report on the topic below.
  Topic: {topic}
  
  Research Gathered:
  {research}
  
  Structure the report as:
  - Introduction
  - Key Findings (minimum 3 well-explained points)
  - Conclusion
  - Sources (list all URLs found in the research)

  Be detailed, factual, and professional.""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# critic_chain
critic_prompt = ChatPromptTemplate.from_messages([
  ("system", "You are a sharp and constructive critic. Be honest and specific."),
  ("human", """Review the research report below and evaluate it strictly.
  Report: {report}
  
  Respond in this exact format:
  
  Score: X/10

  Strengths:
    - ...
    - ...
  
  Areas for Improvement:
    - ...
    - ...
  
    One line verdict: ...""")
])

critic_chain = critic_prompt | llm | StrOutputParser()
