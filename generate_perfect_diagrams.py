"""
Generates high-resolution system design diagrams matching the exact visual style,
layout, framing, and typography of the reference Parul University report:
1. New Use Case Diagram (with actors, boundary, include/extend relationships)
2. Context Level DFD (Level 0)
3. Level 1 DFD (with left entity bus, 6 circular processes, 6 right data stores)
4. Level 2 DFD (with left entity bus, 6 sub-processes, 6 right data stores)
5. UML Class Diagram
6. UML Activity Diagram (with decision diamonds and workflow loops)
7. UML Sequence Diagram (with lifelines and numbered messages)
8. Entity Relationship Diagram (Chen notation with entity boxes, relationship diamonds, attribute ovals)
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = Path("outputs/report_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def draw_framed_canvas(figsize, title_text, fig_caption=""):
    """Creates a canvas with the clean black outer border box seen in the reference report."""
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Outer border box
    outer_box = patches.Rectangle((2, 2), 96, 96, ec="#000000", fc="#ffffff", lw=1.6, zorder=1)
    ax.add_patch(outer_box)

    # Title at top of frame
    if title_text:
        ax.text(50, 94, title_text, fontsize=12.5, fontweight="bold", ha="center", va="center", color="#000000")

    return fig, ax


# ==============================================================================
# 1. NEW USE CASE DIAGRAM
# ==============================================================================
def create_new_use_case_diagram():
    fig, ax = plt.subplots(figsize=(11, 9.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Outer frame
    frame = patches.Rectangle((2, 2), 96, 96, ec="#000000", fc="#ffffff", lw=1.6)
    ax.add_patch(frame)
    ax.text(50, 94.5, "UML Use Case Diagram — AI Research Paper Assistant", fontsize=12.5, fontweight="bold", ha="center")

    # System boundary box
    sys_box = patches.Rectangle((24, 6), 52, 84, ec="#1e3a8a", fc="#f8fafc", lw=1.8, linestyle="--")
    ax.add_patch(sys_box)
    ax.text(50, 87.5, "System Boundary: AI Research Paper Assistant", fontsize=10, fontweight="bold", ha="center", color="#1e3a8a")

    # Actor Left 1: Researcher / Student
    def draw_actor(x, y, label, role="Actor"):
        # Head
        head = patches.Circle((x, y+3.5), 1.8, ec="#000000", fc="#ffffff", lw=1.5)
        ax.add_patch(head)
        # Body
        ax.plot([x, x], [y+1.7, y-2.5], color="#000000", lw=1.8)
        # Arms
        ax.plot([x-2.5, x+2.5], [y, y], color="#000000", lw=1.8)
        # Legs
        ax.plot([x, x-2.0], [y-2.5, y-6.0], color="#000000", lw=1.8)
        ax.plot([x, x+2.0], [y-2.5, y-6.0], color="#000000", lw=1.8)
        # Label
        ax.text(x, y-8.5, label, fontsize=8.5, fontweight="bold", ha="center", va="top")

    draw_actor(11, 62, "Academic Researcher\n/ Student")
    draw_actor(11, 26, "Faculty Guide\n/ Reviewer")

    # External Actor Right: Scholarly & AI APIs
    ext_box = patches.Rectangle((80, 44), 16, 12, ec="#059669", fc="#f0fdf4", lw=1.6)
    ax.add_patch(ext_box)
    ax.text(88, 52, "EXTERNAL SERVICE", fontsize=7, fontweight="bold", ha="center", color="#059669")
    ax.text(88, 47.5, "Semantic Scholar\n& LLM APIs\n(Gemini / OpenAI)", fontsize=8, fontweight="bold", ha="center", va="center")

    # Use Cases (Ovals) inside boundary
    use_cases = [
        ("UC-01: Search & Filter Literature", 50, 81),
        ("UC-02: Curate Material & Lab Notes", 50, 73),
        ("UC-03: Extract Problem & Novel Gap", 50, 65),
        ("UC-04: Plan Conference Outline", 50, 57),
        ("UC-05: Synthesize Related Work Matrix", 50, 49),
        ("UC-06: Draft Manuscript Sections", 50, 41),
        ("UC-07: Polish Tone & Peer Review", 50, 33),
        ("UC-08: Audit Citations & Claims", 50, 25),
        ("UC-09: Render Publication Plots", 50, 17),
        ("UC-10: Compile LaTeX & Overleaf ZIP", 50, 9)
    ]

    for label, cx, cy in use_cases:
        oval = patches.FancyBboxPatch((cx-19, cy-2.6), 38, 5.2, boxstyle="round,pad=0.2", ec="#1e40af", fc="#ffffff", lw=1.4)
        ax.add_patch(oval)
        ax.text(cx, cy, label, fontsize=8.2, fontweight="bold", ha="center", va="center", color="#0f172a")

    # Association lines: Researcher to Use Cases
    for i in [81, 73, 65, 57, 49, 41, 33, 25, 17, 9]:
        ax.plot([14.5, 31], [62, i], color="#475569", lw=1.2)

    # Association lines: Faculty to Peer Review & Audit
    ax.plot([14.5, 31], [26, 33], color="#475569", lw=1.2)
    ax.plot([14.5, 31], [26, 25], color="#475569", lw=1.2)
    ax.plot([14.5, 31], [26, 9], color="#475569", lw=1.2)

    # Associations to External APIs
    ax.plot([69, 80], [81, 52], color="#059669", lw=1.2, linestyle="--")
    ax.plot([69, 80], [65, 50], color="#059669", lw=1.2, linestyle="--")
    ax.plot([69, 80], [41, 48], color="#059669", lw=1.2, linestyle="--")
    ax.plot([69, 80], [33, 46], color="#059669", lw=1.2, linestyle="--")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "new_use_case_diagram.png", bbox_inches="tight")
    plt.close(fig)
    print("New Use Case Diagram generated successfully!")


# ==============================================================================
# 2. CONTEXT LEVEL DFD (LEVEL 0) — Matching 6.jpeg
# ==============================================================================
def create_dfd_level_0():
    fig, ax = draw_framed_canvas((11, 8.5), "Context Level DFD: 0 Level — AI Research Paper Assistant")

    # 4 External Entities around center process
    # Top: Academic Researcher / Student
    top_box = patches.Rectangle((37, 76), 26, 12, ec="#000000", fc="#ffffff", lw=1.5)
    ax.add_patch(top_box)
    ax.text(50, 82, "Academic Researcher\n/ Graduate Student", fontsize=9.5, fontweight="bold", ha="center", va="center")

    # Bottom: Generative AI Services (OpenAI & Gemini)
    bot_box = patches.Rectangle((37, 8), 26, 12, ec="#000000", fc="#ffffff", lw=1.5)
    ax.add_patch(bot_box)
    ax.text(50, 14, "AI / LLM Services\n(OpenAI & Google Gemini)", fontsize=9.5, fontweight="bold", ha="center", va="center")

    # Left: Scholarly Digital Libraries (Semantic Scholar & ArXiv)
    left_box = patches.Rectangle((5, 41), 22, 14, ec="#000000", fc="#ffffff", lw=1.5)
    ax.add_patch(left_box)
    ax.text(16, 48, "Scholarly APIs\n(Semantic Scholar\n& ArXiv Service)", fontsize=9, fontweight="bold", ha="center", va="center")

    # Right: LaTeX & Publication Compiler Service
    right_box = patches.Rectangle((73, 41), 22, 14, ec="#000000", fc="#ffffff", lw=1.5)
    ax.add_patch(right_box)
    ax.text(84, 48, "LaTeX Packaging\n& Overleaf Compiler\nService", fontsize=9, fontweight="bold", ha="center", va="center")

    # Center Process (Circle)
    center_circle = patches.Circle((50, 48), 12, ec="#000000", fc="#ffffff", lw=2)
    ax.add_patch(center_circle)
    ax.text(50, 52.5, "0.0", fontsize=11, fontweight="bold", ha="center")
    ax.text(50, 47, "AI Research Paper\nAssistant System", fontsize=9.5, fontweight="bold", ha="center", va="center")

    # Arrows & Data Flows
    # Top <-> Center
    ax.annotate("", xy=(46, 60), xytext=(46, 76), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(44.5, 68, "FROM\nSearch Queries,\nLab Notes & Config", fontsize=7.5, ha="right", va="center")

    ax.annotate("", xy=(54, 76), xytext=(54, 60), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(55.5, 68, "FROM\nAssembled Manuscript,\nCharts & Diagnostic Score", fontsize=7.5, ha="left", va="center")

    # Bottom <-> Center
    ax.annotate("", xy=(46, 20), xytext=(46, 36), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(44.5, 28, "FROM\nContext Prompts &\nSection Guidelines", fontsize=7.5, ha="right", va="center")

    ax.annotate("", xy=(54, 36), xytext=(54, 20), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(55.5, 28, "FROM\nSynthesized Drafts,\nEquations & Reviews", fontsize=7.5, ha="left", va="center")

    # Left <-> Center
    ax.annotate("", xy=(27, 51), xytext=(38, 51), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(32.5, 54, "FROM REST Search Request", fontsize=7.5, ha="center")

    ax.annotate("", xy=(38, 45), xytext=(27, 45), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(32.5, 42, "FROM Papers, Abstracts & BibTeX", fontsize=7.5, ha="center")

    # Right <-> Center
    ax.annotate("", xy=(73, 51), xytext=(62, 51), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(67.5, 54, "FROM Main.tex & Figure Assets", fontsize=7.5, ha="center")

    ax.annotate("", xy=(62, 45), xytext=(73, 45), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(67.5, 42, "FROM Overleaf ZIP & Compiled PDF", fontsize=7.5, ha="center")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_0.png", bbox_inches="tight")
    plt.close(fig)
    print("DFD Level 0 created successfully!")


# ==============================================================================
# 3. LEVEL 1 DFD — Matching 5.jpeg
# ==============================================================================
def create_dfd_level_1():
    fig, ax = draw_framed_canvas((11.5, 9.5), "AI Research Paper Assistant — Level 1 DFD")

    # Left: Academic Researcher Entity
    ent_left = patches.Rectangle((5, 12), 12, 74, ec="#000000", fc="#ffffff", lw=1.5)
    ax.add_patch(ent_left)
    ax.text(11, 49, "Academic\nResearcher /\nAuthor", fontsize=9.5, fontweight="bold", ha="center", va="center")

    # 6 Central Circular Processes
    procs = [
        ("1.0", "Search & Discover\nLiterature", 78),
        ("2.0", "Ingest Notes &\nExtract Insights", 65),
        ("3.0", "Plan Paper\nOutline & Hierarchy", 52),
        ("4.0", "Draft Sections &\nLiterature Review", 39),
        ("5.0", "Polish Tone &\nPeer Review", 26),
        ("6.0", "Render Plots &\nCompile LaTeX ZIP", 13)
    ]

    for num, name, y in procs:
        c = patches.Circle((48, y), 5.5, ec="#000000", fc="#ffffff", lw=1.6)
        ax.add_patch(c)
        ax.text(48, y+1.8, num, fontsize=9.5, fontweight="bold", ha="center")
        ax.text(48, y-1.2, name, fontsize=7.6, fontweight="bold", ha="center", va="center")

    # 6 Right Data Stores: D1 to D6
    stores = [
        ("D1", "Literature & BibTeX Store", 78),
        ("D2", "Research Materials & Notes", 65),
        ("D3", "Outline & Targets Store", 52),
        ("D4", "Manuscript Drafts Store", 39),
        ("D5", "Visual Assets Store", 26),
        ("D6", "LaTeX Packages Store", 13)
    ]

    for did, dname, y in stores:
        # Standard DFD Data store (open rectangle)
        ax.plot([72, 94], [y-3.2, y-3.2], color="#000000", lw=1.4)
        ax.plot([72, 94], [y+3.2, y+3.2], color="#000000", lw=1.4)
        ax.plot([78, 78], [y-3.2, y+3.2], color="#000000", lw=1.4)
        ax.text(75, y, did, fontsize=8.5, fontweight="bold", ha="center", va="center")
        ax.text(86, y, dname, fontsize=7.6, fontweight="bold", ha="center", va="center")

    # Arrows: Entity to Processes (Left side)
    flows_left = [
        (78, "Search Keywords", "Papers List & BibTeX"),
        (65, "Lab Notes & Hypotheses", "Problem & Novel Gap"),
        (52, "Conference Template", "Outline Sections"),
        (39, "Section Directives", "Section Drafts (Math/Algos)"),
        (26, "Refinement Request", "3-Reviewer Scores & Audit"),
        (13, "Plot Parameters", "Overleaf ZIP Bundle & PDF")
    ]

    for y, f_in, f_out in flows_left:
        # Forward arrow
        ax.annotate("", xy=(42.5, y+1.4), xytext=(17, y+1.4), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(30, y+2.6, f_in, fontsize=7.2, ha="center")
        # Return arrow
        ax.annotate("", xy=(17, y-1.4), xytext=(42.5, y-1.4), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(30, y-3.0, f_out, fontsize=7.2, ha="center")

    # Arrows: Processes to Data Stores (Right side)
    flows_right = [
        (78, "Save Paper Metadata", "Query Citations"),
        (65, "Save Formulated Gap", "Fetch Context"),
        (52, "Save Outline Nodes", "Read Section Goals"),
        (39, "Save Validated Drafts", "Read Prior Sections"),
        (26, "Log Reviewer Scores", "Check Citation Keys"),
        (13, "Save Final Package", "Read .tex & Figures")
    ]

    for y, f_save, f_read in flows_right:
        # Process -> Store
        ax.annotate("", xy=(72, y+1.3), xytext=(53.5, y+1.3), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(62.8, y+2.4, f_save, fontsize=7.2, ha="center")
        # Store -> Process
        ax.annotate("", xy=(53.5, y-1.3), xytext=(72, y-1.3), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(62.8, y-2.8, f_read, fontsize=7.2, ha="center")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_1.png", bbox_inches="tight")
    plt.close(fig)
    print("DFD Level 1 created successfully!")


# ==============================================================================
# 4. LEVEL 2 DFD — Matching 4.jpeg
# ==============================================================================
def create_dfd_level_2():
    fig, ax = draw_framed_canvas((11.5, 9.5), "DFD Level 2 — Drafting, Refinement & LaTeX Packaging Engine")

    # Left Entity: Academic Researcher
    ent_left = patches.Rectangle((5, 12), 12, 74, ec="#000000", fc="#ffffff", lw=1.5)
    ax.add_patch(ent_left)
    ax.text(11, 49, "Academic\nResearcher /\nAuthor", fontsize=9.5, fontweight="bold", ha="center", va="center")

    # 6 Central Circular Sub-Processes
    subprocs = [
        ("4.1", "Prompt Context\nAssembler", 78),
        ("4.2", "Multi-Provider\nLLM Dispatcher", 65),
        ("4.3", "Math, Equation &\nAlgo Formatter", 52),
        ("4.4", "Academic Tone\nPolisher", 39),
        ("4.5", "Citation & Fact\nAuditor", 26),
        ("4.6", "LaTeX Assembler\n& Packager", 13)
    ]

    for num, name, y in subprocs:
        c = patches.Circle((48, y), 5.5, ec="#000000", fc="#ffffff", lw=1.6)
        ax.add_patch(c)
        ax.text(48, y+1.8, num, fontsize=9.5, fontweight="bold", ha="center")
        ax.text(48, y-1.2, name, fontsize=7.6, fontweight="bold", ha="center", va="center")

    # 6 Right Data Stores
    stores2 = [
        ("D1", "Literature & BibTeX Store", 78),
        ("D2", "Research Materials & Notes", 65),
        ("D3", "Outline & Targets Store", 52),
        ("D4", "Manuscript Drafts Store", 39),
        ("D5", "Peer Review Store", 26),
        ("D6", "Overleaf ZIP Store", 13)
    ]

    for did, dname, y in stores2:
        ax.plot([72, 94], [y-3.2, y-3.2], color="#000000", lw=1.4)
        ax.plot([72, 94], [y+3.2, y+3.2], color="#000000", lw=1.4)
        ax.plot([78, 78], [y-3.2, y+3.2], color="#000000", lw=1.4)
        ax.text(75, y, did, fontsize=8.5, fontweight="bold", ha="center", va="center")
        ax.text(86, y, dname, fontsize=7.6, fontweight="bold", ha="center", va="center")

    # Left Flows (Entity <-> Sub-processes)
    flows_left2 = [
        (78, "Section Writing Trigger", "Assembled Context Status"),
        (65, "Provider Selection (Gemini/OpenAI)", "LLM Stream Status"),
        (52, "Equation/Algo Toggles", "Formatted LaTeX Blocks"),
        (39, "Academic Polish Focus", "Polished Text Diff"),
        (26, "Run Peer Review Simulation", "Reviewer Ratings (1-10)"),
        (13, "Build Overleaf ZIP Request", "Downloadable ZIP Archive")
    ]

    for y, f_in, f_out in flows_left2:
        ax.annotate("", xy=(42.5, y+1.4), xytext=(17, y+1.4), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(30, y+2.6, f_in, fontsize=7.2, ha="center")
        ax.annotate("", xy=(17, y-1.4), xytext=(42.5, y-1.4), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(30, y-3.0, f_out, fontsize=7.2, ha="center")

    # Right Flows (Sub-processes <-> Data stores)
    flows_right2 = [
        (78, "Read Active BibTeX Keys", "Extract Citation Tags"),
        (65, "Read Lab Notes & Gap", "Query Context Prompts"),
        (52, "Read Section Objectives", "Target Word Counts"),
        (39, "Save Draft Revisions", "Retrieve Current Text"),
        (26, "Audit Citation Grounding", "Log Reviewer Feedback"),
        (13, "Assemble main.tex & figures", "Deliver Complete ZIP")
    ]

    for y, f_save, f_read in flows_right2:
        ax.annotate("", xy=(72, y+1.3), xytext=(53.5, y+1.3), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(62.8, y+2.4, f_save, fontsize=7.2, ha="center")
        ax.annotate("", xy=(53.5, y-1.3), xytext=(72, y-1.3), arrowprops=dict(arrowstyle="->", lw=1.2))
        ax.text(62.8, y-2.8, f_read, fontsize=7.2, ha="center")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_2.png", bbox_inches="tight")
    plt.close(fig)
    print("DFD Level 2 created successfully!")


# ==============================================================================
# 5. UML CLASS DIAGRAM — Matching 3.jpeg
# ==============================================================================
def create_uml_class_diagram():
    fig, ax = draw_framed_canvas((11.5, 9.5), "UML Class Diagram — Core Domain Architecture")

    def draw_class_box(x, y, w, h, name, attrs, methods):
        box = patches.Rectangle((x, y), w, h, ec="#000000", fc="#ffffff", lw=1.4)
        ax.add_patch(box)
        # Title separator
        ax.plot([x, x+w], [y+h-3.2, y+h-3.2], color="#000000", lw=1.2)
        ax.text(x+w/2, y+h-1.6, name, fontsize=8.8, fontweight="bold", ha="center", va="center")
        # Attributes
        sep_y = y+h-3.2
        for i, a in enumerate(attrs):
            ax.text(x+1.0, sep_y-1.6-i*2.2, a, fontsize=7.2, va="center")
        # Method separator
        meth_sep = sep_y - 2.2*len(attrs) - 1.0
        ax.plot([x, x+w], [meth_sep, meth_sep], color="#000000", lw=1.2)
        for j, m in enumerate(methods):
            ax.text(x+1.0, meth_sep-1.6-j*2.2, m, fontsize=7.2, va="center")

    # Base & Controller Classes
    draw_class_box(6, 68, 26, 22, "BaseAgent",
                   ["- agent_id: String", "- role: String", "- status: State"],
                   ["+ initialize()", "+ execute(task)", "+ report_status()"])

    draw_class_box(37, 68, 28, 22, "ResearchController",
                   ["- active_project: ProjectState", "- current_venue: String"],
                   ["+ run_pipeline()", "+ set_stage(stage_id)", "+ log_milestone()"])

    draw_class_box(70, 68, 24, 22, "PolicyGateway",
                   ["- academic_rules: List", "- venue_spec: Dict"],
                   ["+ validate_format()", "+ evaluate_compliance()"])

    # Engine Classes (Middle Row)
    draw_class_box(6, 36, 26, 24, "LiteratureEngine",
                   ["- s2_endpoint: String", "- cache: List<Paper>", "- api_key: String"],
                   ["+ search_semantic_scholar()", "+ search_arxiv()", "+ paper_to_bibtex()", "+ clean_bibtex_key()"])

    draw_class_box(37, 36, 28, 24, "LLMProvider",
                   ["- openai_key: String", "- gemini_key: String", "- offline_engine: Object"],
                   ["+ generate(prompt, context)", "+ call_gemini(model)", "+ call_openai(model)", "+ _generate_offline()"])

    draw_class_box(70, 36, 24, 24, "PlottingStudio",
                   ["- templates: Dict", "- output_dir: Path", "- dpi: Integer = 300"],
                   ["+ execute_plot_code()", "+ export_highres_png()", "+ generate_latex_snippet()"])

    # Bottom Classes
    draw_class_box(20, 6, 28, 22, "LaTeXCompiler",
                   ["- template_name: String", "- custom_preamble: Text"],
                   ["+ render_manuscript()", "+ create_overleaf_zip()", "+ attempt_local_compile()"])

    draw_class_box(54, 6, 28, 22, "RefinementEngine",
                   ["- peer_reviewers: List", "- bibtex_db: Dict"],
                   ["+ polish_tone()", "+ simulate_3_reviewers()", "+ audit_citations_claims()"])

    # Associations
    ax.annotate("", xy=(32, 79), xytext=(37, 79), arrowprops=dict(arrowstyle="<->", lw=1.2))
    ax.annotate("", xy=(65, 79), xytext=(70, 79), arrowprops=dict(arrowstyle="<->", lw=1.2))

    ax.annotate("", xy=(19, 60), xytext=(19, 68), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.annotate("", xy=(51, 60), xytext=(51, 68), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.annotate("", xy=(82, 60), xytext=(82, 68), arrowprops=dict(arrowstyle="->", lw=1.2))

    ax.annotate("", xy=(34, 28), xytext=(34, 36), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.annotate("", xy=(68, 28), xytext=(68, 36), arrowprops=dict(arrowstyle="->", lw=1.2))

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "uml_class_diagram.png", bbox_inches="tight")
    plt.close(fig)
    print("UML Class Diagram created successfully!")


# ==============================================================================
# 6. UML ACTIVITY DIAGRAM — Matching 2.jpeg
# ==============================================================================
def create_uml_activity_diagram():
    fig, ax = draw_framed_canvas((10, 10), "UML Activity Diagram — Academic Authoring & Policy Workflow")

    # Start Node (Solid circle)
    start_node = patches.Circle((50, 90), 1.8, fc="#000000", ec="#000000")
    ax.add_patch(start_node)

    # Activity 1: Initialize Project
    b1 = patches.Rectangle((32, 80), 36, 6, ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(b1)
    ax.text(50, 83, "Create Project & Select Target Venue", fontsize=8.5, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(50, 86), xytext=(50, 88.2), arrowprops=dict(arrowstyle="->", lw=1.2))

    # Decision 1: Literature search needed?
    d1 = patches.Polygon([[50, 78], [60, 73], [50, 68], [40, 73]], ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(d1)
    ax.text(50, 73, "Literature\nSearch?", fontsize=7.8, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(50, 78), xytext=(50, 80), arrowprops=dict(arrowstyle="->", lw=1.2))

    # Branch Yes -> Execute Semantic Scholar search
    b2 = patches.Rectangle((32, 57), 36, 6, ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(b2)
    ax.text(50, 60, "Search Papers & Ingest BibTeX Citations", fontsize=8.2, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(50, 63), xytext=(50, 68), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(51.5, 65.5, "Yes", fontsize=7.5, fontweight="bold")

    # Branch No -> Use existing lab notes
    b_no = patches.Rectangle((74, 70), 20, 6, ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(b_no)
    ax.text(84, 73, "Use Manual Notes", fontsize=7.5, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(74, 73), xytext=(60, 73), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(66, 74.5, "No", fontsize=7.5, fontweight="bold")
    ax.annotate("", xy=(68, 60), xytext=(84, 70), arrowprops=dict(arrowstyle="->", lw=1.2))

    # Activity 3: Extract Research Gap & Formulate Outline
    b3 = patches.Rectangle((32, 46), 36, 6, ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(b3)
    ax.text(50, 49, "Synthesize Research Gap & Generate Outline", fontsize=8.2, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(50, 52), xytext=(50, 57), arrowprops=dict(arrowstyle="->", lw=1.2))

    # Decision 2: Math/Equation Drafting needed?
    d2 = patches.Polygon([[50, 44], [60, 39], [50, 34], [40, 39]], ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(d2)
    ax.text(50, 39, "Math / Algo\nDrafting?", fontsize=7.8, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(50, 44), xytext=(50, 46), arrowprops=dict(arrowstyle="->", lw=1.2))

    # Branch Yes: Draft with formal equations
    b4 = patches.Rectangle((18, 24), 28, 6, ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(b4)
    ax.text(32, 27, "Synthesize \\begin{equation}\n& Algorithmic Pseudocode", fontsize=7.2, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(32, 30), xytext=(40, 39), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(33, 36, "Yes", fontsize=7.5, fontweight="bold")

    # Branch No: Draft narrative text
    b5 = patches.Rectangle((54, 24), 28, 6, ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(b5)
    ax.text(68, 27, "Synthesize Academic Narrative\n& Related Work Matrix", fontsize=7.2, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(68, 30), xytext=(60, 39), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(66, 36, "No", fontsize=7.5, fontweight="bold")

    # Activity 5: Polish & Peer Review Audit
    b6 = patches.Rectangle((32, 13), 36, 6, ec="#000000", fc="#ffffff", lw=1.4)
    ax.add_patch(b6)
    ax.text(50, 16, "Refine Tone & Run 3-Reviewer Audit", fontsize=8.2, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(46, 19), xytext=(32, 24), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.annotate("", xy=(54, 19), xytext=(68, 24), arrowprops=dict(arrowstyle="->", lw=1.2))

    # Final End Node (Bullseye)
    ax.annotate("", xy=(50, 7.5), xytext=(50, 13), arrowprops=dict(arrowstyle="->", lw=1.2))
    end_outer = patches.Circle((50, 5.5), 1.8, ec="#000000", fc="#ffffff", lw=1.5)
    end_inner = patches.Circle((50, 5.5), 1.1, fc="#000000", ec="#000000")
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "uml_activity_diagram.png", bbox_inches="tight")
    plt.close(fig)
    print("UML Activity Diagram created successfully!")


# ==============================================================================
# 7. UML SEQUENCE DIAGRAM — Matching 1.jpeg
# ==============================================================================
def create_uml_sequence_diagram():
    fig, ax = draw_framed_canvas((11.5, 9.5), "UML Sequence Diagram — End-to-End Academic Manuscript Execution")

    lifelines = [
        (14, "Researcher\n(Author)"),
        (32, "Streamlit\nWeb UI"),
        (50, "Literature API\n(Semantic Scholar)"),
        (68, "LLM Engine\n(Gemini/OpenAI)"),
        (86, "LaTeX Compiler\n& Packaging")
    ]

    for x, name in lifelines:
        box = patches.Rectangle((x-7.5, 84), 15, 6.5, ec="#000000", fc="#ffffff", lw=1.4)
        ax.add_patch(box)
        ax.text(x, 87.2, name, fontsize=8, fontweight="bold", ha="center", va="center")
        ax.plot([x, x], [84, 8], color="#000000", lw=1.0, linestyle="--")

    messages = [
        (14, 32, 80, "1. Enter Search Query & Venue"),
        (32, 50, 73, "2. Query Papers & Metadata"),
        (50, 32, 66, "3. Return Abstracts & BibTeX Citations"),
        (14, 32, 59, "4. Ingest Lab Notes & Request Insights"),
        (32, 68, 52, "5. Dispatch Prompt (Title + Goals + Notes)"),
        (68, 32, 45, "6. Return Math Equations & Section Drafts"),
        (14, 32, 38, "7. Trigger Simulated Peer Review"),
        (32, 68, 31, "8. Evaluate Soundness, Novelty & Citations"),
        (14, 32, 24, "9. Execute Plot Script & Compile LaTeX"),
        (32, 86, 17, "10. Assemble main.tex & Generate Figures"),
        (86, 14, 10, "11. Deliver Overleaf ZIP Package & PDF")
    ]

    for x1, x2, y, text in messages:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", lw=1.3, color="#000000"))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y+1.5, text, fontsize=7.5, ha="center", va="bottom",
                bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "uml_sequence_diagram.png", bbox_inches="tight")
    plt.close(fig)
    print("UML Sequence Diagram created successfully!")


# ==============================================================================
# 8. ENTITY RELATIONSHIP DIAGRAM (CHEN NOTATION) — Matching WhatsApp Image
# ==============================================================================
def create_er_diagram():
    fig, ax = draw_framed_canvas((12, 9.5), "Entity Relationship Diagram (ERD) — Manuscript Database Schema")

    def draw_entity(x, y, w, h, name):
        box = patches.Rectangle((x-w/2, y-h/2), w, h, ec="#000000", fc="#ffffff", lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=8.5, fontweight="bold", ha="center", va="center")

    def draw_rel(x, y, w, h, name):
        diamond = patches.Polygon([[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]], ec="#000000", fc="#ffffff", lw=1.4)
        ax.add_patch(diamond)
        ax.text(x, y, name, fontsize=7.2, fontweight="bold", ha="center", va="center")

    def draw_attr(x, y, name, is_pk=False):
        ellipse = patches.FancyBboxPatch((x-4.5, y-1.4), 9.0, 2.8, boxstyle="round,pad=0.3", ec="#000000", fc="#ffffff", lw=1.1)
        ax.add_patch(ellipse)
        ax.text(x, y, name, fontsize=6.8, ha="center", va="center", fontstyle="italic" if not is_pk else "normal")
        if is_pk:
            ax.plot([x-3.2, x+3.2], [y-1.0, y-1.0], color="#000000", lw=0.9)

    # Top Row Entities
    draw_entity(15, 78, 12, 6, "USER")
    draw_rel(30, 78, 8, 5, "owns")
    draw_entity(45, 78, 12, 6, "PROJECT")
    draw_rel(60, 78, 8, 5, "initiates")
    draw_entity(75, 78, 14, 6, "ASSESSMENT")
    draw_rel(89, 78, 8, 5, "maps")
    draw_entity(94, 65, 10, 6, "SAVED_PAPER")

    # Connect top row
    ax.plot([21, 26], [78, 78], color="#000000", lw=1.2)
    ax.text(23, 79.5, "1", fontsize=7.5)
    ax.plot([34, 39], [78, 78], color="#000000", lw=1.2)
    ax.text(37, 79.5, "N", fontsize=7.5)

    ax.plot([51, 56], [78, 78], color="#000000", lw=1.2)
    ax.text(53, 79.5, "1", fontsize=7.5)
    ax.plot([64, 68], [78, 78], color="#000000", lw=1.2)
    ax.text(66, 79.5, "N", fontsize=7.5)

    ax.plot([82, 85], [78, 78], color="#000000", lw=1.2)
    ax.text(83.5, 79.5, "1", fontsize=7.5)
    ax.plot([93, 94], [78, 68], color="#000000", lw=1.2)
    ax.text(95, 74, "N", fontsize=7.5)

    # Middle Center Relationship
    draw_rel(75, 58, 10, 6, "identifies")
    ax.plot([75, 75], [75, 61], color="#000000", lw=1.2)
    ax.text(76.5, 68, "1", fontsize=7.5)
    ax.plot([75, 75], [55, 41], color="#000000", lw=1.2)
    ax.text(76.5, 47, "N", fontsize=7.5)

    # Bottom Row Entities
    draw_entity(15, 38, 14, 6, "SECTION_DRAFT")
    draw_rel(30, 38, 8, 5, "produces")
    draw_entity(45, 38, 12, 6, "PLOT_FIGURE")
    draw_rel(60, 38, 8, 5, "validates")
    draw_entity(75, 38, 12, 6, "FINDING")
    draw_rel(86, 38, 8, 5, "compiles_into")
    draw_entity(93, 38, 10, 6, "REPORT")

    # Connect bottom row
    ax.plot([22, 26], [38, 38], color="#000000", lw=1.2)
    ax.text(24, 39.5, "1", fontsize=7.5)
    ax.plot([34, 39], [38, 38], color="#000000", lw=1.2)
    ax.text(37, 39.5, "N", fontsize=7.5)

    ax.plot([51, 56], [38, 38], color="#000000", lw=1.2)
    ax.text(53, 39.5, "1", fontsize=7.5)
    ax.plot([64, 69], [38, 38], color="#000000", lw=1.2)
    ax.text(67, 39.5, "N", fontsize=7.5)

    ax.plot([81, 82], [38, 38], color="#000000", lw=1.2)
    ax.text(81.5, 39.5, "1", fontsize=7.5)
    ax.plot([90, 93], [38, 38], color="#000000", lw=1.2)
    ax.text(91.5, 39.5, "1", fontsize=7.5)

    # Attributes (Ellipses) around USER
    draw_attr(10, 88, "user_id", is_pk=True)
    draw_attr(20, 88, "username")
    ax.plot([10, 13], [86.6, 81], color="#000000", lw=0.9)
    ax.plot([20, 17], [86.6, 81], color="#000000", lw=0.9)

    # Attributes around PROJECT
    draw_attr(40, 88, "project_id", is_pk=True)
    draw_attr(50, 88, "name")
    ax.plot([40, 43], [86.6, 81], color="#000000", lw=0.9)
    ax.plot([50, 47], [86.6, 81], color="#000000", lw=0.9)

    # Attributes around ASSESSMENT
    draw_attr(70, 88, "assessment_id", is_pk=True)
    draw_attr(80, 88, "target_venue")
    ax.plot([70, 73], [86.6, 81], color="#000000", lw=0.9)
    ax.plot([80, 77], [86.6, 81], color="#000000", lw=0.9)

    # Attributes around SECTION_DRAFT
    draw_attr(10, 26, "draft_id", is_pk=True)
    draw_attr(20, 26, "content")
    ax.plot([10, 13], [27.4, 35], color="#000000", lw=0.9)
    ax.plot([20, 17], [27.4, 35], color="#000000", lw=0.9)

    # Attributes around PLOT_FIGURE
    draw_attr(40, 26, "figure_id", is_pk=True)
    draw_attr(50, 26, "caption")
    ax.plot([40, 43], [27.4, 35], color="#000000", lw=0.9)
    ax.plot([50, 47], [27.4, 35], color="#000000", lw=0.9)

    # Attributes around FINDING
    draw_attr(70, 26, "finding_id", is_pk=True)
    draw_attr(80, 26, "severity")
    ax.plot([70, 73], [27.4, 35], color="#000000", lw=0.9)
    ax.plot([80, 77], [27.4, 35], color="#000000", lw=0.9)

    # Attributes around REPORT
    draw_attr(92, 26, "report_id", is_pk=True)
    ax.plot([92, 93], [27.4, 35], color="#000000", lw=0.9)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "er_diagram.png", bbox_inches="tight")
    plt.close(fig)
    print("ER Diagram (Chen Notation) created successfully!")


if __name__ == "__main__":
    create_new_use_case_diagram()
    create_dfd_level_0()
    create_dfd_level_1()
    create_dfd_level_2()
    create_uml_class_diagram()
    create_uml_activity_diagram()
    create_uml_sequence_diagram()
    create_er_diagram()
    print("All 8 diagrams generated matching the reference folder!")
