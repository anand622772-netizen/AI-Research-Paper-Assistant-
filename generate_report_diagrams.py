"""
Generates high-resolution System Design Diagrams for the Parul University Project Report:
1. Use Case Diagram
2. DFD Level 0 (Context Diagram)
3. DFD Level 1
4. UML Class Diagram
5. UML Sequence Diagram
6. UML Activity Diagram
7. ER Diagram
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = Path("outputs/report_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Title
    ax.text(5, 9.6, "System Design: Use Case Diagram", fontsize=14, fontweight="bold", ha="center")
    
    # Boundary box
    rect = patches.FancyBboxPatch((2.2, 0.4), 5.6, 8.8, boxstyle="round,pad=0.2", ec="#1e3a8a", fc="#f8fafc", lw=2)
    ax.add_patch(rect)
    ax.text(5, 8.9, "AI Research Paper Assistant System Boundary", fontsize=11, fontweight="bold", ha="center", color="#1e3a8a")

    # Actor: Researcher / Student
    ax.plot([1.0], [5.5], "o", markersize=14, color="#0284c7")
    ax.plot([1.0, 1.0], [5.3, 4.4], "-", color="#0284c7", lw=2)
    ax.plot([0.5, 1.5], [4.9, 4.9], "-", color="#0284c7", lw=2)
    ax.plot([1.0, 0.6], [4.4, 3.6], "-", color="#0284c7", lw=2)
    ax.plot([1.0, 1.4], [4.4, 3.6], "-", color="#0284c7", lw=2)
    ax.text(1.0, 3.2, "Researcher /\nStudent", fontsize=10, fontweight="bold", ha="center")

    # Actor: Faculty / Reviewer
    ax.plot([1.0], [8.0], "o", markersize=14, color="#475569")
    ax.plot([1.0, 1.0], [7.8, 7.1], "-", color="#475569", lw=2)
    ax.plot([0.6, 1.4], [7.5, 7.5], "-", color="#475569", lw=2)
    ax.plot([1.0, 0.7], [7.1, 6.4], "-", color="#475569", lw=2)
    ax.plot([1.0, 1.3], [7.1, 6.4], "-", color="#475569", lw=2)
    ax.text(1.0, 6.0, "Reviewer /\nEvaluator", fontsize=9, fontweight="bold", ha="center")

    # Actor: External API Services
    ax.plot([9.0], [5.0], "s", markersize=18, color="#059669")
    ax.text(9.0, 4.2, "Semantic Scholar\n& LLM APIs", fontsize=10, fontweight="bold", ha="center", color="#059669")

    # Use Cases (Ellipses)
    use_cases = [
        (5.0, 8.2, "UC1: Search Literature & Papers"),
        (5.0, 7.2, "UC2: Curate Material & Lab Notes"),
        (5.0, 6.2, "UC3: Synthesize Problem & Novel Gap"),
        (5.0, 5.2, "UC4: Generate Conference Outline"),
        (5.0, 4.2, "UC5: Draft Manuscript Sections"),
        (5.0, 3.2, "UC6: Polish Academic Tone & Style"),
        (5.0, 2.2, "UC7: Run Simulated Peer Reviews"),
        (5.0, 1.2, "UC8: Generate Publication Plots"),
        (5.0, 0.5, "UC9: Compile LaTeX & Overleaf ZIP")
    ]

    for x, y, text in use_cases:
        ellipse = patches.FancyBboxPatch((x-2.2, y-0.35), 4.4, 0.7, boxstyle="round,pad=0.2", ec="#2563eb", fc="#ffffff", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(x, y, text, fontsize=9, ha="center", va="center", color="#0f172a")
        # Connect to Researcher
        ax.plot([1.4, x-2.2], [4.8, y], ":", color="#64748b", lw=1.2)

    # Connect to External APIs
    ax.plot([x+2.2, 8.6], [8.2, 5.2], "--", color="#059669", lw=1.2)
    ax.plot([x+2.2, 8.6], [4.2, 5.0], "--", color="#059669", lw=1.2)
    ax.plot([1.4, x-2.2], [7.0, 2.2], ":", color="#475569", lw=1.2)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "use_case_diagram.png", bbox_inches="tight")
    plt.close(fig)


def create_dfd_level_0():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(5, 5.6, "Data Flow Diagram: Level 0 (Context Level)", fontsize=14, fontweight="bold", ha="center")

    # Center Process (Circle / Ellipse)
    circle = patches.Circle((5, 3), 1.5, ec="#1e40af", fc="#dbeafe", lw=2.5)
    ax.add_patch(circle)
    ax.text(5, 3.2, "0.0\nAI Research Paper\nAssistant System", fontsize=11, fontweight="bold", ha="center", va="center", color="#1e3a8a")

    # Entity Left: User / Researcher
    ent_user = patches.Rectangle((0.6, 2.1), 2.2, 1.8, ec="#334155", fc="#f1f5f9", lw=2)
    ax.add_patch(ent_user)
    ax.text(1.7, 3.0, "Researcher /\nAcademic Author", fontsize=10, fontweight="bold", ha="center", va="center")

    # Entity Right: External Literature & AI Services
    ent_ext = patches.Rectangle((7.2, 2.1), 2.2, 1.8, ec="#334155", fc="#f1f5f9", lw=2)
    ax.add_patch(ent_ext)
    ax.text(8.3, 3.0, "External Cloud\n(Semantic Scholar,\nGemini / OpenAI)", fontsize=10, fontweight="bold", ha="center", va="center")

    # Flow arrows Left -> Center
    ax.annotate("1. Query, Notes & Directives", xy=(3.5, 3.5), xytext=(2.8, 3.5),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5), fontsize=8.5, ha="right")
    ax.annotate("2. Compiled Manuscript, Plots, ZIP", xy=(2.8, 2.5), xytext=(3.5, 2.5),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5), fontsize=8.5, ha="left")

    # Flow arrows Center -> Right
    ax.annotate("3. Search API & Prompts", xy=(7.2, 3.5), xytext=(6.5, 3.5),
                arrowprops=dict(facecolor="#059669", edgecolor="#059669", arrowstyle="->", lw=1.5), fontsize=8.5, ha="left")
    ax.annotate("4. Papers, BibTeX, AI Drafts", xy=(6.5, 2.5), xytext=(7.2, 2.5),
                arrowprops=dict(facecolor="#059669", edgecolor="#059669", arrowstyle="->", lw=1.5), fontsize=8.5, ha="right")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_0.png", bbox_inches="tight")
    plt.close(fig)


def create_dfd_level_1():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(5.5, 7.6, "Data Flow Diagram: Level 1 (Functional Decomposition)", fontsize=14, fontweight="bold", ha="center")

    # 4 Processes
    p1 = patches.Circle((2.5, 5.8), 1.0, ec="#1d4ed8", fc="#eff6ff", lw=2)
    p2 = patches.Circle((8.5, 5.8), 1.0, ec="#1d4ed8", fc="#eff6ff", lw=2)
    p3 = patches.Circle((2.5, 2.2), 1.0, ec="#1d4ed8", fc="#eff6ff", lw=2)
    p4 = patches.Circle((8.5, 2.2), 1.0, ec="#1d4ed8", fc="#eff6ff", lw=2)

    for p in [p1, p2, p3, p4]:
        ax.add_patch(p)

    ax.text(2.5, 5.8, "1.0\nLiterature\nDiscovery", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.text(8.5, 5.8, "2.0\nOutline &\nStructure", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.text(2.5, 2.2, "3.0\nSection &\nDrafting", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.text(8.5, 2.2, "4.0\nLaTeX &\nPackaging", fontsize=9, fontweight="bold", ha="center", va="center")

    # Data Stores (Double line open rectangle)
    def draw_datastore(x, y, w, h, label):
        ax.plot([x, x+w], [y, y], color="#475569", lw=2)
        ax.plot([x, x+w], [y+h, y+h], color="#475569", lw=2)
        ax.text(x+w/2, y+h/2, label, fontsize=8.5, fontweight="bold", ha="center", va="center")

    draw_datastore(4.6, 5.4, 1.8, 0.8, "D1: Papers &\nBibTeX DB")
    draw_datastore(4.6, 1.8, 1.8, 0.8, "D2: Project State\n(JSON)")

    # Data flows
    ax.annotate("Raw Papers", xy=(4.6, 5.8), xytext=(3.5, 5.8),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5), fontsize=8, ha="right")
    ax.annotate("Citations", xy=(7.5, 5.8), xytext=(6.4, 5.8),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5), fontsize=8, ha="left")
    ax.annotate("Section Drafts", xy=(4.6, 2.2), xytext=(3.5, 2.2),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5), fontsize=8, ha="right")
    ax.annotate("Assembled .tex", xy=(7.5, 2.2), xytext=(6.4, 2.2),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5), fontsize=8, ha="left")

    ax.annotate("Context & Insights", xy=(2.5, 3.2), xytext=(2.5, 4.8),
                arrowprops=dict(facecolor="#059669", edgecolor="#059669", arrowstyle="->", lw=1.5), fontsize=8, ha="center")
    ax.annotate("Outline Targets", xy=(8.5, 3.2), xytext=(8.5, 4.8),
                arrowprops=dict(facecolor="#059669", edgecolor="#059669", arrowstyle="->", lw=1.5), fontsize=8, ha="center")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_1.png", bbox_inches="tight")
    plt.close(fig)


def create_uml_class_diagram():
    fig, ax = plt.subplots(figsize=(11, 8), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(5.5, 7.6, "UML Class Diagram: Core Domain Architecture", fontsize=14, fontweight="bold", ha="center")

    def draw_class(x, y, w, h, name, attrs, methods):
        rect = patches.Rectangle((x, y), w, h, ec="#1e293b", fc="#ffffff", lw=1.5)
        ax.add_patch(rect)
        ax.plot([x, x+w], [y+h-0.6, y+h-0.6], color="#1e293b", lw=1.2)
        ax.plot([x, x+w], [y+h-0.6-0.3*len(attrs)-0.2, y+h-0.6-0.3*len(attrs)-0.2], color="#1e293b", lw=1.2)
        ax.text(x+w/2, y+h-0.3, name, fontsize=9.5, fontweight="bold", ha="center", va="center", color="#1e3a8a")
        for i, a in enumerate(attrs):
            ax.text(x+0.15, y+h-0.8-i*0.28, a, fontsize=7.5, va="center")
        y_m = y+h-0.8-len(attrs)*0.28-0.3
        for j, m in enumerate(methods):
            ax.text(x+0.15, y_m-j*0.28, m, fontsize=7.5, va="center")

    # Classes
    draw_class(0.6, 4.0, 3.0, 3.2, "ProjectState",
               ["+ id: String", "+ project_name: String", "+ template: String", "+ metadata: Dict", "+ sections: Dict"],
               ["+ create_empty_project()", "+ save_project(path)", "+ load_project(path)"])

    draw_class(4.0, 4.0, 3.0, 3.2, "LiteratureEngine",
               ["+ search_url: String", "+ cache_papers: List", "+ api_key: String"],
               ["+ search_semantic_scholar()", "+ search_arxiv()", "+ paper_to_bibtex()", "+ clean_bibtex_key()"])

    draw_class(7.4, 4.0, 3.0, 3.2, "LLMProvider",
               ["+ openai_key: String", "+ gemini_key: String", "+ default_model: String"],
               ["+ generate(prompt, context)", "+ call_gemini(model)", "+ call_openai(model)", "+ _generate_offline()"])

    draw_class(2.0, 0.4, 3.2, 3.0, "PlottingStudio",
               ["+ templates: Dict", "+ output_dir: Path", "+ dpi: Integer = 300"],
               ["+ execute_plot_code()", "+ export_png_pdf()", "+ generate_latex_snippet()"])

    draw_class(6.0, 0.4, 3.4, 3.0, "LaTeXCompiler",
               ["+ conference_templates: Dict", "+ compilers: List"],
               ["+ render_latex_manuscript()", "+ create_latex_package()", "+ attempt_local_compile()"])

    # Relationships
    ax.annotate("", xy=(3.6, 5.6), xytext=(4.0, 5.6), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#2563eb"))
    ax.annotate("", xy=(7.0, 5.6), xytext=(7.4, 5.6), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#2563eb"))
    ax.annotate("", xy=(3.5, 3.4), xytext=(3.5, 4.0), arrowprops=dict(arrowstyle="->", lw=1.5, color="#475569"))
    ax.annotate("", xy=(7.5, 3.4), xytext=(7.5, 4.0), arrowprops=dict(arrowstyle="->", lw=1.5, color="#475569"))

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "uml_class_diagram.png", bbox_inches="tight")
    plt.close(fig)


def create_uml_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(5, 7.6, "UML Sequence Diagram: Literature Search to LaTeX Compilation", fontsize=13, fontweight="bold", ha="center")

    lifelines = [
        (1.2, "Researcher\n(User)"),
        (3.5, "Streamlit\nWeb UI"),
        (5.8, "Semantic\nScholar API"),
        (8.0, "LLM Engine\n(Gemini/OpenAI)"),
        (9.5, "LaTeX\nCompiler")
    ]

    for x, label in lifelines:
        box = patches.Rectangle((x-0.8, 6.5), 1.6, 0.8, ec="#1e293b", fc="#e2e8f0", lw=1.5)
        ax.add_patch(box)
        ax.text(x, 6.9, label, fontsize=8.5, fontweight="bold", ha="center", va="center")
        ax.plot([x, x], [6.5, 0.6], "--", color="#94a3b8", lw=1.2)

    messages = [
        (1.2, 3.5, 6.0, "1: Enter Search Query & Filters"),
        (3.5, 5.8, 5.4, "2: Query Papers & Metadata"),
        (5.8, 3.5, 4.8, "3: Return Papers & BibTeX"),
        (1.2, 3.5, 4.2, "4: Add to Materials & Trigger Synthesis"),
        (3.5, 8.0, 3.6, "5: Request Section Generation / Polish"),
        (8.0, 3.5, 3.0, "6: Return Academic Prose & Equations"),
        (1.2, 3.5, 2.4, "7: Build LaTeX Package"),
        (3.5, 9.5, 1.8, "8: Assemble main.tex & Compile"),
        (9.5, 1.2, 1.1, "9: Deliver Overleaf ZIP Bundle & PDF")
    ]

    for x1, x2, y, text in messages:
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.4))
        ax.text((x1+x2)/2, y+0.12, text, fontsize=7.8, ha="center", color="#0f172a")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "uml_sequence_diagram.png", bbox_inches="tight")
    plt.close(fig)


def create_uml_activity_diagram():
    fig, ax = plt.subplots(figsize=(8.5, 8), dpi=300)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(4, 8.6, "UML Activity Diagram: Research Authoring Workflow", fontsize=13, fontweight="bold", ha="center")

    # Start Node (Solid black circle)
    start = patches.Circle((4, 8.0), 0.22, fc="black", ec="black")
    ax.add_patch(start)

    activities = [
        (4, 7.2, "Search Literature on Semantic Scholar & ArXiv"),
        (4, 6.2, "Curate Papers & Formulate Lab Hypotheses"),
        (4, 5.2, "Extract Novel Problem Statement & Research Gap"),
        (4, 4.2, "Generate Hierarchical Conference Outline"),
        (4, 3.2, "Draft Modular Sections (Equations, Tables, Algos)"),
        (4, 2.2, "Refine Academic Tone & Execute 3-Reviewer Audit"),
        (4, 1.2, "Generate Publication Plots & Compile LaTeX ZIP")
    ]

    y_prev = 8.0
    for x, y, label in activities:
        box = patches.FancyBboxPatch((x-2.7, y-0.35), 5.4, 0.7, boxstyle="round,pad=0.2", ec="#1e40af", fc="#eff6ff", lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=8.5, ha="center", va="center", color="#1e3a8a")
        # Arrow from previous
        ax.annotate("", xy=(x, y+0.4), xytext=(x, y_prev-0.25),
                    arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5))
        y_prev = y

    # End Node (Bullseye)
    end_outer = patches.Circle((4, 0.35), 0.25, ec="black", fc="none", lw=1.5)
    end_inner = patches.Circle((4, 0.35), 0.16, fc="black", ec="black")
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)
    ax.annotate("", xy=(4, 0.65), xytext=(4, 0.8),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#2563eb", arrowstyle="->", lw=1.5))

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "uml_activity_diagram.png", bbox_inches="tight")
    plt.close(fig)


def create_er_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(5.5, 7.6, "Entity Relationship (ER) Diagram: Manuscript Schema", fontsize=13, fontweight="bold", ha="center")

    def draw_entity(x, y, w, h, name, fields):
        rect = patches.Rectangle((x, y), w, h, ec="#0f172a", fc="#ffffff", lw=1.5)
        ax.add_patch(rect)
        ax.plot([x, x+w], [y+h-0.55, y+h-0.55], color="#0f172a", lw=1.2)
        ax.text(x+w/2, y+h-0.28, name, fontsize=9.5, fontweight="bold", ha="center", va="center", color="#0284c7")
        for i, f in enumerate(fields):
            ax.text(x+0.15, y+h-0.85-i*0.28, f, fontsize=7.8, va="center")

    draw_entity(0.6, 4.2, 2.8, 2.8, "PROJECT", ["PK: project_id", "title: String", "template_name: String", "created_at: DateTime", "status: String"])
    draw_entity(4.2, 4.2, 2.8, 2.8, "SAVED_PAPER", ["PK: paper_id", "FK: project_id", "title: String", "year: Integer", "venue: String", "bibtex_key: String"])
    draw_entity(7.6, 4.2, 2.8, 2.8, "OUTLINE_SECTION", ["PK: section_id", "FK: project_id", "title: String", "target_words: Integer", "objective: Text"])

    draw_entity(0.6, 0.8, 2.8, 2.8, "MANUSCRIPT_DRAFT", ["PK: draft_id", "FK: project_id", "section_name: String", "content: Text", "word_count: Integer"])
    draw_entity(4.2, 0.8, 2.8, 2.8, "PLOT_FIGURE", ["PK: figure_id", "FK: project_id", "caption: Text", "latex_label: String", "file_path: String"])
    draw_entity(7.6, 0.8, 2.8, 2.8, "PEER_REVIEW", ["PK: review_id", "FK: project_id", "reviewer_name: String", "overall_score: Decimal", "critique: Text"])

    # Relationships (Diamond)
    def draw_rel(x, y, label):
        poly = patches.Polygon([[x, y+0.35], [x+0.5, y], [x, y-0.35], [x-0.5, y]], ec="#2563eb", fc="#eff6ff", lw=1.2)
        ax.add_patch(poly)
        ax.text(x, y, label, fontsize=7, ha="center", va="center", fontweight="bold")

    draw_rel(3.8, 5.6, "1:N")
    ax.plot([3.4, 3.3], [5.6, 5.6], "-", color="#2563eb", lw=1.2)
    ax.plot([4.3, 4.2], [5.6, 5.6], "-", color="#2563eb", lw=1.2)

    draw_rel(7.2, 5.6, "1:N")
    ax.plot([7.0, 7.6], [5.6, 5.6], "-", color="#2563eb", lw=1.2)

    draw_rel(2.0, 3.9, "1:N")
    ax.plot([2.0, 2.0], [4.2, 3.6], "-", color="#2563eb", lw=1.2)
    ax.plot([2.0, 2.0], [3.9, 3.6], "-", color="#2563eb", lw=1.2)

    draw_rel(5.6, 3.9, "1:N")
    ax.plot([5.6, 5.6], [4.2, 3.6], "-", color="#2563eb", lw=1.2)

    draw_rel(9.0, 3.9, "1:N")
    ax.plot([9.0, 9.0], [4.2, 3.6], "-", color="#2563eb", lw=1.2)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "er_diagram.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    create_use_case_diagram()
    create_dfd_level_0()
    create_dfd_level_1()
    create_uml_class_diagram()
    create_uml_sequence_diagram()
    create_uml_activity_diagram()
    create_er_diagram()
    print("All 7 system design diagrams created successfully!")
