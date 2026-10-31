# AI Studio

Local-first Content Studio and Voice Studio.

- Content Studio: local AI-assisted content creation, review, and publishing through PlayCon.
- Voice Studio: Chatterbox followed by OpenVoice for saved voice profiles.
- SQLite-backed job queue; one heavy AI job at a time.
- Telegram is for intake/notifications; AI inference remains local.

See `docs/ARCHITECTURE.md` for the minimal architecture. Never commit secrets, model files, uploads, or generated media.
