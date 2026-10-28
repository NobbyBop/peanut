# peanut
a minimal harness for tiny models. it's just a little peanut.
has access to your terminal (powershell, but you could easily change that)

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

## what can peanut do?
- have a chat
    - peanut will run commands as you request them
- translate natural language to command and execute it
    - example: `peanut -t "rename all the files in here to MM-DD-YYYY format"`