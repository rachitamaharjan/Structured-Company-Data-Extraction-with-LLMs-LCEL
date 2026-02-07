# OpenAI Agent (kept for later)
# from langchain.agents import initialize_agent, AgentType
# from langchain_openai import ChatOpenAI
# from app.tools import insert_company

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# agent = initialize_agent(
#     tools=[insert_company],
#     llm=llm,
#     agent=AgentType.OPENAI_FUNCTIONS,
#     verbose=True
# )

# Gemini Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.tools import insert_company
from app.config import GEMINI_API_KEY
import os

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

tools = [insert_company]

class CompanyAgent:
    def __init__(self, tools):
        self.tools = {tool.name: tool for tool in tools}
    
    def invoke(self, inputs):
        company_str = inputs.get("input", "")
        try:
            import re
            name_match = re.search(r"company_name='([^']+)'", company_str)
            founded_match = re.search(r"founded_in='([^']+)'", company_str)
            founders_match = re.search(r"founders=\[([^\]]+)\]", company_str)
            
            if name_match:
                company_dict = {
                    "company_name": name_match.group(1),
                    "founded_in": founded_match.group(1) if founded_match else "",
                    "founders": [f.strip().strip("'") for f in founders_match.group(1).split(",")] if founders_match else []
                }
                result = self.tools["insert_company"].invoke(company_dict)
                return {"output": result}
        except Exception as e:
            return {"output": f"Error: {str(e)}"}

agent = CompanyAgent(tools)