"""
Root Cause Engine
-----------------
Categorises an error message using keyword matching and returns a structured
dict with: category, root_cause, suggested_fix.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Category rules: ordered list of (keywords, metadata) tuples.
# The FIRST matching rule wins.
# ---------------------------------------------------------------------------
_RULES: list[tuple[list[str], dict]] = [
    (
        ["nullpointerexception", "null reference", "cannot be null",
         "none type", "nonetype", "attributeerror", "object reference not set"],
        {
            "category": "Null Reference Error",
            "root_cause": (
                "An object or variable that was expected to hold a valid value is None/null. "
                "This usually happens when an API response, database result, or optional field "
                "is accessed without a prior None-check."
            ),
            "suggested_fix": (
                "1. Add a None/null guard before accessing the variable.\n"
                "2. Trace back where the variable is assigned and ensure it is always initialised.\n"
                "3. If it comes from an API or DB call, handle the empty/missing-result case explicitly.\n"
                "4. Use optional chaining or defensive defaults (e.g. `x = value or default`)."
            ),
        },
    ),
    (
        ["connection refused", "connection timed out", "network unreachable",
         "socket timeout", "econnrefused", "no route to host",
         "dns resolution", "ssl handshake", "certificate verify failed",
         "requests.exceptions", "urllib.error"],
        {
            "category": "Network Error",
            "root_cause": (
                "The application failed to establish or maintain a network connection. "
                "Possible causes: the target service is down, firewall rules are blocking "
                "the port, DNS is mis-configured, or TLS/SSL certificates are invalid/expired."
            ),
            "suggested_fix": (
                "1. Verify the target host/port is reachable: `curl -v <host>:<port>`.\n"
                "2. Check firewall rules and security-group inbound/outbound settings.\n"
                "3. Confirm DNS resolves correctly: `nslookup <hostname>`.\n"
                "4. For SSL errors, renew/replace the certificate and verify the CA chain.\n"
                "5. Implement retry logic with exponential back-off for transient failures."
            ),
        },
    ),
    (
        ["payment failed", "payment declined", "card declined", "insufficient funds",
         "transaction error", "stripe error", "payment gateway",
         "invalid card", "charge failed", "billing error"],
        {
            "category": "Payment Failure",
            "root_cause": (
                "A payment transaction was rejected or could not be processed. "
                "This may be due to insufficient funds, an expired/invalid card, "
                "a payment-gateway misconfiguration, or a fraud-detection rule trigger."
            ),
            "suggested_fix": (
                "1. Log the gateway's error code and map it to a user-friendly message.\n"
                "2. Check payment gateway dashboard for blocked transactions or quota limits.\n"
                "3. Verify API keys and webhook signatures are current and correct.\n"
                "4. Implement idempotent retry logic so double-charges cannot occur.\n"
                "5. Alert the customer with clear instructions to update payment details."
            ),
        },
    ),
    (
        ["unauthorized", "401", "403", "forbidden", "authentication failed",
         "invalid token", "jwt", "access denied", "permission denied",
         "invalid credentials", "session expired", "login failed",
         "oauth", "invalid api key"],
        {
            "category": "Authentication Error",
            "root_cause": (
                "The request lacks valid authentication credentials or the credentials "
                "have expired/been revoked. Common causes: expired JWT, missing/wrong API key, "
                "CSRF token mismatch, or an OAuth flow that was not completed."
            ),
            "suggested_fix": (
                "1. Check whether the token/session has expired and refresh it.\n"
                "2. Validate that the correct API key or OAuth scopes are being sent.\n"
                "3. Inspect auth middleware to ensure all protected routes are guarded.\n"
                "4. Enable detailed auth logging (without leaking secrets) to trace the failure.\n"
                "5. Implement proper token rotation and short token lifetimes."
            ),
        },
    ),
    (
        ["database", "db error", "sql", "query failed", "deadlock",
         "duplicate key", "foreign key", "constraint violation",
         "table not found", "column not found", "migration",
         "connection pool", "too many connections", "sqlite", "postgres",
         "mysql", "mongodb", "transaction rollback"],
        {
            "category": "Database Error",
            "root_cause": (
                "A database operation failed. This could be a connection-pool exhaustion, "
                "a constraint/schema violation (duplicate key, foreign-key mismatch), "
                "a deadlock between concurrent transactions, or a missing migration."
            ),
            "suggested_fix": (
                "1. Check database logs for the specific error code and query.\n"
                "2. For connection issues, tune pool size and verify DB host accessibility.\n"
                "3. For constraint violations, review the data being inserted/updated.\n"
                "4. For deadlocks, add appropriate retry logic and inspect locking order.\n"
                "5. Ensure all pending migrations have been applied in the environment."
            ),
        },
    ),
    (
        ["out of memory", "memoryerror", "heap space", "stack overflow",
         "resource exhausted", "too many open files", "disk full",
         "oom", "killed"],
        {
            "category": "Resource Exhaustion",
            "root_cause": (
                "The process ran out of a critical system resource (memory, disk, file handles). "
                "This can be caused by memory leaks, unbounded data loading, infinite loops "
                "accumulating data, or an under-provisioned environment."
            ),
            "suggested_fix": (
                "1. Profile memory usage with tools like `memory_profiler` or APM agents.\n"
                "2. Stream or paginate large data sets instead of loading everything into RAM.\n"
                "3. Close file handles, DB cursors, and network sockets properly.\n"
                "4. Set resource limits (ulimit) and configure swap space as a safety net.\n"
                "5. Consider horizontal scaling or upgrading instance size."
            ),
        },
    ),
    (
        ["timeout", "timed out", "gateway timeout", "504", "request timeout",
         "read timeout", "write timeout", "idle timeout"],
        {
            "category": "Timeout Error",
            "root_cause": (
                "An operation exceeded its allowed time budget. This can stem from slow "
                "downstream services, unoptimised database queries, network congestion, "
                "or insufficient timeout configuration."
            ),
            "suggested_fix": (
                "1. Profile the slow operation and optimise the heaviest queries/calls.\n"
                "2. Add database indexes for frequently queried columns.\n"
                "3. Increase timeout thresholds only as a temporary measure.\n"
                "4. Consider async processing or background jobs for long-running tasks.\n"
                "5. Add circuit-breaker patterns to fail fast on slow dependencies."
            ),
        },
    ),
    (
        ["file not found", "filenotfounderror", "no such file", "ioerror",
         "permissionerror", "is a directory", "path does not exist"],
        {
            "category": "File System Error",
            "root_cause": (
                "The application tried to read or write a file that does not exist, "
                "is in the wrong location, or lacks the necessary permissions."
            ),
            "suggested_fix": (
                "1. Verify the file path is correct and uses the right working directory.\n"
                "2. Use `os.path.exists()` or `Path.exists()` before opening files.\n"
                "3. Check file/directory ownership and permission bits (`ls -la`).\n"
                "4. Ensure volumes and mounts are correctly configured in containerised environments.\n"
                "5. Add clear error messages to help diagnose missing-file issues in production."
            ),
        },
    ),
]

_DEFAULT: dict = {
    "category": "General Application Error",
    "root_cause": (
        "The error does not match a known pattern. It may be an unhandled exception, "
        "an unexpected application state, or a third-party library failure."
    ),
    "suggested_fix": (
        "1. Review the full stack trace to locate the exact line that raised the error.\n"
        "2. Add structured logging around the failing code path.\n"
        "3. Write a unit test that reproduces the error to verify any fix.\n"
        "4. Check recent deployments or dependency upgrades that may have introduced the regression.\n"
        "5. Search the issue tracker / changelog of any involved library for known bugs."
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_error(error_message: str) -> dict:
    """
    Analyse *error_message* and return a dict with keys:
        category, root_cause, suggested_fix
    """
    lower = error_message.lower()

    for keywords, meta in _RULES:
        if any(kw in lower for kw in keywords):
            return {
                "category": meta["category"],
                "root_cause": meta["root_cause"],
                "suggested_fix": meta["suggested_fix"],
            }

    return dict(_DEFAULT)
