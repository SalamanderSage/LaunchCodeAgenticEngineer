# LaunchCodeAgenticEngineer

Course materials for LaunchCode's **Agentic Engineer** course. Each module has its own Docker development environment with Python 3.12, the Anthropic SDK, and the Claude Code CLI already set up, plus the exercises and sample files for that module.

## Project structure

```
.
├── module_1/   Base environment and first agent exercises
├── module_2/   Adds Slack/Gmail MCP servers, skills, and agents
└── module_3/   Multi-agent orchestration, custom MCP servers, and evaluation
```

Each module folder holds a complete environment: `Dockerfile`, `docker-entrypoint.sh`, `requirements.txt`, `settings.json`, `statusline.sh`, a `CLAUDE.md` with guidance for Claude Code, and a `README.md` with build and run steps.

### module_1: Base environment

| File | Purpose |
| --- | --- |
| `module_x.py` | Business-rule utilities (name normalization, discounts, and more). Used for the "Session A" exercise: write unit tests without changing the module. |
| `module_y.py` | Formatting and reporting helpers (currency, report titles, email masking, summary lines, Markdown tables, text truncation). Used for the "Session B" exercise: improve the documentation. |
| `agent_docker_check.md` | Prompt for having an agent check that the Docker image builds. |

### module_2: MCP servers, skills, and agents

| Path | Purpose |
| --- | --- |
| `skills/` | Claude Code skills: `check-gmail`, `send-email`, `send-slack-message`, `summarize-session` |
| `agents/` | Subagents: `code-reviewer`, `email-summarize` |
| `sample_review.py` | Sample code for the code-reviewer agent to review |
| `sample_docs/` | Sample PRD, rubric, and iteration log |

### module_3: Orchestration and evaluation

| Path | Purpose |
| --- | --- |
| `agents/` | Subagents: `planner`, `implementer`, `reviewer`, `code-reviewer`, `docs-reviewer`, `project-manager`, `email-summarize` |
| `skills/` | Same skills as Module 2 |
| `mcp/` | Custom MCP servers: `coursetools_server.py`, `retrieval/`, and `storage/`, plus a role allowlist |
| `eval/` | Evaluation harness: orchestrator, deterministic and rubric tests, regression and holdout runners, and routing analysis |
| `scripts/` | Helper scripts to start MCP servers and run retrieval comparisons |
| `docs/` | PRD, orchestration diagrams, routing map, retrieval report, and iteration and calibration logs |
| `.memory/reference/` | Reference notes used by the retrieval exercises |
| `.eval-artifacts/` | Saved baseline and evaluation run results (dev and holdout) |

## Getting started

Pick a module, then build and run its image from inside that module's folder. For example, for Module 1:

```bash
git clone https://github.com/LaunchCodeEducation/LaunchCodeAgenticEngineer.git
cd LaunchCodeAgenticEngineer/module_1
docker build -t agentic_engineer_1 .
docker run -it --rm -v claude-auth:/claude-auth -p 8501:8501 -v "$PWD":/workspace agentic_engineer_1
```

The `claude-auth` named volume keeps your Claude Code login between container runs and across all modules, so you only log in once.

See each module's `README.md` for full instructions, including Windows commands, pre-built images, and Gmail/Slack credential setup.

> **Keep secrets out of git.** Never commit `credentials.json`, `token.json`, or `.env`. The root `.gitignore` already covers `credentials.json` and `.env`.
