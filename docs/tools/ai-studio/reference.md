---
title: DX AI Studio reference
description: SDK Library, About DEEPX, environment variables, ports, standalone tool servers and third party licenses for DX AI Studio.
---

# DX AI Studio reference

This page lists the reference views, settings and license notes of DX AI Studio.

## SDK Library

The **SDK Library** opens from the hub and shows DEEPX material inside the studio:

* **Documentation:** the DEEPX SDK Markdown docs, rendered in the browser with images and tables.
* **Brochures & Briefs:** product brochures and chip and module briefs as in app PDFs.
* **Search and deep links:** library wide search, and in document find (`Ctrl+F` with next, previous and a match counter). Switch **List** or **Cabinet** view, or open the architecture diagram. The open document, view and query are kept in the URL.

If an entry is unavailable, check that the suite documentation is present. A library entry does not install the SDK.

## About DEEPX

**About DEEPX** is one scrolling page with a section menu: **Developer** (resource cards and distribution channels), **Company** (vision, milestones, offices), **Technology**, **Products**, **Partners**, **Awards** and **News**, plus a link to the DEEPX store.

## Environment variables

Access and security variables are explained on [Install and launch](install-and-launch.md#access-settings). This is the full list.

| Variable | Effect |
|---|---|
| `DX_BIND_LOCAL=1` | Bind the hub to `127.0.0.1` only (tool servers always are) |
| `DX_BIND_HOST=<host>` | Bind the hub to an explicit host. A single tool server bound beyond loopback refuses to start without `DX_API_TOKEN`. |
| `DX_API_TOKEN=<secret>` | Lets remote API clients in with `Authorization: Bearer <secret>` or `X-DX-Api-Token` |
| `DX_PAIRING=off` | No browser pairing; remote access only with `DX_API_TOKEN` |
| `DX_SESSION_DAYS=<n>` | How long a paired browser stays connected (default 30) |
| `DX_ALLOWED_HOSTS=<a,b>` | Extra host names the servers answer to |
| `DX_COMPILER_ALLOWED_ROOTS=<dir:dir>` | Extra folders DX Compiler may read and write |
| `DX_<MODULE>_PORT` | Port override in the hub's proxy map (see the port table) |
| `DX_APP_ROOT`, `DX_COMPILER_ROOT`, `DX_RUNTIME_ROOT`, `DX_STREAM_ROOT` | SDK folder locations (default: the folders next to `dx-ai-studio` in the suite) |
| `DX_APP_MODELS_DIR` | DX App models folder used by **Save to Studio models** (default `dx-runtime/dx_app/assets/models`) |
| `DX_NO_BROWSER=1` | Do not open a browser (also implied under SSH or VS Code remote) |
| `DX_MONITOR_SKIP_HARDWARE_INIT=1` | Skip DX Monitor hardware setup; NPU telemetry stays unavailable, not synthetic |
| `DX_MONITOR_EXPLICIT_MOCK=1` | Demo telemetry, labelled Mock. Never a hardware test. Do not combine with the previous variable. |
| `DX_AGENT_ADAPTER=mock` | DX Agent Dev test adapter for networks without internet |
| `DX_HARNESS_ROOT=<path>` | Path to the `dx-all-suite` checkout, for the agent knowledge that DX Agent Dev needs |
| `DX_CHAT_KNOWLEDGE_SYNC=1` | Regenerate the chat assistant's SDK knowledge from the suite docs |

## Ports and paths

The hub starts every tool on a free port chosen by the OS and proxies it under one address. The fixed numbers below are defaults for standalone runs and the `DX_*_PORT` overrides.

| Tool | Folder | Default port | Path under the hub | Override |
|---|---|---|---|---|
| Hub | `launcher/` | 8890 | (root) | `DX_LAUNCHER_PORT` |
| DX App | `dx_app/` | 8080 | `/app/` | `DX_APP_PORT` |
| DX Stream | `dx_stream/` | 8093 | `/stream/` | `DX_STREAM_PORT` |
| DX Model Zoo | `dx_modelzoo/` | 8094 | `/zoo/` | `DX_ZOO_PORT` |
| DX Compiler | `dx_compiler/` | 8095 | `/compiler/` | `DX_COMPILER_PORT` |
| DX EdgeGuide | `dx_planner/` | 8096 | `/planner/` | `DX_PLANNER_PORT` |
| DX Benchmark | `dx_benchmark/` | 8097 | `/benchmark/` | `DX_BENCHMARK_PORT` |
| DX Monitor | `dx_monitor/` | 8098 | `/dx_monitor/` | `DX_MONITOR_PORT` |
| DX Agent Dev | `dx_agent_dev/` | 8099 | `/agent/` | `DX_AGENT_PORT` |
| DX Cloud | `dx_edge/` | 8100 | `/cloud/` | `DX_EDGE_PORT` |

### Run one tool on its own

Each tool is its own server. For focused work you can run one directly; it then takes its port from `--port` (`--port 0` picks a free one) and ignores the `DX_*_PORT` variables.

```bash
./.venv/bin/python dx_monitor/server.py --port 8098 --no-browser
```

Every tool server accepts `--port`/`-p` and `--no-browser`.

### Files the studio writes

| Path | Content |
|---|---|
| `.launcher-port` | Last hub port used |
| `var/log/studio-debug.log` | User action log with `--debug` |
| `var/runtime/artifacts/` | Checked runtime packages |
| `outputs/dx_app/graph/projects/` | Graph Composer projects (latest 50 versions each) |
| `outputs/dx_app/graph/exports/` | Graph Composer C++ exports (newest five) |
| `~/.dx-ai-studio/agent.json` | The Studio agent and model choice |
| `~/.local/state/dx-ai-studio/logs/` | Tool server error logs |

## Third party licenses

DX AI Studio is a GUI over the DEEPX SDK. The models and sample data it lets you browse, download, compile and run come from third parties and keep **their own licenses**. The studio grants you no rights to them.

* **Sample models:** models in DX Model Zoo and used by DX App and DX Compiler are evaluation and development examples. They come from projects with different terms, including copyleft and non commercial licenses. Check the license fields in the Model Zoo detail view before any commercial use, and get a proper license from the model's authors or use your own model for production.
* **Sample data:** sample images and videos come from public academic or open source datasets (for example ImageNet, non commercial research only) or are AI generated. Use them for evaluation and demos only, and do not redistribute them or use them commercially without the copyright holder's permission.

### Bundled fonts

Paths are relative to `shared/static/fonts/`. These fonts come with SIL Open Font License 1.1 notices:

| Font | Notice file | Copyright named in the notice |
|---|---|---|
| Inter | `LICENSE-Inter.txt` | The Inter Project Authors |
| Noto Sans SC / TC | `LICENSE-NotoSansSC.txt`, `LICENSE-NotoSansTC.txt` | Adobe; reserved font name "Source" |
| Pretendard / Pretendard JP | `LICENSE-Pretendard.txt`, `LICENSE-PretendardJP.txt` | Kil Hyung-jin |

CJK fonts ship as subsets. Other bundled families are JetBrains Mono, Noto Sans and Noto Sans Mono. Keep the notices when you redistribute.

### Bundled JavaScript

| Asset | License information |
|---|---|
| `shared/static/vendor/chart.umd.min.js` | Its header names **MiniChart**, a small Chart.js compatible canvas engine, not an upstream Chart.js bundle |
| `shared/static/vendor/mermaid.min.js` | Mermaid declares MIT; the bundle also holds dependency notices, including DOMPurify's Apache-2.0 / MPL-2.0 notice |
| `dx_compiler/static/js/dagre.min.js` | Contains Chris Pettitt's copyright and MIT text, plus bundled graphlib and lodash code |

We provide these third party models and datasets as is, for convenience, and are not responsible for unauthorized or commercial use. By using the samples you accept responsibility for license compliance.

## Next steps

* [Glossary](../../reference/glossary.md)
