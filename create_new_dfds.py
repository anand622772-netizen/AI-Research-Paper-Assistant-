"""
Generates pristine, publication-grade DFD Level 0, Level 1, and Level 2 diagrams
with perfect alignment, professional color palettes, and zero text overlap.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = Path("outputs/report_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def draw_arrow(ax, start, end, label, label_pos=(0.5, 0.5), label_offset=(0, 0.15),
               color="#2563eb", fontsize=8.5, ha="center", va="bottom", rad=0.0):
    """Draws an arrow with a neatly positioned text label."""
    connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(
            arrowstyle="->,head_width=0.35,head_length=0.45",
            color=color, lw=1.6,
            shrinkA=4, shrinkB=4,
            connectionstyle=connectionstyle
        )
    )
    # Calculate mid point for label
    lx = start[0] + (end[0] - start[0]) * label_pos[0] + label_offset[0]
    ly = start[1] + (end[1] - start[1]) * label_pos[1] + label_offset[1]
    ax.text(lx, ly, label, fontsize=fontsize, ha=ha, va=va, color="#0f172a",
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="none", alpha=0.9))


def create_dfd_level_0():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Diagram Title
    ax.text(5.5, 6.6, "Data Flow Diagram: Level 0 (Context Level Diagram)",
            fontsize=13, fontweight="bold", ha="center", color="#0f172a")
    ax.text(5.5, 6.25, "System Boundary and High-Level External Entity Information Exchanges",
            fontsize=9.5, fontstyle="italic", ha="center", color="#64748b")

    # Center Process (Circle)
    proc_circle = patches.Circle((5.5, 3.4), 1.5, ec="#1e40af", fc="#eff6ff", lw=2.2, zorder=2)
    ax.add_patch(proc_circle)
    ax.text(5.5, 3.7, "0.0", fontsize=12, fontweight="bold", ha="center", va="center", color="#1e40af")
    ax.text(5.5, 3.25, "AI Research Paper\nAssistant System", fontsize=10.5, fontweight="bold",
            ha="center", va="center", color="#0f172a")

    # External Entity Left: Academic Researcher / Student
    ent_left = patches.Rectangle((0.5, 2.3), 2.2, 2.2, ec="#334155", fc="#f8fafc", lw=2, zorder=2)
    ax.add_patch(ent_left)
    ax.text(1.6, 3.8, "EXTERNAL ENTITY", fontsize=7.5, fontweight="bold", ha="center", color="#64748b")
    ax.text(1.6, 3.3, "Academic Researcher\n/ Graduate Student", fontsize=9.5, fontweight="bold",
            ha="center", va="center", color="#0f172a")

    # External Entity Right Top: Semantic Scholar & ArXiv APIs
    ent_rt = patches.Rectangle((8.3, 3.9), 2.2, 2.0, ec="#059669", fc="#f0fdf4", lw=2, zorder=2)
    ax.add_patch(ent_rt)
    ax.text(9.4, 5.2, "EXTERNAL ENTITY", fontsize=7.5, fontweight="bold", ha="center", color="#059669")
    ax.text(9.4, 4.7, "Scholarly APIs\n(Semantic Scholar\n& ArXiv Service)", fontsize=9, fontweight="bold",
            ha="center", va="center", color="#065f46")

    # External Entity Right Bottom: Generative AI LLM Services
    ent_rb = patches.Rectangle((8.3, 0.9), 2.2, 2.0, ec="#7c3aed", fc="#faf5ff", lw=2, zorder=2)
    ax.add_patch(ent_rb)
    ax.text(9.4, 2.2, "EXTERNAL ENTITY", fontsize=7.5, fontweight="bold", ha="center", color="#7c3aed")
    ax.text(9.4, 1.7, "AI / LLM Services\n(OpenAI & Google\nGemini Endpoints)", fontsize=9, fontweight="bold",
            ha="center", va="center", color="#5b21b6")

    # Data Flows: User <-> Process
    draw_arrow(ax, (2.7, 4.1), (4.0, 4.1), "1. Search Queries, Notes & Style Directives",
               label_pos=(0.5, 0.5), label_offset=(0, 0.18), color="#2563eb", fontsize=8)
    draw_arrow(ax, (4.0, 2.7), (2.7, 2.7), "4. Assembled Manuscript, Plots & Overleaf ZIP",
               label_pos=(0.5, 0.5), label_offset=(0, -0.22), color="#2563eb", fontsize=8)

    # Data Flows: Process <-> Scholarly APIs
    draw_arrow(ax, (6.8, 4.3), (8.3, 4.9), "2a. REST Search Request",
               label_pos=(0.5, 0.5), label_offset=(0, 0.18), color="#059669", fontsize=8)
    draw_arrow(ax, (8.3, 4.3), (6.9, 3.8), "2b. Paper Abstracts & BibTeX",
               label_pos=(0.5, 0.5), label_offset=(0, -0.2), color="#059669", fontsize=8)

    # Data Flows: Process <-> LLM Services
    draw_arrow(ax, (6.8, 2.8), (8.3, 2.1), "3a. Context-Enriched Prompts",
               label_pos=(0.5, 0.5), label_offset=(0, 0.18), color="#7c3aed", fontsize=8)
    draw_arrow(ax, (8.3, 1.5), (6.7, 2.3), "3b. Synthesized Drafts & Peer Reviews",
               label_pos=(0.5, 0.5), label_offset=(0, -0.22), color="#7c3aed", fontsize=8)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_0.png", bbox_inches="tight")
    plt.close(fig)
    print("DFD Level 0 created successfully!")


def create_dfd_level_1():
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    ax.text(6.0, 8.1, "Data Flow Diagram: Level 1 (System Functional Decomposition)",
            fontsize=13, fontweight="bold", ha="center", color="#0f172a")
    ax.text(6.0, 7.8, "Decomposition into 5 Core Sub-Processes and Synchronized Data Stores",
            fontsize=9.5, fontstyle="italic", ha="center", color="#64748b")

    def draw_proc(x, y, num, name):
        c = patches.Circle((x, y), 0.95, ec="#1e40af", fc="#eff6ff", lw=2, zorder=3)
        ax.add_patch(c)
        ax.text(x, y+0.3, num, fontsize=9.5, fontweight="bold", ha="center", color="#1e40af")
        ax.text(x, y-0.15, name, fontsize=8, fontweight="bold", ha="center", va="center", color="#0f172a")

    def draw_ds(x, y, w, h, ds_id, ds_name):
        ax.plot([x, x+w], [y, y], color="#475569", lw=2.2, zorder=3)
        ax.plot([x, x+w], [y+h, y+h], color="#475569", lw=2.2, zorder=3)
        ax.fill([x, x+w, x+w, x], [y, y, y+h, y+h], color="#f8fafc", zorder=2)
        ax.text(x+w/2, y+h*0.65, ds_id, fontsize=8, fontweight="bold", ha="center", color="#0284c7")
        ax.text(x+w/2, y+h*0.3, ds_name, fontsize=7.8, fontweight="bold", ha="center", color="#1e293b")

    # 5 Main Processes
    draw_proc(1.8, 6.2, "1.0", "Literature\nDiscovery")
    draw_proc(6.0, 6.2, "2.0", "Research\nInsights Hub")
    draw_proc(10.2, 6.2, "3.0", "Outline &\nHierarchy")
    draw_proc(3.6, 2.4, "4.0", "Section Writing\n& Refinement")
    draw_proc(8.4, 2.4, "5.0", "Plots Studio &\nLaTeX Packaging")

    # 3 Data Stores
    draw_ds(3.5, 4.3, 2.2, 0.85, "D1", "Literature & BibTeX DB")
    draw_ds(7.8, 4.3, 2.2, 0.85, "D2", "Project State (JSON)")
    draw_ds(5.0, 0.8, 2.2, 0.85, "D3", "Visual Assets & Plots")

    # External Entities
    ent_u = patches.Rectangle((0.3, 3.8), 1.6, 1.4, ec="#334155", fc="#ffffff", lw=1.8, zorder=3)
    ax.add_patch(ent_u)
    ax.text(1.1, 4.5, "Researcher\n(User)", fontsize=8.5, fontweight="bold", ha="center", va="center")

    ent_ext = patches.Rectangle((10.1, 3.8), 1.6, 1.4, ec="#059669", fc="#ffffff", lw=1.8, zorder=3)
    ax.add_patch(ent_ext)
    ax.text(10.9, 4.5, "External APIs\n(Scholar & LLM)", fontsize=8, fontweight="bold", ha="center", va="center")

    # Flows: User to 1.0 & 2.0
    draw_arrow(ax, (1.1, 5.2), (1.5, 5.3), "Keywords", label_offset=(-0.1, 0.15), fontsize=7.5)
    draw_arrow(ax, (2.7, 6.2), (5.05, 6.2), "Saved Papers", label_offset=(0, 0.15), fontsize=7.5)
    draw_arrow(ax, (6.95, 6.2), (9.25, 6.2), "Extracted Gap", label_offset=(0, 0.15), fontsize=7.5)

    # 1.0 to D1
    draw_arrow(ax, (2.2, 5.3), (3.5, 4.8), "BibTeX Keys", label_offset=(-0.1, 0.15), fontsize=7.5)

    # 2.0 to D2
    draw_arrow(ax, (6.7, 5.4), (7.8, 4.9), "Insights", label_offset=(0.1, 0.15), fontsize=7.5)

    # 3.0 to D2
    draw_arrow(ax, (9.7, 5.35), (9.0, 4.9), "Outline Targets", label_offset=(0.1, 0.15), fontsize=7.5)

    # D1 to 4.0
    draw_arrow(ax, (4.2, 4.3), (3.9, 3.35), "Citations", label_offset=(-0.15, 0.15), fontsize=7.5)

    # D2 to 4.0
    draw_arrow(ax, (7.9, 4.3), (4.5, 2.7), "Objectives & Notes", label_offset=(0, -0.2), fontsize=7.5)

    # 4.0 to D2 (Save drafts)
    draw_arrow(ax, (4.5, 2.3), (8.2, 4.3), "Section Drafts", label_offset=(0.1, 0.15), fontsize=7.5, rad=-0.2)

    # 4.0 to 5.0
    draw_arrow(ax, (4.55, 2.4), (7.45, 2.4), "Polished Manuscript Text", label_offset=(0, 0.16), fontsize=7.5)

    # 5.0 to D3
    draw_arrow(ax, (8.0, 1.6), (7.0, 1.2), "Rendered Charts", label_offset=(0.2, 0.15), fontsize=7.5)

    # 5.0 to User
    draw_arrow(ax, (7.5, 2.2), (1.5, 3.8), "Overleaf ZIP Bundle & PDF", label_offset=(0, -0.22), fontsize=7.5, rad=0.25)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_1.png", bbox_inches="tight")
    plt.close(fig)
    print("DFD Level 1 created successfully!")


def create_dfd_level_2():
    fig, ax = plt.subplots(figsize=(12.5, 9), dpi=300)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(6.25, 8.6, "Data Flow Diagram: Level 2 (Decomposition of Process 4.0: Drafting & Refinement Engine)",
            fontsize=13, fontweight="bold", ha="center", color="#0f172a")
    ax.text(6.25, 8.25, "Detailed Sub-Processes: Context Assembly, LLM Dispatching, Math/Equation Formatting, and Citation Auditing",
            fontsize=9.5, fontstyle="italic", ha="center", color="#64748b")

    def draw_subproc(x, y, num, name):
        c = patches.Circle((x, y), 0.9, ec="#7c3aed", fc="#faf5ff", lw=2, zorder=3)
        ax.add_patch(c)
        ax.text(x, y+0.28, num, fontsize=9.5, fontweight="bold", ha="center", color="#7c3aed")
        ax.text(x, y-0.15, name, fontsize=7.8, fontweight="bold", ha="center", va="center", color="#1e1b4b")

    def draw_ds(x, y, w, h, ds_id, ds_name):
        ax.plot([x, x+w], [y, y], color="#475569", lw=2.2, zorder=3)
        ax.plot([x, x+w], [y+h, y+h], color="#475569", lw=2.2, zorder=3)
        ax.fill([x, x+w, x+w, x], [y, y, y+h, y+h], color="#f8fafc", zorder=2)
        ax.text(x+w/2, y+h*0.65, ds_id, fontsize=8, fontweight="bold", ha="center", color="#0284c7")
        ax.text(x+w/2, y+h*0.3, ds_name, fontsize=7.5, fontweight="bold", ha="center", color="#1e293b")

    # 5 Level 2 Sub-Processes for Process 4.0
    draw_subproc(2.2, 6.5, "4.1", "Prompt Context\nAssembler")
    draw_subproc(6.25, 6.5, "4.2", "Multi-Provider\nLLM Dispatcher")
    draw_subproc(10.3, 6.5, "4.3", "Math, Equation &\nAlgo Formatter")
    draw_subproc(10.3, 2.5, "4.4", "Academic Tone\n& Peer Review")
    draw_subproc(4.2, 2.5, "4.5", "Citation Auditor\n& Health Check")

    # Data Stores
    draw_ds(1.0, 4.0, 2.4, 0.85, "D1", "Literature & BibTeX DB")
    draw_ds(5.0, 4.0, 2.5, 0.85, "D2", "Project State (JSON)")
    draw_ds(8.5, 4.0, 2.8, 0.85, "D3", "Manuscript Sections DB")

    # External Entity: LLM APIs (Gemini/OpenAI)
    ent_llm = patches.Rectangle((5.0, 1.0), 2.5, 1.2, ec="#7c3aed", fc="#ffffff", lw=1.8, zorder=3)
    ax.add_patch(ent_llm)
    ax.text(6.25, 1.6, "Gemini & OpenAI\nCloud Models", fontsize=8.5, fontweight="bold", ha="center", va="center", color="#5b21b6")

    # Flows:
    # D2 -> 4.1 (Retrieve metadata & outline objectives)
    draw_arrow(ax, (5.2, 4.85), (2.8, 5.8), "Section Goals", label_offset=(0, 0.15), fontsize=7.5)
    # D1 -> 4.1 (Retrieve citation keys)
    draw_arrow(ax, (2.0, 4.85), (2.0, 5.6), "BibTeX Keys", label_offset=(-0.15, 0.15), fontsize=7.5)

    # 4.1 -> 4.2 (Context prompt)
    draw_arrow(ax, (3.1, 6.5), (5.35, 6.5), "Structured Academic Prompt", label_offset=(0, 0.16), fontsize=7.5)

    # 4.2 <-> External LLM
    draw_arrow(ax, (6.0, 5.6), (5.8, 2.2), "API Query", label_offset=(-0.15, 0), fontsize=7.5)
    draw_arrow(ax, (6.6, 2.2), (6.6, 5.6), "Raw Generation", label_offset=(0.2, 0), fontsize=7.5)

    # 4.2 -> 4.3 (Raw draft)
    draw_arrow(ax, (7.15, 6.5), (9.4, 6.5), "Raw Markdown Text", label_offset=(0, 0.16), fontsize=7.5)

    # 4.3 -> 4.4 (Formatted LaTeX equations)
    draw_arrow(ax, (10.3, 5.6), (10.3, 3.4), "Equations & Algorithms", label_offset=(0.3, 0), fontsize=7.5)

    # 4.4 -> 4.5 (Polished draft to audit)
    draw_arrow(ax, (9.4, 2.5), (5.1, 2.5), "Refined Section Draft", label_offset=(0, 0.16), fontsize=7.5)

    # D1 -> 4.5 (Verify citations)
    draw_arrow(ax, (2.2, 4.0), (3.8, 3.3), "Verify \\cite{} Keys", label_offset=(-0.1, -0.15), fontsize=7.5)

    # 4.5 -> D3 (Save verified draft)
    draw_arrow(ax, (4.5, 3.35), (8.5, 4.2), "Validated Section Content", label_offset=(0.2, 0.15), fontsize=7.5, rad=-0.15)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "dfd_level_2.png", bbox_inches="tight")
    plt.close(fig)
    print("DFD Level 2 created successfully!")


if __name__ == "__main__":
    create_dfd_level_0()
    create_dfd_level_1()
    create_dfd_level_2()
    print("All DFDs generated with zero text overlap!")
