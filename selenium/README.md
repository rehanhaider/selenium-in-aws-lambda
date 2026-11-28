# Selenium Lambda

- `src/` contains the Lambda image's `Dockerfile`, the handler in `app.py`, the browser installer in `install-browser.sh`, and the dependency lists in `chrome-deps.txt` and `requirements.txt`.
- `cdk_app.py` and `cdk.json` define and configure the CDK stack.
- `events/event.json` is a sample invocation event.
- `tests/` contains the unit tests.

The handler accepts an event like `{"url": "https://cloudbytes.dev/"}`. It accepts `http`, `https`, and `data` URLs and returns `{"url": ..., "description": ...}` with the page's meta description. Invalid input raises an exception and fails the invocation.

## Run the unit tests

Run the tests from this directory.

```bash
uv sync
uv run pytest
```

## Check the container locally

The image is x86_64, like the deployed function, because the browser download is linux64. On an ARM host, Docker emulates it.

```bash
docker build --platform linux/amd64 -t selenium-lambda src
docker run --rm --platform linux/amd64 --read-only --tmpfs /tmp -p 9000:8080 selenium-lambda
```

Send the sample event from this directory in a second terminal.

```bash
curl -s -XPOST localhost:9000/2015-03-31/functions/function/invocations -d @events/event.json
```

See the [root README](../README.md) for deployment instructions.
