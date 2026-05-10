#!/usr/bin/env python3
"""Build a quoted Calibre ebook-convert command for EPUB-to-PDF conversion."""

from __future__ import annotations

import argparse
import shlex
from pathlib import Path


TOC_ARGS = {
    "source": [],
    "visible": ["--pdf-add-toc", "--toc-title", "目录"],
    "detailed": [
        "--use-auto-toc",
        "--level1-toc",
        "//h:h1",
        "--level2-toc",
        "//h:h2",
        "--level3-toc",
        "//h:h3",
        "--pdf-add-toc",
        "--toc-title",
        "目录",
    ],
    "medium": [
        "--use-auto-toc",
        "--level1-toc",
        "//h:h1",
        "--level2-toc",
        "//h:h2",
        "--level3-toc",
        "/",
        "--pdf-add-toc",
        "--toc-title",
        "目录",
    ],
    "concise": [
        "--use-auto-toc",
        "--level1-toc",
        "//h:h1",
        "--level2-toc",
        "//h:h2[not(contains('0123456789', substring(normalize-space(.), 1, 1)))]",
        "--level3-toc",
        "/",
        "--pdf-add-toc",
        "--toc-title",
        "目录",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_epub", help="Input .epub file")
    parser.add_argument("output_pdf", help="Output .pdf file")
    parser.add_argument("--ebook-convert", default="ebook-convert")
    parser.add_argument("--paper-size", default="a4")
    parser.add_argument("--font", default="Songti SC")
    parser.add_argument("--toc", choices=sorted(TOC_ARGS), default="concise")
    parser.add_argument("--no-page-numbers", action="store_true")
    args = parser.parse_args()

    input_epub = Path(args.input_epub)
    output_pdf = Path(args.output_pdf)
    command = [
        args.ebook_convert,
        str(input_epub),
        str(output_pdf),
        "--paper-size",
        args.paper_size,
        "--pdf-page-margin-left",
        "36",
        "--pdf-page-margin-right",
        "36",
        "--pdf-page-margin-top",
        "48",
        "--pdf-page-margin-bottom",
        "48",
        "--pdf-serif-family",
        args.font,
    ]
    if not args.no_page_numbers:
        command.append("--pdf-page-numbers")
    command.extend(TOC_ARGS[args.toc])

    print(" ".join(shlex.quote(part) for part in command))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
