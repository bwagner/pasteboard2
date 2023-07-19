# Pasteboard2
Pasteboard2 is a simple Python module and command line tool to get content and
its types from the macOS pasteboard (clipboard). The implementation relies on
[PyObjC](https://pypi.org/project/pyobjc/) and is modeled after the
[Swift](https://en.wikipedia.org/wiki/Swift_(programming_language)) program
[pbv](https://github.com/chee/pbv).

## Command Line Usage
### Top Level
```
 Usage: pb2 [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                        │
╰────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────╮
│ clear            Empties the pasteboard.                                           │
│ clip             Print the content of the pasteboard if it's a string.             │
│ types            List the content types of the current pasteboard.                 │
╰────────────────────────────────────────────────────────────────────────────────────╯
```
### Clip Subcommand
```
 Usage: pb2 clip [OPTIONS]

 Print the content of the pasteboard if it's a string.

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ --type  -t      TEXT  The type of content to get [default: public.utf8-plain-text] │
│ --help                Show this message and exit.                                  │
╰────────────────────────────────────────────────────────────────────────────────────╯
```
## Test
```
git clone https://github.com/bwagner/pasteboard2.git
cd pasteboard2
python -m venv ~/venv/pb2
source ~/venv/pb2/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pytest
deactivate
rm -rf ~/venv/pb2
```
## TODO
[pbv](https://github.com/chee/pbv) offers reading from
several pasteboards. We should, too.

## Requirements
- pyobjc
- typer
- pytest (for development)

## Contribute
```
git clone https://github.com/bwagner/pasteboard2.git
cd pasteboard2
source ~/venv/pb2/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pre-commit install

```

## Alternatives
- https://pypi.org/project/pasteboard/ \
  https://github.com/tobywf/pasteboard \
  but it's no longer maintained (checked 20230710)

- https://pypi.org/project/tacky/ \
  https://github.com/friedenberg/tacky
