"""Deterministic data, retrieval, extraction validation and review state.

All business rules are invented teaching rules. This is not a KYC decision engine.
"""
from __future__ import annotations

import csv
import json
import math
import re
import sqlite3
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
AS_OF = date(2026, 10, 21)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def customers():
    with (DATA / "customers_clean.csv").open(encoding="utf-8", newline="") as f:
        return {row["customer_id"]: row for row in csv.DictReader(f)}


def profile_csv(path, as_of=AS_OF):
    with Path(path).open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    counts = Counter(row["customer_id"] for row in rows)
    issues = []
    for number, row in enumerate(rows, 2):  # CSV header is line 1
        labels = []
        if not re.fullmatch(r"C-\d{4}", row["customer_id"]):
            labels.append("invalid_customer_id")
        if counts[row["customer_id"]] > 1:
            labels.append("duplicate_customer_id")
        for field in ("legal_name", "country_code", "onboarding_date", "risk_tier", "source"):
            if not row.get(field, "").strip():
                labels.append("missing_" + field)
        if row["risk_tier"] not in {"low", "medium", "high"}:
            labels.append("invalid_risk_tier")
        if not re.fullmatch(r"[A-Z]{2}", row["country_code"]):
            labels.append("invalid_country_code_format")
        try:
            if date.fromisoformat(row["onboarding_date"]) > as_of:
                labels.append("future_onboarding_date")
        except ValueError:
            labels.append("invalid_onboarding_date")
        try:
            refreshed = date.fromisoformat(row["last_refreshed"])
            if refreshed > as_of:
                labels.append("future_refresh_date")
            elif (as_of - refreshed).days > 90:
                labels.append("stale_record")
        except ValueError:
            labels.append("invalid_refresh_date")
        if row.get("email") and not row["email"].endswith("@example.test"):
            labels.append("invalid_demo_email")
        if labels:
            issues.append({"csv_line": number, "customer_id": row["customer_id"], "issues": labels})
    return {"rows": len(rows), "as_of": as_of.isoformat(), "issues": issues}


def search_policy(query, limit=3):
    """Tiny lexical baseline. Status filtering is intentional, not semantic search."""
    terms = set(re.findall(r"[a-z0-9]+", query.lower())) - {"what", "is", "the", "a", "to", "for", "and"}
    ranked = []
    for doc in read_json(DATA / "policies/index.json"):
        if doc["status"] != "active":
            continue
        text = (DATA / "policies" / doc["file"]).read_text(encoding="utf-8")
        score = len(terms & set(re.findall(r"[a-z0-9]+", text.lower())))
        if score:
            ranked.append({"source_id": doc["source_id"], "version": doc["version"],
                           "score": score, "text": text})
    return sorted(ranked, key=lambda x: (-x["score"], x["source_id"]))[:limit]


class ReviewStore:
    """SQLite persistence and atomic idempotency; designed for a local single-user lab."""

    def __init__(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("""CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY, request_id TEXT UNIQUE NOT NULL,
            customer_id TEXT NOT NULL, reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending', reviewer TEXT)""")
        self.db.commit()

    def close(self):
        self.db.close()

    def create(self, customer_id, reason, request_id):
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO reviews(request_id, customer_id, reason) VALUES(?,?,?)",
                            (request_id, customer_id, reason))
            row = dict(self.db.execute("SELECT * FROM reviews WHERE request_id=?", (request_id,)).fetchone())
            if (row["customer_id"], row["reason"]) != (customer_id, reason):
                return {"error": "idempotency_conflict", "hint": "Use the original payload or a new request ID."}
            return row

    def list(self):
        return [dict(row) for row in self.db.execute("SELECT * FROM reviews ORDER BY id")]

    def decide(self, review_id, decision, reviewer):
        if decision not in {"approved", "rejected"} or not reviewer.strip():
            raise ValueError("Supply approved/rejected and a nonblank reviewer name.")
        with self.db:
            row = self.db.execute("SELECT * FROM reviews WHERE id=?", (review_id,)).fetchone()
            if row is None:
                raise ValueError("Unknown review ID")
            if row["status"] != "pending":
                if row["status"] == decision and row["reviewer"] == reviewer:
                    return dict(row)
                raise ValueError("Review is already decided; a conflicting transition is blocked.")
            self.db.execute("UPDATE reviews SET status=?,reviewer=? WHERE id=?", (decision, reviewer, review_id))
        return dict(self.db.execute("SELECT * FROM reviews WHERE id=?", (review_id,)).fetchone())


