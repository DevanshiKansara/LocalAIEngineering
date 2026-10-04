# Local AI Engineering Assistant

A local LLM-based engineering assistant that combines natural-language interaction with deterministic Python engineering tools.

The project explores how local AI can be integrated into engineering software rather than used only as a general-purpose chatbot.

## What I Built

The assistant uses a local **Qwen3:4B** language model through **Ollama** to interpret engineering requests and decide when deterministic Python tools are required.

The Python tools perform the actual engineering calculations and validation.

Current tools include:

- Spindle speed calculation
- Feed rate calculation
- Cutting time calculation

The assistant can also chain dependent calculations automatically.

For example:

> "For a 10 mm cutter at 120 m/min, with 4 teeth and 0.05 mm/tooth, how long will it take to travel 500 mm?"

The system performs:

`Spindle Speed → Feed Rate → Cutting Time`

The language model handles natural-language understanding and tool orchestration, while Python performs the numerical calculations and input validation.

## Architecture

```mermaid
flowchart TD
    A[User<br/>Natural-language engineering request]
    B[Local LLM<br/>Qwen3:4B via Ollama]
    C[Python Tool Layer]
    D[Engineering Tools]
    E[Deterministic Calculation<br/>and Validation]
    F[Local LLM<br/>Result Interpretation]
    G[User<br/>Engineering result]

    A --> B
    B -->|Tool call| C
    C --> D
    D --> E
    E -->|Tool result| F
    F --> G

    D --> D1[spindle_speed]
    D --> D2[feed_rate]
    D --> D3[cutting_time]
```

### Example Tool Chain

```text
User
  │
  │ "10 mm cutter, 120 m/min,
  │  4 teeth, 0.05 mm/tooth,
  │  500 mm travel"
  ▼
Qwen3:4B
  │
  ├── spindle_speed()
  │       ↓
  │    3819.72 RPM
  │
  ├── feed_rate()
  │       ↓
  │    763.94 mm/min
  │
  └── cutting_time()
          ↓
       0.654 min
          │
          ▼
      Qwen3:4B
          │
          ▼
   "Approximately 39.2 seconds"
```

## Key Features

- **Local LLM inference** — Runs Qwen3:4B locally through Ollama without relying on a cloud AI API.
- **LLM tool calling** — The language model identifies when an engineering calculation requires a Python tool and requests it automatically.
- **Deterministic engineering calculations** — Python performs the numerical calculations instead of relying on the LLM for arithmetic.
- **Multi-step tool orchestration** — Supports dependent calculation chains such as:
  `spindle_speed → feed_rate → cutting_time`
- **Input validation** — Engineering tools validate their inputs and reject invalid values such as zero or negative parameters.
- **Controlled engineering responses** — The assistant is instructed not to invent engineering values or silently replace invalid inputs.
- **Modular tool architecture** — Engineering functions are separated from the LLM interaction layer through a central tool registry.
- **Fully local development** — The complete prototype runs on a laptop using local software and models.

**Current milestone:** Milestone 1 — Local LLM + deterministic engineering tool calling

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Local LLM Runtime | Ollama |
| Language Model | Qwen3:4B |
| LLM Integration | Ollama Python Client |
| Engineering Tools | Python |
| Tool Calling | Ollama tool-calling API |
| Environment | Python virtual environment |
| Version Control | Git / GitHub |
| Hardware | NVIDIA RTX 3050 Laptop GPU (6 GB VRAM) |

### Engineering Tools

| Tool | Purpose |
|---|---|
| `spindle_speed()` | Calculates spindle speed from cutting speed and tool diameter |
| `feed_rate()` | Calculates feed rate from spindle speed, number of teeth, and feed per tooth |
| `cutting_time()` | Calculates machining time from travel distance and feed rate |

## Demo

### Successful Engineering Calculation

[Watch successful calculation demo](demo/LocalAIEngineering_demo_success.mp4)

Demonstrates:

`Natural-language request -> Qwen3:4B -> Python tool calls -> deterministic calculations -> final result`

### Invalid Input Handling

[Watch validation/error-handling demo](demo/LocalAIEngineering_demo_error.mp4)

Demonstrates:

`Invalid input -> Python validation -> controlled error response`

