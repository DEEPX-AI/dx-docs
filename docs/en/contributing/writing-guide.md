---
title: Writing guide
description: The rules every page in these docs follows, with a page template.
---

# Writing guide

This page lists the rules every page follows, so all our docs read the same way.

## Four page types

Each page is one of these types. The navigation inside each tool follows them.

| Type | Purpose | Example |
|---|---|---|
| Tutorial | Learn by doing, from start to a working result | [Quickstart](../get-started/quickstart.md) |
| How to | One task, for someone who knows the basics | Compile a model |
| Reference | Complete and dry: CLI options, APIs, config keys, error codes | [Python API](../runtime/python-api.md) |
| Explanation | Concepts and why things work the way they do | [Overview](../get-started/index.md) |

## Rules for every page

1. The first sentence says what the page lets you do.
2. Prerequisites go in a "Before you start" list: board, OS, Python version, SDK version.
3. Every command can be copied and run as is. Show the expected output in a separate `text` block.
4. Python and C++ examples sit side by side in tabs.
5. Use the current versions from the [Compatibility](../get-started/compatibility.md) page.
6. One topic, one page. Link to it, never copy it. Install steps live only on the [Install](../get-started/install.md) page.
7. Short sentences, active voice, "you", present tense. Write "we" and "our" for DEEPX.
8. No dashes in prose. Use a comma, a colon or a new sentence. Use `*` for bullets.
9. Use admonitions only for things that can break something.
10. Every page ends with "Next steps" links.
11. Use our product names exactly as listed in the [glossary](../reference/glossary.md).

## Page template

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

## LLM friendly by design

Developers often ask a coding assistant before they read our pages, so every page must be easy for an LLM to read.

* Pages make sense on their own. No meaning hides only in an image.
* Commands and code sit in fenced blocks with a language tag.
* Agent files in our repositories point to these pages instead of copying facts from them.

## Next steps

* [Contribute to the docs](index.md)
* [README rule for product repositories](readme-rule.md)
