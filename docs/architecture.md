# MovieWizard Architecture

## Core Components

- **Web Interface (`interface.html`):** The primary user-facing tool for visual film discovery.
- **CLI Tool (`main.py` -> `src/app/cli.py`):** A command-line script for deep searching and scraping movie data into JSON files.

## Project Structure

- **`src/`:** Contains the application source code.
    - **`app/`:** CLI application logic and entry points.
    - **`components/`:** UI components for the web interface (JS/CSS).
    - **`constants/`:** Shared configuration and metadata (TMDb genres, providers).
    - **`domain/`:** Core business logic and filtering rules.
    - **`services/`:** API interaction layers and external clients.
    - **`utils/`:** Generic helper functions.
- **`tests/`:** Automated test suite.
    - **`integration/`:** End-to-end and integration tests.
    - **`unit/`:** Granular tests for specific modules.
- **`scripts/`:** Platform-specific automation and launcher scripts.

## Data Flow

1. **User Interaction:** User selects filters in the Web UI or via the CLI prompts.
2. **Filter Construction:** Domain logic processes user input into TMDb API-compatible parameters.
3. **API Request:** Service layer sends requests to the TMDb Discovery API using the provided API key.
4. **Data Processing:** Results are formatted and presented to the user (Web) or saved to a JSON file (CLI).

## Design Principles

- **Modular Design:** Separation of concerns between UI, domain logic, and API interactions.
- **TDD Workflow:** Features are developed using a test-first approach.
- **Privacy First:** Sensitive data (API keys) are never stored on a server.
