"""
Script to generate the exact 4 diagrams requested from user photos:
1. Use Case Diagrams (Administrator & Fraud Analyst - Page 26)
2. Data Flow Diagrams:
   - DFD Level 0 (Context Level with 4 external entities - Page 35)
   - DFD Level 1 (Admin Side & User Side - Page 36)
3. Activity Diagram (4 Swimlanes: User, System, Vector Database, LLM Service - Page 34)
4. Sequence Diagram (8 Lifelines, 14 numbered messages - Page 33)
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = Path("outputs/report_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Drawing Helpers
# -----------------------------------------------------------------------------
def draw_stick_man(ax, x, y, scale=1.0, label=""):
    """Draws a clean UML actor stick figure."""
    # Head
    r = 0.22 * scale
    head = patches.Circle((x, y + 0.65 * scale), r, fc="#ffffff", ec="#000000", lw=1.8, zorder=5)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y + 0.43 * scale, y - 0.15 * scale], color="#000000", lw=1.8, zorder=5)
    # Arms
    ax.plot([x - 0.35 * scale, x + 0.35 * scale], [y + 0.22 * scale, y + 0.22 * scale], color="#000000", lw=1.8, zorder=5)
    # Left leg
    ax.plot([x, x - 0.30 * scale], [y - 0.15 * scale, y - 0.65 * scale], color="#000000", lw=1.8, zorder=5)
    # Right leg
    ax.plot([x, x + 0.30 * scale], [y - 0.15 * scale, y - 0.65 * scale], color="#000000", lw=1.8, zorder=5)
    # Label
    if label:
        ax.text(x, y - 0.85 * scale, label, fontsize=9.0 * scale, fontweight="bold", ha="center", va="top", color="#000000")


def draw_open_data_store(ax, x, y, w, h, ds_id, ds_name, font_scale=1.0):
    """Draws a classical DFD open-ended data store."""
    ax.plot([x, x + w], [y + h, y + h], color="#000000", lw=1.6, zorder=3)
    ax.plot([x, x + w], [y, y], color="#000000", lw=1.6, zorder=3)
    ax.plot([x, x], [y, y + h], color="#000000", lw=1.6, zorder=3)
    id_w = 0.55 * font_scale
    ax.plot([x + id_w, x + id_w], [y, y + h], color="#000000", lw=1.4, zorder=3)
    ax.text(x + id_w / 2, y + h / 2, ds_id, fontsize=8.5 * font_scale, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)
    ax.text(x + id_w + (w - id_w) / 2, y + h / 2, ds_name, fontsize=8.0 * font_scale, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)


# =============================================================================
# 1. USE CASE DIAGRAM (Page 26 of user photos)
# =============================================================================
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(9.5, 14.0), dpi=300)
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 14.0)
    ax.axis("off")

    # Header and Footer text matching photo
    ax.text(0.6, 13.6, "3.7 Use Case Diagram", fontsize=13, fontweight="bold", ha="left", color="#1e293b")
    ax.text(6.8, 13.6, "Requirement Analysis | 2026 - 2027", fontsize=10, ha="right", color="#64748b")
    ax.plot([0.6, 8.9], [13.45, 13.45], color="#cbd5e1", lw=1.2)

    ax.text(0.6, 0.4, "AI-Powered Document Question Answering System for Fraud Prevention", fontsize=9.5, ha="left", color="#475569")
    ax.text(8.9, 0.4, "26", fontsize=10, fontweight="bold", ha="right", color="#0f172a",
            bbox=dict(boxstyle="square,pad=0.25", fc="#cbd5e1", ec="none"))
    ax.plot([0.6, 8.9], [0.55, 0.55], color="#cbd5e1", lw=1.2)

    # -------------------------------------------------------------------------
    # TOP: Use Case Diagram - Administrator
    # -------------------------------------------------------------------------
    top_outer = patches.Rectangle((1.5, 7.3), 6.5, 5.8, fc="#ffffff", ec="#000000", lw=1.6, zorder=1)
    ax.add_patch(top_outer)

    # System boundary
    sys_top = patches.Rectangle((3.5, 7.5), 4.3, 5.4, fc="#fbfcfd", ec="#000000", lw=1.3, zorder=2)
    ax.add_patch(sys_top)
    ax.text(5.65, 12.65, "<<AI-Powered Document Question Answering System>>", fontsize=8.0, ha="center", va="center", color="#334155")

    # Administrator actor
    draw_stick_man(ax, 2.3, 10.1, scale=0.9, label="Administrator")

    # Admin use case ovals
    admin_ucs = ["Login", "Manage Users", "Manage Documents", "Monitor System", "Logout"]
    y_admin = [11.9, 10.9, 9.9, 8.9, 7.9]

    for uc_text, y_pos in zip(admin_ucs, y_admin):
        oval = patches.Ellipse((5.65, y_pos), 2.2, 0.58, fc="#ffffff", ec="#000000", lw=1.4, zorder=3)
        ax.add_patch(oval)
        ax.text(5.65, y_pos, uc_text, fontsize=8.5, ha="center", va="center", color="#000000", zorder=4)
        # Line from actor hand to oval left edge
        ax.plot([2.55, 4.55], [10.3, y_pos], color="#000000", lw=1.3, zorder=3)

    ax.text(4.75, 7.05, "Use Case Diagram - Administrator", fontsize=10.5, fontweight="bold", ha="center", color="#000000")

    # -------------------------------------------------------------------------
    # BOTTOM: Use Case Diagram - Fraud Analyst
    # -------------------------------------------------------------------------
    bot_outer = patches.Rectangle((1.5, 1.0), 6.5, 5.8, fc="#ffffff", ec="#000000", lw=1.6, zorder=1)
    ax.add_patch(bot_outer)

    # System boundary
    sys_bot = patches.Rectangle((3.5, 1.2), 4.3, 5.4, fc="#fbfcfd", ec="#000000", lw=1.3, zorder=2)
    ax.add_patch(sys_bot)
    ax.text(5.65, 6.35, "<<AI-Powered Document Question Answering System>>", fontsize=8.0, ha="center", va="center", color="#334155")

    # Fraud Analyst actor
    draw_stick_man(ax, 2.3, 3.7, scale=0.9, label="Fraud Analyst")

    # Fraud analyst use case ovals
    analyst_ucs = ["Login", "Upload Documents", "Ask Question", "View AI Response", "Verify Source", "View Chat History", "Logout"]
    y_analyst = [5.8, 5.1, 4.4, 3.7, 3.0, 2.3, 1.6]

    for uc_text, y_pos in zip(analyst_ucs, y_analyst):
        oval = patches.Ellipse((5.65, y_pos), 2.2, 0.48, fc="#ffffff", ec="#000000", lw=1.4, zorder=3)
        ax.add_patch(oval)
        ax.text(5.65, y_pos, uc_text, fontsize=8.0, ha="center", va="center", color="#000000", zorder=4)
        # Line from actor hand to oval left edge
        ax.plot([2.55, 4.55], [3.9, y_pos], color="#000000", lw=1.3, zorder=3)

    ax.text(4.75, 0.75, "Use Case Diagram - Fraud Analyst", fontsize=10.5, fontweight="bold", ha="center", color="#000000")

    out_path = OUTPUT_DIR / "use_case_diagram_smartdoc.png"
    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated: {out_path}")


# =============================================================================
# 2. DFD LEVEL 0 (Page 35 of user photos)
# =============================================================================
def generate_dfd_level_0():
    fig, ax = plt.subplots(figsize=(11.0, 7.5), dpi=300)
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 7.5)
    ax.axis("off")

    # Framing rectangle
    outer = patches.Rectangle((0.4, 0.4), 10.2, 6.7, fc="#ffffff", ec="#000000", lw=1.8, zorder=1)
    ax.add_patch(outer)
    ax.text(0.6, 6.85, "Context Level DFD: 0 level", fontsize=11, fontweight="bold", ha="left", color="#000000")

    # Center Process 0.0 Circle
    cx, cy, cr = 5.5, 3.6, 1.25
    center_circle = patches.Circle((cx, cy), cr, fc="#ffffff", ec="#000000", lw=1.8, zorder=3)
    ax.add_patch(center_circle)
    ax.text(cx, cy + 0.42, "0.0", fontsize=12, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)
    ax.text(cx, cy + 0.05, "SmartDoc AI", fontsize=10.5, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)
    ax.text(cx, cy - 0.35, "(AI-Powered Document\nQuestion Answering\nSystem)", fontsize=7.8, ha="center", va="center", color="#000000", zorder=4)

    # 4 External Entities
    # Top: Fraud Analyst
    box_fa = patches.Rectangle((4.6, 5.8), 1.8, 0.65, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
    ax.add_patch(box_fa)
    ax.text(5.5, 6.12, "Fraud Analyst", fontsize=8.8, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

    # Left: Administrator
    box_adm = patches.Rectangle((0.8, 3.2), 1.8, 0.75, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
    ax.add_patch(box_adm)
    ax.text(1.7, 3.57, "Administrator", fontsize=8.8, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

    # Right: Compliance Officer
    box_co = patches.Rectangle((8.4, 3.2), 1.8, 0.75, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
    ax.add_patch(box_co)
    ax.text(9.3, 3.57, "Compliance Officer", fontsize=8.8, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

    # Bottom: Researcher / Student
    box_rs = patches.Rectangle((4.4, 0.8), 2.2, 0.65, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
    ax.add_patch(box_rs)
    ax.text(5.5, 1.12, "Researcher / Student", fontsize=8.8, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

    # -------------------------------------------------------------------------
    # Flows
    # -------------------------------------------------------------------------
    # 1. Left (Administrator <-> 0.0)
    # Admin -> 0.0 (top line)
    y_adm_in = 3.8
    ax.annotate("", xy=(cx - cr, y_adm_in), xytext=(2.6, y_adm_in),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(3.4, y_adm_in + 0.12, "Admin requesting for login,\nmanage users,documents,\nmonitor system",
            fontsize=6.8, ha="center", va="bottom", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    # 0.0 -> Admin (bottom line)
    y_adm_out = 3.3
    ax.annotate("", xy=(2.6, y_adm_out), xytext=(cx - cr, y_adm_out),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(3.4, y_adm_out - 0.12, "Admin gets acknowledgement &\nreports and alerts",
            fontsize=6.8, ha="center", va="top", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    # 2. Right (Compliance Officer <-> 0.0)
    # 0.0 -> Officer (top line)
    y_co_out = 3.8
    ax.annotate("", xy=(8.4, y_co_out), xytext=(cx + cr, y_co_out),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(7.6, y_co_out + 0.12, "Officer gets AI answers,\nsource citations and\nchat history",
            fontsize=6.8, ha="center", va="bottom", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    # Officer -> 0.0 (bottom line)
    y_co_in = 3.3
    ax.annotate("", xy=(cx + cr, y_co_in), xytext=(8.4, y_co_in),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(7.6, y_co_in - 0.12, "Officer requesting for login\nand compliance queries",
            fontsize=6.8, ha="center", va="top", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    # 3. Top (Fraud Analyst <-> 0.0)
    # Analyst -> 0.0 (left line)
    x_fa_in = 5.2
    ax.annotate("", xy=(x_fa_in, cy + cr), xytext=(x_fa_in, 5.8),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(x_fa_in - 0.12, 5.35, "Fraud Analyst requesting\nfor login, upload documents\nand ask questions",
            fontsize=6.8, ha="right", va="center", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    # 0.0 -> Analyst (right line)
    x_fa_out = 5.8
    ax.annotate("", xy=(x_fa_out, 5.8), xytext=(x_fa_out, cy + cr),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(x_fa_out + 0.12, 5.35, "Fraud Analyst gets AI answers,\nsource citations and\nchat history",
            fontsize=6.8, ha="left", va="center", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    # 4. Bottom (Researcher / Student <-> 0.0)
    # 0.0 -> Student (left line)
    x_rs_out = 5.2
    ax.annotate("", xy=(x_rs_out, 1.45), xytext=(x_rs_out, cy - cr),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(x_rs_out - 0.12, 1.9, "Researcher/Student gets AI\nanswers, source citations\nand chat history",
            fontsize=6.8, ha="right", va="center", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    # Student -> 0.0 (right line)
    x_rs_in = 5.8
    ax.annotate("", xy=(x_rs_in, cy - cr), xytext=(x_rs_in, 1.45),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#000000", lw=1.3), zorder=4)
    ax.text(x_rs_in + 0.12, 1.9, "Researcher/Student requesting\nfor login, upload documents\nand ask questions",
            fontsize=6.8, ha="left", va="center", color="#000000",
            bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"))

    ax.text(5.5, 0.15, "Context Level DFD: 0 Level", fontsize=10.5, fontweight="bold", ha="center", color="#000000")

    out_path = OUTPUT_DIR / "dfd_level_0_smartdoc.png"
    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated: {out_path}")


# =============================================================================
# 3. DFD LEVEL 1 (Page 36 of user photos - Admin side & User side)
# =============================================================================
def generate_dfd_level_1():
    fig, ax = plt.subplots(figsize=(10.0, 14.5), dpi=300)
    ax.set_xlim(0, 10.0)
    ax.set_ylim(0, 14.5)
    ax.axis("off")

    # Header & Footer text
    ax.text(0.6, 14.2, "4.2.1.5.2 Level 1", fontsize=10, ha="left", color="#475569")
    ax.text(9.4, 14.2, "Design | 2026 - 2027", fontsize=10, ha="right", color="#64748b")
    ax.plot([0.6, 9.4], [14.05, 14.05], color="#cbd5e1", lw=1.2)

    ax.text(0.6, 0.4, "AI-Powered Document Question Answering System for Fraud Prevention", fontsize=9, ha="left", color="#475569")
    ax.text(9.4, 0.4, "36", fontsize=9.5, fontweight="bold", ha="right", color="#0f172a",
            bbox=dict(boxstyle="square,pad=0.25", fc="#cbd5e1", ec="none"))
    ax.plot([0.6, 9.4], [0.55, 0.55], color="#cbd5e1", lw=1.2)

    # -------------------------------------------------------------------------
    # TOP: Admin side DFD :- 1st Level
    # -------------------------------------------------------------------------
    box_top = patches.Rectangle((0.6, 7.5), 8.8, 6.3, fc="#ffffff", ec="#000000", lw=1.6, zorder=1)
    ax.add_patch(box_top)
    ax.text(5.0, 13.55, "Admin side DFD :- 1st Level", fontsize=11.5, fontweight="bold", ha="center", color="#000000")

    # Administrator Entity
    ent_adm = patches.Rectangle((1.0, 12.6), 2.2, 0.6, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
    ax.add_patch(ent_adm)
    ax.text(2.1, 12.9, "Administrator", fontsize=8.8, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

    # Admin Processes
    adm_procs = [
        {"num": "1.0", "name": "Login", "y": 12.5, "ds_id": "D1", "ds_name": "User Database",
         "req": "Admin request\nfor login", "res": "Admin gets the\nacknowledgement",
         "st_in": "Admin request\nfor login", "st_out": "Admin gets the\nacknowledgement"},
        {"num": "2.0", "name": "Manage\nUsers", "y": 11.1, "ds_id": "D1", "ds_name": "User Database",
         "req": "Requesting for\nManage Users", "res": "Get the response",
         "st_in": "Requesting for\nAdd/Edit Users", "st_out": "Get the response"},
        {"num": "3.0", "name": "Manage\nDocuments", "y": 9.7, "ds_id": "D2", "ds_name": "Document\nRepository",
         "req": "Requesting for\nManage Documents", "res": "Get the response",
         "st_in": "Requesting for\nmanage documents", "st_out": "Get the response"},
        {"num": "4.0", "name": "Monitor\nSystem", "y": 8.3, "ds_id": "D5", "ds_name": "System Logs",
         "req": "Requesting for\nMonitor System", "res": "System reports\nand statistics",
         "st_in": "Requesting for\nsystem logs", "st_out": "Display logs and\nprocessing status"}
    ]

    # Pre-calculated 6 bus coordinates under ent_adm [1.15 to 3.05]
    adm_bus_x = [1.15 + k * (1.9 / 6) for k in range(7)]

    # Draw Processes & Connections
    for idx, p in enumerate(adm_procs):
        py = p["y"]
        # Circle
        circ = patches.Circle((5.0, py), 0.52, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
        ax.add_patch(circ)
        ax.text(5.0, py + 0.12, p["num"], fontsize=8.5, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)
        ax.text(5.0, py - 0.14, p["name"], fontsize=7.2, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

        # Data store
        draw_open_data_store(ax, 7.0, py - 0.28, 2.0, 0.56, p["ds_id"], p["ds_name"], font_scale=0.9)

        # Lines between Process and Data Store
        ax.annotate("", xy=(7.0, py + 0.15), xytext=(5.52, py + 0.15),
                    arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color="#000000", lw=1.2), zorder=4)
        ax.text(6.26, py + 0.20, p["st_in"], fontsize=5.8, ha="center", va="bottom", color="#000000")

        ax.annotate("", xy=(5.52, py - 0.15), xytext=(7.0, py - 0.15),
                    arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color="#000000", lw=1.2), zorder=4)
        ax.text(6.26, py - 0.20, p["st_out"], fontsize=5.8, ha="center", va="top", color="#000000")

        # Lines between Entity and Process
        if idx == 0:
            # Direct horizontal lines for process 1.0
            ax.annotate("", xy=(4.48, py + 0.12), xytext=(3.2, py + 0.12),
                        arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color="#000000", lw=1.2), zorder=4)
            ax.text(3.84, py + 0.16, p["req"], fontsize=5.8, ha="center", va="bottom", color="#000000")

            ax.annotate("", xy=(3.2, py - 0.12), xytext=(4.48, py - 0.12),
                        arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color="#000000", lw=1.2), zorder=4)
            ax.text(3.84, py - 0.16, p["res"], fontsize=5.8, ha="center", va="top", color="#000000")
        else:
            bus_idx_req = 6 - (idx - 1) * 2
            bus_idx_res = bus_idx_req - 1
            bx_req = adm_bus_x[bus_idx_req]
            bx_res = adm_bus_x[bus_idx_res]

            # Request: Entity -> Process (bottom edge of ent_adm at y=12.6)
            ax.plot([bx_req, bx_req], [12.6, py + 0.12], color="#000000", lw=1.2, zorder=3)
            ax.annotate("", xy=(4.48, py + 0.12), xytext=(bx_req, py + 0.12),
                        arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color="#000000", lw=1.2), zorder=4)
            ax.text((bx_req + 4.48) / 2, py + 0.16, p["req"], fontsize=5.8, ha="center", va="bottom", color="#000000")

            # Response: Process -> Entity
            ax.plot([4.48, bx_res], [py - 0.12, py - 0.12], color="#000000", lw=1.2, zorder=3)
            ax.annotate("", xy=(bx_res, 12.6), xytext=(bx_res, py - 0.12),
                        arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color="#000000", lw=1.2), zorder=4)
            ax.text((bx_res + 4.48) / 2, py - 0.16, p["res"], fontsize=5.8, ha="center", va="top", color="#000000")

    ax.text(5.0, 7.25, "Admin Side DFD: 1st Level", fontsize=10.0, fontweight="bold", ha="center", color="#000000")

    # -------------------------------------------------------------------------
    # BOTTOM: User side DFD :- 1st Level
    # -------------------------------------------------------------------------
    box_bot = patches.Rectangle((0.6, 0.8), 8.8, 6.3, fc="#ffffff", ec="#000000", lw=1.6, zorder=1)
    ax.add_patch(box_bot)
    ax.text(5.0, 6.85, "User side DFD :- 1st Level", fontsize=11.5, fontweight="bold", ha="center", color="#000000")

    # User Entity
    ent_usr = patches.Rectangle((1.0, 5.8), 2.2, 0.75, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
    ax.add_patch(ent_usr)
    ax.text(2.1, 6.17, "Fraud Analyst /\nCompliance Officer /\nResearcher / Student", fontsize=7.2, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

    # User Processes
    usr_procs = [
        {"num": "1.0", "name": "Login", "y": 5.9, "ds_id": "D1", "ds_name": "User Database",
         "req": "Registration/Login", "res": "Login successfully",
         "st_in": "Registration/Login", "st_out": "Login successfully"},
        {"num": "2.0", "name": "Upload\nDocuments", "y": 4.8, "ds_id": "D2", "ds_name": "Document\nRepository",
         "req": "Requesting for\nUpload Documents", "res": "Document uploaded\nsuccessfully",
         "st_in": "Requesting for\nstore document", "st_out": "Document stored\nsuccessfully"},
        {"num": "3.0", "name": "Ask\nQuestion", "y": 3.7, "ds_id": "D3", "ds_name": "Vector Store\n(Embeddings)",
         "req": "Requesting for\nAsk Question", "res": "Display AI answer with\nsource citation",
         "st_in": "Requesting for\nrelevant chunks", "st_out": "Get relevant\nchunks"},
        {"num": "4.0", "name": "Verify\nSource", "y": 2.6, "ds_id": "D2", "ds_name": "Document\nRepository",
         "req": "Requesting for\nVerify Source", "res": "Display source document\nand page number",
         "st_in": "Requesting for\nsource document", "st_out": "Get document\nand page number"},
        {"num": "5.0", "name": "View Chat\nHistory", "y": 1.5, "ds_id": "D4", "ds_name": "Chat History\nDatabase",
         "req": "Requesting for\nChat History", "res": "Display previous questions\nand answers",
         "st_in": "Requesting for\nchat history", "st_out": "Get previous chats"}
    ]

    # Pre-calculated 9 bus coordinates under ent_usr [1.15 to 3.05]
    usr_bus_x = [1.15 + k * (1.9 / 8) for k in range(9)]

    for idx, p in enumerate(usr_procs):
        py = p["y"]
        # Circle
        circ = patches.Circle((5.0, py), 0.45, fc="#ffffff", ec="#000000", lw=1.5, zorder=3)
        ax.add_patch(circ)
        ax.text(5.0, py + 0.10, p["num"], fontsize=8.0, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)
        ax.text(5.0, py - 0.12, p["name"], fontsize=6.8, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

        # Data store
        draw_open_data_store(ax, 7.0, py - 0.25, 2.0, 0.50, p["ds_id"], p["ds_name"], font_scale=0.85)

        # Lines between Process and Data Store
        ax.annotate("", xy=(7.0, py + 0.12), xytext=(5.45, py + 0.12),
                    arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.30", color="#000000", lw=1.2), zorder=4)
        ax.text(6.22, py + 0.16, p["st_in"], fontsize=5.5, ha="center", va="bottom", color="#000000")

        ax.annotate("", xy=(5.45, py - 0.12), xytext=(7.0, py - 0.12),
                    arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.30", color="#000000", lw=1.2), zorder=4)
        ax.text(6.22, py - 0.16, p["st_out"], fontsize=5.5, ha="center", va="top", color="#000000")

        # Lines between Entity and Process
        if idx == 0:
            ax.annotate("", xy=(4.55, py + 0.10), xytext=(3.2, py + 0.10),
                        arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.30", color="#000000", lw=1.2), zorder=4)
            ax.text(3.87, py + 0.14, p["req"], fontsize=5.5, ha="center", va="bottom", color="#000000")

            ax.annotate("", xy=(3.2, py - 0.10), xytext=(4.55, py - 0.10),
                        arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.30", color="#000000", lw=1.2), zorder=4)
            ax.text(3.87, py - 0.14, p["res"], fontsize=5.5, ha="center", va="top", color="#000000")
        else:
            bus_idx_req = 8 - (idx - 1) * 2
            bus_idx_res = bus_idx_req - 1
            bx_req = usr_bus_x[bus_idx_req]
            bx_res = usr_bus_x[bus_idx_res]

            # Request: Entity -> Process (bottom edge of ent_usr at y=5.8)
            ax.plot([bx_req, bx_req], [5.8, py + 0.10], color="#000000", lw=1.2, zorder=3)
            ax.annotate("", xy=(4.55, py + 0.10), xytext=(bx_req, py + 0.10),
                        arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.30", color="#000000", lw=1.2), zorder=4)
            ax.text((bx_req + 4.55) / 2, py + 0.14, p["req"], fontsize=5.5, ha="center", va="bottom", color="#000000")

            # Response: Process -> Entity
            ax.plot([4.55, bx_res], [py - 0.10, py - 0.10], color="#000000", lw=1.2, zorder=3)
            ax.annotate("", xy=(bx_res, 5.8), xytext=(bx_res, py - 0.10),
                        arrowprops=dict(arrowstyle="->,head_width=0.20,head_length=0.30", color="#000000", lw=1.2), zorder=4)
            ax.text((bx_res + 4.55) / 2, py - 0.14, p["res"], fontsize=5.5, ha="center", va="top", color="#000000")

    ax.text(5.0, 0.55, "User Side DFD: 1st Level", fontsize=10.0, fontweight="bold", ha="center", color="#000000")

    out_path = OUTPUT_DIR / "dfd_level_1_smartdoc.png"
    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated: {out_path}")


# =============================================================================
# =============================================================================
# 4. ACTIVITY DIAGRAM (Page 34 of user photos)
# =============================================================================
def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 15.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 15.5)
    ax.axis("off")

    # Header and Footer text
    ax.text(0.6, 15.1, "4.2.1.3 Activity Diagram", fontsize=10, ha="left", color="#475569")
    ax.text(9.9, 15.1, "Design | 2026 - 2027", fontsize=10, ha="right", color="#64748b")
    ax.plot([0.6, 9.9], [14.95, 14.95], color="#cbd5e1", lw=1.2)

    ax.text(0.6, 0.4, "AI-Powered Document Question Answering System for Fraud Prevention", fontsize=9, ha="left", color="#475569")
    ax.text(9.9, 0.4, "34", fontsize=9.5, fontweight="bold", ha="right", color="#0f172a",
            bbox=dict(boxstyle="square,pad=0.25", fc="#cbd5e1", ec="none"))
    ax.plot([0.6, 9.9], [0.55, 0.55], color="#cbd5e1", lw=1.2)

    # Outer border
    border = patches.Rectangle((0.6, 0.8), 9.3, 13.9, fc="#ffffff", ec="#000000", lw=1.8, zorder=1)
    ax.add_patch(border)

    # Title inside
    ax.text(5.25, 14.35, "ACTIVITY DIAGRAM", fontsize=13, fontweight="bold", ha="center", color="#000000")
    ax.text(5.25, 14.05, "AI-Powered Document Question Answering System for Fraud Prevention\n(Document Processing to Answer Generation)",
            fontsize=8.5, ha="center", va="center", color="#334155")

    # Swimlane columns (4 lanes)
    lanes = [
        {"name": "User", "x1": 0.6, "x2": 2.8, "cx": 1.7},
        {"name": "System", "x1": 2.8, "x2": 5.4, "cx": 4.1},
        {"name": "Vector Database", "x1": 5.4, "x2": 7.8, "cx": 6.6},
        {"name": "LLM Service", "x1": 7.8, "x2": 9.9, "cx": 8.85}
    ]

    header_y = 13.4
    ax.plot([0.6, 9.9], [header_y, header_y], color="#000000", lw=1.4, zorder=2)

    for l in lanes:
        ax.text(l["cx"], 13.55, l["name"], fontsize=9.5, fontweight="bold", ha="center", va="center", color="#000000")
        if l["x2"] < 9.9:
            ax.plot([l["x2"], l["x2"]], [0.8, header_y + 0.3], color="#000000", lw=1.2, zorder=2)

    def draw_action_box(cx, cy, w, h, text, fontsize=7.2):
        box = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                     boxstyle="round,pad=0.08,rounding_size=0.12",
                                     fc="#ffffff", ec="#000000", lw=1.2, zorder=4)
        ax.add_patch(box)
        ax.text(cx, cy, text, fontsize=fontsize, ha="center", va="center", color="#000000", zorder=5)

    def draw_decision_diamond(cx, cy, w, h, text, fontsize=6.8):
        pts = [[cx, cy + h/2], [cx + w/2, cy], [cx, cy - h/2], [cx - w/2, cy]]
        poly = patches.Polygon(pts, closed=True, fc="#ffffff", ec="#000000", lw=1.2, zorder=4)
        ax.add_patch(poly)
        ax.text(cx, cy, text, fontsize=fontsize, ha="center", va="center", color="#000000", zorder=5)

    # -------------------------------------------------------------------------
    # Activity Nodes
    # -------------------------------------------------------------------------
    u_cx = 1.7
    s_cx = 4.1
    v_cx = 6.6
    l_cx = 8.85

    # 1. Start node in User lane
    start_circle = patches.Circle((u_cx, 13.0), 0.12, fc="#000000", ec="#000000", zorder=5)
    ax.add_patch(start_circle)

    # Arrow to Login
    ax.annotate("", xy=(u_cx, 12.65), xytext=(u_cx, 12.88),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)

    # Login box
    draw_action_box(u_cx, 12.5, 1.0, 0.32, "Login", fontsize=7.5)

    # Arrow to Valid Credentials diamond
    ax.annotate("", xy=(u_cx, 12.0), xytext=(u_cx, 12.34),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)

    # Diamond: Valid Credentials?
    draw_decision_diamond(u_cx, 11.75, 1.1, 0.5, "Valid\nCredentials?", fontsize=6.2)

    # "No" loop back to Login
    ax.plot([u_cx - 0.55, 0.95], [11.75, 11.75], color="#000000", lw=1.2, zorder=4)
    ax.plot([0.95, 0.95], [11.75, 12.5], color="#000000", lw=1.2, zorder=4)
    ax.annotate("", xy=(u_cx - 0.5, 12.5), xytext=(0.95, 12.5),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    ax.text(1.1, 11.85, "No", fontsize=6.2, ha="center", va="bottom", color="#000000")

    # "Yes" arrow to Dashboard
    ax.annotate("", xy=(u_cx, 11.1), xytext=(u_cx, 11.5),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    ax.text(u_cx + 0.12, 11.3, "Yes", fontsize=6.2, ha="left", va="center", color="#000000")

    # Dashboard box
    draw_action_box(u_cx, 10.95, 1.1, 0.30, "Dashboard", fontsize=7.2)

    # Arrow to Upload Document
    ax.annotate("", xy=(u_cx, 10.55), xytext=(u_cx, 10.8),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)

    # Upload Document box
    draw_action_box(u_cx, 10.35, 1.1, 0.38, "Upload\nDocument", fontsize=7.0)

    # Arrow from Upload Document across to System: Validate Document
    ax.annotate("", xy=(s_cx - 0.7, 10.35), xytext=(u_cx + 0.55, 10.35),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)

    # System: Validate Document
    draw_action_box(s_cx, 10.35, 1.4, 0.32, "Validate Document", fontsize=7.0)

    # Arrow to Valid Document? diamond
    ax.annotate("", xy=(s_cx, 9.95), xytext=(s_cx, 10.19),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)

    # Diamond: Valid Document?
    draw_decision_diamond(s_cx, 9.7, 1.1, 0.5, "Valid\nDocument?", fontsize=6.2)

    # "No" arrow to Show Error Message
    ax.plot([s_cx + 0.55, 5.15], [9.7, 9.7], color="#000000", lw=1.2, zorder=4)
    ax.annotate("", xy=(5.15, 9.43), xytext=(5.15, 9.7),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    ax.text(4.8, 9.8, "No", fontsize=6.2, ha="center", va="bottom", color="#000000")

    draw_action_box(5.15, 9.25, 0.85, 0.36, "Show Error\nMessage", fontsize=6.0)

    # From Show Error Message back into Extract Text
    ax.plot([5.15, 5.15], [9.07, 9.05], color="#000000", lw=1.2, zorder=4)
    ax.annotate("", xy=(s_cx + 0.725, 9.05), xytext=(5.15, 9.05),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)

    # "Yes" arrow to Extract Text from Document
    ax.annotate("", xy=(s_cx, 9.2), xytext=(s_cx, 9.45),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    ax.text(s_cx + 0.12, 9.35, "Yes", fontsize=6.2, ha="left", va="center", color="#000000")

    # Extract Text from Document
    draw_action_box(s_cx, 9.05, 1.45, 0.32, "Extract Text from\nDocument", fontsize=6.8)

    # Clean & Preprocess Text
    ax.annotate("", xy=(s_cx, 8.65), xytext=(s_cx, 8.89),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 8.5, 1.45, 0.32, "Clean & Preprocess\nText", fontsize=6.8)

    # Split into Chunks
    ax.annotate("", xy=(s_cx, 8.1), xytext=(s_cx, 8.34),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 7.95, 1.3, 0.32, "Split into\nChunks", fontsize=6.8)

    # Generate Embeddings for Chunks
    ax.annotate("", xy=(s_cx, 7.55), xytext=(s_cx, 7.79),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 7.35, 1.55, 0.36, "Generate Embeddings\nfor Chunks", fontsize=6.8)

    # Arrow to Vector DB: Store Embeddings in Vector DB
    ax.annotate("", xy=(v_cx - 0.75, 7.35), xytext=(s_cx + 0.775, 7.35),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(v_cx, 7.35, 1.5, 0.36, "Store Embeddings\nin Vector DB", fontsize=6.8)

    # Flow from Store Embeddings down and left to Preprocess Question line
    ax.plot([v_cx, v_cx], [7.17, 7.02], color="#000000", lw=1.2, zorder=4)
    ax.plot([v_cx, 2.25], [7.02, 7.02], color="#000000", lw=1.2, zorder=4)
    # Line from Upload Document down
    ax.plot([2.25, 2.25], [10.15, 6.7], color="#000000", lw=1.2, zorder=4)

    # -------------------------------------------------------------------------
    # Second phase: Enter Question -> Answer
    # -------------------------------------------------------------------------
    # User: Enter Question
    draw_action_box(u_cx, 6.7, 1.15, 0.32, "Enter Question", fontsize=7.0)

    # Arrow to System: Preprocess Question (passing through x=2.25 junction)
    ax.annotate("", xy=(s_cx - 0.7, 6.7), xytext=(u_cx + 0.575, 6.7),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 6.7, 1.4, 0.32, "Preprocess\nQuestion", fontsize=6.8)

    # Generate Query Embedding
    ax.annotate("", xy=(s_cx, 6.3), xytext=(s_cx, 6.54),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 6.1, 1.4, 0.36, "Generate Query\nEmbedding", fontsize=6.8)

    # Arrow to Vector DB: Semantic Search
    ax.annotate("", xy=(v_cx - 0.8, 6.1), xytext=(s_cx + 0.7, 6.1),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(v_cx, 6.1, 1.6, 0.44, "Semantic Search\n(Find Top-K Relevant\nChunks)", fontsize=6.5)

    # Clean single elbow arrow from bottom of Semantic Search to Receive Relevant Chunks
    ax.plot([v_cx, v_cx], [5.88, 5.5], color="#000000", lw=1.2, zorder=4)
    ax.annotate("", xy=(s_cx + 0.7, 5.5), xytext=(v_cx, 5.5),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 5.5, 1.4, 0.34, "Receive Relevant\nChunks", fontsize=6.8)

    # Build Prompt with Context
    ax.annotate("", xy=(s_cx, 5.1), xytext=(s_cx, 5.33),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 4.9, 1.45, 0.34, "Build Prompt with\nContext", fontsize=6.8)

    # Arrow to LLM Service: Generate Answer
    ax.annotate("", xy=(l_cx - 0.75, 4.9), xytext=(s_cx + 0.725, 4.9),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(l_cx, 4.9, 1.5, 0.36, "Generate Answer\n(Using LLM)", fontsize=6.8)

    # Dashed return arrow: Return Answer from LLM bottom to Receive Answer
    ax.plot([l_cx, l_cx], [4.72, 4.3], color="#000000", lw=1.2, linestyle="--", zorder=4)
    ax.annotate("", xy=(s_cx + 0.725, 4.3), xytext=(l_cx, 4.3),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2, linestyle="--"), zorder=5)
    ax.text((s_cx + l_cx) / 2, 4.38, "Return Answer", fontsize=6.2, ha="center", va="bottom", color="#000000")

    # Receive Answer from LLM
    draw_action_box(s_cx, 4.3, 1.45, 0.34, "Receive Answer\nfrom LLM", fontsize=6.8)

    # Extract Sources and References
    ax.annotate("", xy=(s_cx, 3.9), xytext=(s_cx, 4.13),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 3.7, 1.45, 0.34, "Extract Sources and\nReferences", fontsize=6.8)

    # Save Question, Answer, Sources & Chat History in Database
    ax.annotate("", xy=(s_cx, 3.3), xytext=(s_cx, 3.53),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(s_cx, 3.0, 1.55, 0.50, "Save Question, Answer,\nSources & Chat History\nin Database", fontsize=6.5)

    # Branch 1 to LLM/Database column: Store in Database
    ax.annotate("", xy=(l_cx - 0.65, 3.0), xytext=(s_cx + 0.775, 3.0),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(l_cx, 3.0, 1.3, 0.36, "Store in\nDatabase", fontsize=6.8)

    # Branch 2 back to User: View Answer with Sources
    ax.annotate("", xy=(u_cx + 0.75, 3.0), xytext=(s_cx - 0.775, 3.0),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)
    draw_action_box(u_cx, 3.0, 1.5, 0.36, "View Answer with\nSources", fontsize=6.8)

    # Final End node in User lane
    ax.annotate("", xy=(u_cx, 2.3), xytext=(u_cx, 2.82),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.28", color="#000000", lw=1.2), zorder=5)

    outer_end = patches.Circle((u_cx, 2.15), 0.16, fc="#ffffff", ec="#000000", lw=1.4, zorder=5)
    inner_end = patches.Circle((u_cx, 2.15), 0.10, fc="#000000", ec="#000000", zorder=6)
    ax.add_patch(outer_end)
    ax.add_patch(inner_end)

    out_path = OUTPUT_DIR / "activity_diagram_smartdoc.png"
    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated: {out_path}")


# =============================================================================
# 5. SEQUENCE DIAGRAM (Page 33 of user photos)
# =============================================================================
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(14.2, 10.8), dpi=300)
    ax.set_xlim(0, 14.2)
    ax.set_ylim(0, 10.8)
    ax.axis("off")

    # Header and Footer text
    ax.text(0.6, 10.45, "4.2.1.2 Sequence Diagram", fontsize=10, ha="left", color="#475569")
    ax.text(13.6, 10.45, "Design | 2026 - 2027", fontsize=10, ha="right", color="#64748b")
    ax.plot([0.6, 13.6], [10.30, 10.30], color="#cbd5e1", lw=1.2)

    ax.text(0.6, 0.35, "AI-Powered Document Question Answering System for Fraud Prevention", fontsize=9, ha="left", color="#475569")
    ax.text(13.6, 0.35, "33", fontsize=9.5, fontweight="bold", ha="right", color="#0f172a",
            bbox=dict(boxstyle="square,pad=0.25", fc="#cbd5e1", ec="none"))
    ax.plot([0.6, 13.6], [0.50, 0.50], color="#cbd5e1", lw=1.2)

    # Outer border
    border = patches.Rectangle((0.6, 0.65), 13.0, 9.45, fc="#ffffff", ec="#000000", lw=1.8, zorder=1)
    ax.add_patch(border)

    # Title
    ax.text(7.1, 9.75, "SEQUENCE DIAGRAM", fontsize=13, fontweight="bold", ha="center", color="#000000")
    ax.text(7.1, 9.45, "AI-Powered Document Question Answering System for Fraud Prevention using Domain-Specific RAG\n( Ask Question & Get Answer )",
            fontsize=8.8, ha="center", va="center", color="#334155")

    # 8 Lifelines
    lifelines = [
        {"name": "User", "is_actor": True, "x": 1.15},
        {"name": "Web UI", "is_actor": False, "x": 2.65},
        {"name": "API Server", "is_actor": False, "x": 4.15},
        {"name": "Query\nProcessor", "is_actor": False, "x": 5.65},
        {"name": "Embedding\nService", "is_actor": False, "x": 7.20},
        {"name": "Vector DB\n(ChromaDB)", "is_actor": False, "x": 8.75},
        {"name": "LLM Service\n(Gemini / Llama)", "is_actor": False, "x": 10.45},
        {"name": "Database", "is_actor": False, "x": 12.15}
    ]

    top_box_y = 8.85
    bottom_line_y = 1.15

    for ll in lifelines:
        lx = ll["x"]
        if ll["is_actor"]:
            draw_stick_man(ax, lx, top_box_y - 0.22, scale=0.6, label="User")
            # Lifeline dashed vertical
            ax.plot([lx, lx], [top_box_y - 0.72, bottom_line_y], color="#94a3b8", lw=1.2, linestyle="--", zorder=2)
        else:
            box = patches.Rectangle((lx - 0.62, top_box_y - 0.36), 1.24, 0.46, fc="#ffffff", ec="#000000", lw=1.3, zorder=3)
            ax.add_patch(box)
            ax.text(lx, top_box_y - 0.13, ll["name"], fontsize=7.2, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)
            # Lifeline dashed vertical
            ax.plot([lx, lx], [top_box_y - 0.36, bottom_line_y], color="#94a3b8", lw=1.2, linestyle="--", zorder=2)

    # Activation bars
    def draw_activation(lx, y_top, y_bot, width=0.15):
        rect = patches.Rectangle((lx - width/2, y_bot), width, y_top - y_bot, fc="#f8fafc", ec="#000000", lw=1.1, zorder=3)
        ax.add_patch(rect)

    draw_activation(2.65, 8.0, 2.70)     # Web UI (msg 1 to 12)
    draw_activation(4.15, 7.6, 3.20)     # API Server (msg 2 to 11)
    draw_activation(5.65, 7.2, 1.70)     # Query Processor (msg 3 to 14)
    draw_activation(7.20, 6.7, 5.25)     # Embedding Service (msg 4 to 7)
    draw_activation(8.75, 6.25, 5.75)    # Vector DB (msg 5 to 6)
    draw_activation(10.45, 4.75, 4.25)   # LLM Service (msg 8 to 9)
    draw_activation(12.15, 2.20, 1.70)   # Database (msg 13 to 14)

    # 14 Numbered Messages with abundant vertical spacing
    messages = [
        # 1. User -> Web UI (sync)
        {"num": "1. Enter Question", "x1": 1.15, "x2": 2.575, "y": 8.00, "is_return": False, "txt_y": 8.12},
        # 2. Web UI -> API Server (sync)
        {"num": "2. Send Question", "x1": 2.725, "x2": 4.075, "y": 7.60, "is_return": False, "txt_y": 7.72},
        # 3. API Server -> Query Processor (sync)
        {"num": "3. Process Question", "x1": 4.225, "x2": 5.575, "y": 7.20, "is_return": False, "txt_y": 7.32},
        # 4. Query Processor -> Embedding Service (sync)
        {"num": "4. Generate Query Embedding", "x1": 5.725, "x2": 7.125, "y": 6.70, "is_return": False, "txt_y": 6.82},
        # 5. Embedding Service -> Vector DB (sync)
        {"num": "5. Semantic Search\n(Top-K Chunks)", "x1": 7.275, "x2": 8.675, "y": 6.25, "is_return": False, "txt_y": 6.38},
        # 6. Vector DB -> Embedding Service (return)
        {"num": "6. Relevant Chunks", "x1": 8.675, "x2": 7.275, "y": 5.75, "is_return": True, "txt_y": 5.87},
        # 7. Embedding Service -> Query Processor (return)
        {"num": "7. Return Relevant Chunks", "x1": 7.125, "x2": 5.725, "y": 5.25, "is_return": True, "txt_y": 5.37},
        # 8. Query Processor -> LLM Service (sync)
        {"num": "8. Build Prompt with Context\n& Send to LLM", "x1": 5.725, "x2": 10.375, "y": 4.75, "is_return": False, "txt_y": 4.88},
        # 9. LLM Service -> Query Processor (return)
        {"num": "9. Generate Answer", "x1": 10.375, "x2": 5.725, "y": 4.25, "is_return": True, "txt_y": 4.37},
        # 10. Query Processor -> API Server (return)
        {"num": "10. Return Answer\nwith Sources", "x1": 5.575, "x2": 4.225, "y": 3.70, "is_return": True, "txt_y": 3.82},
        # 11. API Server -> Web UI (return)
        {"num": "11. Send Answer\n& Sources", "x1": 4.075, "x2": 2.725, "y": 3.20, "is_return": True, "txt_y": 3.32},
        # 12. Web UI -> User (return)
        {"num": "12. Display Answer\nwith Sources", "x1": 2.575, "x2": 1.15, "y": 2.70, "is_return": True, "txt_y": 2.82},
        # 13. Query Processor -> Database (sync)
        {"num": "13. Save Question, Answer,\nChat History & Sources", "x1": 5.725, "x2": 12.075, "y": 2.20, "is_return": False, "txt_y": 2.32},
        # 14. Database -> Query Processor (return)
        {"num": "14. Save Confirmation", "x1": 12.075, "x2": 5.725, "y": 1.70, "is_return": True, "txt_y": 1.82}
    ]

    for m in messages:
        x1, x2, my = m["x1"], m["x2"], m["y"]
        linestyle = "--" if m["is_return"] else "-"
        arrowstyle = "->,head_width=0.22,head_length=0.32"

        ax.annotate("", xy=(x2, my), xytext=(x1, my),
                    arrowprops=dict(arrowstyle=arrowstyle, color="#000000", lw=1.2, linestyle=linestyle), zorder=5)

        mid_x = (x1 + x2) / 2
        ax.text(mid_x, m["txt_y"], m["num"], fontsize=6.8, ha="center", va="bottom", color="#000000",
                bbox=dict(boxstyle="square,pad=0.08", fc="#ffffff", ec="none"))

    # Legend in bottom left corner
    leg_box = patches.Rectangle((0.85, 0.78), 3.2, 0.72, fc="#ffffff", ec="#cbd5e1", lw=1.0, zorder=3)
    ax.add_patch(leg_box)
    ax.plot([1.0, 1.7], [1.26, 1.26], color="#000000", lw=1.2)
    ax.annotate("", xy=(1.7, 1.26), xytext=(1.0, 1.26),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.3", color="#000000", lw=1.2))
    ax.text(1.85, 1.26, "Synchronous Call", fontsize=7.2, va="center", color="#000000")

    ax.plot([1.0, 1.7], [0.94, 0.94], color="#000000", lw=1.2, linestyle="--")
    ax.annotate("", xy=(1.7, 0.94), xytext=(1.0, 0.94),
                arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.3", color="#000000", lw=1.2, linestyle="--"))
    ax.text(1.85, 0.94, "Return / Response", fontsize=7.2, va="center", color="#000000")

    out_path = OUTPUT_DIR / "sequence_diagram_smartdoc.png"
    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated: {out_path}")


# =============================================================================
# 6. CLASS DIAGRAM (Page 33 of user photos - Top Half)
# =============================================================================
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(15.0, 11.0), dpi=300)
    ax.set_xlim(0, 15.0)
    ax.set_ylim(0, 11.0)
    ax.axis("off")

    # Header and Footer text
    ax.text(0.6, 10.65, "4.2.1.1 Class Diagram", fontsize=10, ha="left", color="#475569")
    ax.text(14.4, 10.65, "Design | 2026 - 2027", fontsize=10, ha="right", color="#64748b")
    ax.plot([0.6, 14.4], [10.50, 10.50], color="#cbd5e1", lw=1.2)

    ax.text(0.6, 0.35, "AI-Powered Document Question Answering System for Fraud Prevention", fontsize=9, ha="left", color="#475569")
    ax.text(14.4, 0.35, "33", fontsize=9.5, fontweight="bold", ha="right", color="#0f172a",
            bbox=dict(boxstyle="square,pad=0.25", fc="#cbd5e1", ec="none"))
    ax.plot([0.6, 14.4], [0.50, 0.50], color="#cbd5e1", lw=1.2)

    # Outer border
    border = patches.Rectangle((0.6, 0.65), 13.8, 9.65, fc="#ffffff", ec="#000000", lw=1.8, zorder=1)
    ax.add_patch(border)

    # Title
    ax.text(7.5, 9.95, "CLASS DIAGRAM", fontsize=13, fontweight="bold", ha="center", color="#000000")
    ax.text(7.5, 9.68, "AI-Powered Document Question Answering System for Fraud Prevention\nusing Domain-Specific RAG",
            fontsize=8.5, ha="center", va="center", color="#334155")

    def draw_uml_class(ax, cx, cy, w, h, name, attrs, methods, font_size=5.8):
        # Total box
        x = cx - w / 2
        y = cy - h / 2
        rect = patches.Rectangle((x, y), w, h, fc="#ffffff", ec="#000000", lw=1.3, zorder=3)
        ax.add_patch(rect)

        # Title compartment height
        title_h = 0.32
        ax.plot([x, x + w], [cy + h/2 - title_h, cy + h/2 - title_h], color="#000000", lw=1.1, zorder=3)
        ax.text(cx, cy + h/2 - title_h/2, name, fontsize=font_size + 1.2, fontweight="bold", ha="center", va="center", color="#000000", zorder=4)

        # Attribute compartment height based on number of attributes
        attr_line_h = 0.165
        attr_h = max(len(attrs) * attr_line_h + 0.1, 0.25)
        meth_sep_y = cy + h/2 - title_h - attr_h

        if len(methods) > 0:
            ax.plot([x, x + w], [meth_sep_y, meth_sep_y], color="#000000", lw=1.1, zorder=3)

        # Draw attributes
        start_attr_y = cy + h/2 - title_h - 0.10
        for i, att in enumerate(attrs):
            ax.text(x + 0.08, start_attr_y - i * attr_line_h, att, fontsize=font_size, ha="left", va="top", color="#000000", zorder=4)

        # Draw methods
        start_meth_y = meth_sep_y - 0.08
        for j, meth in enumerate(methods):
            ax.text(x + 0.08, start_meth_y - j * attr_line_h, meth, fontsize=font_size, ha="left", va="top", color="#000000", zorder=4)

    # 1. User
    draw_uml_class(ax, 1.85, 8.0, 1.9, 2.3, "User",
                   ["- userId: int", "- name: string", "- email: string", "- password: string", "- role: Role", "- status: string", "- createdAt: datetime"],
                   ["+ login(email, password): bool", "+ logout(): void", "+ updateProfile(): void"])

    # 2. Role
    draw_uml_class(ax, 4.35, 8.2, 1.7, 1.8, "Role",
                   ["- roleId: int", "- roleName: string", "- description: string"],
                   ["+ addRole(): void", "+ updateRole(): void", "+ deleteRole(): void"])

    # 3. Document
    draw_uml_class(ax, 7.35, 8.0, 2.0, 2.3, "Document",
                   ["- docId: int", "- title: string", "- filePath: string", "- fileType: string", "- uploadedAt: datetime", "- uploadedBy: int", "- status: string"],
                   ["+ upload(): void", "+ delete(): void", "+ getMetadata(): Document"])

    # 4. DocumentChunk
    draw_uml_class(ax, 10.35, 8.2, 1.8, 1.8, "DocumentChunk",
                   ["- chunkId: int", "- docId: int", "- content: text", "- pageNo: int", "- chunkIndex: int"],
                   ["+ getText(): string"])

    # 5. Embedding
    draw_uml_class(ax, 13.20, 8.2, 1.8, 1.8, "Embedding",
                   ["- embeddingId: int", "- chunkId: int", "- vector: vector<float>", "- model: string"],
                   ["+ getVector(): vector<float>"])

    # 6. ChatSession
    draw_uml_class(ax, 3.90, 5.75, 2.2, 1.7, "ChatSession",
                   ["- sessionId: int", "- userId: int", "- startTime: datetime", "- endTime: datetime"],
                   ["+ getHistory(): List<ChatMessage>", "+ endSession(): void"])

    # 7. ChatMessage
    draw_uml_class(ax, 6.85, 5.75, 2.1, 1.6, "ChatMessage",
                   ["- messageId: int", "- sessionId: int", "- role: string  // USER or SYSTEM", "- message: text", "- timestamp: datetime"],
                   ["+ save(): void"])

    # 8. Question
    draw_uml_class(ax, 9.80, 5.75, 1.9, 1.6, "Question",
                   ["- questionId: int", "- sessionId: int", "- questionText: text", "- createdAt: datetime"],
                   ["+ getEmbedding(): vector<float>"])

    # 9. VectorStore
    draw_uml_class(ax, 13.15, 6.0, 2.4, 1.8, "VectorStore",
                   ["- storeId: int", "- storeName: string", "- vectorDB: string", "- description: string"],
                   ["+ addEmbedding(embedding): void", "+ search(queryVector, topK): List<Chunk>"], font_size=5.4)

    # 10. RetrievedChunk
    draw_uml_class(ax, 13.15, 4.05, 2.0, 1.45, "RetrievedChunk",
                   ["- retrievedId: int", "- questionId: int", "- chunkId: int", "- score: float", "- rank: int"], [])

    # 11. Source
    draw_uml_class(ax, 13.15, 2.20, 2.0, 1.55, "Source",
                   ["- sourceId: int", "- docId: int", "- pageNo: int", "- chunkText: text"],
                   ["+ getSourceInfo(): string"])

    # 12. Answer
    draw_uml_class(ax, 9.80, 3.20, 1.9, 1.5, "Answer",
                   ["- answerId: int", "- questionId: int", "- answerText: text", "- createdAt: datetime"],
                   ["+ getSources(): List<Source>"])

    # 13. LLMService
    draw_uml_class(ax, 6.85, 3.20, 2.1, 1.5, "LLMService",
                   ["- serviceId: int", "- modelName: string", "- apiProvider: string", "- apiKey: string"],
                   ["+ generateAnswer(prompt, context): string"], font_size=5.4)

    # 14. PromptTemplate
    draw_uml_class(ax, 3.90, 3.20, 1.9, 1.5, "PromptTemplate",
                   ["- templateId: int", "- name: string", "- templateText: text", "- description: string"],
                   ["+ getTemplate(): string"])

    # 15. SystemConfig
    draw_uml_class(ax, 1.65, 3.20, 1.7, 1.6, "SystemConfig",
                   ["- configId: int", "- key: string", "- value: string", "- description: string"],
                   ["+ getValue(key): string", "+ updateValue(key, value): void"])

    # -------------------------------------------------------------------------
    # Relationship Lines
    # -------------------------------------------------------------------------
    def draw_assoc_line(p1, p2, label=None, card1=None, card2=None, linestyle="-", is_arrow=False):
        if is_arrow:
            ax.annotate("", xy=p2, xytext=p1,
                        arrowprops=dict(arrowstyle="->,head_width=0.2,head_length=0.3", color="#000000", lw=1.1, linestyle=linestyle), zorder=4)
        else:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#000000", lw=1.1, linestyle=linestyle, zorder=4)

        if label:
            mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2 + 0.12
            ax.text(mx, my, label, fontsize=6.2, ha="center", va="bottom", color="#000000")

        # Direction-aware cardinality placement along the segment
        if card1:
            dx = 0.15 if p2[0] >= p1[0] else -0.15
            dy = 0.10 if p2[1] >= p1[1] else -0.15
            if abs(p2[0] - p1[0]) > abs(p2[1] - p1[1]):
                ax.text(p1[0] + dx, p1[1] + 0.08, card1, fontsize=6.2, ha="center", va="bottom", color="#000000")
            else:
                ax.text(p1[0] + 0.10, p1[1] + dy, card1, fontsize=6.2, ha="left", va="center", color="#000000")

        if card2:
            dx = -0.15 if p2[0] >= p1[0] else 0.15
            dy = -0.10 if p2[1] >= p1[1] else 0.15
            if abs(p2[0] - p1[0]) > abs(p2[1] - p1[1]):
                ax.text(p2[0] + dx, p2[1] + 0.08, card2, fontsize=6.2, ha="center", va="bottom", color="#000000")
            else:
                ax.text(p2[0] + 0.10, p2[1] + dy, card2, fontsize=6.2, ha="left", va="center", color="#000000")

    # User - Role
    draw_assoc_line((2.80, 8.2), (3.50, 8.2), card1="1", card2="1")

    # Role - Document (uploads)
    draw_assoc_line((5.20, 8.2), (6.35, 8.2), label="uploads", card1="*", card2="1")

    # Document - DocumentChunk
    draw_assoc_line((8.35, 8.2), (9.45, 8.2), card1="1", card2="*")

    # DocumentChunk - Embedding
    draw_assoc_line((11.25, 8.2), (12.30, 8.2), card1="1", card2="1")

    # DocumentChunk - VectorStore (elbow line)
    ax.plot([10.35, 10.35], [7.30, 6.70], color="#000000", lw=1.1, zorder=4)
    ax.plot([10.35, 11.95], [6.70, 6.70], color="#000000", lw=1.1, zorder=4)

    # Embedding - VectorStore
    draw_assoc_line((13.20, 7.30), (13.20, 6.90), card1="1", card2="1")

    # User - ChatSession
    ax.plot([2.40, 2.40], [6.85, 5.75], color="#000000", lw=1.1, zorder=4)
    ax.plot([2.40, 2.80], [5.75, 5.75], color="#000000", lw=1.1, zorder=4)
    ax.text(2.48, 6.70, "1", fontsize=6.2, color="#000000")
    ax.text(2.72, 5.85, "*", fontsize=6.2, color="#000000")

    # ChatSession - ChatMessage
    draw_assoc_line((5.00, 5.75), (5.80, 5.75), card1="1", card2="*")

    # ChatMessage - Question
    draw_assoc_line((7.90, 5.75), (8.85, 5.75), card1="*", card2="1")

    # Question - Answer (vertical line between 4.95 and 3.95)
    ax.plot([9.80, 9.80], [4.95, 3.95], color="#000000", lw=1.1, zorder=4)
    ax.text(9.90, 4.80, "1", fontsize=6.2, color="#000000")
    ax.text(9.90, 4.05, "1", fontsize=6.2, color="#000000")

    # Question - RetrievedChunk
    ax.plot([10.75, 11.85], [5.75, 5.75], color="#000000", lw=1.1, zorder=4)
    ax.plot([11.85, 11.85], [5.75, 4.05], color="#000000", lw=1.1, zorder=4)
    ax.plot([11.85, 12.15], [4.05, 4.05], color="#000000", lw=1.1, zorder=4)
    ax.text(10.85, 5.85, "1", fontsize=6.2, color="#000000")
    ax.text(12.05, 4.15, "*", fontsize=6.2, color="#000000")

    # RetrievedChunk - Source
    draw_assoc_line((13.15, 3.32), (13.15, 2.98), card1="*", card2="1")

    # Answer - LLMService (uses)
    draw_assoc_line((8.85, 3.20), (7.90, 3.20), label="uses", card1="1", card2="1", linestyle="--")

    # PromptTemplate - LLMService (uses)
    draw_assoc_line((4.85, 3.20), (5.80, 3.20), label="uses", card1="1", card2="*", linestyle="--")

    # User - SystemConfig
    ax.plot([1.65, 1.65], [6.85, 4.00], color="#000000", lw=1.1, zorder=4)
    ax.text(1.75, 6.70, "1", fontsize=6.2, color="#000000")
    ax.text(1.75, 4.10, "1", fontsize=6.2, color="#000000")

    out_path = OUTPUT_DIR / "class_diagram_smartdoc.png"
    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    generate_use_case_diagram()
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_activity_diagram()
    generate_sequence_diagram()
    generate_class_diagram()

