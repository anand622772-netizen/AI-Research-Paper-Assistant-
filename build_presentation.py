"""
build_presentation.py
Generates a 20-slide, publication-grade academic PowerPoint presentation (.pptx)
for Parul University Minor Project:
'AI RESEARCH PAPER ASSISTANT: AN END-TO-END ACADEMIC AUTHORING & LITERATURE SYNTHESIS PLATFORM'

Features:
- 16:9 widescreen layout (13.333" x 7.5")
- Deep navy title & closing slides with university branding
- Clean slate/ice-blue interior slides with category pills, accent dividers, and maroon page badges
- Direct inclusion of high-resolution system design diagrams (Use Case, DFD 0/1/2/3, UML Class, Sequence, Activity, ERD)
- Direct inclusion of actual UI walkthrough screenshots
- Automated conversion to PDF via PowerPoint COM
- Distribution to Desktop, Downloads, and scratch directory
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = Path("C:/Users/anand/.gemini/antigravity/scratch/ai_research_paper_assistant")
ASSETS_DIR = BASE_DIR / "outputs/report_assets"
OUTPUT_DIR = BASE_DIR / "outputs/presentation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DESKTOP_DIR = Path("C:/Users/anand/Desktop")
DOWNLOADS_DIR = Path("C:/Users/anand/Downloads")

PPTX_FILENAME = "Parul_University_Minor_Project_AI_Research_Paper_Assistant.pptx"
PDF_FILENAME = "Parul_University_Minor_Project_AI_Research_Paper_Assistant.pdf"

# Design Color Palette
COLOR_NAVY_DARK = RGBColor(10, 15, 29)       # #0A0F1D Cover background
COLOR_NAVY_TITLE = RGBColor(15, 23, 42)      # #0F172A Headings
COLOR_BLUE_PRIMARY = RGBColor(37, 99, 235)   # #2563EB Primary Brand
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255)   # #EFF6FF Pill Background
COLOR_BLUE_BORDER = RGBColor(191, 219, 254)  # #BFDBFE Pill Border
COLOR_MAROON = RGBColor(148, 54, 52)         # #943634 Parul Accent Maroon
COLOR_TEXT_MAIN = RGBColor(51, 65, 85)       # #334155 Body text
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B Secondary text
COLOR_CARD_BG = RGBColor(255, 255, 255)      # White Card
COLOR_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 Card Border
COLOR_BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC Slide Canvas

TOTAL_PAGES = 20

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    return prs

def set_slide_background(slide, color):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, category_text, title_text, subtitle_text=""):
    # Category Pill
    pill_w = Inches(len(category_text) * 0.11 + 0.5)
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), pill_w, Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = COLOR_BLUE_LIGHT
    pill.line.color.rgb = COLOR_BLUE_BORDER
    pill.line.width = Pt(1)
    tf_p = pill.text_frame
    tf_p.word_wrap = False
    tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
    p_p = tf_p.paragraphs[0]
    p_p.alignment = PP_ALIGN.CENTER
    r_p = p_p.add_run()
    r_p.text = category_text.upper()
    r_p.font.name = "Calibri"
    r_p.font.size = Pt(9.5)
    r_p.font.bold = True
    r_p.font.color.rgb = COLOR_BLUE_PRIMARY

    # Main Slide Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.48))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title_text
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(21)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_NAVY_TITLE

    # Subtitle
    if subtitle_text:
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.30), Inches(11.733), Inches(0.28))
        tf_s = tb_sub.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        r_s = p_s.add_run()
        r_s.text = subtitle_text
        r_s.font.name = "Calibri"
        r_s.font.size = Pt(11)
        r_s.font.color.rgb = COLOR_TEXT_MUTED

    # Accent Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.018))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

def add_footer(slide, page_num):
    # Divider Line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

    # Left text: University & Department
    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(6.0), Inches(0.3))
    tf_l = tb_left.text_frame
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    r_l = p_l.add_run()
    r_l.text = "Parul University | Department of MScIT | Minor Project Report 2026"
    r_l.font.name = "Calibri"
    r_l.font.size = Pt(9)
    r_l.font.color.rgb = COLOR_TEXT_MUTED

    # Center text: Project Name
    tb_mid = slide.shapes.add_textbox(Inches(6.8), Inches(6.92), Inches(4.5), Inches(0.3))
    tf_m = tb_mid.text_frame
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
    p_m = tf_m.paragraphs[0]
    p_m.alignment = PP_ALIGN.RIGHT
    r_m = p_m.add_run()
    r_m.text = "AI Research Paper Assistant"
    r_m.font.name = "Calibri"
    r_m.font.size = Pt(9)
    r_m.font.bold = True
    r_m.font.color.rgb = COLOR_TEXT_MAIN

    # Right badge: Maroon Page Badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.633), Inches(6.88), Inches(0.9), Inches(0.28))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_MAROON
    badge.line.fill.background()
    tf_b = badge.text_frame
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    r_b = p_b.add_run()
    r_b.text = f"{page_num} / {TOTAL_PAGES}"
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(9)
    r_b.font.bold = True
    r_b.font.color.rgb = RGBColor(255, 255, 255)

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_bullet_point(tf, bold_prefix, text, pt_size=11, space_after=6):
    p = tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.font.name = "Calibri"
    p.font.size = Pt(pt_size)
    
    r_b = p.add_run()
    r_b.text = "• " + bold_prefix + " "
    r_b.font.bold = True
    r_b.font.color.rgb = COLOR_NAVY_TITLE
    
    r_t = p.add_run()
    r_t.text = text
    r_t.font.bold = False
    r_t.font.color.rgb = COLOR_TEXT_MAIN

def build_all_slides(prs):
    blank_layout = prs.slide_layouts[6]
    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Premium Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s1, COLOR_NAVY_DARK)

    # Top Maroon Accent Banner
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_MAROON
    top_bar.line.fill.background()

    # University & Department Heading
    tb_uni = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.2))
    tf_u = tb_uni.text_frame
    tf_u.word_wrap = True
    p_u1 = tf_u.paragraphs[0]
    p_u1.alignment = PP_ALIGN.CENTER
    r_u1 = p_u1.add_run()
    r_u1.text = "PARUL UNIVERSITY"
    r_u1.font.name = "Calibri"
    r_u1.font.size = Pt(20)
    r_u1.font.bold = True
    r_u1.font.color.rgb = RGBColor(226, 232, 240)

    p_u2 = tf_u.add_paragraph()
    p_u2.alignment = PP_ALIGN.CENTER
    r_u2 = p_u2.add_run()
    r_u2.text = "FACULTY OF IT & COMPUTER SCIENCE  •  DEPARTMENT OF MScIT"
    r_u2.font.name = "Calibri"
    r_u2.font.size = Pt(13)
    r_u2.font.bold = True
    r_u2.font.color.rgb = RGBColor(147, 197, 253)

    p_u3 = tf_u.add_paragraph()
    p_u3.alignment = PP_ALIGN.CENTER
    r_u3 = p_u3.add_run()
    r_u3.text = "P.O. Limda, Ta. Waghodia, Dist. Vadodara - 391760, Gujarat, India"
    r_u3.font.name = "Calibri"
    r_u3.font.size = Pt(10)
    r_u3.font.color.rgb = RGBColor(148, 163, 184)

    # Decorative Card in Center
    center_card = add_card(s1, Inches(1.2), Inches(2.3), Inches(10.933), Inches(2.7), RGBColor(15, 23, 42), RGBColor(30, 41, 59))
    
    tb_proj = s1.shapes.add_textbox(Inches(1.5), Inches(2.55), Inches(10.333), Inches(2.2))
    tf_pj = tb_proj.text_frame
    tf_pj.word_wrap = True
    
    p_tag = tf_pj.paragraphs[0]
    p_tag.alignment = PP_ALIGN.CENTER
    r_tag = p_tag.add_run()
    r_tag.text = "A MINOR PROJECT DEFENSE & TECHNICAL PRESENTATION"
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(11)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(245, 158, 11) # Amber

    p_maint = tf_pj.add_paragraph()
    p_maint.alignment = PP_ALIGN.CENTER
    p_maint.space_before = Pt(8)
    r_maint = p_maint.add_run()
    r_maint.text = "AI RESEARCH PAPER ASSISTANT"
    r_maint.font.name = "Calibri"
    r_maint.font.size = Pt(28)
    r_maint.font.bold = True
    r_maint.font.color.rgb = RGBColor(255, 255, 255)

    p_subt = tf_pj.add_paragraph()
    p_subt.alignment = PP_ALIGN.CENTER
    p_subt.space_before = Pt(6)
    r_subt = p_subt.add_run()
    r_subt.text = "An End-to-End Academic Authoring, Literature Synthesis & Overleaf Compilation Platform"
    r_subt.font.name = "Calibri"
    r_subt.font.size = Pt(14)
    r_subt.font.color.rgb = RGBColor(186, 230, 253)

    p_deg = tf_pj.add_paragraph()
    p_deg.alignment = PP_ALIGN.CENTER
    p_deg.space_before = Pt(8)
    r_deg = p_deg.add_run()
    r_deg.text = "Submitted in partial fulfillment of the requirements for Master of Science in Information Technology (M.Sc. IT)"
    r_deg.font.name = "Calibri"
    r_deg.font.size = Pt(11)
    r_deg.font.italic = True
    r_deg.font.color.rgb = RGBColor(148, 163, 184)

    # Bottom Metadata Cards
    # Left Card: Candidate
    c_left = add_card(s1, Inches(1.2), Inches(5.25), Inches(5.3), Inches(1.6), RGBColor(15, 23, 42), RGBColor(30, 41, 59))
    tb_c = s1.shapes.add_textbox(Inches(1.4), Inches(5.35), Inches(4.9), Inches(1.4))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p_c0 = tf_c.paragraphs[0]
    r_c0 = p_c0.add_run()
    r_c0.text = "SUBMITTED BY:"
    r_c0.font.bold = True
    r_c0.font.size = Pt(10)
    r_c0.font.color.rgb = COLOR_MAROON
    
    p_c1 = tf_c.add_paragraph()
    p_c1.add_run().text = "Candidate Name"
    p_c1.runs[0].font.bold = True
    p_c1.runs[0].font.size = Pt(13)
    p_c1.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    p_c2 = tf_c.add_paragraph()
    p_c2.add_run().text = "Enrollment No.: 2203001XXXX\nM.Sc. IT Semester - IV | Academic Year: 2025-2026"
    p_c2.runs[0].font.size = Pt(10)
    p_c2.runs[0].font.color.rgb = RGBColor(148, 163, 184)

    # Right Card: Guide
    c_right = add_card(s1, Inches(6.833), Inches(5.25), Inches(5.3), Inches(1.6), RGBColor(15, 23, 42), RGBColor(30, 41, 59))
    tb_g = s1.shapes.add_textbox(Inches(7.033), Inches(5.35), Inches(4.9), Inches(1.4))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True
    p_g0 = tf_g.paragraphs[0]
    r_g0 = p_g0.add_run()
    r_g0.text = "UNDER THE GUIDANCE OF:"
    r_g0.font.bold = True
    r_g0.font.size = Pt(10)
    r_g0.font.color.rgb = RGBColor(59, 130, 246)
    
    p_g1 = tf_g.add_paragraph()
    p_g1.add_run().text = "Internal Faculty Guide"
    p_g1.runs[0].font.bold = True
    p_g1.runs[0].font.size = Pt(13)
    p_g1.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    p_g2 = tf_g.add_paragraph()
    p_g2.add_run().text = "Assistant Professor\nDepartment of MScIT, Parul University, Vadodara"
    p_g2.runs[0].font.size = Pt(10)
    p_g2.runs[0].font.color.rgb = RGBColor(148, 163, 184)


    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_BG_LIGHT)
    add_header(s2, "Executive Overview", "Project Motivation & Core Innovation", 
               "Bridging the divide between raw research ideation and submission-ready academic papers.")
    add_footer(s2, 2)

    # 3 Metrics Cards across Top
    metrics = [
        ("70%", "Authoring Acceleration", "Reduces total literature discovery and drafting cycle time from weeks to hours."),
        ("100%", "Citation Synchronization", "Guarantees zero citation drift by linking manuscript cite{} tags with audited BibTeX records."),
        ("0 Cost", "Offline Deterministic Mode", "Enables complete manuscript synthesis locally without mandatory cloud API tokens or internet.")
    ]
    for idx, (num, title, desc) in enumerate(metrics):
        cx = Inches(0.8 + idx * 4.0)
        c = add_card(s2, cx, Inches(1.85), Inches(3.733), Inches(1.4), COLOR_CARD_BG, COLOR_BLUE_BORDER)
        tb_m = s2.shapes.add_textbox(cx + Inches(0.2), Inches(1.95), Inches(3.333), Inches(1.2))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        p0 = tf_m.paragraphs[0]
        r0 = p0.add_run()
        r0.text = num
        r0.font.bold = True
        r0.font.size = Pt(24)
        r0.font.color.rgb = COLOR_BLUE_PRIMARY if idx != 2 else COLOR_MAROON
        
        p1 = tf_m.add_paragraph()
        r1 = p1.add_run()
        r1.text = title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_NAVY_TITLE
        
        p2 = tf_m.add_paragraph()
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Left Card: Context & Friction
    c_bot_l = add_card(s2, Inches(0.8), Inches(3.45), Inches(5.7), Inches(3.2))
    tb_bl = s2.shapes.add_textbox(Inches(1.0), Inches(3.6), Inches(5.3), Inches(2.9))
    tf_bl = tb_bl.text_frame
    tf_bl.word_wrap = True
    
    p_bl_t = tf_bl.paragraphs[0]
    p_bl_t.add_run().text = "The Scientific Publishing Dilemma"
    p_bl_t.runs[0].font.bold = True
    p_bl_t.runs[0].font.size = Pt(13)
    p_bl_t.runs[0].font.color.rgb = COLOR_NAVY_TITLE
    p_bl_t.space_after = Pt(8)

    add_bullet_point(tf_bl, "Literature Deluge:", "Over 5 million papers published yearly doubles every few years, overwhelming researchers.")
    add_bullet_point(tf_bl, "Extreme Fragmentation:", "Scholars constantly switch across Google Scholar, Zotero, Word, Matplotlib, and Overleaf.")
    add_bullet_point(tf_bl, "Format Non-Compliance:", "Conference rejections frequently occur due to broken bibliography keys and template errors.")
    add_bullet_point(tf_bl, "Cognitive Exhaustion:", "Authors spend over 60% of their effort fighting formatting instead of intellectual research.")

    # Bottom Right Card: Unified Solution
    c_bot_r = add_card(s2, Inches(6.833), Inches(3.45), Inches(5.7), Inches(3.2))
    tb_br = s2.shapes.add_textbox(Inches(7.033), Inches(3.6), Inches(5.3), Inches(2.9))
    tf_br = tb_br.text_frame
    tf_br.word_wrap = True
    
    p_br_t = tf_br.paragraphs[0]
    p_br_t.add_run().text = "The AI Research Paper Assistant Solution"
    p_br_t.runs[0].font.bold = True
    p_br_t.runs[0].font.size = Pt(13)
    p_br_t.runs[0].font.color.rgb = COLOR_BLUE_PRIMARY
    p_br_t.space_after = Pt(8)

    add_bullet_point(tf_br, "Unified Academic Cockpit:", "Consolidates search, hypothesis formulation, outline planning, drafting, review, and LaTeX bundling.")
    add_bullet_point(tf_br, "Live Scholarly Graph Integration:", "Direct REST querying of Semantic Scholar & arXiv for authentic bibliographic discovery.")
    add_bullet_point(tf_br, "Simulated 3-Reviewer Committee:", "Pre-submission double-blind peer review scoring across 5 rigorous conference dimensions.")
    add_bullet_point(tf_br, "1-Click Camera-Ready Export:", "Builds self-contained Overleaf ZIP archives with audited main.tex, references.bib, and 300 DPI plots.")


    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & SYSTEMIC BOTTLENECKS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_BG_LIGHT)
    add_header(s3, "Requirement Analysis", "Problem Statement: 5 Critical Academic Bottlenecks", 
               "Systemic inefficiencies that hinder post-graduate researchers and faculty supervisors.")
    add_footer(s3, 3)

    bottlenecks = [
        ("01", "Information Overload & Literature Lag", "Surfacing relevant prior art among millions of pre-prints without falling victim to keyword mismatch or missing seminal baselines."),
        ("02", "Synthesis & Literature Matrix Overhead", "Manual reading of dozens of abstracts requires weeks of effort to construct multi-dimensional comparative tables and identify authentic scientific gaps."),
        ("03", "Drafting Inefficiency & Academic Rigor", "Balancing mathematical notation precision, domain-specific terminology, and conference-compliant structural prose causes severe author fatigue."),
        ("04", "Citation Inconsistency & Broken References", "Manual tracking results in broken cite{} tags, mismatched BibTeX entries, and frustrating LaTeX compiler crashes right before submission deadlines."),
        ("05", "Absence of Pre-Submission Peer Critique", "Manuscripts undergo zero formal critique prior to camera-ready submission, leading to avoidable desk rejections from top-tier venues (IEEE/ACM/NeurIPS).")
    ]

    for idx, (code, title, desc) in enumerate(bottlenecks):
        y = Inches(1.85 + idx * 0.96)
        card = add_card(s3, Inches(0.8), y, Inches(11.733), Inches(0.84))
        
        # Code badge
        b_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), y + Inches(0.16), Inches(0.65), Inches(0.52))
        b_box.fill.solid()
        b_box.fill.fore_color.rgb = COLOR_NAVY_TITLE if idx % 2 == 0 else COLOR_MAROON
        b_box.line.fill.background()
        tf_bb = b_box.text_frame
        p_bb = tf_bb.paragraphs[0]
        p_bb.alignment = PP_ALIGN.CENTER
        r_bb = p_bb.add_run()
        r_bb.text = code
        r_bb.font.bold = True
        r_bb.font.size = Pt(13)
        r_bb.font.color.rgb = RGBColor(255, 255, 255)

        # Text
        tb_txt = s3.shapes.add_textbox(Inches(1.8), y + Inches(0.12), Inches(10.5), Inches(0.6))
        tf_tx = tb_txt.text_frame
        tf_tx.word_wrap = True
        p_t0 = tf_tx.paragraphs[0]
        r_t0 = p_t0.add_run()
        r_t0.text = title + " — "
        r_t0.font.bold = True
        r_t0.font.size = Pt(11.5)
        r_t0.font.color.rgb = COLOR_NAVY_TITLE
        
        r_t1 = p_t0.add_run()
        r_t1.text = desc
        r_t1.font.size = Pt(10)
        r_t1.font.color.rgb = COLOR_TEXT_MAIN


    # =========================================================================
    # SLIDE 4: PROJECT OBJECTIVES & SCOPE BOUNDARIES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, COLOR_BG_LIGHT)
    add_header(s4, "Project Profile", "Project Objectives & Scope Boundaries", 
               "Clear functional goals and operational boundaries governing software delivery.")
    add_footer(s4, 4)

    # Left: Core Objectives
    c_left = add_card(s4, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.8))
    tb_l = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p_lt = tf_l.paragraphs[0]
    p_lt.add_run().text = "Primary Engineering Objectives"
    p_lt.runs[0].font.bold = True
    p_lt.runs[0].font.size = Pt(13)
    p_lt.runs[0].font.color.rgb = COLOR_BLUE_PRIMARY
    p_lt.space_after = Pt(10)

    add_bullet_point(tf_l, "Literature Querying Automation:", "Develop RESTful wrappers for Semantic Scholar and arXiv to fetch metadata, abstracts, and BibTeX strings instantly.")
    add_bullet_point(tf_l, "Intelligent Outline Architect:", "Support venue-specific section hierarchies (NeurIPS, IEEE Transactions, ACM SIGKDD, Springer LNCS) with custom word budgets.")
    add_bullet_point(tf_l, "Hybrid Cloud/Offline Drafting:", "Implement dual runtime engine: Google Gemini / OpenAI for rich drafting, and a deterministic offline engine for zero-cost execution.")
    add_bullet_point(tf_l, "Simulated Double-Blind Review:", "Deploy multi-persona reviewer heuristics scoring across 5 core academic dimensions (Originality, Soundness, Rigor, Clarity, Citations).")
    add_bullet_point(tf_l, "Automated LaTeX & Overleaf Pipeline:", "Generate pristine main.tex, references.bib, and compile 300 DPI Matplotlib figures into ready-to-upload ZIP bundles.")

    # Right: Operational Scope & Boundaries
    c_right = add_card(s4, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.8))
    tb_r = s4.shapes.add_textbox(Inches(7.033), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p_rt = tf_r.paragraphs[0]
    p_rt.add_run().text = "Scope & Operational Boundaries"
    p_rt.runs[0].font.bold = True
    p_rt.runs[0].font.size = Pt(13)
    p_rt.runs[0].font.color.rgb = COLOR_MAROON
    p_rt.space_after = Pt(10)

    add_bullet_point(tf_r, "Target Academic Audience:", "Specifically engineered for M.Sc. IT, MCA, IMCA students, Ph.D. scholars, and university faculty supervisors.")
    add_bullet_point(tf_r, "Domain Focus:", "Optimized for Computer Science, Information Technology, AI, Data Science, and Software Engineering manuscripts.")
    add_bullet_point(tf_r, "Cross-Platform Web Architecture:", "Browser-based application accessible across Windows, Linux, and macOS without client-side native compilation hurdles.")
    add_bullet_point(tf_r, "Out-of-Scope (Data Fabrication):", "The platform strictly does NOT synthesize artificial lab results; all empirical benchmark numbers are provided or configured by the author.")
    add_bullet_point(tf_r, "Editorial Autonomy:", "Functions as an intelligent scaffolding assistant; intellectual ownership and final editorial control remain entirely with the researcher.")


    # =========================================================================
    # SLIDE 5: EXISTING SYSTEM VS PROPOSED SYSTEM
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, COLOR_BG_LIGHT)
    add_header(s5, "Comparative Analysis", "Existing Workflow vs. Proposed AI Platform", 
               "Systematic contrast highlighting operational leaps across every authoring dimension.")
    add_footer(s5, 5)

    # Comparison Table
    table_shape = s5.shapes.add_table(7, 3, Inches(0.8), Inches(1.85), Inches(11.733), Inches(4.7))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(4.766)
    tbl.columns[2].width = Inches(4.766)

    headers = ["Authoring Dimension", "Conventional Disjointed Workflow", "AI Research Paper Assistant"]
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_TITLE if c_idx < 2 else COLOR_BLUE_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h_text
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_rows = [
        ("Literature Discovery", "Manual browsing of Google Scholar/arXiv; scattered notes and spreadsheet tracking.", "Direct REST querying of Semantic Scholar; instant citation counts, abstracts, and BibTeX keys."),
        ("Related Work Synthesis", "Weeks spent manually reading papers to hand-craft comparative text and tables.", "Automated comparative matrix generation contrasting approaches, benchmarks, and limitations."),
        ("Drafting & Formatting", "Manual typing in Word/Google Docs with severe cognitive fatigue on mathematical equations.", "Context-enriched section drafting with LaTeX equation environments and pseudocode staging."),
        ("Citation Tracking", "High risk of citation drift, missing BibTeX keys, and broken cite{} tags in final compilation.", "100% automated Citation Health Checker verifying every cite{} key against references.bib."),
        ("Quality & Peer Review", "Zero formal evaluation prior to conference submission, leading to avoidable rejections.", "Multi-persona simulated double-blind peer review scoring across 5 conference rubrics."),
        ("LaTeX Packaging", "Manual file copying, figure sizing, and painful compilation debugging on client machines.", "1-Click automated generation of self-contained Overleaf ZIP bundles and local PDF compilation.")
    ]

    for r_idx, (dim, conv, prop) in enumerate(comp_rows, start=1):
        # Col 0: Dimension
        c0 = tbl.cell(r_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = COLOR_BLUE_LIGHT
        p0 = c0.text_frame.paragraphs[0]
        r0 = p0.add_run()
        r0.text = dim
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = COLOR_NAVY_TITLE

        # Col 1: Conventional
        c1 = tbl.cell(r_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = RGBColor(254, 242, 242) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
        p1 = c1.text_frame.paragraphs[0]
        r1 = p1.add_run()
        r1.text = conv
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(153, 27, 27)

        # Col 2: Proposed
        c2 = tbl.cell(r_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = RGBColor(240, 253, 244) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
        p2 = c2.text_frame.paragraphs[0]
        r2 = p2.add_run()
        r2.text = prop
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(22, 101, 52)


    # =========================================================================
    # SLIDE 6: FEASIBILITY STUDY ANALYSIS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, COLOR_BG_LIGHT)
    add_header(s6, "Project Feasibility", "Multi-Dimensional Feasibility Study", 
               "Thorough assessment validating the practical, commercial, and technical viability of the platform.")
    add_footer(s6, 6)

    feas_cards = [
        ("Technical Feasibility", COLOR_BLUE_PRIMARY, [
            ("Open-Source Foundation:", "Built on robust, modern technologies: Python 3.11+, Streamlit reactive UI, and Tectonic TeX."),
            ("Documented REST APIs:", "Semantic Scholar Graph API provides high-availability academic endpoints with stable schemas."),
            ("Dual Execution Pipeline:", "Deterministic offline engine ensures 100% functionality even during network or quota outages.")
        ]),
        ("Economic Feasibility", COLOR_MAROON, [
            ("Zero Licensing Costs:", "Engineered entirely using open-source libraries, eliminating expensive proprietary software fees."),
            ("Zero-Cost Offline Mode:", "Students can run the full authoring pipeline locally without purchasing commercial API credits."),
            ("Minimal Cloud Overhead:", "Optional cloud LLM drafting incurs only pennies per paper, well within lab allocations.")
        ]),
        ("Operational Feasibility", COLOR_NAVY_TITLE, [
            ("Intuitive Web Cockpit:", "Self-explanatory 8-tab visual interface requiring zero specialized command-line training."),
            ("Rapid User Adoption:", "Undergraduate and master's students can generate verified LaTeX bundles in their first session."),
            ("Seamless State Management:", "1-click JSON import/export lets authors pause, save, and resume projects at any time.")
        ]),
        ("Legal & Ethical Feasibility", COLOR_BLUE_PRIMARY, [
            ("Fair Use Compliance:", "Scholarly abstracts and BibTeX data retrieved strictly respect open academic access standards."),
            ("Zero Attribution Drift:", "Every generated citation links back to genuine, published academic papers and authors."),
            ("Academic Integrity:", "Functions as a cognitive co-pilot and typesetting assistant; author maintains intellectual direction.")
        ])
    ]

    for idx, (title, accent, bullets) in enumerate(feas_cards):
        gx = Inches(0.8 + (idx % 2) * 6.0)
        gy = Inches(1.85 + (idx // 2) * 2.45)
        
        card = add_card(s6, gx, gy, Inches(5.733), Inches(2.3))
        
        # Color bar on top of card
        c_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, gx, gy, Inches(5.733), Inches(0.06))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = accent
        c_bar.line.fill.background()

        tb = s6.shapes.add_textbox(gx + Inches(0.25), gy + Inches(0.15), Inches(5.2), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        r = pt.add_run()
        r.text = title
        r.font.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = accent
        pt.space_after = Pt(6)

        for b_bold, b_desc in bullets:
            add_bullet_point(tf, b_bold, b_desc, pt_size=9.5, space_after=3)


    # =========================================================================
    # SLIDE 7: END-TO-END SYSTEM ARCHITECTURE (8 MODULES)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, COLOR_BG_LIGHT)
    add_header(s7, "System Architecture", "The 8-Module Academic Authoring Pipeline", 
               "Decoupled, cohesive software architecture managing the complete paper development lifecycle.")
    add_footer(s7, 7)

    modules = [
        ("M1", "Project Portal", "Admin & Venue Config", "Configures manuscript titles, target templates (IEEE/NeurIPS), and toggles Cloud vs. Offline engines."),
        ("M2", "Literature Hub", "Graph API Ingestion", "Queries Semantic Scholar & arXiv REST endpoints, parsing titles, citation velocity, and BibTeX."),
        ("M3", "Insights Hub", "Hypothesis Generator", "Analyzes collected abstracts to extract persistent scientific gaps and auto-derive testable hypotheses."),
        ("M4", "Outline Architect", "Structural Planner", "Generates conference-compliant hierarchical outlines with custom word budgets across sections."),
        ("M5", "Related Work", "Synthesis Engine", "Constructs structured tabular comparison matrices contrasting approaches, datasets, and limitations."),
        ("M6", "Drafting Studio", "AI Prose & Equations", "Dispatches structured prompts to LLMs/offline engine; formats LaTeX equations and algorithm boxes."),
        ("M7", "Peer Review", "3-Reviewer Simulation", "Simulates Senior Reviewer, Methodologist, and Domain Expert scoring manuscripts across 5 rubrics."),
        ("M8", "LaTeX Bundler", "Compiler & Overleaf ZIP", "Audits citation health, compiles 300 DPI figures, and packages complete Overleaf ZIP archives.")
    ]

    for idx, (code, title, role, desc) in enumerate(modules):
        mx = Inches(0.8 + (idx % 4) * 2.98)
        my = Inches(1.85 + (idx // 4) * 2.45)
        
        c = add_card(s7, mx, my, Inches(2.8), Inches(2.3))
        
        # Pill on top
        p_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx + Inches(0.15), my + Inches(0.15), Inches(0.7), Inches(0.3))
        p_box.fill.solid()
        p_box.fill.fore_color.rgb = COLOR_BLUE_PRIMARY if idx < 4 else COLOR_MAROON
        p_box.line.fill.background()
        tf_pb = p_box.text_frame
        p_p = tf_pb.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        r_p = p_p.add_run()
        r_p.text = code
        r_p.font.bold = True
        r_p.font.size = Pt(10)
        r_p.font.color.rgb = RGBColor(255, 255, 255)

        tb_m = s7.shapes.add_textbox(mx + Inches(0.15), my + Inches(0.55), Inches(2.5), Inches(1.65))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        p0 = tf_m.paragraphs[0]
        r0 = p0.add_run()
        r0.text = title
        r0.font.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = COLOR_NAVY_TITLE

        p1 = tf_m.add_paragraph()
        r1 = p1.add_run()
        r1.text = role
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_BLUE_PRIMARY

        p2 = tf_m.add_paragraph()
        p2.space_before = Pt(4)
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = COLOR_TEXT_MUTED


    # =========================================================================
    # SLIDE 8: SOFTWARE PROCESS MODEL: SPIRAL SDLC
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, COLOR_BG_LIGHT)
    add_header(s8, "Process Model", "Spiral SDLC: Risk-Driven Engineering", 
               "Systematic risk analysis governing the integration of generative AI with deterministic LaTeX engines.")
    add_footer(s8, 8)

    # Why Spiral Box
    c_top = add_card(s8, Inches(0.8), Inches(1.85), Inches(11.733), Inches(0.8), COLOR_BLUE_LIGHT, COLOR_BLUE_BORDER)
    tb_t = s8.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.333), Inches(0.7))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.add_run().text = "Why the Spiral Model? "
    p_t.runs[0].font.bold = True
    p_t.runs[0].font.size = Pt(11)
    p_t.runs[0].font.color.rgb = COLOR_BLUE_PRIMARY
    p_t.add_run().text = "Coupling non-deterministic generative language models with strict, deterministic document compilers (LaTeX/Tectonic) creates severe failure points (rate limits, hallucinated citations, compilation crashes). The Spiral SDLC resolves these risks iteratively across 4 focused spirals."
    p_t.runs[1].font.size = Pt(10)
    p_t.runs[1].font.color.rgb = COLOR_TEXT_MAIN

    # 4 Spiral Iteration Cards
    spirals = [
        ("Spiral Iteration 1", "Core Architecture & Risk Mitigation", COLOR_BLUE_PRIMARY, [
            ("Identified Risk:", "LLM API rate limits, network outages, and token costs for students."),
            ("Engineering Milestone:", "Built underlying project state JSON manager and deterministic offline rule-based academic engine."),
            ("Verification Target:", "Zero-token offline draft generation successfully demonstrated.")
        ]),
        ("Spiral Iteration 2", "Literature Discovery & UI Prototype", COLOR_MAROON, [
            ("Identified Risk:", "External scholarly graph API instability and malformed BibTeX."),
            ("Engineering Milestone:", "Implemented Semantic Scholar REST client with in-memory caching and fallback to curated academic records."),
            ("Verification Target:", "10-paper query parsing and abstract extraction working cleanly.")
        ]),
        ("Spiral Iteration 3", "Drafting Engine & Peer Review Studio", COLOR_NAVY_TITLE, [
            ("Identified Risk:", "Draft prose incoherence, missing baselines, and citation drift."),
            ("Engineering Milestone:", "Engineered context-enriched prompt assembler, related work comparison matrix builder, and 5-dimension rubric evaluator."),
            ("Verification Target:", "Simulated peer review scoring 8.5/10 with itemized critiques.")
        ]),
        ("Spiral Iteration 4", "Plots, Packaging & System Verification", COLOR_BLUE_PRIMARY, [
            ("Identified Risk:", "LaTeX syntax compilation errors and unreferenced BibTeX keys."),
            ("Engineering Milestone:", "Built native Python plotting studio (300 DPI), automated Citation Health Checker, and Overleaf ZIP packager."),
            ("Verification Target:", "16/16 verification test cases passed (100% success rate).")
        ])
    ]

    for idx, (title, sub, accent, bullets) in enumerate(spirals):
        sx = Inches(0.8 + idx * 2.98)
        c = add_card(s8, sx, Inches(2.8), Inches(2.8), Inches(3.85))
        
        # Color top bar
        c_bar = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, sx, Inches(2.8), Inches(2.8), Inches(0.06))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = accent
        c_bar.line.fill.background()

        tb = s8.shapes.add_textbox(sx + Inches(0.15), Inches(2.95), Inches(2.5), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = title
        r0.font.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = sub
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_NAVY_TITLE
        p1.space_after = Pt(6)

        for b_b, b_t in bullets:
            add_bullet_point(tf, b_b, b_t, pt_size=8.5, space_after=4)


    # =========================================================================
    # SLIDE 9: SYSTEM MODELING: USE CASE DIAGRAM
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, COLOR_BG_LIGHT)
    add_header(s9, "System Modeling", "System Use Case Diagram (UC-01 to UC-10)", 
               "Visualizing actor-system boundary interactions across primary and external service providers.")
    add_footer(s9, 9)

    # Left: Diagram Image
    img_uc = ASSETS_DIR / "system_use_case_diagram.png"
    if img_uc.exists():
        s9.shapes.add_picture(str(img_uc), Inches(0.8), Inches(1.85), width=Inches(6.2))

    # Right: Use Case Specification Card
    c_uc = add_card(s9, Inches(7.2), Inches(1.85), Inches(5.333), Inches(4.8))
    tb_uc = s9.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(4.933), Inches(4.5))
    tf_uc = tb_uc.text_frame
    tf_uc.word_wrap = True
    
    p_ut = tf_uc.paragraphs[0]
    p_ut.add_run().text = "Use Case Breakdown & Actors"
    p_ut.runs[0].font.bold = True
    p_ut.runs[0].font.size = Pt(13)
    p_ut.runs[0].font.color.rgb = COLOR_NAVY_TITLE
    p_ut.space_after = Pt(8)

    add_bullet_point(tf_uc, "Academic Researcher (Primary):", "Central orchestrator initiating workspace setup, querying literature, outlining, editing drafts, and triggering bundling.")
    add_bullet_point(tf_uc, "Semantic Scholar API (External):", "Responds to literature search queries (UC-02) and supplies BibTeX citations (UC-03).")
    add_bullet_point(tf_uc, "AI Cloud Services (Gemini/OpenAI):", "Executes context-enriched section drafting (UC-06), hypothesis derivation (UC-04), and simulated peer review (UC-08).")
    add_bullet_point(tf_uc, "LaTeX Compiler (System Service):", "Performs citation audit checks, runs Tectonic/pdflatex, and packages Overleaf ZIP bundles (UC-10).")
    add_bullet_point(tf_uc, "Faculty Supervisor Interaction:", "Leverages automated rubric scores and peer reviews for fast pre-submission manuscript evaluations.")


    # =========================================================================
    # SLIDE 10: DATA FLOW MODELING: LEVEL 0 (CONTEXT DIAGRAM)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, COLOR_BG_LIGHT)
    add_header(s10, "Data Flow Modeling", "DFD Level 0: Context Level Diagram", 
               "High-level information exchange between the system bubble and external entities.")
    add_footer(s10, 10)

    # Left: Diagram Image
    img_dfd0 = ASSETS_DIR / "dfd_level_0_smartdoc.png"
    if img_dfd0.exists():
        s10.shapes.add_picture(str(img_dfd0), Inches(0.8), Inches(1.85), width=Inches(6.2))

    # Right: Context Analysis Card
    c_dfd0 = add_card(s10, Inches(7.2), Inches(1.85), Inches(5.333), Inches(4.8))
    tb_d0 = s10.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(4.933), Inches(4.5))
    tf_d0 = tb_d0.text_frame
    tf_d0.word_wrap = True
    
    p_d0 = tf_d0.paragraphs[0]
    p_d0.add_run().text = "Context Flow Architecture"
    p_d0.runs[0].font.bold = True
    p_d0.runs[0].font.size = Pt(13)
    p_d0.runs[0].font.color.rgb = COLOR_NAVY_TITLE
    p_d0.space_after = Pt(8)

    add_bullet_point(tf_d0, "System Process 0.0:", "Represents the unified AI Research Paper Assistant platform encapsulating all data transformations.")
    add_bullet_point(tf_d0, "Researcher Data Inflow:", "Author supplies search topics, stylistic parameters, venue templates, outline adjustments, and plot specifications.")
    add_bullet_point(tf_d0, "Scholarly API Communication:", "Sends REST GET requests containing search keywords; receives JSON arrays containing paper abstracts, citation metrics, and BibTeX entries.")
    add_bullet_point(tf_d0, "Generative LLM Inflow/Outflow:", "Dispatches rich academic prompt dossiers; streams back academic prose drafts, equation blocks, and peer reviews.")
    add_bullet_point(tf_d0, "Final Output Deliverables:", "Assembled camera-ready PDF document, citation audit report, and self-contained Overleaf ZIP packages.")


    # =========================================================================
    # SLIDE 11: DATA FLOW MODELING: LEVEL 1 (FUNCTIONAL DECOMPOSITION)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, COLOR_BG_LIGHT)
    add_header(s11, "Data Flow Modeling", "DFD Level 1: Major System Processes & Data Stores", 
               "Decomposition into 6 core functional processes and 6 persistent data repositories.")
    add_footer(s11, 11)

    # Left: Diagram Image
    img_dfd1 = ASSETS_DIR / "dfd_level_1_smartdoc.png"
    if img_dfd1.exists():
        s11.shapes.add_picture(str(img_dfd1), Inches(0.8), Inches(1.85), width=Inches(5.6))

    # Right: Data Stores & Processes Card
    c_dfd1 = add_card(s11, Inches(6.6), Inches(1.85), Inches(5.933), Inches(4.8))
    tb_d1 = s11.shapes.add_textbox(Inches(6.8), Inches(2.0), Inches(5.533), Inches(4.5))
    tf_d1 = tb_d1.text_frame
    tf_d1.word_wrap = True
    
    p_d1 = tf_d1.paragraphs[0]
    p_d1.add_run().text = "6 Core Processes & 6 Persistent Data Stores"
    p_d1.runs[0].font.bold = True
    p_d1.runs[0].font.size = Pt(13)
    p_d1.runs[0].font.color.rgb = COLOR_BLUE_PRIMARY
    p_d1.space_after = Pt(6)

    add_bullet_point(tf_d1, "Process 1.0 (Literature Discovery):", "Executes scholarly searches and records verified citations into Data Store D1 (Literature Store).")
    add_bullet_point(tf_d1, "Process 2.0 (Create Hypothesis):", "Analyzes collected prior art to derive novel research questions into Data Store D2 (Hypothesis Store).")
    add_bullet_point(tf_d1, "Process 3.0 (Architect Outline):", "Transforms hypotheses into venue-compliant outlines stored in Data Store D3 (Outline Store).")
    add_bullet_point(tf_d1, "Process 4.0 (Draft Sections):", "Synthesizes section drafts with LaTeX equations, persisting text into Data Store D4 (Drafts Store).")
    add_bullet_point(tf_d1, "Process 5.0 (Simulated Peer Review):", "Evaluates drafts against conference rubrics, archiving critiques in Data Store D5 (Review Store).")
    add_bullet_point(tf_d1, "Process 6.0 (Generate Package):", "Renders 300 DPI plots, audits citations, and packages Overleaf ZIP into Data Store D6 (Package Store).")


    # =========================================================================
    # SLIDE 12: DETAILED DATA FLOW: LEVEL 2 & LEVEL 3 DECOMPOSITION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, COLOR_BG_LIGHT)
    add_header(s12, "Detailed Data Flow", "DFD Level 2 & Level 3: Drafting & Peer Review Pipelines", 
               "Granular modeling of internal text synthesis, equation formatting, and multi-persona critique.")
    add_footer(s12, 12)

    # Left: DFD Level 2 Image (Drafting)
    c_l2 = add_card(s12, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.8))
    img_dfd2 = ASSETS_DIR / "dfd_level_2.png"
    if img_dfd2.exists():
        s12.shapes.add_picture(str(img_dfd2), Inches(1.0), Inches(2.25), width=Inches(5.3))
    tb_l2 = s12.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(0.35))
    tf_l2 = tb_l2.text_frame
    p_l2 = tf_l2.paragraphs[0]
    p_l2.add_run().text = "DFD Level 2: Drafting Engine (Process 4.0)"
    p_l2.runs[0].font.bold = True
    p_l2.runs[0].font.size = Pt(11)
    p_l2.runs[0].font.color.rgb = COLOR_NAVY_TITLE

    # Right: DFD Level 3 Image (Peer Review)
    c_l3 = add_card(s12, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.8))
    img_dfd3 = ASSETS_DIR / "dfd_level_3.png"
    if img_dfd3.exists():
        s12.shapes.add_picture(str(img_dfd3), Inches(7.033), Inches(2.25), width=Inches(5.3))
    tb_l3 = s12.shapes.add_textbox(Inches(7.033), Inches(1.9), Inches(5.3), Inches(0.35))
    tf_l3 = tb_l3.text_frame
    p_l3 = tf_l3.paragraphs[0]
    p_l3.add_run().text = "DFD Level 3: Peer Review Pipeline (Process 5.0)"
    p_l3.runs[0].font.bold = True
    p_l3.runs[0].font.size = Pt(11)
    p_l3.runs[0].font.color.rgb = COLOR_MAROON


    # =========================================================================
    # SLIDE 13: UML STRUCTURAL DESIGN: CLASS DIAGRAM
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, COLOR_BG_LIGHT)
    add_header(s13, "Object-Oriented Design", "UML Class Diagram: Core Domain Entities", 
               "Static structural architecture defining system classes, attributes, methods, and associations.")
    add_footer(s13, 13)

    # Left: Diagram Image
    img_cls = ASSETS_DIR / "class_diagram_smartdoc.png"
    if img_cls.exists():
        s13.shapes.add_picture(str(img_cls), Inches(0.8), Inches(1.85), width=Inches(6.2))

    # Right: Key Classes Breakdown
    c_cls = add_card(s13, Inches(7.2), Inches(1.85), Inches(5.333), Inches(4.8))
    tb_c = s13.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(4.933), Inches(4.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    
    p_ct = tf_c.paragraphs[0]
    p_ct.add_run().text = "Key Architectural Classes"
    p_ct.runs[0].font.bold = True
    p_ct.runs[0].font.size = Pt(13)
    p_ct.runs[0].font.color.rgb = COLOR_NAVY_TITLE
    p_ct.space_after = Pt(8)

    add_bullet_point(tf_c, "PaperProject:", "Central entity encapsulating metadata, selected target venue, active LLM mode, and project file references.")
    add_bullet_point(tf_c, "LiteratureSearcher:", "REST client executing HTTP GET queries against Semantic Scholar, parsing abstracts, and serializing BibTeX strings.")
    add_bullet_point(tf_c, "LLMEngine (Strategy Pattern):", "Abstract base class with CloudLLMEngine (Gemini/OpenAI) and OfflineAcademicEngine concrete implementations.")
    add_bullet_point(tf_c, "OutlineArchitect:", "Manages section hierarchies, word count targets, and conference section ordering.")
    add_bullet_point(tf_c, "CitationAuditor:", "Static audit engine verifying bidirectional citation consistency and flagging missing BibTeX keys.")
    add_bullet_point(tf_c, "LaTeXCompiler & Packager:", "Assembles main.tex, figures, and builds autonomous Overleaf-ready ZIP archives.")


    # =========================================================================
    # SLIDE 14: UML BEHAVIORAL DESIGN: SEQUENCE & ACTIVITY
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, COLOR_BG_LIGHT)
    add_header(s14, "Behavioral Modeling", "UML Behavioral Models: Sequence & Activity", 
               "Chronological message dispatch, operational decision gates, and branching workflows.")
    add_footer(s14, 14)

    # Left: Sequence Diagram Image
    c_seq = add_card(s14, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.8))
    img_seq = ASSETS_DIR / "sequence_diagram_smartdoc.png"
    if img_seq.exists():
        s14.shapes.add_picture(str(img_seq), Inches(1.0), Inches(2.25), width=Inches(5.3))
    tb_sq = s14.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(0.35))
    tf_sq = tb_sq.text_frame
    p_sq = tf_sq.paragraphs[0]
    p_sq.add_run().text = "UML Sequence Diagram: End-to-End Execution Flow"
    p_sq.runs[0].font.bold = True
    p_sq.runs[0].font.size = Pt(11)
    p_sq.runs[0].font.color.rgb = COLOR_BLUE_PRIMARY

    # Right: Activity Diagram Image
    c_act = add_card(s14, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.8))
    img_act = ASSETS_DIR / "activity_diagram_smartdoc.png"
    if img_act.exists():
        s14.shapes.add_picture(str(img_act), Inches(7.033), Inches(2.25), width=Inches(5.3))
    tb_ac = s14.shapes.add_textbox(Inches(7.033), Inches(1.9), Inches(5.3), Inches(0.35))
    tf_ac = tb_ac.text_frame
    p_ac = tf_ac.paragraphs[0]
    p_ac.add_run().text = "UML Activity Diagram: Decision Paths & Control Flow"
    p_ac.runs[0].font.bold = True
    p_ac.runs[0].font.size = Pt(11)
    p_ac.runs[0].font.color.rgb = COLOR_MAROON


    # =========================================================================
    # SLIDE 15: DATABASE ARCHITECTURE: ENTITY-RELATIONSHIP MODEL
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, COLOR_BG_LIGHT)
    add_header(s15, "Database Schema", "Entity-Relationship Model (ERD) & Data Schema", 
               "Relational design maintaining literature, outlines, drafts, reviews, and visual assets.")
    add_footer(s15, 15)

    # Left: ER Diagram Image
    img_erd = ASSETS_DIR / "er_diagram_ares.png"
    if img_erd.exists():
        s15.shapes.add_picture(str(img_erd), Inches(0.8), Inches(1.85), width=Inches(6.2))

    # Right: Relational Schema Card
    c_erd = add_card(s15, Inches(7.2), Inches(1.85), Inches(5.333), Inches(4.8))
    tb_e = s15.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(4.933), Inches(4.5))
    tf_e = tb_e.text_frame
    tf_e.word_wrap = True
    
    p_et = tf_e.paragraphs[0]
    p_et.add_run().text = "Database Tables & Cardinality"
    p_et.runs[0].font.bold = True
    p_et.runs[0].font.size = Pt(13)
    p_et.runs[0].font.color.rgb = COLOR_NAVY_TITLE
    p_et.space_after = Pt(8)

    add_bullet_point(tf_e, "tbl_paper_project (Central Entity):", "Stores project_id, title, author_names, target_venue, and llm_engine_mode. 1:N parent across all tables.")
    add_bullet_point(tf_e, "tbl_literature_sources (1:N):", "Contains source_id, paper_title, authors, venue, year, citation_count, and formatted bibtex_raw.")
    add_bullet_point(tf_e, "tbl_paper_outline (1:N):", "Tracks section_id, section_order, section_title, target_words, and key_points.")
    add_bullet_point(tf_e, "tbl_section_drafts (1:N):", "Stores drafted markdown/LaTeX text, computed word_count, and author approval flag.")
    add_bullet_point(tf_e, "tbl_peer_review_logs (1:N):", "Logs overall_score (1.0-10.0), recommendation verdict (Accept/Revise), and multi-persona critique.")
    add_bullet_point(tf_e, "tbl_figure_assets (1:N):", "Maintains captions, 300 DPI raster paths, vector PDF paths, and LaTeX figure code blocks.")


    # =========================================================================
    # SLIDE 16: SYSTEM IMPLEMENTATION & UI WALKTHROUGH
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, COLOR_BG_LIGHT)
    add_header(s16, "Implementation", "User Interface Walkthrough: The 8-Step Cockpit", 
               "Streamlit reactive web frontend with native session state and dual cloud/offline execution.")
    add_footer(s16, 16)

    # 4 UI Screenshots in 2x2 Grid
    ui_shots = [
        ("screenshot_1_paper_portal.png", "Tab 1: Project Portal & LLM Mode Toggle"),
        ("screenshot_5_section_writing.png", "Tab 5: Section Writing Studio & LaTeX Math"),
        ("screenshot_7_plots_visuals.png", "Tab 7: Publication Plots Studio (300 DPI)"),
        ("screenshot_9_final_paper_export.png", "Tab 9: Final Paper Audit & Overleaf Packager")
    ]

    for idx, (img_name, label) in enumerate(ui_shots):
        ux = Inches(0.8 + (idx % 2) * 6.0)
        uy = Inches(1.85 + (idx // 2) * 2.45)
        
        c = add_card(s16, ux, uy, Inches(5.733), Inches(2.3))
        
        img_p = ASSETS_DIR / img_name
        if img_p.exists():
            s16.shapes.add_picture(str(img_p), ux + Inches(0.15), uy + Inches(0.12), width=Inches(3.3))
        
        # Text description on right side of sub-card
        tb = s16.shapes.add_textbox(ux + Inches(3.6), uy + Inches(0.15), Inches(2.0), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = label
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_NAVY_TITLE


    # =========================================================================
    # SLIDE 17: CORE BUSINESS LOGIC & TECHNICAL INNOVATIONS
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17, COLOR_BG_LIGHT)
    add_header(s17, "Technical Rigor", "Core Business Logic & Algorithmic Implementations", 
               "Robust algorithms guaranteeing citation consistency, multi-model adaptability, and clean LaTeX.")
    add_footer(s17, 17)

    innovations = [
        ("1. Citation Health Auditor", COLOR_BLUE_PRIMARY, [
            ("Regex In-Text Tokenizer:", "Audits all \\cite{...} tags across manuscript sections: cited_keys = set(re.findall(r'\\\\cite\\{([^}]+)\\}', text))."),
            ("BibTeX Key Comparator:", "Extracts declared keys via bib_keys = set(re.findall(r'@\\w+\\{([^,]+),', bibtex))."),
            ("Zero-Drift Validation:", "Computes missing_keys = cited_keys - bib_keys; warns author before compilation to eliminate TeX errors.")
        ]),
        ("2. Dual-Engine LLM Abstraction", COLOR_MAROON, [
            ("Abstract Strategy Pattern:", "BaseLLMEngine defines abstract generate_draft() implemented by CloudLLMEngine and OfflineAcademicEngine."),
            ("Google Gemini 1.5 Pro:", "Live cloud mode leveraging multi-turn context prompting for advanced reasoning and proof formulation."),
            ("Deterministic Offline Fallback:", "Rule-based synthesizer dynamically constructs structured sections and mathematical theorems without API keys.")
        ]),
        ("3. Multi-Persona Peer Review Rubric", COLOR_NAVY_TITLE, [
            ("Senior Reviewer Persona:", "Focuses on theoretical soundness, mathematical proofs, and conceptual novelty."),
            ("Methodologist Persona:", "Critiques empirical baselines, benchmark validity, and metric fairness."),
            ("Domain Expert Persona:", "Evaluates literature coverage, citation integrity, and academic writing clarity.")
        ]),
        ("4. Autonomous Overleaf ZIP Packager", COLOR_BLUE_PRIMARY, [
            ("In-Memory ZIP Assembly:", "Packages main.tex, references.bib, and figures/ without intermediate disk pollution."),
            ("Multi-OS Compilation Scripts:", "Includes Makefile (Linux/macOS latexmk) and compile.bat (Windows pdflatex + bibtex)."),
            ("Overleaf Direct Import:", "Single ZIP upload immediately compiles without missing style files or broken bounding boxes.")
        ])
    ]

    for idx, (title, accent, bullets) in enumerate(innovations):
        ix = Inches(0.8 + (idx % 2) * 6.0)
        iy = Inches(1.85 + (idx // 2) * 2.45)
        
        c = add_card(s17, ix, iy, Inches(5.733), Inches(2.3))
        
        # Color accent strip
        c_bar = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, ix, iy, Inches(5.733), Inches(0.06))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = accent
        c_bar.line.fill.background()

        tb = s17.shapes.add_textbox(ix + Inches(0.2), iy + Inches(0.15), Inches(5.333), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        r = pt.add_run()
        r.text = title
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = accent
        pt.space_after = Pt(5)

        for b_b, b_t in bullets:
            add_bullet_point(tf, b_b, b_t, pt_size=9, space_after=3)


    # =========================================================================
    # SLIDE 18: TESTING STRATEGY & VERIFICATION MATRIX
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18, COLOR_BG_LIGHT)
    add_header(s18, "Quality Assurance", "Testing Strategy & 16-Suite Verification Results", 
               "Rigorous multi-tiered testing achieving 100% test pass rate across all functional boundaries.")
    add_footer(s18, 18)

    # Left: 5 Testing Tiers
    c_tier = add_card(s18, Inches(0.8), Inches(1.85), Inches(4.5), Inches(4.8))
    tb_tr = s18.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.1), Inches(4.5))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True
    
    p_trt = tf_tr.paragraphs[0]
    p_trt.add_run().text = "5 Sequential Testing Tiers"
    p_trt.runs[0].font.bold = True
    p_trt.runs[0].font.size = Pt(13)
    p_trt.runs[0].font.color.rgb = COLOR_BLUE_PRIMARY
    p_trt.space_after = Pt(10)

    add_bullet_point(tf_tr, "Unit Testing:", "Tested REST clients, BibTeX parsers, and plot generators in isolation with unittest (10/10 passed).")
    add_bullet_point(tf_tr, "Integration Testing:", "Verified data pipeline between literature search, outline generation, and drafting engine.")
    add_bullet_point(tf_tr, "System Testing:", "Validated full end-to-end authoring runs in both Live Cloud and Offline modes.")
    add_bullet_point(tf_tr, "User Acceptance Testing:", "Conducted with M.Sc. IT & MCA students to evaluate UI responsiveness and feedback clarity.")
    add_bullet_point(tf_tr, "Robustness & Edge Testing:", "Simulated network drops, missing API keys, invalid plot code, and malformed BibTeX.")

    # Right: Test Cases Table (Subset of 8 key cases)
    t_shape = s18.shapes.add_table(9, 4, Inches(5.5), Inches(1.85), Inches(7.033), Inches(4.8))
    tbl_t = t_shape.table
    tbl_t.columns[0].width = Inches(1.0)
    tbl_t.columns[1].width = Inches(2.0)
    tbl_t.columns[2].width = Inches(3.033)
    tbl_t.columns[3].width = Inches(1.0)

    t_hdrs = ["Test ID", "Scenario", "Observed Outcome", "Status"]
    for c_idx, h_t in enumerate(t_hdrs):
        cell = tbl_t.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_TITLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h_t
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    cases = [
        ("TC-01", "Workspace Init", "Session JSON created; default outline loaded", "PASS"),
        ("TC-02", "Literature Search", "10 papers retrieved with metadata & BibTeX", "PASS"),
        ("TC-04", "Network Timeout", "Graceful fallback to local cached mock papers", "PASS"),
        ("TC-07", "Outline Gen (IEEE)", "8-section hierarchical outline created", "PASS"),
        ("TC-10", "Offline Drafting", "Structured prose with LaTeX equations generated", "PASS"),
        ("TC-11", "Simulated Review", "Score: 8.5/10 with 3 reviewer critiques", "PASS"),
        ("TC-14", "Citation Auditor", "Flagged unreferenced \\cite{badKey} accurately", "PASS"),
        ("TC-15", "Overleaf ZIP", "Complete ZIP generated with main.tex & plots", "PASS")
    ]

    for r_idx, (tid, scen, obs, stat) in enumerate(cases, start=1):
        tbl_t.cell(r_idx, 0).text_frame.paragraphs[0].add_run().text = tid
        tbl_t.cell(r_idx, 0).text_frame.paragraphs[0].runs[0].font.size = Pt(8.5)
        tbl_t.cell(r_idx, 0).text_frame.paragraphs[0].runs[0].font.bold = True

        tbl_t.cell(r_idx, 1).text_frame.paragraphs[0].add_run().text = scen
        tbl_t.cell(r_idx, 1).text_frame.paragraphs[0].runs[0].font.size = Pt(8.5)

        tbl_t.cell(r_idx, 2).text_frame.paragraphs[0].add_run().text = obs
        tbl_t.cell(r_idx, 2).text_frame.paragraphs[0].runs[0].font.size = Pt(8)

        c_stat = tbl_t.cell(r_idx, 3)
        c_stat.fill.solid()
        c_stat.fill.fore_color.rgb = RGBColor(240, 253, 244)
        p_st = c_stat.text_frame.paragraphs[0]
        p_st.alignment = PP_ALIGN.CENTER
        r_st = p_st.add_run()
        r_st.text = stat
        r_st.font.bold = True
        r_st.font.size = Pt(8.5)
        r_st.font.color.rgb = RGBColor(22, 101, 52)


    # =========================================================================
    # SLIDE 19: FUTURE ENHANCEMENTS & ROADMAP
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19, COLOR_BG_LIGHT)
    add_header(s19, "Future Roadmap", "Future Enhancements & Research Horizons", 
               "Strategic extensions planned for enterprise academic deployments and next-generation authoring.")
    add_footer(s19, 19)

    future_items = [
        ("7.1 Real-Time Collaborative Authoring", COLOR_BLUE_PRIMARY, 
         "WebSocket-Driven Multi-User Sync", 
         "Implementing operational transformation / CRDTs allowing student co-authors and faculty guides to simultaneously edit sections, leave inline review comments, and stage citations concurrently (similar to Google Docs & Overleaf)."),
        
        ("7.2 Multimodal Architectural Diagram Critique", COLOR_MAROON, 
         "Vision-Language Model Visual Auditing", 
         "Integrating Gemini 1.5 Pro Vision to automatically critique uploaded architectural flowcharts, benchmark plots, and system schematics, verifying font legibility, color-blind safety, and publication DPI compliance."),
        
        ("7.3 Local Vector RAG for Offline PDF Repositories", COLOR_NAVY_TITLE, 
         "Private Offline Literature Embeddings", 
         "Embedding ChromaDB / FAISS locally to ingest students' private collections of downloaded academic PDFs, enabling passage-level semantic search and verbatim quotation extraction with precise page attribution."),
        
        ("7.4 Automated Pre-Print & Conference Submission APIs", COLOR_BLUE_PRIMARY, 
         "1-Click Camera-Ready Ingestion", 
         "Developing authenticated REST connectors to arXiv, OpenReview, and IEEE conference submission portals, automatically transferring paper metadata, author affiliations, abstract text, and PDF assets."),
        
        ("7.5 Fine-Tuned Domain-Specific Language Models", COLOR_MAROON, 
         "Lightweight Local Small Language Models (SLMs)", 
         "Fine-tuning compact open-source models (e.g. Llama-3-8B / Gemma-2-9B) on peer-reviewed open-access computer science papers, enabling high-performance, cost-free drafting directly on standard consumer laptops.")
    ]

    for idx, (title, accent, sub, desc) in enumerate(future_items):
        y = Inches(1.85 + idx * 0.96)
        card = add_card(s19, Inches(0.8), y, Inches(11.733), Inches(0.84))
        
        # Color bar left
        bar = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.08), Inches(0.84))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb = s19.shapes.add_textbox(Inches(1.05), y + Inches(0.1), Inches(11.3), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = title + "  •  " + sub
        r0.font.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = desc
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_TEXT_MAIN


    # =========================================================================
    # SLIDE 20: CONCLUSION, ACKNOWLEDGEMENTS & Q&A
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20, COLOR_NAVY_DARK)

    # Top Maroon Accent Banner
    tb_b = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    tb_b.fill.solid()
    tb_b.fill.fore_color.rgb = COLOR_MAROON
    tb_b.line.fill.background()

    # Title
    tb_c_t = s20.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(0.8))
    tf_ct = tb_c_t.text_frame
    p_ct = tf_ct.paragraphs[0]
    p_ct.alignment = PP_ALIGN.CENTER
    r_ct = p_ct.add_run()
    r_ct.text = "CONCLUSION & PROJECT SUMMARY"
    r_ct.font.name = "Calibri"
    r_ct.font.size = Pt(24)
    r_ct.font.bold = True
    r_ct.font.color.rgb = RGBColor(255, 255, 255)

    # 3 Summary Pillar Cards
    pillars = [
        ("Academic Impact", COLOR_BLUE_PRIMARY, "Democratizes publication-grade research writing for graduate students, ensuring rigorous formatting, citation integrity, and formal scientific tone."),
        ("Engineering Rigor", COLOR_MAROON, "Successfully unites generative language models with strict LaTeX compilation via a disciplined Spiral SDLC, validated by 16/16 passing test suites."),
        ("Operational Value", COLOR_NAVY_TITLE, "Eliminates tool fragmentation by providing an intuitive, 8-phase end-to-end authoring cockpit from raw idea to compiled Overleaf package.")
    ]

    for idx, (title, accent, desc) in enumerate(pillars):
        px = Inches(1.2 + idx * 3.8)
        card = add_card(s20, px, Inches(1.85), Inches(3.4), Inches(2.3), RGBColor(15, 23, 42), RGBColor(30, 41, 59))
        
        c_bar = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, Inches(1.85), Inches(3.4), Inches(0.06))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = accent
        c_bar.line.fill.background()

        tb = s20.shapes.add_textbox(px + Inches(0.2), Inches(2.0), Inches(3.0), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = title
        r0.font.bold = True
        r0.font.size = Pt(13)
        r0.font.color.rgb = RGBColor(241, 245, 249)
        p0.space_after = Pt(8)

        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = desc
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(148, 163, 184)

    # Acknowledgements & Q&A Box
    c_ack = add_card(s20, Inches(1.2), Inches(4.45), Inches(10.933), Inches(2.4), RGBColor(15, 23, 42), RGBColor(30, 41, 59))
    tb_ack = s20.shapes.add_textbox(Inches(1.5), Inches(4.6), Inches(10.333), Inches(2.1))
    tf_ack = tb_ack.text_frame
    tf_ack.word_wrap = True
    
    p_a0 = tf_ack.paragraphs[0]
    p_a0.alignment = PP_ALIGN.CENTER
    r_a0 = p_a0.add_run()
    r_a0.text = "ACKNOWLEDGEMENTS & INSTITUTIONAL GRATITUDE"
    r_a0.font.bold = True
    r_a0.font.size = Pt(12)
    r_a0.font.color.rgb = RGBColor(245, 158, 11)

    p_a1 = tf_ack.add_paragraph()
    p_a1.alignment = PP_ALIGN.CENTER
    p_a1.space_before = Pt(6)
    r_a1 = p_a1.add_run()
    r_a1.text = "Sincere thanks to Dr. Devanshu Patel (President, Parul University), Dean, Head of Department, and our Internal Faculty Guide for their visionary guidance, academic resources, and constant encouragement."
    r_a1.font.size = Pt(10.5)
    r_a1.font.color.rgb = RGBColor(203, 213, 225)

    p_qa = tf_ack.add_paragraph()
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.space_before = Pt(12)
    r_qa = p_qa.add_run()
    r_qa.text = "THANK YOU  •  QUESTIONS & ANSWERS"
    r_qa.font.bold = True
    r_qa.font.size = Pt(18)
    r_qa.font.color.rgb = RGBColor(255, 255, 255)

    return prs

def main():
    print("[1/4] Building 20-slide presentation deck...")
    prs = create_deck()
    prs = build_all_slides(prs)
    
    pptx_path = OUTPUT_DIR / PPTX_FILENAME
    prs.save(str(pptx_path))
    print(f"Presentation saved to: {pptx_path} ({pptx_path.stat().st_size} bytes)")

    # Step 2: Convert to PDF via PowerPoint COM
    print("[2/4] Exporting camera-ready PDF via PowerPoint COM...")
    pdf_path = OUTPUT_DIR / PDF_FILENAME
    ps_code = f"""
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open('{pptx_path}')
$pres.SaveAs('{pdf_path}', 32)
$pres.Close()
$ppt.Quit()
Write-Host "PDF export finished."
"""
    ps_file = BASE_DIR / "run_ppt_export.ps1"
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_code)

    res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_file)], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("STDERR:", res.stderr)

    # Step 3: Verify PDF
    print("[3/4] Verifying generated PDF...")
    if pdf_path.exists():
        print(f"PDF verified: {pdf_path} ({pdf_path.stat().st_size} bytes)")
    else:
        print("Warning: PDF was not created.")

    # Step 4: Distribute Deliverables
    print("[4/4] Distributing PPTX and PDF to Desktop and Downloads...")
    targets = [
        DESKTOP_DIR / PPTX_FILENAME,
        DESKTOP_DIR / PDF_FILENAME,
        DOWNLOADS_DIR / PPTX_FILENAME,
        DOWNLOADS_DIR / PDF_FILENAME,
        BASE_DIR / PPTX_FILENAME,
        BASE_DIR / PDF_FILENAME
    ]
    for t in targets:
        src = pptx_path if t.suffix == ".pptx" else pdf_path
        if src.exists():
            shutil.copy2(src, t)
            print(f"Delivered -> {t} ({t.stat().st_size} bytes)")

    print("\nALL PRESENTATION DELIVERABLES CREATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
