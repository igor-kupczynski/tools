# EPUB Converter

A simple command-line tool to convert EPUB files to plain text.

*Vibe coded with AI assistance.*

## Usage

```bash
# Print to stdout (preserves formatting by default)
uv run epub_converter.py book.epub

# Save to file (preserves formatting by default)
uv run epub_converter.py book.epub -o book.txt

# Verbose mode
uv run epub_converter.py book.epub -v -o book.txt

# Compress whitespace and remove formatting
uv run epub_converter.py book.epub --no-formatting -o book.txt

# Quiet mode (no progress messages)
uv run epub_converter.py book.epub -q -o book.txt
```

## Options

- `-o, --output PATH` - Output file path (prints to stdout if not specified)
- `-v, --verbose` - Show progress information
- `-q, --quiet` - Suppress non-error output
- `--no-formatting` - Remove paragraph breaks and compress whitespace
- `--encoding TEXT` - Output file encoding (default: utf-8)
- `--version` - Show version
- `--help` - Show help

## Requirements

- Python 3.12+
- Dependencies managed via inline script metadata (uv handles this automatically)

## License

MIT License - see LICENSE file.
