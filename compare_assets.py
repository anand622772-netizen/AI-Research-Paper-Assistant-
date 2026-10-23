import filecmp
from pathlib import Path

assets_dir = Path(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\report_assets")
doc2_dir = Path(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\doc2_diagrams")

mapping = {
    "system_use_case_diagram.png": "rId15_image2.png", # or check if png or jpg
    "system_use_case_diagram.jpg": "rId14_image1.jpeg",
    "use_case_both_actors.png": "rId17_image4.png",
    "use_case_researcher.png": "rId15_image2.png",
    "use_case_supervisor.png": "rId16_image3.png",
    "dfd_level_0_smartdoc.png": "rId24_image5.jpg",
    "dfd_level_1_smartdoc.png": "rId25_image6.jpg",
    "dfd_level_2.png": "rId26_image7.jpg",
    "dfd_level_3.png": "rId27_image8.jpg",
    "class_diagram_smartdoc.png": "rId28_image9.jpg",
    "sequence_diagram_smartdoc.png": "rId29_image10.png",
    "activity_diagram_smartdoc.png": "rId30_image11.jpg",
    "er_diagram_ares.png": "rId31_image12.png",
}

for asset_name, doc2_name in mapping.items():
    a_path = assets_dir / asset_name
    d_path = doc2_dir / doc2_name
    a_size = a_path.stat().st_size if a_path.exists() else 0
    d_size = d_path.stat().st_size if d_path.exists() else 0
    print(f"{asset_name} ({a_size}b) vs {doc2_name} ({d_size}b)")
