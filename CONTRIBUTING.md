# Contributing

dx-docs only holds copies, so fixes go to the place the original lives.

| You want to | Do this |
| --- | --- |
| Fix a typo or error in `modules/<repo>/` | Open an issue here (or in `DEEPX-AI/<repo>`) describing the page and the fix. The DEEPX team applies it at the source, and it reaches this repository with the next release. |
| Fix a typo or error in `common/<repo>/` | Open a pull request in `DEEPX-AI/<repo>`. It is copied here on the next daily sync. |
| Change the landing README of this repository | Open a pull request here. |
| Add a repository to the collection | Open a pull request that adds it to `sources.yml`. |

Pull requests that change files under `modules/` or `common/` fail the `guard` check by design.
