# DEEPX Tech Docs

Documentation for the DEEPX SDK, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Local development

Serve the docs locally with live reload:

```bash
mkdocs serve
```

Open [http://localhost:8000](http://localhost:8000) in your browser. Changes to any file are reflected immediately.

## Build

Build a static site into the `site/` directory:

```bash
mkdocs build
```

The output in `site/` is a self-contained static site you can host anywhere.

## Versioning

Versioning is handled by [mike](https://github.com/jimporter/mike), which deploys versioned builds to the `gh-pages` branch. Each version is served from its own subdirectory (e.g. `/2.5/`, `/latest/`), and a version picker appears in the top bar.

### Deploy a new version

```bash
mike deploy --push --update-aliases 2.5 latest
```

This builds the site and pushes it to `gh-pages` under `/2.5/`, then points the `latest` alias to it.

### Set the default version

The default version is what users land on when they visit the root URL:

```bash
mike set-default --push latest
```

### List deployed versions

```bash
mike list
```

### Delete a version

```bash
mike delete --push 2.4
```

### Preview all versions locally

```bash
mike serve
```

### Typical release workflow

```bash
# After merging changes for a new release:
mike deploy --push --update-aliases <version> latest
mike set-default --push latest
```

## Project structure

```
dx-docs/
├── docs/               # Markdown source files
│   ├── index.md        # Homepage
│   ├── assets/         # Images and static files
│   ├── get-started/    # Install, quickstart, compatibility, troubleshooting
│   ├── compiler/       # DX-COM compiler docs
│   ├── runtime/        # DX-RT runtime docs
│   ├── app/            # DX-APP docs
│   ├── stream/         # DX-Stream docs
│   ├── model-zoo/      # DX-ModelZoo docs
│   ├── ai-studio/      # DX AI Studio docs
│   ├── tools/          # Benchmark, Kubernetes, DX-Edge, agent dev
│   ├── tutorials/      # Step-by-step tutorials and demos
│   └── reference/      # Glossary and reference pages
├── mkdocs.yml          # MkDocs configuration
└── requirements.txt    # Python dependencies
```
