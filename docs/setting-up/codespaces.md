# Codespaces

For this workshop, since we're not really doing any heavy lifting, we can work entirely within Github Codespaces. If you would rather not use GitHub Codespaces, you can follow the instructions detailed on the "Running locally" page under "Setting up".

First create a new repository on Github, and then create a codespace from that repository. 

Navigate to the LLM workshop repo (click the GitHub symbol in the top right of this page). Switch to the `Handson` branch, and download the content as a zip file. Upload this to your new repo. Open the repo as a Codespace. There is no need to create a virtual environment, since you're already in a containerized environment anyway with a version of Python 3.12.

You don’t need to create or manage a virtual environment yourself. The devcontainer will automatically install `uv`, create and activate a `.venv`, and install all required dependencies when your Codespace is built.

You will also need to run the following in the terminal in order to use `chromadb`:

```bash
mkdir mkdir -p /home/codespace/.local/lib/python3.12/site-packages/google/colab
```

Add a new file in the root directory called `.gitignore`. Add the following to the `.gitignore` file:

```bash
.env
```

and save it.

You should then create a new file called `.env` and add your OpenAI API key to it.

```bash
OPENAI_API_KEY=<YOUR_API_KEY>
```

!!! warning

    Please add `.env` to your `.gitignore` before adding the API key to the `.env` file and before pushing any changes to your repo! There are bots crawling GitHub for exposed API keys.