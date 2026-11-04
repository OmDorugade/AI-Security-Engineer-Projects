import csv
import io
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

#Function for reading documents
def load_uploaded_file(file_name,file_bytes):
    #reading the uploaded file and extension .pdf
    extension = Path(file_name).suffix.lower()
    documents = []


    if extension == ".pdf":
        reader = PdfReader(io.BytesIO(file_bytes))

        #iterating through pages and retreiving the pages from pdf
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": file_name,
                            "detail": f"Page {page_number}"
                        }
                    )
                )

    #for txt files
    elif extension == ".txt":
        text = file_bytes.decode("utf-8", errors="replace").strip()
        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file_name,
                        "detail": "Text file"
                    }
                )
            )

    # Convert each CSV row into searchable text.
    elif extension == ".csv":
        text = file_bytes.decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(io.StringIO(text))

        if not reader.fieldnames:
            raise ValueError("CSV must contain a header row.")

        for row_number, row in enumerate(reader, start=2):
            row_text = " | ".join(
                f"{key}: {value}"
                for key, value in row.items()
                if key and value is not None and str(value).strip()
            )

            if row_text:
                documents.append(
                    Document(
                        page_content=row_text,
                        metadata={
                            "source": file_name,
                            "detail": f"Row {row_number}"
                        }
                    )
                )

    else:
        raise ValueError("Only PDF, TXT, and CSV are supported.")

    if not documents:
        raise ValueError(
            "No readable text found in this file."
        )


    return documents