def validate_extraction(item, threshold=0.85, as_of=AS_OF):
    """Return reasons for human review. Threshold is a demo value, not calibrated."""
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1")
    required = ("invoice_id", "supplier_name", "invoice_date", "total_amount", "currency")
    reasons = []
    for field in required:
        value = item.get(field)
        if value is None or value == "":
            reasons.append("missing_" + field)
        elif field != "total_amount" and (not isinstance(value, str) or not value.strip()):
            reasons.append("invalid_" + field)
    amount = item.get("total_amount")
    if type(amount) not in (int, float) or not math.isfinite(amount) or amount < 0:
        reasons.append("invalid_total_amount")
    if item.get("currency") not in {"USD", "GBP", "EUR"}:
        reasons.append("unsupported_currency")
    try:
        if date.fromisoformat(item.get("invoice_date", "")) > as_of:
            reasons.append("future_invoice_date")
    except (TypeError, ValueError):
        reasons.append("invalid_invoice_date")
    record = customers().get(item.get("customer_id"))
    if record is None:
        reasons.append("unknown_customer")
    elif str(item.get("supplier_name", "")).strip().casefold() != record["legal_name"].casefold():
        reasons.append("supplier_name_mismatch")
    confidences = item.get("confidence")
    if not isinstance(confidences, dict):
        confidences = {}
    for field in required:
        value = confidences.get(field)
        if value is None:
            reasons.append("missing_confidence:" + field)
        elif type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
            reasons.append("invalid_confidence:" + field)
        elif value < threshold:
            reasons.append("low_confidence:" + field)
    return {"document_id": item.get("document_id"), "status": "review" if reasons else "validated",
            "reasons": reasons, "threshold": threshold, "as_of": as_of.isoformat()}


TOOLS = [
    {"name": "lookup_customer", "description": "Read one synthetic customer by exact ID C-####. No write.",
     "parameters": {"type": "object", "properties": {"customer_id": {"type": "string"}},
                    "required": ["customer_id"], "additionalProperties": False}},
    {"name": "search_policy", "description": "Search active fictional training policies. Cite returned source_id; no match means insufficient evidence.",
     "parameters": {"type": "object", "properties": {"query": {"type": "string"}},
                    "required": ["query"], "additionalProperties": False}},
    {"name": "flag_for_review", "description": "Create a pending local review for ONE exact customer, only when explicitly requested. Does not approve onboarding. Application authorization is required.",
     "parameters": {"type": "object", "properties": {"customer_id": {"type": "string"}, "reason": {"type": "string"}},
                    "required": ["customer_id", "reason"], "additionalProperties": False}},
]


class ToolContext:
    def __init__(self, store, request_id, allow_write=False, allowed_customer_id=None):
        self.store, self.request_id, self.allow_write = store, request_id, allow_write
        self.allowed_customer_id = allowed_customer_id

    def dispatch(self, name, arguments):
        definition = next((t for t in TOOLS if t["name"] == name), None)
        if definition is None:
            return {"error": "unknown_tool", "hint": "Choose a declared tool."}
        required = set(definition["parameters"]["required"])
        if not isinstance(arguments, dict) or set(arguments) != required:
            return {"error": "invalid_arguments", "hint": "Supply exactly the declared fields."}
        if any(not isinstance(v, str) or not v.strip() or len(v) > 1000 for v in arguments.values()):
            return {"error": "invalid_arguments", "hint": "Use nonblank strings of at most 1000 characters."}
        if name == "search_policy":
            return {"matches": search_policy(arguments["query"])}
        customer_id = arguments["customer_id"]
        if not re.fullmatch(r"C-\d{4}", customer_id):
            return {"error": "invalid_customer_id", "hint": "Use C-####."}
        customer = customers().get(customer_id)
        if customer is None:
            return {"error": "customer_not_found", "hint": "Ask for a valid customer ID; do not invent one."}
        if name == "lookup_customer":
            return customer
        if not self.allow_write:
            return {"error": "approval_required", "hint": "Application has disabled writes. Ask the human to enable a specific demo request."}
        if self.allowed_customer_id != customer_id:
            return {"error": "write_scope_denied", "hint": "This customer is outside the caller-approved write scope."}
        return self.store.create(customer_id, arguments["reason"], self.request_id)
