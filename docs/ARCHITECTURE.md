# Architecture

Keep the system to one FastAPI service, SQLite, local files, and one heavy-job worker.

- **Content Studio:** local text model + ComfyUI for images; FFmpeg can assemble short videos from generated images, voice, captions, and music.
- **Voice Studio:** Chatterbox, then OpenVoice; save profile files and metadata locally.
- **Queue:** SQLite stores requests durably. Only one heavy AI job should run at once to protect CPU/RAM.
- **Integrations:** Telegram is for intake/notifications. PlayCon handles publishing. Neither is used for AI inference.
- **Storage:** put DATA_DIR on a mounted data disk when available. Keep models, uploads, outputs, and backups out of Git.

## Security

- Dashboard/API routes require HTTP Basic authentication. Set a strong APP_PASSWORD.
- /health is intentionally public for service checks.
- Bind to localhost by default. Expose only the authenticated dashboard through a protected reverse proxy/tunnel.
- Keep ComfyUI, text model runtimes, SQLite, and worker ports private.
- Never commit .env, tokens, source media, voice profiles, or generated files.

The initial backend stores job requests; the actual ComfyUI, Chatterbox/OpenVoice, Telegram, and PlayCon adapters are not represented as working until implemented and tested.
