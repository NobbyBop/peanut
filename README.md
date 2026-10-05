# peanut
a minimal harness for tiny models. it's just a little peanut.

## how to run it quickly
1. install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. install [ollama](https://ollama.com/download)
3. `ollama serve`
4. (in another terminal) `ollama pull <model>`
5. in `.env`, set `MODEL=<model>` (defaults to `gemma4:e2b`)
2. `uv sync`
3. `uv run peanut`

## sessions
1. created when exiting a chat with /exit
2. keyed by date
3. format:
```json
{
    "title":"example title",
    "messages":[
        {
            'role':'user',
            'content':"blah blah blah"
        },
        {
            'role':'assistant',
            'content':"blah blah blah"
        }, 
    ]
}
```

## tools
1. defined in `TOOLS_DIR` as individual python modules.
2. module `<name>.py` must define functions:
 1. `<name>()` - the tool logic
 2. `describe()` - an optional explanation of the tool and when to use it