# NAOMI Streamlit

## Overview
NAOMI Streamlit is the user-facing web application built with Streamlit, providing an interface for interacting with NAOMI. It allows users to manage responsibilities, monitor NAOMI's internal thinking, view observations, and track actions in real time.

## Features

### Currently Implemented
- **Chat Interface**: Communicate with NAOMI through an intuitive chat-based UI.
- **Database Integration**: Retrieves and updates data from the shared database.

### Planned Features
- **Responsibility Management**: Create, modify, and track assigned responsibilities.
- **Internal Monitoring**: View NAOMI's decision-making process, observations, and event triggers.
- **Task and Event Tracking**: Keep track of NAOMI's scheduled actions and insights.

## User Guide
### Accessing the Chat Interface
- Open the Streamlit app in your browser.
- Interact with NAOMI through text input.

### Managing Responsibilities
- Navigate to the Responsibilities tab.
- Add, modify, or delete assigned tasks.

### Monitoring Internal Insights
- View NAOMI's decision-making and thought processes in real-time.
- Track how responsibilities and events influence NAOMI's actions.

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

## Development Setup

### Working with local naomi_core

For streamlined development across both `naomi_streamlit` and `naomi_core` repositories, this project includes a development mode that allows for hot-reloading of changes made to the `naomi_core` codebase.

#### How it works

1. A symbolic link to the `naomi_core` directory is created in this project
2. The `pyproject.toml` is modified to include this symlinked directory as a package
3. Streamlit watches this directory and reloads when changes are detected
4. `.gitignore` is configured to prevent these development-specific changes from being committed

#### Usage

To toggle between development and production modes, use the provided script:

```bash
# Enable development mode (use local naomi_core)
poetry run python dev_mode.py on

# Disable development mode (use naomi_core from git)
poetry run python dev_mode.py off
```

After switching modes, restart your Streamlit app for changes to take effect.

#### Working with Git

The following files are ignored in `.gitignore` to prevent committing development-specific changes:

- `/naomi_core` - The symlink to local naomi_core
- `.streamlit/config.toml` - Local Streamlit configuration

#### Reset to production state

If you need to reset to a clean state for committing changes:

1. Run `poetry run python dev_mode.py off` to disable development mode
2. Run `git status` to ensure there are no unintended changes

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