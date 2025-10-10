# Development

Intall dependencies:
```
uv sync
```

Sort imports:
```
uv run ruff check --select I --fix
```

Format code:
```
uv run ruff format
```

Run tests:
```
uv run pytest
```

Run a specific test and print results:
```
uv run pytest -s test/test_google_news.py
```

Run tests for type checking:
```
uv run pytest src/
```
