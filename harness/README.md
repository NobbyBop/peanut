# harness
a minimal harness for tiny models. it's just a little peanut.

## how to run it quickly
1. install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. install [ollama](https://ollama.com/download)
3. `ollama serve`
4. (in another terminal) `ollama pull gemma4:e2b`
5. `uv sync`
6. `uv run peanut`

## findings
- local models struggle with tools, i worked around this by using the `format` option on `ollama.generate()`
    - required the model to select `respond` or `<tool_name>` as its `action`
