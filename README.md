<div align="center">

# MovieWizard

**A powerful, dual-interface film discovery tool powered by TMDb.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Web](https://img.shields.io/badge/Interface-HTML%2FJS-E34F26?style=flat&logo=html5&logoColor=white)](interface.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Features](#features) | [Installation](#installation) | [Usage](#usage) | [Structure](#directory-structure)

</div>

---

## Important: API Key Required

To use **MovieWizard**, you **must** have your own API key from The Movie Database (TMDb). This software does not come with a built-in key for security and rate-limiting reasons.

1. **Register:** Create a free account at [themoviedb.org](https://www.themoviedb.org/).
2. **Generate Key:** Go to your [Account Settings > API](https://www.themoviedb.org/settings/api) and request a **v3 API Key**.
3. **Use:** You will be prompted to enter this key when you launch the Web UI or CLI tool.

---

## Overview

**MovieWizard** helps you find exactly what to watch by leveraging the deep metadata of The Movie Database (TMDb). It offers two ways to explore: a visual **Web Interface** for finding a movie tonight, and a **CLI Tool** for scraping comprehensive lists of movies based on specific criteria (genre, era, keywords) for data analysis or backlogs.

## Features

- **Visual Wizard:** A step-by-step UI to narrow down choices by mood, rating, and era.
- **Deep Search CLI:** A Python script to scrape thousands of movies into JSON databases.
- **Advanced Logic:** Filter by specific Keywords (e.g., "Time Loop", "Cyberpunk"), Streaming Providers (Netflix, Disney+), and Runtime.
- **Letterboxd Ready:** Results link directly to Letterboxd for reviews and logging.
- **Privacy Focused:** API keys are stored locally in your browser/session and never sent to our servers.

## Directory Structure

```text
MovieWizard/
|-- interface.html       # Main Visual Web Interface
|-- smart_filter.py      # Python CLI for Bulk Downloading
|-- requirements.txt     # Python Dependencies
|-- start.bat            # Launcher for Windows
|-- start.sh             # Launcher for Linux
|-- start.command        # Launcher for macOS
|-- __tests__/           # Automated Test Suite
`-- README.md            # Documentation
```

## Installation

### Prerequisites

1. **Python 3.x** (Required for the CLI tool only).
2. **TMDb API Key:** You can get one for free at [themoviedb.org](https://www.themoviedb.org/settings/api).

### Setup

Clone the repository and install the dependencies:

```bash
# 1. Clone the repository
git clone https://github.com/FelixCAxO/MovieWizard.git
cd MovieWizard

# 2. Install dependencies (Only needed for CLI Deep Search)
pip install -r requirements.txt
```

---

## Usage

### Option 1: The Web Interface (Visual)

*Best for: Finding a movie to watch right now.*

You do not need Python for this. Just double-click the starter script for your OS:

* **Windows:** Double-click `start.bat`
* **macOS:** Double-click `start.command`
* **Linux:** Run `./start.sh`

*Alternatively, simply open `interface.html` in Chrome, Firefox, or Edge.*

### Option 2: The CLI Tool (Deep Search)

*Best for: Generating large lists of movies (JSON) based on strict criteria.*

Run the python script to start the interactive terminal wizard:

```bash
python smart_filter.py
```

**The script will prompt you for:**

1. **API Key** (Input once per session).
2. **Genre** (e.g., "Science Fiction").
3. **Specific Filters** (Country origin, Runtime, Provider).
4. **Year Range** (Scans year-by-year for maximum results).

**Output:**
The script saves a detailed JSON file (e.g., `deep_database_150.json`) containing all matching movies, their IDs, ratings, and overviews.

---

## Configuration

**API Key Security:**

* **Web UI:** The key is stored in your browser's temporary memory. It is lost when you close the tab.
* **CLI:** You can hardcode your key in `smart_filter.py` line 9 to skip entry every time:
```python
# smart_filter.py
DEFAULT_API_KEY = "your_key_here"
```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request for any improvements.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
