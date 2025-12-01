# GlucoSnap - Applicazione per il Monitoraggio del Diabete

GlucoSnap è un'applicazione completa basata su Django progettata per aiutare gli utenti a monitorare il diabete. Offre tracciamento della glicemia, analisi dei pasti basata su AI e reportistica dettagliata.

## Funzionalità

- **Tracciamento Glicemia**: Registra i livelli di glicemia con contesto (digiuno, post-prandiale, ecc.).
- **Analisi Pasti AI**: Carica foto dei tuoi pasti per ottenere descrizioni automatiche, stime delle calorie e conteggio dei carboidrati utilizzando OpenAI GPT-4 Vision.
- **Dashboard**: Grafici interattivi e statistiche per visualizzare i tuoi progressi.
- **Esportazione Dati**: Esporta i tuoi dati in formato Excel, ODS o CSV.
- **Report PDF**: Genera report PDF professionali per il tuo medico.
- **Internazionalizzazione**: Supporto per le lingue Inglese e Italiano.

## Installazione

### Prerequisiti

- Python 3.10+
- Chiave API OpenAI (per l'analisi dei pasti)

### Setup

1.  **Clona il repository:**
    ```bash
    git clone <repository-url>
    cd GlucoSnap
    ```

2.  **Crea e attiva un ambiente virtuale:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Installa le dipendenze:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura le Variabili d'Ambiente:**
    - Copia `.env.example` in `.env`:
      ```bash
      cp .env.example .env
      ```
    - Modifica `.env` e aggiungi la tua `OPENAI_API_KEY`.
    - Imposta `DEBUG=True` per lo sviluppo.

5.  **Esegui le Migrazioni:**
    ```bash
    python manage.py migrate
    ```

6.  **Crea un Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Avvia il Server:**
    ```bash
    python manage.py runserver
    ```

8.  **Accedi all'applicazione:**
    Apri [http://127.0.0.1:8000](http://127.0.0.1:8000) nel tuo browser.

## Configurazione

### OpenAI API
Per abilitare la funzionalità di analisi AI dei pasti, devi fornire una chiave API OpenAI valida nel file `.env`:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### Internazionalizzazione
Il progetto è configurato per Inglese e Italiano. Per compilare le traduzioni (richiede GNU gettext):
```bash
python manage.py compilemessages
```

## Stack Tecnologico

- **Backend**: Django 5.x
- **Database**: SQLite (Sviluppo), PostgreSQL (Pronto per la produzione)
- **Frontend**: Bootstrap 5, Chart.js
- **AI**: OpenAI GPT-4 Turbo con Vision
- **Reportistica**: WeasyPrint (PDF), OpenPyXL (Excel), ODFPy (ODS)

## Licenza

GNU General Public License v3.0
