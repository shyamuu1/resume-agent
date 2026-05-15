from tools.pdf_reader import extract_pdf_text

text = extract_pdf_text("C:/Users/shyam/Downloads/Resume 02_08_2026.pdf")
print("\n--- Extracted Resume Text ---\n")
print(text[500:])
print(f"\nTotal characters extracted: {len(text)}")