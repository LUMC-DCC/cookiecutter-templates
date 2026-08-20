# Metadata

Generated projects expose the same public facts in the formats used by package
managers, citation tools, registries, archives, and container tooling.

## Metadata model

`codemeta.json` is the canonical cross-language metadata record. Ecosystem
files such as Python's `pyproject.toml`, optional `CITATION.cff`, and OCI image
labels repeat only the fields their consumers understand. README and project
documentation remain concise human-facing entry points.

The generated files follow the
[LUMC CodeMeta profile](https://lumc-dcc.github.io/rs-metadata/schema/1.0.0/codemeta-lumc.schema.json).
The [rs-metadata crosswalk](https://lumc-dcc.github.io/rs-metadata/developing/crosswalk.html)
defines which overlapping values must agree and which differences are merely
reported.

## After generation

Cookiecutter creates the initial metadata from one validated context. After
generation, maintain `codemeta.json` as the metadata anchor and update the
relevant ecosystem files when shared facts change.

The LUMC profile requires a release identifier and a license. Supply these
values before expecting the metadata workflow to pass.

Run the same validation used by CI locally:

```console
uvx --python 3.11 \
  --from git+https://github.com/LUMC-DCC/rs-metadata.git@v1 \
  rs-metadata validate .
```

The generated `metadata.yml` workflow uses the official `LUMC-DCC/rs-metadata`
action. It validates the LUMC profile, discovers supported ecosystem files,
and checks their semantic overlap with CodeMeta. Projects that intentionally
omit `CITATION.cff` do not receive this profile workflow because the profile
requires a citation file.
