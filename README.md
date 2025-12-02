# MCP Quiz server

A MCP server to create and manage quizzes. It allows MCP clients to create, retrieve and delete quizzes from a supabase DB.
The project is in a very early stage and the schemas are not public, although they can be inferred from the handlers.

## 🔥 What's new

- Create quizzes with three type of questions: fill-in-blank, multiple choice, and column match.

## ✨ Key Features

The server exposes 4 tools: 
- `list_quizzes`
- `get_quiz`
- `create_quiz`
- `delete_quiz`

## 🚀 Installation & Development

As a user you normally don't need to install it, you should only add it to your MCP Client or LLM agent.

For development I use a podman image with python and `uv`, the container file is included in `/containers`.

To build the image you can use podman like this: `podman build -t uv -f containers/Containerfile.uv .`.

After creating the image you need to:

- Log into your container, you can use better methods like setting an entry point and workdir but you can also have a totally generic uv image and work from the shell `podman run -it --rm --name uv-dev -v .:/app -p 9000:9000 uv /bin/bash`
- Create a venv with `uv venv`.
- Activate the virtual environment with `source .venv/bin/activate`.
- Run MCP server using fastmcp with `fastmcp run -t streamable-http --host 0.0.0.0 -p 9000 main.py`

There are a few different ways to work with the MCP, the one that worked the best for me, since I already had node in my local machine is to run `npx @modelcontextprotocol/inspector http://127.0.0.1:9000/mcp --transport http`.
That command is used to run the official [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector).

## 🤝 Contributing

Contributions are welcome, please open an issue first so we can be sure your merge request will actually be merged.
