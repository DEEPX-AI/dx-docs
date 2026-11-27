# Contributing to dx-docs

This guide is for DEEPX authors. It shows you how to change a page, check it locally and send it for review. Users who find a problem can ask in the [DEEPX Developer Community](https://community.deepx.ai/) or [open an issue](#report-a-problem).

All our public docs live in one repository, [DEEPX-AI/dx-docs](https://github.com/DEEPX-AI/dx-docs). There are no other copies: product repositories keep only a short README that links here.

## Before you start

* Git and a GitHub account with write access to `DEEPX-AI/dx-docs`
* Python 3.10 or newer

## Change a page

Pick the way that fits your change.

### Small fix in the browser

For a typo, a wrong value or a broken link on one page:

1. Click the edit icon at the top of the page. GitHub opens the file in its editor.
2. Make the change and choose **Create a new branch for this commit and start a pull request**.
3. Open the pull request to `main`.

### Larger change on your machine

For new pages, several files, images or nav changes:

1. Clone the repository and create a branch from `main`:

    ```bash
    git clone https://github.com/DEEPX-AI/dx-docs.git
    cd dx-docs
    git switch -c docs/<short-topic>
    ```

2. Install the site builder.

    Linux and macOS:

    ```bash
    python3 -m venv .venv
    . .venv/bin/activate
    pip install zensical==0.1.1 -r requirements.txt
    ```

    Windows (PowerShell):

    ```powershell
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install zensical==0.1.1 -r requirements.txt
    ```

3. Start a local preview and open `http://localhost:8000`:

    ```bash
    zensical serve
    ```

4. Edit the Markdown files under `docs/`. Follow the [writing guide](#writing-guide) below.
    * A new page also needs a line in the `nav` of `mkdocs.yml`.
    * A new top tab or folder also needs an entry under `llmstxt` > `sections` in `mkdocs.yml`, or its pages are missing from `llms.txt`. New pages in an existing folder are picked up automatically.

5. Build in strict mode. The build must finish with no warnings:

    ```bash
    zensical build --strict
    ```

6. Push the branch and open a pull request to `main`.

## What CI checks on every pull request

| Check | Fails when |
|---|---|
| `zensical build --strict` | A link, anchor or snippet is broken |

The workflow (`.github/workflows/build-check.yml`) is on the `build-check-action` branch and runs on `main` once that branch is merged. Until then, run step 5 yourself before you open a pull request.

## Release checklist

When a new DEEPX SDK version ships:

1. Update the version matrix in [Compatibility](docs/get-started/compatibility.md).
2. Rewrite **What's new** on the [home page](docs/index.md) for the new release.
3. Check the version notes in the [glossary](docs/reference/glossary.md), for example removed tools and the `.dxnn` format version.
4. Find every other place that names the old version and update it. Search for both spellings, because download URLs write the version with underscores (for example `2_5_0`):

    ```bash
    git grep -nE "<old-version>|<old_version>" -- docs snippets
    ```

5. Build in strict mode and open one pull request for the release.

## Report a problem

If you find a mistake but do not want to fix it yourself, open an issue in [DEEPX-AI/dx-docs](https://github.com/DEEPX-AI/dx-docs/issues) with the page link and what is wrong.

## Writing guide

These are the rules every page in `docs/` follows, so all our docs read the same way.

### Four page types

Each page is one of these types. The navigation inside each tool follows them.

| Type | Purpose | Example |
|---|---|---|
| Tutorial | Learn by doing, from start to a working result | [Quickstart](docs/get-started/quickstart.md) |
| How to | One task, for someone who knows the basics | [Compile a model](docs/compiler/compile-a-model.md) |
| Reference | Complete and dry: CLI options, APIs, config keys, error codes | [Python API](docs/runtime/python-api.md) |
| Explanation | Concepts and why things work the way they do | [Overview](docs/get-started/index.md) |

### Rules for every page

1. The first sentence says what the page lets you do.
2. Prerequisites go in a "Before you start" list: board, OS, Python version, SDK version.
3. Every command can be copied and run as is. Show the expected output in a separate `text` block.
4. Python and C++ examples sit side by side in tabs when both exist.
5. Use the current versions from the [Compatibility](docs/get-started/compatibility.md) page.
6. One topic, one page. Link to it, never copy it. Text that several pages must show, such as the install steps, lives once in `snippets/` and is included with `--8<--`.
7. Put a new page in the folder of the top tab it belongs to, for example `docs/runtime/` for the Runtime tab.
8. Short sentences, active voice, "you", present tense. Write "we" and "our" for DEEPX.
9. No dashes in prose. Use a comma, a colon or a new sentence. Use `*` for bullets.
10. Use admonitions only for things that can break something.
11. Tutorial and how-to pages end with "Next steps" links. Reference pages such as the glossary do not.
12. Use our product names exactly as listed in the [glossary](docs/reference/glossary.md).
13. Write numbered step headings as `Step 1. Do something`, not `1. Do something`, so readers can tell a procedure from an ordinary numbered list. When you add or reorder steps, also update links to them and text such as "see step 3".

### Page template

````markdown
---
title: Run a compiled model in Python
description: Run a .dxnn model on the NPU and read the output.
---

# Run a compiled model in Python

Run a `.dxnn` model on the NPU and read the output.

## Before you start

* DX-RT installed ([Install](../get-started/install.md))
* A compiled model

## Steps

=== "Python"

    ```python
    # code here
    ```

=== "C++"

    ```cpp
    // code here
    ```

## Next steps

* [Python API](python-api.md)
````

### LLM friendly by design

Developers often ask a coding assistant before they read our pages, so every page must be easy for an LLM to read.

* Pages make sense on their own. No meaning hides only in an image.
* Commands and code sit in fenced blocks with a language tag.
* Agent files in our repositories point to these pages instead of copying facts from them.

## README rule for product repositories

Every README in our public product repositories says what the repository is, how to install it and where the docs are. Nothing else.

No tutorials, no API notes and no change log in a README. Those live in the SDK Docs, so there is only one copy to keep up to date.

Link to the SDK Docs home page, not to a deeper page. Page addresses change when the site moves from the current tech-docs site to this repository.

### Template

```markdown
# dx-compiler

Compiles ONNX models into .dxnn models for DEEPX NPUs.

## Install

pip install dx-com

## Documentation

Everything else is in the SDK Docs:
https://developer.deepx.ai/tech-docs/
```

### Checklist

* [ ] One sentence that says what the repository is
* [ ] The shortest working install command
* [ ] One link to the SDK Docs home page
* [ ] No other sections
