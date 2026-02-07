from pydantic import BaseModel
from typing import List, Optional

class CompanyInfo(BaseModel):
    company_name: str
    founded_in: str
    founders: List[str]
    headquarters: Optional[str] = None

class CompanyList(BaseModel):
    companies: List[CompanyInfo]
