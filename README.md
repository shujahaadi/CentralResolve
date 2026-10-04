# CentralResolve

> One project. Multiple conversations. One clear picture.

CentralResolve analyzes team conversations from WhatsApp and Discord to find contradictions that can easily get buried when a project is discussed across multiple platforms.

It answers one simple question:

**Are we actually on the same page?**

## The Problem

Teams rarely keep all of their communication in one place.

A task can be assigned on WhatsApp, discussed again on Discord, and changed later without everyone seeing the update.

That can lead to:

- Conflicting task ownership
- Different deadlines
- Contradictory project statuses
- Unresolved decisions

Reading through long exports from multiple platforms manually is slow and easy to get wrong.

CentralResolve brings those conversations together and surfaces the parts that need attention.

## How It Works

~~~text
WhatsApp Export ──┐
                  ├──> FastAPI ──> Gemma 3 4B
Discord Export ───┘                 │
                                    ↓
                             Structured Facts
                                    ↓
                       Deterministic Conflict Detection
                                    ↓
                              React Dashboard
~~~

### 1. Parse

CentralResolve accepts:

- WhatsApp chat exports (`.txt`)
- Discord message exports (`.json`)

Messages from both platforms are converted into a common structure while preserving their original platform.

### 2. Understand

CentralResolve uses **Gemma 3 4B locally through Ollama** to extract structured project facts from the conversations.

It identifies facts such as:

- Task assignments
- Deadlines
- Project status
- Decisions
- Unresolved issues

The model is instructed to preserve the original message as evidence instead of inventing information.

### 3. Detect

The extracted facts are passed to deterministic Python logic.

CentralResolve currently detects:

- **Ownership conflicts**
- **Deadline conflicts**
- **Status conflicts**
- **Unresolved decisions**

The conflict detector is separate from the LLM. This keeps the final conflict rules explicit, inspectable, and reproducible.

### 4. Explain

Every detected conflict includes the evidence that caused it, along with its original platform.

For example:

~~~text
OWNERSHIP CONFLICT
deployment

WhatsApp
"Rahul: I'll handle deployment."

Discord
"Rahul: I can't handle deployment anymore."
~~~

The goal is not just to say that something is wrong, but to show **why** it was flagged.

## Why Open-Source AI Matters

CentralResolve works with potentially private team conversations.

The current implementation runs **Gemma 3 4B locally through Ollama**, meaning AI inference can happen on the user's own machine instead of requiring a closed third-party AI API.

~~~text
Conversation Files
       ↓
    FastAPI
       ↓
 Local Ollama
       ↓
 Gemma 3 4B
       ↓
Structured Facts
~~~

This matters because conversation data does not have to leave the machine just to be analyzed by an AI model.

Using an open-weight model also gives the project flexibility to:

- Swap models
- Change prompts and behavior
- Run inference locally
- Adapt the system without being locked to a proprietary AI API

For CentralResolve, privacy is particularly important because the input may contain private conversations between teammates.

## Built for a Friend

CentralResolve was built around a real communication problem faced by a friend working with a team.

Their conversations were spread across multiple platforms, making it difficult to keep track of changing decisions, responsibilities, and deadlines.

Instead of building another generic chat summarizer, CentralResolve focuses on a more practical question:

**What important disagreements are hiding between our conversations?**

The result is a tool that highlights the issues that may actually require a human decision.

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Ollama
- Gemma 3 4B

### Frontend

- React
- Vite
- JavaScript
- CSS

### Analysis

- Structured LLM extraction
- Deterministic conflict detection

## Architecture

~~~text
                     CentralResolve

┌──────────────────┐
│ WhatsApp Export  │
└────────┬─────────┘
         │
         │
         ├──────────────┐
         │              │
         │      ┌───────▼────────┐
         │      │                 │
