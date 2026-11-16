---
title: Contribute to the docs
description: How to propose a change to these docs, build them locally and get it reviewed.
---

# Contribute to the docs

This page shows you how to change a page, check it locally and send it for review.

All our public docs live in one repository, [DEEPX-AI/docs](https://github.com/DEEPX-AI/docs). There are no other copies: product repositories keep only a short README that links here.

## Before you start

* Git and a GitHub account
* Python 3.10 or newer

## Change a page

1. Click the edit icon at the top of any page, or clone the repository:

    ```bash
    git clone https://github.com/DEEPX-AI/docs.git
    cd docs
    ```

2. Install the site builder:

    ```bash
    python3 -m venv .venv
    . .venv/bin/activate
    pip install zensical
    ```

3. Start a local preview and open `http://localhost:8000`:

    ```bash
    zensical serve
    ```

4. Edit the Markdown files under `docs/`. A new page also needs a line in the `nav` of `mkdocs.yml`. Follow the [writing guide](writing-guide.md).

5. Build in strict mode. The build must finish with no warnings:

    ```bash
    zensical build --strict
    ```

6. Open a pull request. The team that owns the folder reviews it.

## Who reviews what

| Folder | Owner |
|---|---|
| `docs/get-started/`, `docs/reference/`, `docs/release-notes/index.md`, `docs/contributing/` | Technical writer |
| `docs/compiler/`, `docs/model-zoo/` | Compiler and Deep Learning team |
| `docs/runtime/`, `docs/app/`, `docs/stream/` | Runtime team |
| `docs/ai-studio/`, `docs/tools/`, `docs/tutorials/` | ATD team |

## What CI checks on every pull request

| Check | Fails when |
|---|---|
| `zensical build --strict` | A link, anchor or snippet is broken |

## Report a problem

If you find a mistake but do not want to fix it yourself, open an issue in [DEEPX-AI/docs](https://github.com/DEEPX-AI/docs/issues) with the page link and what is wrong.

## Next steps

* [Writing guide](writing-guide.md)
* [README rule for product repositories](readme-rule.md)
