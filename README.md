<div align="center">
  <img src="./banner.svg" alt="entropy-check" width="800">
</div>

# entropy-check

> Measure file entropy to flag packed or encrypted artefacts

Part of a red-team tooling collection for **authorised** security testing.

## Install

```bash
git clone https://github.com/amooryx/entropy-check.git
cd entropy-check
```

## Usage

```bash
python entropy_check.py <file>
python entropy_check.py <file> --yes --output results.json
```

| Flag | Description |
|---|---|
| `-o, --output` | Write results as JSON to a file |
| `-q, --quiet` | Omit the banner and summary |
| `-y, --yes` | Skip the authorisation prompt |

The tool reads the file locally in chunks, so its memory use does not grow with
the file size. Paths are passed to Python's filesystem APIs without decoding or
rewriting them, including paths containing Unicode characters. An empty file
reports a size of zero and an entropy value of zero.

## Interpreting results

The reported value is the Shannon entropy of the observed **byte distribution**
in the file, measured in bits per byte (from 0 to 8). Elevated values are a
heuristic that can be consistent with compression, encryption, or obfuscation;
they do not identify the cause, and low values do not prove that a file is
benign or uncompressed. File size, format, and the region analyzed also affect
the result.

This is not a password-strength estimator. Shannon entropy of observed file
bytes is not a reliable guarantee of password unpredictability or resistance
to guessing.

## Disclaimer

> **Authorised security testing only.** Use this against systems you own or have
> explicit written permission to test. The tool prompts for authorisation before
> acting and is provided for professional engagements, labs, and research.

## Author

**Omar Khalid** — [omareldemery.com](https://omareldemery.com) | [@amooryx](https://github.com/amooryx)

Certifications: OSCP+ · OSCP · CRTP · eWPTX · eCPPT · eCDFP · eCIR · eJPT
