from document_loader import load_uploaded_file
from text_splitter import split_documents

from vector import add_documents

from ollama_client import generate_document_answer

# Security modules
from security.document_security import (
    scan_documents,
    remove_indexed_source
)

from security.prompt_injection import detect_direct_injection

from security.retrieval_security import (
    inspect_retrieval_scores
)



#INDEX UPLOADED DOCUMENTS
def index_files(uploaded_files):
    """Load, scan, split, and index safe document content."""

    all_chunks = []
    files_without_safe_content = []
    total_flagged = 0

    for uploaded_file in uploaded_files:

        filename = uploaded_file.name

        try:
            # Load uploaded document.
            raw_documents = load_uploaded_file(
                filename,
                uploaded_file.getvalue()
            )

            # Scan extracted pages or rows for indirect injection.
            safe_documents, flagged_documents = scan_documents(
                raw_documents
            )

            total_flagged += len(flagged_documents)

            if not safe_documents:

                files_without_safe_content.append(filename)

                print(
                    f"[DOCUMENT SECURITY] No safe content in {filename}"
                )

                continue

            # Split only clean document content.
            chunks = split_documents(safe_documents)

            all_chunks.extend(chunks)

        except Exception as error:

            print(
                f"[DOCUMENT SECURITY] Processing failed for "
                f"{filename}: {error}"
            )

            # Do not delete previously indexed content if loading
            # or processing fails.
            raise

    # Index all safe chunks.
    indexed_count = 0

    if all_chunks:

        indexed_count = add_documents(all_chunks)

    # Remove stale vectors for files containing no safe content.
    for filename in files_without_safe_content:

        remove_indexed_source(filename)

    # Security summary.
    print("\n========== DOCUMENT SECURITY SUMMARY ==========")

    print(f"Clean chunks indexed: {indexed_count}")

    print(
        f"Suspicious pages/rows excluded: {total_flagged}"
    )

    print(
        f"Files with no safe content: {len(files_without_safe_content)}"
    )

    print("================================================")

    if not all_chunks:

        raise ValueError(
            "No safe document chunks were available for indexing."
        )

    return indexed_count



#ANSWER EMPLOYEE QUESTIONS
def answer_question(question):
    """Answer questions using retrieved document evidence."""

    # Step 1: Detect direct prompt injection.
    injection_result = detect_direct_injection(question)

    if injection_result["is_suspicious"]:

        return {
            "answer": (
                "I can't process this request because it contains "
                "instructions that appear to attempt to override "
                "the assistant's security rules."
            ),
            "sources": []
        }

    # Step 2: Retrieve documents.
    # Observation mode: inspect scores before activating threshold filtering.
    matches = inspect_retrieval_scores(question, k=4)

    if not matches:

        return {
            "answer": (
                "I couldn't find supporting information "
                "in the indexed documents."
            ),
            "sources": []
        }

    # Step 3: Build context and collect source references.
    context_parts = []
    sources = []
    seen_sources = set()

    for document, distance in matches:

        source = document.metadata.get(
            "source", "Unknown file"
        )

        detail = document.metadata.get(
            "detail", "Unknown location"
        )

        context_parts.append(
            f"Source: {source} ({detail})\n"
            f"Document text:\n{document.page_content}"
        )

        source_key = (source, detail)

        if source_key not in seen_sources:

            seen_sources.add(source_key)

            sources.append({
                "source": source,
                "detail": detail,
                "distance": round(float(distance), 4)
            })

    context = "\n\n---\n\n".join(context_parts)

    # Step 4: Generate the answer using Ollama.
    response = generate_document_answer(
        context,
        question
    )

    return {
        "answer": response,
        "sources": sources
    }