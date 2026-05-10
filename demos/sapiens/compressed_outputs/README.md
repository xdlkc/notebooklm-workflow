# Compressed NotebookLM artifacts for 《人类简史》

This directory contains compressed, repo-friendly viewing copies derived from the real Drive artifacts. They are meant for quick GitHub browsing/review and should not replace the original full-quality files on Drive.

Compression policy:

- PPTX files are rebuilt as image-only viewing decks from the original NotebookLM slide images.
- PDF files are rasterized/downscaled viewing copies.
- MP4 files are downscaled to 854px width with lower bitrate audio/video.
- Original full-quality PPTX/PDF/MP4 files remain linked from `../drive_outputs/README.md`.

## Included compressed files

| File | Original size | Compressed size | Notes |
|---|---:|---:|---|
| `sapiens_slide_deck_concise_compressed.pptx` | 14.42 MB | 0.90 MB | Image-only PPTX viewing copy; use Drive original for higher quality. |
| `sapiens_slide_deck_concise_compressed.pdf` | 11.60 MB | 0.43 MB | Rasterized/downscaled PDF viewing copy. |
| `sapiens_slide_deck_detailed_compressed.pptx` | 41.13 MB | 2.85 MB | Image-only PPTX viewing copy; use Drive original for higher quality. |
| `sapiens_slide_deck_detailed_compressed.pdf` | 29.57 MB | 1.37 MB | Rasterized/downscaled PDF viewing copy. |
| `sapiens_video_part1_compressed.mp4` | 59.26 MB | 5.60 MB | Downscaled video preview. |
| `sapiens_video_part2_compressed.mp4` | 53.27 MB | 6.20 MB | Downscaled video preview. |
| `sapiens_video_part3_compressed.mp4` | 70.08 MB | 6.62 MB | Downscaled video preview. |

## Verification

The compressed files were checked with:

```bash
unzip -t demos/sapiens/compressed_outputs/*.pptx
python -c "import fitz; ..."  # PDF page-count check
ffprobe ...                  # MP4 duration/size check
```

Expected counts:

- concise deck: 10 slides/pages;
- detailed deck: 19 slides/pages;
- videos: approximately 529s, 609s, and 588s.
