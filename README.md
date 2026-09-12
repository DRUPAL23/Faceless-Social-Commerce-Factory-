# Faceless Social Commerce Factory

AI-powered content factory for faceless Instagram social commerce.

## Current milestone: Sprint 4

```text
Strategy → Content Director → Scoring → Top 90 → AI Script Engine → QA → Media → Publishing → Analytics
```

### Implemented
- FastAPI API
- 30-day / 90-Reel calendar generation
- Candidate scoring and content-pillar balancing
- Structured Reel copy generation
- Provider abstraction with deterministic mock provider
- Optional OpenAI provider
- Retry + JSON validation + safe fallback
- PostgreSQL schema for ideas and generated copy
- Docker and GitHub Actions CI

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD
uvicorn apps.api.app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `/docs` for Swagger UI.

## AI provider

Development requires no API key:

```bash
LLM_PROVIDER=mock
```

Production/OpenAI:

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY='YOUR_KEY'
export OPENAI_MODEL='gpt-5.6-mini'
```

Never commit API keys.

## API

`POST /ideas` generates scored candidates.

`POST /scripts` generates structured Reel copy.

`POST /calendar` creates a 30-day / 90-Reel scripted calendar.

## Roadmap

- Sprint 5: voice generation + subtitle timestamps
- Sprint 6: visual asset pipeline
- Sprint 7: FFmpeg Reel renderer
- Sprint 8: automated content QA
- Sprint 9: Instagram publishing
- Sprint 10: analytics feedback loop
- Sprint 11: social-commerce funnel
- Sprint 12: autonomous content factory
