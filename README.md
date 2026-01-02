# UK Visa Jobs Platform

A dedicated recruitment platform designed to bridge the gap between UK international students and employers willing to sponsor visas. This platform ingests and verifies employer sponsorship status against official government data to ensure high-match quality for students on Student or Graduate route visas.

## Architecture

This project is a monorepo containing:

*   **`backend/`**: Python FastAPI service handling the core API, user management, and eligibility logic.
*   **`frontend/`**: (Planned) Next.js web application for students and employers.
*   **`scraper/`**: Python scripts for data ingestion (Gov.uk sponsor list) and normalization.

## Getting Started

### Prerequisites

*   Python 3.9+
*   Node.js 18+ (for frontend)
*   PostgreSQL (Local or Cloud)
*   Elasticsearch

### Setup

See individual directories for specific setup instructions.
