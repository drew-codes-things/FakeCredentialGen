<div align="center">

# FakeCredentialGenerator

**A Python CLI tool that generates randomised fake user credentials for testing, with configurable fields, locales, and export to CSV or JSON.**

[![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Faker](https://img.shields.io/badge/faker-library-orange?style=flat-square)](https://faker.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

</div>

---

Generates realistic-looking fake user records for testing purposes. Each record is built from a Faker locale so names, addresses, phone numbers, and postcodes are region-appropriate. Output is printed as a formatted table in the terminal and saved to a file. No real personal data is used or stored at any point.

---

## Core Fields (always included)

| Field | Example |
|---|---|
| `first_name` | `Sarah` |
| `last_name` | `Williams` |
| `username` | `sarahwilliams42` |
| `email` | `sarah.williams42@gmail.com` |
| `password` | `Xk9#mP2!qR7$nL0w` |
| `company` | `Smith and Sons Ltd` |
| `ipv4` | `82.45.123.7` |
| `user_agent` | `Mozilla/5.0 (Windows NT 10.0...)` |

---

## Optional Fields

Enable with the flags below. Use `--fields` to pick an exact subset.

| Flag | Fields added |
|---|---|
| `--include-address` | `address`, `city`, `country`, `postcode` |
| `--include-dob` | `birthday` (format: `YYYY-MM-DD`, age 18-80) |
| `--include-phone` | `phone` |
| `--include-job` | `job` |

---

## Usage

```bash
python main.py [options]
```

### Options

| Flag | Default | Description |
|---|---|---|
| `-n`, `--count` | `20` | Number of records to generate |
| `-l`, `--locale` | `en_GB` | Faker locale (e.g. `fr_FR`, `de_DE`, `en_US`) |
| `-f`, `--format` | `csv` | Output format: `csv` or `json` |
| `-o`, `--output` | `users` | Output filename without extension |
| `--fields` | *(all core)* | Comma-separated list of exact fields to include; overrides `--include-*` flags |
| `--no-save` | off | Print to terminal only, no file written |
| `--append` | off | Append to existing file instead of overwriting; skips header row if file exists |
| `--private-ip` | off | Generate private/LAN IPs (`10.x`, `172.16.x`, `192.168.x`) instead of public ones |

### Examples

Generate 50 records with address and date of birth, saved as JSON:

```bash
python main.py -n 50 --include-address --include-dob -f json
```

Generate 10 French-locale records with only username and email, printed to terminal only:

```bash
python main.py -n 10 -l fr_FR --fields username,email --no-save
```

Append 100 records to an existing CSV:

```bash
python main.py -n 100 --append -o users
```

---

## Output

### CSV (default)

Saved to `users.csv` (or `--output` value). Column headers match the field names. Appending skips the header row if the file already exists.

### JSON

Saved to `users.json`. Output is a JSON array of objects, one per record, indented with 2 spaces.

### Terminal table

All records are printed as an aligned plain-text table before the file is saved, regardless of format.

---

## Requirements

```bash
pip install faker
```

- Python 3.8+
- [`faker`](https://faker.readthedocs.io/) - all other dependencies are stdlib

---

---

## Install as a command (pipx)

Install this folder as a CLI so it is available on your PATH:

```bash
pipx install .
fake-credential-generator
```


## License

MIT - made by [Drew](https://github.com/drew-codes-things)
