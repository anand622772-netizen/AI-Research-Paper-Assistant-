from PIL import Image
from pathlib import Path

doc2_dir = Path(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\doc2_diagrams")
assets_dir = Path(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\report_assets")

copy_and_convert_map = {
    "rId15_image2.png": "system_use_case_diagram.png",
    "rId14_image1.jpeg": "use_case_both_actors.png",
    "rId16_image3.png": "use_case_researcher.png",
    "rId17_image4.png": "use_case_supervisor.png",
    "rId24_image5.jpg": "dfd_level_0_smartdoc.png",
    "rId25_image6.jpg": "dfd_level_1_smartdoc.png",
    "rId26_image7.jpg": "dfd_level_2.png",
    "rId27_image8.jpg": "dfd_level_3.png",
    "rId28_image9.jpg": "class_diagram_smartdoc.png",
    "rId29_image10.png": "sequence_diagram_smartdoc.png",
    "rId30_image11.jpg": "activity_diagram_smartdoc.png",
    "rId31_image12.png": "er_diagram_ares.png",
}

for src_name, dst_name in copy_and_convert_map.items():
    src_file = doc2_dir / src_name
    dst_file = assets_dir / dst_name
    
    im = Image.open(src_file)
    if im.mode in ("RGBA", "P") and dst_name.endswith(".png"):
        im = im.convert("RGBA")
        im.save(dst_file, format="PNG")
    elif im.mode == "RGB" and dst_name.endswith(".png"):
        im.save(dst_file, format="PNG")
    else:
        im.convert("RGB").save(dst_file, format="PNG")
    print(f"Properly saved {src_name} ({im.size}, {im.mode}) -> {dst_name} ({dst_file.stat().st_size} bytes, format=PNG)")
