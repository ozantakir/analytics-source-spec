# Analytics Spec Extractor

This repository serves as the entry point for extracting analytics event definitions from product specifications and converting them into standardized raw data formats.

## Architecture & Flow
- **Sources:** Event tables, figma screenshots and response data.
- **Role:** Parses free-form text, headers, and tables into structured event definitions.
- **Output:** Triggers downstream workflows to push normalized JSON Schemas to **https://github.com/ozantakir/analytics-schema-repo**.

## How It Works
1. GitHub Actions inspect updated product documents.
2. Python-based LLM parsers extract event metadata (`event_name`, `destinations`, `parameters`).
3. Validated event structures are committed directly to the central Schema Repo.
