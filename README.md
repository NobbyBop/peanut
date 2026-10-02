# peanut
A minimal harness for tiny models. It's just a little peanut.

## How to run it quickly
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Install [ollama](https://ollama.com/download)
3. `ollama serve`
4. (In another terminal) `ollama pull <model>`
5. In `.env`, set `MODEL=<model>` (defaults to `gemma4:e2b`)
2. `uv sync`
3. `uv run peanut`