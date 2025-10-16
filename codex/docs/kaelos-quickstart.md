# Kaelos Quickstart

Follow these steps to get the Codex Vault KaelOS environment running locally for development or documentation updates.

1. **Clone the repository**
   ```bash
   git clone https://github.com/codex-kael/autonomous-framework.git
   cd autonomous-framework
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Upgrade packaging tools**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```
4. **Install project dependencies**
   ```bash
   pip install -e .
   ```
5. **Review example agents and tools**
   Explore the `codex_framework/agents` and `codex_framework/tools` directories to understand available building blocks.

6. **Run the default smoke tests**
   ```bash
   pytest
   ```
7. **Start the Codex KaelOS orchestration loop**
   ```bash
   python -m codex_framework.codex_autonomous
   ```
8. **Implement your changes**
   Modify Python modules inside `codex_framework`, update documentation in `examples`, or extend datasets in `knowledge_base_text` as needed.

9. **Stage your updates without pathspec errors**
   Use `git add` with only the paths that currently exist in this repository:
   ```bash
   git add codex_framework examples knowledge_base_text pyproject.toml setup.py
   ```
   If you later introduce new directories or files (for example `codex/`, `Makefile`, or `requirements.txt`), create them first and then include them with an additional `git add` command or mark them as optional in the documentation until they exist.

10. **Commit and push**
    ```bash
    git commit -m "feat: describe your change"
    git push origin <your-branch>
    ```
