---
title: README rule
description: What a README in a DEEPX product repository contains, with a template to copy.
---

# README rule

Every README in our GitHub organization says what the repository is, how to install it and where the docs are. Nothing else.

No tutorials, no API notes and no change log in a README. Those live in these docs, so there is only one copy to keep up to date.

## Template

```markdown
# dx-compiler

Compiles ONNX models into .dxnn models for DEEPX NPUs.

## Install

pip install dx-com

## Documentation

Everything else is in the DEEPX Tech Docs:
https://developer.deepx.ai/tech-docs/compiler/
```

## Checklist

* [ ] One sentence that says what the repository is
* [ ] The shortest working install command
* [ ] One link to the matching section of the docs
* [ ] No other sections

## Next steps

* [Writing guide](writing-guide.md)
* [Contribute to the docs](index.md)
