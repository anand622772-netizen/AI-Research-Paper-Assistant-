from PIL import Image
import os

p = r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\doc2_diagrams"
for f in ["rId14_image1.jpeg", "rId15_image2.png", "rId16_image3.png", "rId17_image4.png"]:
    im = Image.open(os.path.join(p, f))
    print(f, im.size, im.mode)
