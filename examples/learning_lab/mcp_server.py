"""Local stdio server. Stdout is reserved for MCP messages; do not print here."""
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from .core import ReviewQueue, get_application as lookup, screen_watchlist as screen, search_policy as search

server = FastMCP('learning-review-tools')


@server.tool()
def get_application(application_id: str) -> dict:
    """Read one fictional application and its linked parties/documents by ID."""
    return lookup(application_id)


@server.tool()
def screen_watchlist(party_id: str) -> dict:
    """Check one fictional party. A possible match requires human review."""
    return screen(party_id)


@server.tool()
def search_policy(query: str, entity_type: str, jurisdiction: str, as_of: str) -> list[dict]:
    """Find fictional policies with required scope and ISO YYYY-MM-DD date."""
    return search(query, entity_type, jurisdiction, as_of)


@server.tool()
def open_review_case(application_id: str, reason: str, request_id: str) -> dict:
    """Create a pending human-review record. Never approve/reject an application."""
    # Trusted local process configuration, NEVER tool arguments, supplies permission.
    path = Path(os.environ.get('LEARNING_REVIEW_DB', 'output/mcp-learning.sqlite3'))
    path.parent.mkdir(parents=True, exist_ok=True)
    queue = ReviewQueue(path)
    try:
        if 'error' in lookup(application_id):
            return {'error': 'not_found', 'retryable': False}
        return queue.open(application_id, reason, request_id, role=os.environ.get('LEARNING_REVIEW_ROLE', 'reader'), allowed_application=os.environ.get('LEARNING_REVIEW_APPLICATION'))
    finally:
        queue.close()


if __name__ == '__main__':
    server.run(transport='stdio')
