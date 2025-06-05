# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "ebooklib",
#     "beautifulsoup4",
# ]
# ///

import click
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import sys
from pathlib import Path

__version__ = "1.0.0"


def extract_text_from_epub(epub_path, preserve_formatting=False, verbose=False):
    """Extract plain text from an EPUB file."""
    try:
        book = epub.read_epub(epub_path)
    except FileNotFoundError:
        raise click.ClickException(f"EPUB file not found: {epub_path}")
    except ebooklib.epub.EpubException as e:
        raise click.ClickException(f"Invalid EPUB file: {e}")
    except Exception as e:
        raise click.ClickException(f"Error reading EPUB file: {e}")
    
    text_content = []
    items = list(book.get_items())
    
    if verbose:
        click.echo(f"Processing {len(items)} items from EPUB...", err=True)
    
    # Get all items in the book
    for i, item in enumerate(items):
        if verbose and len(items) > 10:
            if i % max(1, len(items) // 10) == 0:
                click.echo(f"Progress: {i}/{len(items)} items processed", err=True)
        
        # Only process HTML/XHTML content
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text and clean up whitespace
            if preserve_formatting:
                # Preserve paragraph breaks
                for p in soup.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                    p.append('\n\n')
                text = soup.get_text()
            else:
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
            
            if text.strip():
                text_content.append(text)
    
    if verbose:
        click.echo(f"Extracted text from {len(text_content)} sections", err=True)
    
    return '\n\n'.join(text_content)


def validate_epub_file(epub_path):
    """Validate that the file is a proper EPUB file."""
    path = Path(epub_path)
    
    # Check if file exists
    if not path.exists():
        raise click.ClickException(f"File does not exist: {epub_path}")
    
    # Check file extension
    if not epub_path.lower().endswith('.epub'):
        raise click.ClickException("Input file must have .epub extension")
    
    # Check if file is readable
    if not os.access(epub_path, os.R_OK):
        raise click.ClickException(f"Cannot read file: {epub_path}")
    
    # Check file size (basic sanity check)
    if path.stat().st_size == 0:
        raise click.ClickException("EPUB file is empty")


@click.command()
@click.argument('epub_file', type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option('-o', '--output', type=click.Path(path_type=str), 
              help='Output file path. If not specified, prints to stdout.')
@click.option('--encoding', default='utf-8', 
              help='Output file encoding (default: utf-8)')
@click.option('-v', '--verbose', is_flag=True, 
              help='Enable verbose output with progress information.')
@click.option('-q', '--quiet', is_flag=True, 
              help='Suppress all non-error output.')
@click.option('--no-formatting', is_flag=True,
              help='Remove paragraph breaks and compress whitespace.')
@click.version_option(version=__version__, prog_name='epub-converter')
def main(epub_file, output, encoding, verbose, quiet, no_formatting):
    """Convert EPUB file to plain text.
    
    EPUB_FILE: Path to the EPUB file to convert.
    
    Examples:
        epub_converter book.epub                    # Print to stdout (with formatting)
        epub_converter book.epub -o book.txt        # Save to file (with formatting)
        epub_converter book.epub -v                 # Verbose mode
        epub_converter book.epub --no-formatting    # Compress whitespace
    """
    # Validate conflicting options
    if verbose and quiet:
        raise click.ClickException("Cannot use both --verbose and --quiet options")
    
    # Validate EPUB file
    validate_epub_file(epub_file)
    
    try:
        # Extract text from EPUB
        if not quiet:
            click.echo(f"Converting {epub_file}...", err=True)
        
        text_content = extract_text_from_epub(
            epub_file, 
            preserve_formatting=not no_formatting,
            verbose=verbose and not quiet
        )
        
        if not text_content.strip():
            if not quiet:
                click.echo("Warning: No text content found in EPUB file", err=True)
        
        # Output the text
        if output:
            try:
                output_path = Path(output)
                # Create parent directories if they don't exist
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output, 'w', encoding=encoding) as f:
                    f.write(text_content)
                
                if not quiet:
                    file_size = output_path.stat().st_size
                    click.echo(f"Text saved to {output} ({file_size:,} bytes)", err=True)
                    
            except PermissionError:
                raise click.ClickException(f"Permission denied writing to: {output}")
            except Exception as e:
                raise click.ClickException(f"Error writing output file: {e}")
        else:
            # Print to stdout
            click.echo(text_content)
            
    except click.ClickException:
        raise
    except KeyboardInterrupt:
        raise click.ClickException("Operation cancelled by user")
    except Exception as e:
        raise click.ClickException(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()