┌────────▼────┐ │    FastAPI     │
│ Discord     │ │    Backend     │
│ JSON Export │ │                 │
└─────────────┘ └───────┬────────┘
                        │
                        ▼
                ┌───────────────┐
                │ Ollama        │
                │ Gemma 3 4B    │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Project Facts │
                └───────┬───────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Conflict Detector  │
              │ Deterministic      │
              │ Python Rules       │
              └─────────┬──────────┘
                        │
                        ▼
                ┌───────────────┐
                │ React         │
                │ Dashboard     │
                └───────────────┘
~~~

## Project Structure

~~~text
CentralResolve/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── analysis.py
│   │   ├── parsers/
│   │   │   ├── whatsapp.py
│   │   │   └── discord.py
│   │   ├── schemas/
│   │   │   ├── analysis.py
│   │   │   ├── conflict.py
│   │   │   ├── message.py
│   │   │   └── response.py
│   │   └── services/
│   │       ├── analyzer.py
│   │       └── conflict_detector.py
│   ├── main.py
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConflictCard.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   └── StatCard.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   └── package.json
│
└── README.md
~~~

## Running Locally

### Prerequisites

Make sure you have:

- Python
- Node.js
- Ollama

### Backend

Clone the repository and enter the backend:

~~~bash
cd CentralResolve/backend
~~~

Create a virtual environment:

~~~bash
python -m venv .venv
~~~

Activate it on Windows:

~~~cmd
.venv\Scripts\activate
~~~

Install dependencies:

~~~bash
pip install -r requirements.txt
~~~

Make sure Gemma 3 4B is available through Ollama:

~~~bash
ollama pull gemma3:4b
~~~

Start FastAPI:

~~~bash
fastapi dev app/main.py
~~~

The API will be available at:

~~~text
http://127.0.0.1:8000
~~~

### Frontend

Open another terminal:

~~~bash
cd CentralResolve/frontend
~~~

Install dependencies:

~~~bash
npm install
~~~

Start the development server:

~~~bash
npm run dev
~~~

Open the URL shown by Vite, usually:

~~~text
http://localhost:5173
~~~

## Using CentralResolve

1. Open the web application.
2. Click **Analyze Conversations**.
3. Upload a WhatsApp `.txt` export.
4. Upload a Discord `.json` export.
5. Click **Analyze Conversations**.
6. CentralResolve sends the conversations to the FastAPI backend.
7. Gemma 3 4B extracts structured project facts locally through Ollama.
8. Deterministic Python rules identify conflicts.
9. The dashboard displays the conflicts and their supporting evidence.

## Example

Given these conversations:

~~~text
[whatsapp] Rahul: I'll handle deployment.
[whatsapp] Sana: The presentation deadline is Monday.
[discord] Rahul: I can't handle deployment anymore.
[discord] Sana: I thought the presentation was due Friday.
~~~

CentralResolve can identify:

### Ownership Conflict

~~~text
deployment

WhatsApp
"Rahul: I'll handle deployment."

Discord
"Rahul: I can't handle deployment anymore."
~~~

### Deadline Conflict

~~~text
presentation

WhatsApp
"Sana: The presentation deadline is Monday."

Discord
"Sana: I thought the presentation was due Friday."
~~~

## Current Capabilities

- WhatsApp chat parsing
- Discord JSON parsing
- Platform-aware message normalization
- Local Gemma fact extraction
- Deterministic conflict detection
- Cross-platform evidence
- Conflict severity levels
- Analysis dashboard
- Frontend and backend integration

## Future Improvements

- More robust deadline reasoning
- Better handling of indirect ownership changes
- Conversation timeline visualization
- Support for additional communication platforms
- Configurable local models
- More advanced conflict reasoning
- Better handling of larger conversation exports

## Hacktoberfest Weekend Challenge 2026

CentralResolve was built for the DEV Hacktoberfest Weekend Challenge:

**Build for a Friend**

The project was built from scratch during the challenge entry period and uses open-source AI at its core through **Gemma 3 4B running locally through Ollama**.

The project focuses on a real communication problem: keeping team decisions, ownership, deadlines, and project status consistent when conversations are spread across multiple platforms.

Challenge:

https://dev.to/challenges/hacktoberfest-weekend-2026-10-01

## License

MIT