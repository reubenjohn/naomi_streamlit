# The `streamlit hello` multipage demo app, on Railway!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/nj-Wms?referralCode=ySCnWl)

This project highlights Streamlit's new multipage app functionality. Now deployable directly to Railway!

![In-use Animation](https://github.com/streamlit/hello/blob/main/mpa-hero.gif?raw=true "In-use Animation")

## Project Setup

For instructions on setting up the project for development and contributions, see [CONTRIBUTING.md](CONTRIBUTING.md)

Configuring OAuth with streamlit see [docs](https://docs.streamlit.io/develop/concepts/connections/authentication).

And define the .streamlit/secrets.toml file accordingly:
```toml
[auth]
redirect_uri = "http://localhost:8088/oauth2callback"
cookie_secret = "..."
client_id = "..."
client_secret = "."
server_metadata_url = "..."
```

To set up the environment variables, create a `.env` file in the root directory of your project (See [.env.example](.env.example)) and add the following lines:

```shell
OPENAI_BASE_URL=https://your_openai_endpoint
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_MODEL=your_model_name
```

Note that the OpenAI endpoint can be any endpoint that implements the OpenAI API (eg. Ollama).
Alternatively, you can provide the `--openai_base_url` and `--openai_api_key` arguments when running the CLI:

```bash
$ python -m token_world --openai_base_url http://192.168.1.199:11434/v1 --openai_api_key your_openai_api_key_here
#or
$ token_world --openai_base_url http://192.168.1.199:11434/v1 --openai_api_key your_openai_api_key_here
```


## How to run this project locally

- pip install -r requirements.txt
- streamlit run Hello.py
- open your browser to `http://127.0.0.1:8501`

## Learn more

- [The original repository that this template used](https://github.com/streamlit/hello)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Multipage Documentation](https://docs.streamlit.io/library/get-started/multipage-apps)
- [Blog post](https://blog.streamlit.io/introducing-multipage-apps/)

## What makes this work on Railway?

For this project to run on Railway I have added a `railway.json` file with a custom start command, let me break the start command down:
- `streamlit run Hello.py` tells streamlit to run `Hello.py`
- `--server.address 0.0.0.0` listen on host `0.0.0.0` so that streamlit is accessible externally
- `--server.port $PORT` configures streamlit to listen on the auto assigned `PORT` variable that railway expects the app to listen on
- `--server.fileWatcherType none` turns off the file watcher, code changes can't be made after the deployment so starting a file watcher uses unnecessary resources and can cause instabilities
- `--browser.gatherUsageStats false` disables telemetry reporting
- `--client.showErrorDetails false` disables showing debug messages in the browser
- `--client.toolbarMode minimal` removes the 3-dot debug menu from the deployed site

Documentation for additional configurations can be found [here](https://docs.streamlit.io/library/advanced-features/configuration)

I have also updated the dependencies in the `requirements.txt` file, and added a `.python-version` file that tells Railway to build this project with Python 3.10

## Questions? Comments? - Streamlit

Please ask in the [community forum](https://discuss.streamlit.io)

## Questions? Comments? - Railway

Join our [discord server](https://discord.gg/railway) and open a `#Help` thread!
