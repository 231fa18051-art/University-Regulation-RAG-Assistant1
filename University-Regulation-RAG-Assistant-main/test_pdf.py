import pymupdf

pdf_path = "documents/R26_Regulations_B.Tech.pdf"

document = pymupdf.open(pdf_path)

print("PDF opened successfully!")
print("Number of pages:", len(document))

for page_number in range(3):
    page = document[page_number]
    text = page.get_text()

    print(f"\n--- Page {page_number + 1} ---")
    print(text[:1000])

document.close()