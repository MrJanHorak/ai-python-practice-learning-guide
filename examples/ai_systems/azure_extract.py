"""Live Azure Document Intelligence extraction; run only with an approved resource.

python -m examples.ai_systems.azure_extract --file data/documents/invoice-clean.pdf --customer-id C-1001
"""
import argparse
import json
import os
from pathlib import Path

from .core import ROOT, validate_extraction


def normalize_document(document, customer_id, document_id):
    """Map the invoice model into our own lab contract, not an Azure response clone."""
    fields = document.fields or {}
    mapping = {"invoice_id": "InvoiceId", "supplier_name": "VendorName", "invoice_date": "InvoiceDate",
               "total_amount": "InvoiceTotal", "currency": "InvoiceTotal"}
    result = {"document_id": document_id, "customer_id": customer_id, "confidence": {}}
    for target, source in mapping.items():
        field = fields.get(source)
        result["confidence"][target] = field.confidence if field else None
        value = None
        if field:
            if target == "total_amount":
                value = field.value_currency.amount if field.value_currency else None
            elif target == "currency":
                value = field.value_currency.currency_code if field.value_currency else None
            elif target == "invoice_date":
                value = field.value_date.isoformat() if field.value_date else None
            else:
                value = field.value_string or field.content
        result[target] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--customer-id", required=True, help="Assigned by caller, not inferred from the invoice")
    parser.add_argument("--output", type=Path, default=ROOT / "output/azure-normalized.json")
    args = parser.parse_args()
    # Optional dependencies are imported only when this live command is run.
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential
    from azure.identity import DefaultAzureCredential

    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ.get("DOCUMENTINTELLIGENCE_API_KEY")
    credential = AzureKeyCredential(key) if key else DefaultAzureCredential()
    with DocumentIntelligenceClient(endpoint, credential=credential, connection_timeout=15, read_timeout=60,
                                    retry_total=0) as client:
        with args.file.open("rb") as stream:
            poller = client.begin_analyze_document("prebuilt-invoice", body=stream)
        result = poller.result(timeout=120)
    documents = result.documents or []
    if len(documents) != 1:
        raise ValueError(f"Expected one invoice, received {len(documents)}; split or review this file.")
    normalized = normalize_document(documents[0], args.customer_id, args.file.stem)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    raw_path = args.output.with_name(args.output.stem + "-raw.json")
    raw_path.write_text(json.dumps(result.as_dict(), indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"normalized_file": str(args.output), "raw_file": str(raw_path),
                      "validation": validate_extraction(normalized)}, indent=2))


if __name__ == "__main__":
    main()
