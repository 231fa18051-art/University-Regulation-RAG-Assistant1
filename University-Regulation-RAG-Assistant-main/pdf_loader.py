import pymupdf
import json

PDF_PATH = "documents/R26_Regulations_B.Tech.pdf"
OUTPUT_PATH = "regulations_data.json"

document = pymupdf.open(PDF_PATH)

pages = []

for page_number, page in enumerate(document, start=1):
    text = page.get_text().strip()

    if text:
        pages.append({
            "page_number": page_number,
            "text": text
        })

document.close()

with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
    json.dump(pages, file, ensure_ascii=False, indent=2)

print("PDF processing completed!")
print("Total PDF pages:", page_number)
print("Pages containing text:", len(pages))
print("Saved extracted data to:", OUTPUT_PATH)