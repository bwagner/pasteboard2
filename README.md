# Pasteboard2
Pasteboard2 is a simple Python module and command line tool to get content and
its types from the macOS pasteboard (clipboard). The implementation relies on
[PyObjC](https://pypi.org/project/pyobjc/) and is modeled after the
[Swift](https://en.wikipedia.org/wiki/Swift_(programming_language)) program
[pbv](https://github.com/chee/pbv).

## Command Line Usage
### Top Level
```
 Usage: pasteboard2.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                        │
╰────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────╮
│ clear            Empties the pasteboard.                                           │
│ clip             Print the content of the pasteboard if it's a string.             │
│ test             Run tests with pytest and doctest.                                │
│ types            List the content types of the current pasteboard.                 │
╰────────────────────────────────────────────────────────────────────────────────────╯
```
### Clip Subcommand
```
 Usage: pasteboard2.py clip [OPTIONS]

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
pip install -r requirements.txt
./src/pasteboard2/pasteboard2.py test
deactivate
rm -rf ~/venv/pb2
```
## Requirements
- pyobjc
- typer
- pytest (for development)
## Alternatives
- https://pypi.org/project/pasteboard/ \
  https://github.com/tobywf/pasteboard \
  but it's no longer maintained (checked 20230710)

- https://pypi.org/project/tacky/ \
  https://github.com/friedenberg/tacky

