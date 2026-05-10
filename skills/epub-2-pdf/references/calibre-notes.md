# Calibre EPUB to PDF Notes

- `ebook-convert input.epub output.pdf -h` prints output-specific PDF options.
- `--pdf-add-toc` adds a visible TOC page near the end of the PDF.
- PDF outline/bookmarks are separate from visible TOC pages.
- `--use-auto-toc` overrides the source EPUB TOC and uses XPath selectors.
- Namespaced XHTML headings use XPath like `//h:h1`, `//h:h2`, `//h:h3`.
- For Chinese books, `Songti SC` is a practical macOS default if available.
- On macOS app installs, the binary is often `/Applications/calibre.app/Contents/MacOS/ebook-convert`.
