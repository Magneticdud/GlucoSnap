# GlucoSnap - Diabetes Monitoring Application

GlucoSnap is a comprehensive Django-based application designed to help users monitor their diabetes. It features glucose tracking, AI-powered meal analysis, and detailed reporting.

## Features

- **Glucose Tracking**: Log your glucose levels with context (fasting, post-meal, etc.).
- **AI Meal Analysis**: Upload photos of your meals to get automatic descriptions, calorie estimates, and carb counts using OpenAI GPT-4 Vision.
- **Dashboard**: Interactive charts and statistics to visualize your progress.
- **Data Export**: Export your data to Excel, ODS, or CSV formats.
- **PDF Reports**: Generate professional PDF reports for your doctor.
- **Internationalization**: Support for English and Italian languages.

## Installation

### Prerequisites

- Python 3.10+
- OpenAI API Key (for meal analysis)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd GlucoSnap
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` and add your `OPENAI_API_KEY`.
    - Set `DEBUG=True` for development.

5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

8.  **Access the application:**
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Configuration

### OpenAI API
To enable the AI meal analysis feature, you must provide a valid OpenAI API key in the `.env` file:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### Internationalization
The project is set up for English and Italian. To compile translations (requires GNU gettext):
```bash
python manage.py compilemessages
```

## Technology Stack

- **Backend**: Django 5.x
- **Database**: SQLite (Development), PostgreSQL (Production ready)
- **Frontend**: Bootstrap 5, Chart.js
- **AI**: OpenAI GPT-4 Turbo with Vision
- **Reporting**: WeasyPrint (PDF), OpenPyXL (Excel), ODFPy (ODS)

## License

GNU General Public License v3.0
