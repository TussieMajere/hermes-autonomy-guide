# 🧠 Hermes Agent: Autonomi & Selvlæring Guide

> **Live Web-manual:** https://tussiemajere.github.io/hermes-autonomy-guide/  
> **Oppdatert:** 2026-09-01  
> **Arkitektur:** Linux Mint 22.3 MATE/X11, Nvidia RTX 5060 Ti, CUA-Driver v0.23.2, Gemini 3.1 Flash / 2.5 Pro.

Denne guiden dokumenterer hvordan **Hermes Agent** (**MajereAI**) opererer med full skrivebordsautonomi, Set-of-Marks (SoM) resonneringsloop, automatiske BankID/2FA-takeovers, og Gemini-drevne videoopptak som konverterer menneskelige demonstrasjoner til permanente oppskrifter (`recipes`).

---

## ⚡ Hurtigoversikt over Modulene

| Modul / Ferdighet | Filsti | Hovedfunksjon |
|---|---|---|
| **Visuell Computer Use** | `~/.hermes/skills/computer-use-visual/` | 5-stegs fokusprotokoll på X11/MATE mot Z-index panel-konflikter og GPU SIGTRAP-krasj. |
| **X11 Desktop Controller** | `~/hermes-agent/x11_desktop_ctl.py` | Rå deterministisk mus/tastatur/vindu-kontroll med `xdotool`, `wmctrl`, `scrot`. |
| **Set-of-Marks Closed Loop** | `~/hermes-agent/som_closed_loop.py` | Capture → Analyze (SoM noder) → Act (element ID) → Verify. |
| **Sensitiv Deteksjon & Takeover** | `~/hermes-agent/takeover_handler.py` | Sikkerhetsvakt som pauser autonomi ved BankID/2FA/Sudo og starter FFmpeg-skjermopptak. |
| **Recipe Recorder & Avspiller** | `~/hermes-agent/recipe_recorder.py` | Tar opp, lagrer (JSON/SHA-256) og spiller av handlinger i høyt tempo (0ms LLM forsinkelse). |
| **Gemini Videoanalyse** | `~/hermes-agent/learning/analyzer.py` | OpenCV trekker ut nøkkelbilder fra opptak, Gemini syntetiserer til ny oppskrift. |
| **Dual-Track Router** | `~/hermes-agent/dual_track_router.py` | Ruter handlinger intelligent til Track A (DOM/Playwright), Track B (Physical X11) eller Track C (Hybrid). |
| **Bibliotek- og Kartotekmodellen** | `~/hermes-memory/` | Hukommelse med kortkartotek (<10k tegn i `MEMORY.md`), SQLite FTS5 og ChromaDB. |

---

## 🚀 Hurtigstart

### 1. Start interaktiv agent-konsoll (REPL):
```bash
cd ~/hermes-agent
~/pytorch-env/bin/python -m core.agent
```

### 2. Kjør visuell Set-of-Marks test:
```bash
~/pytorch-env/bin/python ~/hermes-agent/test_visual_loop.py
```

### 3. Spill av en ferdig oppskrift:
```bash
~/pytorch-env/bin/python -c "
from recipe_recorder import RecipeRecorder
RecipeRecorder().play_recipe('467ac5307553', speed=1.2)
"
```

### 4. Søk i minnekartoteket:
```bash
hermes-memory kartotek
hermes-memory search "oppskrifter og autonomi"
```

---

## 🔄 Automatisk Selvoppdatering via Bootstrap

Denne nettsiden og guiden synkroniseres automatisk hver gang du starter `agy` og kjører bootstrap. Skriptet [`update_guide.py`](update_guide.py) scanner etter nye skills, recipes og logger, og oppdaterer GitHub-nettsiden i sanntid.
