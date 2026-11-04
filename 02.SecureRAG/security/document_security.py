from vector import get_vector_store
from security.indirect_injection import detect_indirect_injection


def scan_document(document):
    """
    Scan one extracted document page or CSV row
    for potential indirect prompt injection.
    """

    result = detect_indirect_injection(document)

    return result


def scan_documents(documents):
    """
    Separate clean documents from suspicious documents.
    """

    safe_documents = []
    flagged_documents = []

    for document in documents:

        result = scan_document(document)

        source = document.metadata.get(
            "source", "Unknown file"
        )

        detail = document.metadata.get(
            "detail", "Unknown location"
        )

        if result["is_suspicious"]:

            document.metadata["security_status"] = "flagged"

            flagged_documents.append({
                "source": source,
                "detail": detail,
                "matched_patterns": result["matched_patterns"]
            })

            print("\n[DOCUMENT SECURITY] Document rejected")
            print(f"Source: {source}")
            print(f"Location: {detail}")
            print(
                "Matched patterns:",
                result["matched_patterns"]
            )

        else:

            document.metadata["security_status"] = "scanned_clean"

            safe_documents.append(document)

    return safe_documents, flagged_documents


def remove_indexed_source(filename):
    """
    Remove previously indexed chunks for a filename.

    Prevents an older version of a document from remaining
    searchable when its newly uploaded version is rejected.
    """

    store = get_vector_store()

    store.delete(
        where={"source": filename}
    )

    print(
        f"[DOCUMENT SECURITY] Removed previously indexed content: "
        f"{filename}"
    )
