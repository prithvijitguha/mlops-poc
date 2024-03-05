# MLOps POC

## Example poc for MLops testing

## Instructions to run:
```shell
pip install .[dev] .
```
OR

```shell
pip install -r requirements-dev.txt -r requirements.txt -r requirements-docs.txt

```

Create a file called `.env` in the root directory with your Open AI API Key

Your file contents should look like

```
# environment variables defined inside a .env file
OPENAI_API_KEY=my-open-ai-api-key
```

Now run
```
python src/main.py
```


Some reference reading:
- [open-ai-documentation](https://platform.openai.com/docs/introduction)
- [openai-python](https://github.com/openai/openai-python/tree/main)
- [open-ai-cookbook](https://github.com/openai/openai-cookbook/tree/main)
