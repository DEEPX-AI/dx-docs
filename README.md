# dx-docs

All DEEPX developer documentation, collected in one place.

This repository **collects copies**. The original of every document lives in its own repository, and the DEEPX team copies the latest version here. To read the docs as a website, visit **[developer.deepx.ai/tech-docs](https://developer.deepx.ai/tech-docs/)**.

## Layout

| Folder | What it contains | Original lives in |
| --- | --- | --- |
| `modules/<repo>/` | README, release notes and `docs/` of each SDK module | the module repository (mirrored from DEEPX internal development) |
| `common/<repo>/` | Guides and tutorials that exist only on GitHub | the repository of the same name |

Each folder has a `.source.json` that records the source repository, the commit it was copied from and when it was copied. The list of collected repositories is in [`sources.yml`](sources.yml).

## Found a problem in a document?

Please **do not edit files in `modules/` or `common/`**. They are overwritten on the next sync, so pull requests that change them are not merged.

- For `modules/`: open an issue in this repository or in the module repository. The DEEPX team fixes it at the source.
- For `common/`: open a pull request in the source repository named in `.source.json`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## How syncing works

Copies are made by [`scripts/sync.py`](scripts/sync.py). For every repository enabled in `sources.yml`, it copies `README*.md`, `RELEASE_NOTES*.md` and the `docs/` folder from the default branch, skipping tool folders such as `.github/` and `.claude/`. Only public repositories are copied; if a source repository is private, it is skipped and any existing copy is removed.

The [`sync`](.github/workflows/sync.yml) workflow is set up to run the script every day at 01:00 KST. Until it is enabled, the DEEPX team runs the script by hand.

To run it locally (requires Git and Python 3):

```bash
pip install pyyaml
python scripts/sync.py            # sync all enabled repositories
python scripts/sync.py dx_rt      # sync one repository
python scripts/sync.py --check    # report copies that are behind their source
```
