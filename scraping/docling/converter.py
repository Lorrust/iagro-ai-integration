from docling.document_converter import DocumentConverter
from docs.doc_paths import DOC_PATHS

print(DOC_PATHS)

source = DOC_PATHS[0]  # PDF path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())