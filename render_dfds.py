"""
Pristine, publication-grade DFD generator strictly following the reference image:
- DFD Level 0: Clean context diagram with generous spacing and ZERO text overlay.
- DFD Level 1: Small entity box at top-left, clean nested bus lines, 6 circular processes, 6 right data stores.
- DFD Level 2: Small entity box at top-left, nested bus lines, 6 sub-processes, 6 right data stores.
- DFD Level 3: Small entity box at top-left, nested bus lines, 6 atomic sub-processes, 6 right data stores.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = Path("outputs/report_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def draw_framed_canvas(figsize, title_text):
    """Draws outer border canvas matching the reference images."""
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(100, 0) if False else ax.set_ylim(0, 100)
    ax.axis("off")

    # Outer border box
    outer_box = patches.Rectangle((2.0, 2.0), 96.0, 96.0, ec="#000000", fc="#ffffff", lw=1.6, zorder=1)
    ax.add_patch(outer_box)

    # Title at top of frame
    ax.text(50, 95.2, title_text, fontsize=12.5, fontweight="bold", ha="center", va="center", color="#000000", zorder=10)
    return fig, ax


# ==============================================================================
# DFD LEVEL 0: CONTEXT LEVEL (ZERO OVERLAY, SUPER CLEAN)
# ==============================================================================
def create_dfd_level_0():
    fig, ax = draw_framed_canvas((11.5, 9.2), "Context Level DFD: 0 Level — AI Research Paper Assistant")

    # Center Process (Circle)
    cx, cy, r = 50.0, 50.0, 11.0
    circle = patches.Circle((cx, cy), r, ec="#000000", fc="#ffffff", lw=1.8, zorder=2)
    ax.add_patch(circle)
    ax.text(cx, cy + 3.2, "0.0", fontsize=11.5, fontweight="bold", ha="center", va="center", zorder=10)
    ax.text(cx, cy - 2.0, "AI Research Paper\nAssistant System", fontsize=9.2, fontweight="bold", ha="center", va="center", zorder=10)

    # 4 External Entities (Rectangles)
    # Top: Academic Researcher / Graduate Student
    top_x, top_y, top_w, top_h = 36.0, 80.0, 28.0, 11.5
    ax.add_patch(patches.Rectangle((top_x, top_y), top_w, top_h, ec="#000000", fc="#ffffff", lw=1.5, zorder=2))
    ax.text(top_x + top_w/2, top_y + top_h/2, "Academic Researcher\n/ Graduate Student", fontsize=9.2, fontweight="bold", ha="center", va="center", zorder=10)

    # Bottom: AI / LLM Cloud Services
    bot_x, bot_y, bot_w, bot_h = 36.0, 8.5, 28.0, 11.5
    ax.add_patch(patches.Rectangle((bot_x, bot_y), bot_w, bot_h, ec="#000000", fc="#ffffff", lw=1.5, zorder=2))
    ax.text(bot_x + bot_w/2, bot_y + bot_h/2, "AI / LLM Cloud Services\n(OpenAI & Google Gemini)", fontsize=9.2, fontweight="bold", ha="center", va="center", zorder=10)

    # Left: Scholarly APIs
    l_x, l_y, l_w, l_h = 3.5, 42.0, 19.5, 16.0
    ax.add_patch(patches.Rectangle((l_x, l_y), l_w, l_h, ec="#000000", fc="#ffffff", lw=1.5, zorder=2))
    ax.text(l_x + l_w/2, l_y + l_h/2, "Scholarly APIs\n(Semantic Scholar\n& ArXiv Service)", fontsize=8.6, fontweight="bold", ha="center", va="center", zorder=10)

    # Right: LaTeX Compiler & Packaging Service
    r_x, r_y, r_w, r_h = 77.0, 42.0, 19.5, 16.0
    ax.add_patch(patches.Rectangle((r_x, r_y), r_w, r_h, ec="#000000", fc="#ffffff", lw=1.5, zorder=2))
    ax.text(r_x + r_w/2, r_y + r_h/2, "LaTeX Packaging\n& Overleaf Service\n(Local / Cloud)", fontsize=8.6, fontweight="bold", ha="center", va="center", zorder=10)

    # ARROWS WITH AMPLE CLEARANCE AND NO COLLISION
    arrow_props = dict(arrowstyle="->", lw=1.2, color="#000000")

    # 1. Top to Center (User Input to System: x=44.5)
    ax.annotate("", xy=(44.5, cy + r), xytext=(44.5, top_y), arrowprops=arrow_props)
    ax.text(43.0, 70.5, "Search Queries, Lab Notes,\nOutline Directives & Config", fontsize=7.2, ha="right", va="center", zorder=10)

    # 2. Center to Top (System Output to User: x=55.5)
    ax.annotate("", xy=(55.5, top_y), xytext=(55.5, cy + r), arrowprops=arrow_props)
    ax.text(57.0, 70.5, "Assembled Manuscripts,\nPublication Plots & Reports", fontsize=7.2, ha="left", va="center", zorder=10)

    # 3. Center to Bottom (System to LLM: x=44.5)
    ax.annotate("", xy=(44.5, bot_y + bot_h), xytext=(44.5, cy - r), arrowprops=arrow_props)
    ax.text(43.0, 29.5, "Context-Enriched Prompts\n& Section Objectives", fontsize=7.2, ha="right", va="center", zorder=10)

    # 4. Bottom to Center (LLM to System: x=55.5)
    ax.annotate("", xy=(55.5, cy - r), xytext=(55.5, bot_y + bot_h), arrowprops=arrow_props)
    ax.text(57.0, 29.5, "Synthesized Section Drafts,\nMath Formulations & Reviews", fontsize=7.2, ha="left", va="center", zorder=10)

    # 5. Center to Left (System to Scholarly APIs: y=53.5)
    ax.annotate("", xy=(l_x + l_w, 53.5), xytext=(cx - r, 53.5), arrowprops=arrow_props)
    ax.text((l_x + l_w + cx - r)/2, 55.4, "Search Queries & Paper IDs", fontsize=6.8, ha="center", va="bottom", zorder=10)

    # 6. Left to Center (Scholarly APIs to System: y=46.5)
    ax.annotate("", xy=(cx - r, 46.5), xytext=(l_x + l_w, 46.5), arrowprops=arrow_props)
    ax.text((l_x + l_w + cx - r)/2, 44.6, "Paper Metadata & BibTeX Keys", fontsize=6.8, ha="center", va="top", zorder=10)

    # 7. Center to Right (System to LaTeX Service: y=53.5)
    ax.annotate("", xy=(r_x, 53.5), xytext=(cx + r, 53.5), arrowprops=arrow_props)
    ax.text((cx + r + r_x)/2, 55.4, "LaTeX Sources (.tex) & Figures", fontsize=6.8, ha="center", va="bottom", zorder=10)

    # 8. Right to Center (LaTeX Service to System: y=46.5)
    ax.annotate("", xy=(cx + r, 46.5), xytext=(r_x, 46.5), arrowprops=arrow_props)
    ax.text((cx + r + r_x)/2, 44.6, "Compiled PDF & Overleaf ZIP", fontsize=6.8, ha="center", va="top", zorder=10)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_0.png", bbox_inches="tight")
    plt.close(fig)
    print("DFD Level 0 created cleanly with zero text overlap!")


# ==============================================================================
# HELPER FOR LEVEL 1, 2, 3: REFERENCE BUS ARCHITECTURE
# ==============================================================================
def draw_bus_dfd(figsize, title_text, entity_label, procs, stores, flows_left, flows_right, filename):
    """
    Renders a DFD strictly following the reference image layout:
    - Small entity box at top-left, vertically aligned with Process 1.0
    - Non-intersecting nested vertical bus lines dropping down
    - 6 circular processes in the center
    - 6 data stores on the right
    - Clean horizontal arrows with perfectly legible labels
    """
    fig, ax = draw_framed_canvas(figsize, title_text)

    # Number of processes
    n = len(procs)
    # y positions for 6 processes, evenly spaced
    y_positions = [80.0, 66.5, 53.0, 39.5, 26.0, 12.5]

    # Small Entity Box at Top Left (Vertically aligned with Process 1.0)
    ent_x = 4.0
    ent_w = 14.0
    ent_y = 75.5
    ent_h = 9.0
    ax.add_patch(patches.Rectangle((ent_x, ent_y), ent_w, ent_h, ec="#000000", fc="#ffffff", lw=1.5, zorder=3))
    ax.text(ent_x + ent_w/2, ent_y + ent_h/2, entity_label, fontsize=8.0, fontweight="bold", ha="center", va="center", color="#000000", zorder=10)

    # Central Circular Processes
    proc_cx = 48.0
    proc_r = 5.6
    for i, (p_num, p_name) in enumerate(procs):
        cy = y_positions[i]
        c = patches.Circle((proc_cx, cy), proc_r, ec="#000000", fc="#ffffff", lw=1.5, zorder=3)
        ax.add_patch(c)
        ax.text(proc_cx, cy + 1.9, p_num, fontsize=9.2, fontweight="bold", ha="center", va="center", zorder=10)
        ax.text(proc_cx, cy - 1.3, p_name, fontsize=6.8, fontweight="bold", ha="center", va="center", zorder=10)

    # Right Data Stores (D1 to D6)
    ds_x = 73.0
    ds_w = 23.5
    ds_h = 5.6
    for i, (d_id, d_name) in enumerate(stores):
        cy = y_positions[i]
        # Data store open box (top and bottom horizontal lines, vertical divider, left vertical line)
        ax.plot([ds_x, ds_x + ds_w], [cy - ds_h/2, cy - ds_h/2], color="#000000", lw=1.3, zorder=3)
        ax.plot([ds_x, ds_x + ds_w], [cy + ds_h/2, cy + ds_h/2], color="#000000", lw=1.3, zorder=3)
        ax.plot([ds_x, ds_x], [cy - ds_h/2, cy + ds_h/2], color="#000000", lw=1.3, zorder=3)
        ax.plot([ds_x + 4.5, ds_x + 4.5], [cy - ds_h/2, cy + ds_h/2], color="#000000", lw=1.3, zorder=3)
        # Text
        ax.text(ds_x + 2.25, cy, d_id, fontsize=8.0, fontweight="bold", ha="center", va="center", zorder=10)
        ax.text(ds_x + 4.5 + (ds_w - 4.5)/2, cy, d_name, fontsize=7.2, fontweight="bold", ha="center", va="center", zorder=10)

    # RIGHT FLOWS: Process <-> Data Store
    arrow_props_r = dict(arrowstyle="->", lw=1.1, color="#000000")
    for i, (f_save, f_read) in enumerate(flows_right):
        cy = y_positions[i]
        # Process -> Data Store (Top arrow)
        y_top = cy + 1.4
        ax.annotate("", xy=(ds_x, y_top), xytext=(proc_cx + proc_r, y_top), arrowprops=arrow_props_r)
        ax.text((proc_cx + proc_r + ds_x)/2, y_top + 1.1, f_save, fontsize=6.6, ha="center", va="bottom", zorder=10)

        # Data Store -> Process (Bottom arrow)
        y_bot = cy - 1.4
        ax.annotate("", xy=(proc_cx + proc_r, y_bot), xytext=(ds_x, y_bot), arrowprops=arrow_props_r)
        ax.text((proc_cx + proc_r + ds_x)/2, y_bot - 1.1, f_read, fontsize=6.6, ha="center", va="top", zorder=10)

    # LEFT FLOWS WITH REFERENCE NESTED BUS ARCHITECTURE
    # Process 1.0 (Direct horizontal arrows straight to/from entity box right edge)
    y1 = y_positions[0]
    ax.annotate("", xy=(proc_cx - proc_r, y1 + 1.4), xytext=(ent_x + ent_w, y1 + 1.4), arrowprops=arrow_props_r)
    ax.text((ent_x + ent_w + proc_cx - proc_r)/2, y1 + 2.4, flows_left[0][0], fontsize=6.6, ha="center", va="bottom", zorder=10)

    ax.annotate("", xy=(ent_x + ent_w, y1 - 1.4), xytext=(proc_cx - proc_r, y1 - 1.4), arrowprops=arrow_props_r)
    ax.text((ent_x + ent_w + proc_cx - proc_r)/2, y1 - 2.4, flows_left[0][1], fontsize=6.6, ha="center", va="top", zorder=10)

    # Processes 2.0 to 6.0: Nested vertical bus lines
    # To guarantee ZERO intersections:
    # Process 2.0 (highest) gets the rightmost pair of bus lines.
    # Process 6.0 (lowest) gets the leftmost pair of bus lines.
    # Each pair has:
    # - Line 2 (right): input at cy + 1.4 (turns right at y_top)
    # - Line 1 (left): output at cy - 1.4 (turns left at y_bot, turns up to entity)
    # Because Line 2 stops above at cy + 1.4, Line 1 at cy - 1.4 never crosses Line 2!
    # And because higher processes use rightward lines and stop earlier, lower processes never cross higher processes!
    x_start = 5.8
    delta_proc = 2.4
    delta_line = 1.0

    for i in range(1, n):
        cy = y_positions[i]
        f_in, f_out = flows_left[i]

        k = (n - 1) - i  # for i=1 (2.0): k=4 (rightmost); for i=5 (6.0): k=0 (leftmost)
        bx_bot = x_start + k * delta_proc          # Line 1 (left of pair, for bottom output)
        bx_top = bx_bot + delta_line               # Line 2 (right of pair, for top input)

        # 1. Input Line (Entity bottom -> down bx_top -> right to Process at cy + 1.4)
        ax.plot([bx_top, bx_top], [ent_y, cy + 1.4], color="#000000", lw=1.1, zorder=2)
        ax.annotate("", xy=(proc_cx - proc_r, cy + 1.4), xytext=(bx_top, cy + 1.4), arrowprops=arrow_props_r)
        ax.text((bx_top + proc_cx - proc_r)/2, cy + 2.4, f_in, fontsize=6.6, ha="center", va="bottom", zorder=10)

        # 2. Output Line (Process at cy - 1.4 -> left to bx_bot -> up to Entity bottom)
        ax.plot([bx_bot, bx_bot], [cy - 1.4, ent_y], color="#000000", lw=1.1, zorder=2)
        ax.annotate("", xy=(bx_bot, cy - 1.4), xytext=(proc_cx - proc_r, cy - 1.4), arrowprops=arrow_props_r)
        ax.text((bx_bot + proc_cx - proc_r)/2, cy - 2.4, f_out, fontsize=6.6, ha="center", va="top", zorder=10)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, bbox_inches="tight")
    plt.close(fig)
    print(f"{filename} generated successfully with reference bus layout!")


# ==============================================================================
# DFD LEVEL 1: MAJOR SYSTEM PROCESSES
# ==============================================================================
def create_dfd_level_1():
    procs = [
        ("1.0", "Authenticate &\nSearch Literature"),
        ("2.0", "Ingest Notes &\nExtract Insights"),
        ("3.0", "Plan Paper\nOutline & Hierarchy"),
        ("4.0", "Draft Sections &\nRelated Work"),
        ("5.0", "Polish Tone &\nPeer Review"),
        ("6.0", "Render Plots &\nCompile LaTeX")
    ]
    stores = [
        ("D1", "User & Auth Store"),
        ("D2", "Literature & BibTeX Store"),
        ("D3", "Research Notes & Gap Store"),
        ("D4", "Outline & Targets Store"),
        ("D5", "Manuscript Drafts Store"),
        ("D6", "LaTeX Packages & Reports")
    ]
    flows_left = [
        ("Search Queries / Keywords", "Papers List & BibTeX"),
        ("Lab Notes & Hypotheses", "Extracted Problem & Gap"),
        ("Conference Template Choice", "Hierarchical Outline Nodes"),
        ("Section Writing Directives", "Section Drafts (Math/Algos)"),
        ("Academic Refinement Request", "3-Reviewer Scores & Critiques"),
        ("Plot Config & Build Request", "Overleaf ZIP Bundle & PDF")
    ]
    flows_right = [
        ("Validate Auth", "Query User Session"),
        ("Save Paper Metadata", "Fetch BibTeX Keys"),
        ("Save Research Gaps", "Read Context Notes"),
        ("Save Outline Nodes", "Read Section Goals"),
        ("Save Refined Drafts", "Read Prior Sections"),
        ("Save Package & PDF", "Read .tex & Plots")
    ]
    draw_bus_dfd((12.0, 10.0), "AI Research Paper Assistant — Level 1 DFD",
                 "Academic\nResearcher /\nAuthor",
                 procs, stores, flows_left, flows_right, "dfd_level_1.png")


# ==============================================================================
# DFD LEVEL 2: DRAFTING, REFINEMENT & PACKAGING ENGINE
# ==============================================================================
def create_dfd_level_2():
    procs = [
        ("4.1", "Prompt Context\nAssembler"),
        ("4.2", "Multi-Provider\nLLM Dispatcher"),
        ("4.3", "Math, Equation &\nAlgo Formatter"),
        ("4.4", "Academic Tone\nPolisher"),
        ("4.5", "Citation & Fact\nAuditor"),
        ("4.6", "LaTeX Assembler\n& Packager")
    ]
    stores = [
        ("D1", "Literature & BibTeX Store"),
        ("D2", "Research Materials & Notes"),
        ("D3", "Outline & Targets Store"),
        ("D4", "Manuscript Drafts Store"),
        ("D5", "Peer Review Store"),
        ("D6", "Overleaf ZIP Store")
    ]
    flows_left = [
        ("Section Writing Trigger", "Assembled Context Status"),
        ("Provider Selection (Gemini/OpenAI)", "LLM Stream Status"),
        ("Equation & Algo Toggles", "Formatted LaTeX Blocks"),
        ("Academic Polish Directives", "Polished Text Diff"),
        ("Run Peer Review Simulation", "Reviewer Ratings (1-10)"),
        ("Build Overleaf ZIP Request", "Downloadable ZIP Archive")
    ]
    flows_right = [
        ("Read Active BibTeX Keys", "Extract Citation Tags"),
        ("Read Lab Notes & Gap", "Query Context Prompts"),
        ("Read Section Objectives", "Target Word Counts"),
        ("Save Draft Revisions", "Retrieve Current Text"),
        ("Audit Citation Grounding", "Log Reviewer Feedback"),
        ("Assemble main.tex & figures", "Deliver Complete ZIP")
    ]
    draw_bus_dfd((12.0, 10.0), "DFD Level 2 — Drafting, Refinement & LaTeX Packaging Engine",
                 "Academic\nResearcher /\nAuthor",
                 procs, stores, flows_left, flows_right, "dfd_level_2.png")


# ==============================================================================
# DFD LEVEL 3: DETAILED EXECUTION & VERIFICATION WORKFLOW
# ==============================================================================
def create_dfd_level_3():
    procs = [
        ("4.3.1", "Parse Math Notation\n& Variables"),
        ("4.3.2", "Formulate State-Space\nEquations"),
        ("4.3.3", "Synthesize Triton\nAlgo Blocks"),
        ("4.3.4", "Construct Booktabs\nResults Tables"),
        ("4.3.5", "Cross-Reference\nBibTeX Keys"),
        ("4.3.6", "Validate LaTeX\nSyntax & Compile")
    ]
    stores = [
        ("D1", "Math Symbols DB"),
        ("D2", "SSM State Parameters"),
        ("D3", "Algorithmic Blocks DB"),
        ("D4", "Benchmark Results DB"),
        ("D5", "BibTeX References DB"),
        ("D6", "Compiler Logs & Artifacts")
    ]
    flows_left = [
        ("Notation Parameters", "Validated Symbol Table"),
        ("Discretization Step Size", "Continuous SSM Matrix"),
        ("Triton Scan Kernel Directives", "Pseudocode Algorithm Block"),
        ("Benchmark Accuracy & Latency", "Booktabs LaTeX Table"),
        ("Claim & Reference Audit Request", "Verified Citation Mapping"),
        ("Execute Local PDF Test", "Compilation Log & Errors")
    ]
    flows_right = [
        ("Save Symbol Map", "Read Active Tokens"),
        ("Store Discretized A, B", "Query Step Sizes"),
        ("Save Kernel Algorithm", "Read SRAM Hierarchy"),
        ("Save Results Table", "Read Baseline Scores"),
        ("Cross-Verify Keys", "Flag Missing Citations"),
        ("Log Output Artifacts", "Read main.pdf Status")
    ]
    draw_bus_dfd((12.0, 10.0), "DFD Level 3 — Tool Execution & LaTeX Code Verification Workflow",
                 "Academic\nResearcher /\nAuthor",
                 procs, stores, flows_left, flows_right, "dfd_level_3.png")


if __name__ == "__main__":
    create_dfd_level_0()
    create_dfd_level_1()
    create_dfd_level_2()
    create_dfd_level_3()
    print("All DFD Levels (0, 1, 2, and 3) successfully created!")
