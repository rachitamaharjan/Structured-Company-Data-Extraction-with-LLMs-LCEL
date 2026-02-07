from langchain.tools import tool
from app.db import get_connection
from app.models import CompanyInfo
from datetime import datetime
import re

def parse_date(date_string):
    """
    Parse date string with fallback logic:
    - If only year: default to January 1st
    - If year and month: default to 1st day of month
    - If full date: parse as is
    """
    if not date_string:
        return None
    
    # Try full date first (e.g., "May 8, 1886", "April 15, 1955")
    try:
        return datetime.strptime(date_string, "%B %d, %Y").date()
    except:
        pass
    
    try:
        return datetime.strptime(date_string, "%b %d, %Y").date()
    except:
        pass
    
    # Try month and year (e.g., "January 1969")
    try:
        return datetime.strptime(date_string, "%B %Y").replace(day=1).date()
    except:
        pass
    
    # Try just year (e.g., "1969", "2010")
    year_match = re.search(r'\b(\d{4})\b', date_string)
    if year_match:
        year = int(year_match.group(1))
        return datetime(year, 1, 1).date()
    
    return None

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
    founded_date = parse_date(company_obj.founded_in)

    cur.execute(
        """
        INSERT INTO company_details (company_name, founded_in, founded_by, headquarters)
        VALUES (%s, %s, %s, %s)
        """,
        (
            company_obj.company_name,
            founded_date,
            company_obj.founders,
            company_obj.headquarters,
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    return "Inserted successfully"

