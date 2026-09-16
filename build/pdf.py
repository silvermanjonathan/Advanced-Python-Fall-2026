"""Render the printable pages to PDF. Run after make.py when a worksheet changes.

Needs WeasyPrint (pip install weasyprint). The web fonts load from Google Fonts,
so a machine without network access falls back to its own sans and mono fonts;
the layout is the same either way.
"""

import os

from weasyprint import HTML

from build import OUT

PAGES = ["wed01_worksheet.html"]

for name in PAGES:
    src = os.path.join(OUT, name)
    dst = src[:-5] + ".pdf"
    HTML(src).write_pdf(dst)
    print(f"wrote {os.path.basename(dst)}")
