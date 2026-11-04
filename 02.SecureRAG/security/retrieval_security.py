
import math
import os

from vector import retrieve_documents


# Set this only after inspecting your actual retrieval scores.
# Example format: SECURERAG_MAX_DISTANCE=0.75
# Do not use an example value without calibrating it first.
_threshold_value = os.getenv("SECURERAG_MAX_DISTANCE")
MAX_DISTANCE = (
    float(_threshold_value)
    if _threshold_value is not None
    else None
)


def inspect_retrieval_scores(question, k=4):
    """Retrieve chunks and display their distance scores for calibration."""

    results = retrieve_documents(question, k=k)

    print("\n========== RETRIEVAL RESULTS ==========")
    print(f"Question: {question}")

    if not results:
        print("No documents retrieved.")
        return []

    for index, (document, score) in enumerate(results, start=1):
        filename = document.metadata.get("source", "Unknown source")
        detail = document.metadata.get("detail", "Unknown location")

        print(f"\nResult {index}")
        print(f"Source: {filename}")
        print(f"Location: {detail}")
        print(f"Distance score: {float(score):.6f}")
        print(f"Content: {document.page_content[:200]}")

    print("\n=======================================")

    return results


def filter_relevant_documents(results, max_distance):
    """Keep only chunks whose distance is within the calibrated threshold."""

    if max_distance is None or max_distance < 0:
        raise ValueError("A valid calibrated max_distance is required.")

    relevant_documents = []

    for document, score in results:
        try:
            score = float(score)
        except (TypeError, ValueError):
            continue

        if not math.isfinite(score):
            continue

        if score <= max_distance:
            relevant_documents.append((document, score))

    return relevant_documents


def secure_retrieve_documents(question, k=4, max_distance=None):
    """Retrieve and filter chunks using a calibrated distance threshold."""

    if max_distance is None:
        max_distance = MAX_DISTANCE

    if max_distance is None:
        raise ValueError(
            "Retrieval threshold is not configured. "
            "Inspect actual scores and set SECURERAG_MAX_DISTANCE."
        )

    results = inspect_retrieval_scores(question, k=k)

    relevant_documents = filter_relevant_documents(
        results,
        max_distance
    )

    print("\n========== RETRIEVAL SECURITY ==========")
    print(f"Retrieved chunks: {len(results)}")
    print(f"Relevant chunks: {len(relevant_documents)}")
    print(f"Rejected chunks: {len(results) - len(relevant_documents)}")
    print(f"Maximum allowed distance: {max_distance}")
    print("========================================")

    return relevant_documents
