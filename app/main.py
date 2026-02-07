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
    total_companies = 0

    for i, para in enumerate(paragraphs):
        try:
            # Gemini free tier: (15 RPM max)
            if i > 0:
                print(f"Waiting 5 seconds before processing next paragraph...")
                time.sleep(5)
            
            print(f"\nProcessing paragraph {i + 1}/{len(paragraphs)}...")
            result = extract_chain.invoke({"paragraph": para})
            
            if result.companies:
                print(f"Found {len(result.companies)} companies:")
                for company in result.companies:
                    if company.company_name:
                        print(f"  - {company.company_name}")
                        # Call the tool function directly
                        insert_result = insert_company.func(company.model_dump())
                        total_companies += 1
                print(f"Inserted {len(result.companies)} companies")
            else:
                print("No companies found in this paragraph")
        except Exception as e:
            print(f"Error in paragraph {i + 1}:", e)
    
    print(f"\n{'='*50}")
    print(f"Total companies extracted and inserted: {total_companies}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()