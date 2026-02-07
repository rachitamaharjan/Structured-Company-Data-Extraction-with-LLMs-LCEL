from langchain.tools import tool
from app.db import get_connection
from app.models import CompanyInfo
from datetime import datetime
import re


@tool
def insert_company(company: dict):
    """
    Insert extracted company data into PostgreSQL.
    """
    # Convert dict to CompanyInfo
    company_obj = CompanyInfo(**company)

    conn = get_connection()
    cur = conn.cursor()
    
    # Parse the founding date

    cur.execute(
        """
        INSERT INTO company_details (company_name, founded_in, founded_by, headquarters)
        VALUES (%s, %s, %s, %s)
        """,
        (
            company_obj.company_name,
            company_obj.founders,
            company_obj.headquarters,
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    return "Inserted successfully"

