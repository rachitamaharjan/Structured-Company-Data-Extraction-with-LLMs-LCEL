from dotenv import load_dotenv
load_dotenv()

from app.chains import extract_chain
from app.tools import insert_company
import time

def load_paragraphs():
    with open("data/essay.txt") as f:
        return [p.strip() for p in f.read().split("\n\n") if p.strip()]

def main():
    paragraphs = load_paragraphs()

    for i, para in enumerate(paragraphs):
        try:
            if i > 0:
                print(f"Waiting 5 seconds before processing next paragraph...")
                time.sleep(5)
            
            print(f"Processing paragraph {i + 1}/{len(paragraphs)}...")
            company = extract_chain.invoke({"paragraph": para})
            if company.company_name:
                print(f"Found company: {company.company_name}")
                result = insert_company.func(company.model_dump())
                print(f"{result}")
        except Exception as e:
            print(f"Skipping paragraph {i + 1}:", e)

if __name__ == "__main__":
    main()