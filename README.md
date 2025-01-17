
<div style="display:flex; gap: 8px">

[![unit test](https://img.shields.io/badge/Unit%20Test-passing-<COLOR>.svg)](https://shields.io/) ![pylint](https://img.shields.io/badge/PyLint-9.44-green) [![license](https://img.shields.io/badge/LICENSE-MIT-<COLOR>.svg)](https://shields.io/)

</div>


🚧 **Under Development** 🚧

# AI-OPS

### Table of Contents
1. [Overview](#-overview)
   - [Key Features](#key-features)
3. [Install](#-install)
4. [Usage](#-usage)
   - [Commands](#commands) 
   - [Supported Models](#supported-models)
5. [Tools](#tools)
   - [Available Tools](#available-tools)
   - [Add a Tool](#add-a-tool)
6. [Knowledge](#-knowledge-)
   - [Available Collections](#available-collections)
   - [Add a Collection](#add-a-collection)
7. [Ethical and Legal Considerations](#-ethical-and-legal-considerations)

## 💡 Overview

**AI-OPS** is an AI-powered, open-source **Penetration Testing assistant** that leverages large language models (LLMs) with [Ollama](https://github.com/ollama/ollama) in order to be cost-free. It is <ins>designed to enhance, not replace, the capabilities of human penetration testers</ins>.

> **Note:** AI-OPS is currently in development and some functionalities are not implemented. Any support or feedback is highly appreciated. For more details refer to [CONTRIBUTE.md](./CONTRIBUTE.md).

## 🚀 Key Features

- 🎁 **Full Open-Source**: No need for third-party LLM providers; use any model you prefer with [Ollama](https://github.com/ollama/ollama).
- 🔧 **Tool Integration**: Execute common penetration testing tools or integrate new ones without needing to code in Python.
- 📚 **Up-to-date Knowledge**: Use Online Search and RAG to keep the agent informed with the latest documents and data. (*Under Development*)

<!-- ## ▶️ Demo

### Write-Ups

- [Brute It — Try Hack Me Writeup](https://medium.com/@lorenzoantonino946/brute-it-walkthrough-try-hack-me-writeup-8b93c65213cb)


TODO
-->

## 💻 Install
**Requirements**
- Python (>= 3.11)
- Ollama (>= 0.3.0)
- Docker

```
# Clone Repository 
git clone https://github.com/antoninoLorenzo/AI-OPS.git

# Launch Ollama Locally
./scripts/ollama_serve.* -i OLLAMA_HOST -o OLLAMA_ORIGINS
 
# Run `ai_ops_api.py` or build manually:
docker build -t ai-ops:api-dev --build-arg ollama_endpoint=ENDPOINT ollama_model=MODEL .
docker run -p 8000:8000 ai-ops:api-dev

# Install Client
pip install .

# Run Client
ai-ops-cli --api AGENT_API_ADDRESS
```
  
<!--
qdrant

ps
docker run -p 6333:6333 -p 6334:6334 -v "${Env:USERPROFILE}\.aiops\qdrant_storage:/qdrant/storage:z" qdrant/qdrant

-->

## 📝 Usage

After deploying the Large Language Model (LLM) with Ollama and the AI Agent API, you can access the API using **ai-ops-cli.py**. 
If you have deployed the AI Agent API using Docker on a specific machine (e.g., an old laptop), you can specify the Agent API endpoint with the `--api` option.

To view the available options and commands, run `python ai-ops-cli.py -h`:
```
usage: ai-ops-cli.py [-h] [--api API]        
                                             
options:                                     
  -h, --help  show this help message and exit
  --api API   The Agent API address      
```

### Commands

Once the CLI is running, you can interact with the agent using the following commands:

| Command                 | Description                                         |
|-------------------------|-----------------------------------------------------|
| **Basic Commands**      |                                                     |
| `help`                  | Display a list of available commands.               |
| `clear`                 | Clears the terminal.                                |
| `exit`                  | Exit the program.                                   |
| **Assistant Commands**  |                                                     |
| `chat`                  | Open a chat session with the agent.                 |
| `back`                  | Exit the chat session.                              |
| `exec`                  | Execute the last plan generated by the agent.       |
| `plans`                 | List all plans created in the current session.      |
| **Session Commands**    |                                                     |
| `new`                   | Create a new session.                               |
| `save`                  | Save the current session.                           |
| `load`                  | Load a saved session.                               |
| `delete`                | Delete a saved session from the persistent storage. |
| `rename`                | Rename the current session.                         |
| `list sessions`         | Display all saved sessions.                         |
| **RAG Commands**        |                                                     |
| `list collections`      | Lists all collections in RAG.                       |
| `create collection`     | SUpload a collection to RAG.                        |

### Supported Models
To integrate a LLM see [LLM Integration](./CONTRIBUTE.md#llm-integration) in CONTRIBUTE.md

| Name          | Implemented   | RAG Support  | 
|---------------|---------------|--------------|
| **Mistral**   | &check;       | &check;      |
| **Gemma 7B**  | &check;       | ✖️           |
| **Gemma2 9B** | &check;       | ✖️           |

> RAG Support depends on Tool Support for Ollama models, see [Ollama Library](https://ollama.com/library).  

<!--| **LLama 3**  | &cross;               | -->

<!--
### Components
| Component                                  | Description       |
|--------------------------------------------|-------------------|
| AI Agent                                   | `FastAPI` Backend |
| [Qdrant](https://github.com/qdrant/qdrant) | Vector Database   |
| [Ollama](https://github.com/ollama/ollama) | LLM Provider      | 

| Frontend                                   | Web interface for the AI Agent built in `React` (**not implemented***)  |

> **The frontend is prototyped in `frontend-prototype` branch, containing a `React` application, however it is not currently in development*
-->
<!--
![Deployment Diagram](static/images/deployment_diagram.svg)
-->

## 🛠️Tools

### Available Tools

| Name                                                    | Use Case                         | Implemented         |
|---------------------------------------------------------|----------------------------------|---------------------|
| [nmap](https://github.com/nmap/nmap)                    | Scanning/Network Exploitation    | &check;             |
| [gobuster](https://github.com/OJ/gobuster)              | Enumeration                      | &check;             |
| [hashcat](https://github.com/hashcat/hashcat)           | Password Cracking                | &check;             |
| [thc-hydra](https://github.com/vanhauser-thc/thc-hydra) | Brute Force                      | &check;             |
| [SQLmap](https://github.com/sqlmapproject/sqlmap)       | SQL Injection                    | &check;             | 
| [searchsploit](https://www.kali.org/tools/exploitdb/)   | Research Vulnerabilities         | &check;             |

*Note: virtually any tools that do not require additional code (such as Metasploit) can be executed*


### Add a Tool

Penetration Testing tools can be integrated using either JSON documentation or custom classes.

1. **JSON Documentation**: the content of the JSON documentation is provided in the `system prompt` of the 
Agent; to ensure correct tool usage the documentation quality should be as high as possible, while keeping
it as short as possible to maintain the context of a reasonable length.

    For this reason it is provided a python script at `scripts/gen_tool_guidelines.py` that generates the 
    JSON documentation file given its documentation; it requires the original tool documentation and a 
    **GEMINI API KEY**, its usage is as follows:
    ```
    usage: gen_tool_guidelines.py [-h] --tool-name TOOL_NAME --docs-path DOCS_PATH --api-key API_KEY [--output-path OUTPUT_PATH]
                                                                                                                                
    options:                                                                                                                    
      -h, --help                 show this help message and exit      
                                                                  
      --tool-name TOOL_NAME      The name of the tool                                                                                                      
      --docs-path DOCS_PATH      The path to the JSON documentation file                                                                                                     
      --api-key API_KEY          API key for Gemini                                                                                  
      --output-path OUTPUT_PATH  Specifies the path for tool guidelines (*Optional*)                                                                                               
                              
    ```
    Once the file is created add it to `/home/YOUR_USERNAME/.aiops/tools` (or `../Users/YOUR_USERNAME/.aiops/tools`); 
   all available tools that use JSON Documentation are already available in `tools_settings` with the following structure:
    ```json
    {
        "name": "...",
        "tool_description": "...",
        "args_description": [
            "Multiline JSON\n",
            "instructions\n",
            "..."
        ]
    }
    ```
    > *Note*: always check the JSON file structure, it is generated by a LLM and can eventually fail. 
    If you want to integrate the tool in the repository see [CONTRIBUTE.md](./CONTRIBUTE.md) 

2. **Custom Class**: tools that require more advanced usage can be implemented extending the class
`Tool` at `src.agent.tools.base`; you're welcome to **open an issue** for a tool request/proposal.


## 📚 Knowledge (RAG)

🚧 *Under Development* 🚧

<!--

### Available Collections

**TODO**


### Add a Collection

**TODO**
-->

## ⚖️ Ethical and Legal Considerations

**AI-OPS** is designed as a penetration testing tool intended for academic and educational purposes only. Its primary goal is to assist cybersecurity professionals and enthusiasts in enhancing their understanding and skills in penetration testing through the use of AI-driven automation and tools.

### Responsible Use

- **Legal Compliance**: Ensure that you comply with all relevant laws and regulations when using this tool. Unauthorized access to computer systems is illegal and unethical.
- **Permission**: Always obtain explicit permission from the system owner before performing any penetration testing. Unauthorized testing is illegal and can cause significant harm.
- **Academic Integrity**: Use this tool to support your learning and research in ethical hacking and cybersecurity. Do not use it for malicious purposes.

### Disclaimer

The creators and contributors of **AI-OPS** are not responsible for any misuse of this tool. By using **AI-OPS**, you agree to take full responsibility for your actions and to use the tool in a manner that is ethical, legal, and in accordance with the intended purpose.

> **Note**: This project is provided "as-is" without any warranties, express or implied. The creators are not liable for any damages or legal repercussions resulting from the use of this tool.

