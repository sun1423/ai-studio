# AI Studio

A compact, local-first dashboard/backend for:

- **Content Studio:** create content variants, review them, and publish approved work through PlayCon.
- **Voice Studio:** process WAV audio through Chatterbox then OpenVoice and manage saved profiles.
- **Queue:** persist jobs in SQLite and run heavy AI work sequentially.
- **Telegram:** optional intake and notifications, not AI inference.

## Current status

The initial commit provides the configuration, SQLite schema, protected API, and persistent job-request storage. Model runners, UI, Telegram, and PlayCon adapters are not yet wired up.

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set a strong APP_PASSWORD in .env, then run:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

/health is public. Other endpoints require HTTP Basic authentication. Do not expose the service directly to the internet.

## Azure optimisation

Set DATA_DIR to the mounted data disk path if one exists. Model files, uploads, generated media, and backups should live there rather than in the Git checkout or OS disk. The worker will be limited to one heavy job at a time.

## Secrets and licensing

Never commit secrets or user media. Verify individual model and runtime licenses before redistribution.
