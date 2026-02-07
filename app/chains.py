# OpenAI Chain (kept for later)
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.output_parsers import PydanticOutputParser
# from app.models import CompanyInfo

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# parser = PydanticOutputParser(pydantic_object=CompanyInfo)

# prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         "Extract company information from the paragraph. "
#         "If no company is mentioned, return null fields."
#     ),
#     ("human", "{paragraph}")
# ])

# extract_chain = prompt | llm | parser

# Gemini Chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.models import CompanyList
from app.config import GEMINI_API_KEY
import os

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

parser = PydanticOutputParser(pydantic_object=CompanyList)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Extract ALL companies with complete founding information from the paragraph. "
        "For each company, include: company name, founding date, founders (as a list), and headquarters/founding location if mentioned. "
        "Return a JSON object with a 'companies' array containing all companies found. "
        "Format:\n{format_instructions}"
    ),
    ("human", "{paragraph}")
]).partial(format_instructions=parser.get_format_instructions())

extract_chain = prompt | llm | parser
