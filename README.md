# DEEPX SDK Docs

Documentation for the DEEPX SDK, built with [Zensical](https://zensical.org/) from `mkdocs.yml` (Material for MkDocs theme).

## Setup

Python 3.10 or newer:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install zensical==0.1.1 -r requirements.txt
```

## Local development

Serve the docs locally with live reload:

```bash
zensical serve
```

Open [http://localhost:8000](http://localhost:8000). Changes under `docs/` and `snippets/` are reflected immediately.

## Build

```bash
zensical build --strict
```

The build must finish with no warnings. The CI workflow that runs this command on `main` is on the `build-check-action` branch until it is merged. The output in `site/` is a self-contained static site you can host anywhere.

## Add or change a page

1. Edit or add Markdown under `docs/`, in the folder of the top tab it belongs to.
2. Add new pages to `nav` in `mkdocs.yml`.
3. Put content shared by several pages in `snippets/` and include it with `--8<-- "snippets/<file>.md"`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute and the writing guide.

## Versioning

Not configured yet. Versioned docs are planned for adding the docs of earlier SDK releases. `mike` is listed in `requirements.txt`, but `mkdocs.yml` has no version provider yet, and it still needs to be checked whether `mike` works with Zensical.

## Project structure

```
dx-docs/
├── docs/               # Markdown source files (one folder per top tab)
│   ├── index.md        # Homepage
│   ├── assets/         # Images and static files
│   ├── get-started/    # Overview, install, quickstart, compatibility, troubleshooting
│   ├── compiler/       # DX-COM compiler docs
│   ├── runtime/        # DX-RT runtime docs
│   ├── tools/          # Benchmark, Kubernetes, DX-Edge, agent dev
│   │   ├── app/        # DX-APP docs
│   │   ├── stream/     # DX-Stream docs
│   │   ├── model-zoo/  # DX-ModelZoo docs
│   │   └── ai-studio/  # DX AI Studio docs
│   ├── tutorials/      # Step-by-step tutorials and demos
│   └── reference/      # Release notes and glossary
├── snippets/           # Shared Markdown included with --8<-- (not built as pages)
├── mkdocs.yml          # Site configuration and nav
├── CONTRIBUTING.md     # How to contribute, writing guide and README rule (not published)
└── requirements.txt    # Python dependencies
```
