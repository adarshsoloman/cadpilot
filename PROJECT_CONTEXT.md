# Project Context — VYASN × FreeCAD MCP × Gemini Desktop
**Author:** Adarsh Soloman Banjare, CTO — VYASN  
**Date:** May 2026  
**Purpose:** Full context document to share with any AI assistant to get them up to speed instantly.

---

## Who Is Adarsh?

Solo developer and CTO of **VYASN** — a marine intelligence startup building smart ocean monitoring buoys. The VYASN Mark 1 buoy is a physical hardware product that collects oceanic data (temperature, salinity, fish disease indicators, etc.) and transmits it to a cloud dashboard in real time.

He has already:
- Built a working **prototype backend** (Python, InfluxDB, Grafana, Telegram alerts)
- Conducted a **live stakeholder demo** with choreographed sensor data and alert sequences
- Started planning **Phase 1** — the real product, called **Isomorph**

---

## How We Got Here — The Journey

### Step 1: The Hardware Design Problem
To move from prototype to real product, Adarsh needs to design the **physical enclosure** of the VYASN Mark 1 buoy — a marine-grade housing with:
- Hexagonal body
- Solar panel array on top
- Single antenna on top center
- Three sensor probes hanging from the bottom

He uses **FreeCAD** (free, open-source CAD software) for 3D modeling. But FreeCAD is slow and manual — you click through menus, write Python scripts by hand, iterate slowly.

### Step 2: The FreeCAD MCP Server Idea
Adarsh decided to build a **Model Context Protocol (MCP) server** that bridges an AI assistant to FreeCAD. The idea:

```
You describe the buoy in natural language
        ↓
AI (Gemini / Claude) understands it
        ↓
MCP Server translates to FreeCAD Python API commands
        ↓
FreeCAD builds the 3D model automatically
        ↓
Exports .STL / .STEP / .FCStd file
```

No manual clicking. No writing Python by hand. Just describe → it gets built.

### Step 3: The PRD Was Written
A full **Product Requirements Document** was written for the FreeCAD MCP Server, covering:
- 8 MCP tools: `create_primitive`, `boolean_operation`, `transform_object`, `export_model`, `execute_raw`, `list_objects`, `new_document`, `reset_session`
- Windows-specific FreeCAD path resolution
- **File-based session state** — the key architectural decision (see below)
- `uv` for Python environment management
- Gemini CLI as the AI client
- Full implementation code for `session_manager.py`, `script_runner.py`, `freecad_mcp_server.py`

### Step 4: The Key Architectural Problem — State Persistence
The critical challenge: FreeCAD MCP runs each tool call as a **separate subprocess**. This means:

```
Tool Call 1: new_document → creates doc in memory → subprocess exits → DOC IS GONE
Tool Call 2: create_primitive → new subprocess → no document exists → FAILS
```

The solution chosen: **File-based session state**

Every tool call:
1. Loads `session.FCStd` from disk at the start
2. Runs the user's code
3. Saves `session.FCStd` back to disk at the end

This means sequential tool calls share the same persistent document across subprocess boundaries. A `reset_session` tool clears the file to start fresh.

### Step 5: The Client Question
Adarsh asked: *"Can I connect the MCP server to you (the AI in my IDE) instead of Gemini CLI, so I just type to you and FreeCAD builds it?"*

Answer:
- **This IDE environment (Antigravity)** — Not currently capable of acting as an MCP client
- **Claude Desktop** — Yes, fully supports MCP. But Adarsh doesn't have a Claude subscription.
- **Gemini CLI** — Free, already in the PRD, works perfectly. ✅
- **Cursor, Windsurf** — Also support MCP, free tiers available

### Step 6: The Gemini Desktop Idea
Adarsh asked: *"Since there's no Gemini Desktop app like Claude Desktop, can I build one myself as a solo developer and package it as a .exe?"*

Answer: **Yes, absolutely.**

Claude Desktop is just an **Electron app** — a browser shell around a chat UI, connected to the Claude API, with MCP client support built in. Anthropic didn't build anything a solo developer can't replicate.

**The proposed Gemini Desktop app:**

```
Electron shell (desktop app)
    +
React / HTML chat UI
    +
Gemini API (free key from Google AI Studio)
    +
MCP Client (Node.js, ~100 lines)
    +
electron-builder → packages as .exe
```

Effort: ~1 week for a personal-use version.

Significance: **There is no official Gemini Desktop app.** Nobody has built this properly as an open-source project. Adarsh would be the first.

---

## The Two Projects On The Table

### Project A — FreeCAD MCP Server (In Progress)
**Status:** PRD complete, ready to code  
**Goal:** Connect Gemini CLI to FreeCAD so the VYASN buoy can be built from natural language  
**Stack:** Python, uv, FreeCAD Python API, MCP stdio protocol  
**Repo:** `d:\ADARSH\15_Freelance\VYASAN\Phase_0\freecad_mcp\`

### Project B — Gemini Desktop App (Idea Stage)
**Status:** Concept only, not started  
**Goal:** A Claude Desktop-style app powered by Gemini API, with MCP client support, packaged as .exe  
**Stack:** Electron, React, Gemini API (free), Node.js MCP client, electron-builder  
**Significance:** First open-source Gemini Desktop equivalent

---

## Current Decision Point
Adarsh is deciding whether to:
1. Finish the FreeCAD MCP Server first, then build Gemini Desktop around it
2. Build Gemini Desktop first, then use it with the FreeCAD MCP server

Both projects are independent but deeply complementary — the end vision is:

```
Gemini Desktop (built by Adarsh)
        ↓
FreeCAD MCP Server (built by Adarsh)
        ↓
FreeCAD builds VYASN buoy automatically
```

A fully custom AI-to-CAD pipeline, built solo, for free.

---

## Key Files
- `PRD.md` — Full FreeCAD MCP Server PRD (668 lines, complete)
- `PROJECT_CONTEXT.md` — This file

---

*If you're an AI reading this: Adarsh is a sharp solo builder working fast.  
Keep responses concise, technical, and don't over-explain basics.*
