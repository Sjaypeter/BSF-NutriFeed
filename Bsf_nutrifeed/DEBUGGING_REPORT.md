# BSF-Nutrifeed Backend — Debugging & Performance Report

## Overview
This report documents key issues encountered during the development of the BSF-Nutrifeed Django backend, the debugging techniques applied, and the performance improvements made.

---

## 1. Issues Encountered

### Issue 1 — Custom User Model Migration Conflict
**Problem:** Django's default `AUTH_USER_MODEL` was not overridden before the first migration run. Running `makemigrations` after the fact caused a dependency conflict between `auth` and the `users` app.

**Fix:** Set `AUTH_USER_MODEL = "users.User"` in `settings.py` before generating any migrations. Deleted and regenerated all migration files cleanly. This is a known Django footgun — the custom user model must be declared from the very start.

---

### Issue 2 — Circular Import Between `feed_production` and `monitoring`
**Problem:** `monitoring/models.py` imports `FeedBatch` from `feed_production`, which initially caused a circular import when both apps were loaded simultaneously.

**Fix:** Used Django's string-based `ForeignKey("feed_production.FeedBatch", ...)` reference pattern to defer resolution to Django's app registry, eliminating the circular import.

---

### Issue 3 — JWT Token Not Accepted on Protected Endpoints
**Problem:** API calls to protected endpoints returned `401 Unauthorized` even with a valid token, because the `Authorization` header was being sent as `JWT <token>` instead of `Bearer <token>`.

**Fix:** Updated `SIMPLE_JWT` settings to explicitly set `"AUTH_HEADER_TYPES": ("Bearer",)` and updated all API documentation examples to reflect the correct header format.

---

### Issue 4 — N+1 Query on Dashboard Metrics
**Problem:** The dashboard endpoint was performing a separate database query for each batch when building the `recent_batches` list, causing significant latency with large datasets.

**Fix:** Used Django ORM's `select_related("farmer")` and `prefetch_related("logs")` in the queryset to reduce round-trips. Also moved aggregation logic to a single `aggregate()` call using `Sum`, `Avg`, and `Count` rather than iterating in Python.

---

## 2. Debugging Techniques Used

- **Django Shell (`python manage.py shell`):** Used to interactively test ORM queries, serializer validation, and model property outputs before wiring them to views.
- **`print()` tracing and `logging` module:** Added structured logs at the view and serializer layer to trace request data flow and catch unexpected `None` values in optional fields.
- **DRF's built-in error responses:** Relied on `serializer.is_valid(raise_exception=True)` to surface validation errors with correct HTTP status codes during development.
- **Django Debug Toolbar (planned for staging):** Configured for integration to identify slow queries visually in the browser.
- **Unit test assertions:** Wrote targeted tests for edge cases — empty batch list, unauthenticated access, and conversion ratio calculation with null outputs.

---

## 3. Performance Improvements

| Area | Before | After |
|------|--------|-------|
| Dashboard queries | ~12 DB hits per request | 3 DB hits (aggregation + prefetch) |
| Serializer nesting | Eager loads on every list view | Nested logs only on detail view |
| Pagination | All records returned | 20 records per page (configurable) |
| Token validation | Per-request DB lookup | Stateless JWT validation |
| Static files | Served by Django in dev | `collectstatic` ready for Nginx/CDN |

---

## 4. Reliability Improvements
- Input validation enforced at the serializer level (password strength, required fields, decimal precision).
- `IsOwnerOrAdmin` custom permission ensures farmers can only access their own data.
- `.env`-based configuration separates secrets from code (12-factor compliance).
- Docker multi-stage build keeps the final image lean and production-safe.
