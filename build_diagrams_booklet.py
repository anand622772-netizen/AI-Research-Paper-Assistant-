import os
from pathlib import Path
import shutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image

ASSETS_DIR = Path("C:/Users/anand/.gemini/antigravity/scratch/ai_research_paper_assistant/outputs/report_assets")
DESKTOP_DIR = Path("C:/Users/anand/Desktop")
DOWNLOADS_DIR = Path("C:/Users/anand/Downloads")
BRAIN_DIR = Path("C:/Users/anand/.gemini/antigravity/brain/73d17954-adc4-4c76-9ba7-fdbec9180065")

# 1. Ensure standalone ER Diagram PDF exists
erd_png = ASSETS_DIR / "er_diagram_ares.png"
erd_pdf = ASSETS_DIR / "er_diagram_ares.pdf"

print(f"Checking ER diagram PNG: {erd_png.exists()} ({erd_png.stat().st_size} bytes)")
print(f"Checking ER diagram PDF: {erd_pdf.exists()} ({erd_pdf.stat().st_size} bytes)")

# 2. Build Updated SmartDoc_AI_Design_and_UML_Diagrams.pdf
diagrams = [
    {
        "title": "Use Case Diagram (Administrator & Fraud Analyst)",
        "file": ASSETS_DIR / "use_case_diagram_smartdoc.png",
        "orientation": "portrait",
    },
    {
        "title": "Context Level DFD: 0 Level",
        "file": ASSETS_DIR / "dfd_level_0_smartdoc.png",
        "orientation": "landscape",
    },
    {
        "title": "DFD Level 1 (Admin side & User side)",
        "file": ASSETS_DIR / "dfd_level_1_smartdoc.png",
        "orientation": "portrait",
    },
    {
        "title": "Activity Diagram (Document Processing to Answer Generation)",
        "file": ASSETS_DIR / "activity_diagram_smartdoc.png",
        "orientation": "portrait",
    },
    {
        "title": "Sequence Diagram (Ask Question & Get Answer)",
        "file": ASSETS_DIR / "sequence_diagram_smartdoc.png",
        "orientation": "landscape",
    },
    {
        "title": "Class Diagram (Domain-Specific RAG Architecture)",
        "file": ASSETS_DIR / "class_diagram_smartdoc.png",
        "orientation": "landscape",
    },
    {
        "title": "Entity Relationship Diagram (ERD - ARES Database Schema)",
        "file": ASSETS_DIR / "er_diagram_ares.png",
        "orientation": "landscape",
    },
]

booklet_pdf = ASSETS_DIR / "SmartDoc_AI_Design_and_UML_Diagrams.pdf"

with PdfPages(booklet_pdf) as pdf:
    for d in diagrams:
        if not d["file"].exists():
            print(f"Warning: File not found {d['file']}")
            continue
        img = Image.open(d["file"])
        is_portrait = d["orientation"] == "portrait"
        figsize = (8.27, 11.69) if is_portrait else (11.69, 8.27)
        fig = plt.figure(figsize=figsize, dpi=300)
        ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
        ax.axis("off")
        ax.imshow(img)
        pdf.savefig(fig, dpi=300)
        plt.close(fig)

print(f"Generated Booklet PDF: {booklet_pdf} ({booklet_pdf.stat().st_size} bytes)")

# 3. Distribute assets to Desktop, Downloads, and Brain directories
destinations = [DESKTOP_DIR, DOWNLOADS_DIR, BRAIN_DIR]

files_to_copy = [
    erd_png,
    erd_pdf,
    booklet_pdf,
]

for dest in destinations:
    if dest.exists():
        for src_file in files_to_copy:
            target = dest / src_file.name
            shutil.copy2(src_file, target)
            print(f"Copied {src_file.name} -> {target}")

print("Distribution complete!")
