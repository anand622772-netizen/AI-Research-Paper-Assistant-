import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUTPUT_DIR = Path("outputs/report_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(13.5, 9.8), dpi=300)
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 9.8)
    ax.axis("off")

    # -------------------------------------------------------------------------
    # Header and Narrative Text (matching uploaded photo)
    # -------------------------------------------------------------------------
    ax.text(
        0.7,
        9.45,
        "4.2.2 Entity Relationship Diagram (ERD)",
        fontsize=13.0,
        fontweight="bold",
        ha="left",
        color="#000000",
    )
    desc_text = (
        "The relational schema of ARES is centered around the primary assessments entity, which maintains\n"
        "one-to-many relationships with child entities capturing findings, activity logs, generated reports,\n"
        "attack surfaces, and pentest actions."
    )
    ax.text(
        0.7,
        8.90,
        desc_text,
        fontsize=9.0,
        ha="left",
        va="center",
        color="#0f172a",
        linespacing=1.35,
    )

    # -------------------------------------------------------------------------
    # Outer Border Box
    # -------------------------------------------------------------------------
    border = patches.Rectangle(
        (0.7, 0.75), 12.1, 7.70, fc="#ffffff", ec="#000000", lw=1.6, zorder=1
    )
    ax.add_patch(border)

    # Figure Caption below box
    ax.text(
        6.75,
        0.40,
        "Fig 4.8: Entity Relationship Diagram (ERD) of ARES Database Schema",
        fontsize=10.8,
        fontweight="bold",
        ha="center",
        va="center",
        color="#000000",
    )

    # -------------------------------------------------------------------------
    # Helper Drawing Functions
    # -------------------------------------------------------------------------
    def draw_entity(cx, cy, w, h, text):
        rect = patches.Rectangle(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            fc="#ffffff",
            ec="#000000",
            lw=1.5,
            zorder=4,
        )
        ax.add_patch(rect)
        ax.text(
            cx,
            cy,
            text,
            fontsize=8.5,
            fontweight="bold",
            ha="center",
            va="center",
            color="#000000",
            zorder=5,
        )

    def draw_relationship(cx, cy, w, h, text):
        pts = [
            [cx, cy + h / 2],
            [cx + w / 2, cy],
            [cx, cy - h / 2],
            [cx - w / 2, cy],
        ]
        poly = patches.Polygon(
            pts, closed=True, fc="#ffffff", ec="#000000", lw=1.4, zorder=4
        )
        ax.add_patch(poly)
        ax.text(
            cx,
            cy,
            text,
            fontsize=7.2,
            ha="center",
            va="center",
            color="#000000",
            zorder=5,
        )

    def draw_attribute(cx, cy, w, h, text, is_pk=False):
        ellipse = patches.Ellipse(
            (cx, cy), w, h, fc="#ffffff", ec="#000000", lw=1.2, zorder=4
        )
        ax.add_patch(ellipse)
        if is_pk:
            # Underline primary key
            ax.text(
                cx,
                cy,
                text,
                fontsize=7.0,
                fontweight="bold",
                ha="center",
                va="center",
                color="#000000",
                zorder=5,
            )
            # Underline bar below text
            under_w = len(text) * 0.046
            ax.plot(
                [cx - under_w, cx + under_w],
                [cy - 0.09, cy - 0.09],
                color="#000000",
                lw=1.1,
                zorder=5,
            )
        else:
            ax.text(
                cx,
                cy,
                text,
                fontsize=7.0,
                ha="center",
                va="center",
                color="#000000",
                zorder=5,
            )

    # -------------------------------------------------------------------------
    # Layout Coordinates
    # -------------------------------------------------------------------------
    # Row Heights
    y_top = 6.00
    y_bot = 3.20

    # Entity Column Centers
    x_c1 = 2.05
    x_c2 = 5.15
    x_c3 = 8.35
    x_c4 = 11.45

    # -------------------------------------------------------------------------
    # 1. TOP ROW ENTITIES
    # -------------------------------------------------------------------------
    draw_entity(x_c1, y_top, 1.30, 0.50, "USER")
    draw_entity(x_c2, y_top, 1.35, 0.50, "PROJECT")
    draw_entity(x_c3, y_top, 1.45, 0.50, "ASSESSMENT")
    draw_entity(x_c4, y_top, 1.65, 0.50, "ATTACK_SURFACE")

    # -------------------------------------------------------------------------
    # 2. TOP ROW RELATIONSHIPS & CONNECTORS
    # -------------------------------------------------------------------------
    # USER -- [owns] -- PROJECT
    x_owns = (x_c1 + x_c2) / 2
    draw_relationship(x_owns, y_top, 0.95, 0.52, "owns")
    # Line USER to owns
    ax.plot([x_c1 + 0.65, x_owns - 0.475], [y_top, y_top], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c1 + 0.78, y_top + 0.08, "N", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")
    # Line owns to PROJECT
    ax.plot([x_owns + 0.475, x_c2 - 0.675], [y_top, y_top], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c2 - 0.78, y_top + 0.08, "1", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")

    # PROJECT -- [initiates] -- ASSESSMENT
    x_init = (x_c2 + x_c3) / 2
    draw_relationship(x_init, y_top, 1.05, 0.52, "initiates")
    # Line PROJECT to initiates
    ax.plot([x_c2 + 0.675, x_init - 0.525], [y_top, y_top], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c2 + 0.82, y_top + 0.08, "N", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")
    # Line initiates to ASSESSMENT
    ax.plot([x_init + 0.525, x_c3 - 0.725], [y_top, y_top], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c3 - 0.84, y_top + 0.08, "1", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")

    # ASSESSMENT -- [maps] -- ATTACK_SURFACE
    x_maps = (x_c3 + x_c4) / 2
    draw_relationship(x_maps, y_top, 0.90, 0.52, "maps")
    # Line ASSESSMENT to maps
    ax.plot([x_c3 + 0.725, x_maps - 0.45], [y_top, y_top], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c3 + 0.85, y_top + 0.08, "1", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")
    # Line maps to ATTACK_SURFACE
    ax.plot([x_maps + 0.45, x_c4 - 0.825], [y_top, y_top], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c4 - 0.95, y_top + 0.08, "N", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")

    # -------------------------------------------------------------------------
    # 3. BOTTOM ROW ENTITIES
    # -------------------------------------------------------------------------
    draw_entity(x_c1, y_bot, 1.65, 0.50, "PENTEST_ACTION")
    draw_entity(x_c2, y_bot, 1.35, 0.50, "EVIDENCE")
    draw_entity(x_c3, y_bot, 1.45, 0.50, "FINDING")
    draw_entity(x_c4, y_bot, 1.35, 0.50, "REPORT")

    # -------------------------------------------------------------------------
    # 4. BOTTOM ROW RELATIONSHIPS & CONNECTORS
    # -------------------------------------------------------------------------
    # PENTEST_ACTION -- [produces] -- EVIDENCE
    x_prod = (x_c1 + x_c2) / 2
    draw_relationship(x_prod, y_bot, 1.05, 0.52, "produces")
    # Line PENTEST_ACTION to produces
    ax.plot([x_c1 + 0.825, x_prod - 0.525], [y_bot, y_bot], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c1 + 0.95, y_bot + 0.08, "1", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")
    # Line produces to EVIDENCE
    ax.plot([x_prod + 0.525, x_c2 - 0.675], [y_bot, y_bot], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c2 - 0.80, y_bot + 0.08, "N", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")

    # EVIDENCE -- [validates] -- FINDING
    x_val = (x_c2 + x_c3) / 2
    draw_relationship(x_val, y_bot, 1.05, 0.52, "validates")
    # Line EVIDENCE to validates
    ax.plot([x_c2 + 0.675, x_val - 0.525], [y_bot, y_bot], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c2 + 0.80, y_bot + 0.08, "N", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")
    # Line validates to FINDING
    ax.plot([x_val + 0.525, x_c3 - 0.725], [y_bot, y_bot], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c3 - 0.84, y_bot + 0.08, "1", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")

    # FINDING -- [compiles_into] -- REPORT
    x_comp = (x_c3 + x_c4) / 2
    draw_relationship(x_comp, y_bot, 1.15, 0.52, "compiles_into")
    # Line FINDING to compiles_into
    ax.plot([x_c3 + 0.725, x_comp - 0.575], [y_bot, y_bot], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c3 + 0.85, y_bot + 0.08, "N", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")
    # Line compiles_into to REPORT
    ax.plot([x_comp + 0.575, x_c4 - 0.675], [y_bot, y_bot], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c4 - 0.80, y_bot + 0.08, "1", fontsize=7.5, fontweight="bold", ha="center", va="bottom", color="#000000")

    # -------------------------------------------------------------------------
    # 5. VERTICAL CONNECTOR: ASSESSMENT -- [identifies] -- FINDING
    # -------------------------------------------------------------------------
    y_id = (y_top + y_bot) / 2
    draw_relationship(x_c3, y_id, 1.15, 0.55, "identifies")

    # Top segment: ASSESSMENT bottom to identifies top
    ax.plot([x_c3, x_c3], [y_top - 0.25, y_id + 0.275], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c3 + 0.12, y_top - 0.40, "1", fontsize=7.5, fontweight="bold", ha="left", va="center", color="#000000")
    ax.text(x_c3 + 0.12, y_id + 0.45, "1", fontsize=7.5, fontweight="bold", ha="left", va="center", color="#000000")

    # Bottom segment: identifies bottom to FINDING top
    ax.plot([x_c3, x_c3], [y_id - 0.275, y_bot + 0.25], color="#000000", lw=1.3, zorder=3)
    ax.text(x_c3 + 0.12, y_id - 0.45, "N", fontsize=7.5, fontweight="bold", ha="left", va="center", color="#000000")
    ax.text(x_c3 + 0.12, y_bot + 0.40, "N", fontsize=7.5, fontweight="bold", ha="left", va="center", color="#000000")

    # -------------------------------------------------------------------------
    # 6. ATTRIBUTES (OVALS & CONNECTING SPOKES)
    # -------------------------------------------------------------------------
    def connect_attr(attr_cx, attr_cy, ent_anchor_x, ent_edge_y):
        ax.plot([ent_anchor_x, attr_cx], [ent_edge_y, attr_cy], color="#000000", lw=1.1, zorder=2)

    # 6.1 USER Attributes (Top)
    # Distinct top-edge anchors across USER [1.50 to 2.60]
    user_attrs = [
        {"name": "user_id", "x": 1.25, "y": 7.25, "w": 0.82, "h": 0.38, "pk": True, "anchor_x": 1.60},
        {"name": "username", "x": 1.78, "y": 7.78, "w": 0.90, "h": 0.38, "pk": False, "anchor_x": 1.90},
        {"name": "role", "x": 2.45, "y": 7.78, "w": 0.70, "h": 0.38, "pk": False, "anchor_x": 2.20},
        {"name": "is_active", "x": 2.95, "y": 7.25, "w": 0.85, "h": 0.38, "pk": False, "anchor_x": 2.50},
    ]
    for att in user_attrs:
        connect_attr(att["x"], att["y"], att["anchor_x"], y_top + 0.25)
        draw_attribute(att["x"], att["y"], att["w"], att["h"], att["name"], att["pk"])

    # 6.2 PROJECT Attributes (Top)
    # Distinct top-edge anchors across PROJECT [4.50 to 5.80]
    proj_attrs = [
        {"name": "project_id", "x": 4.15, "y": 7.25, "w": 0.90, "h": 0.38, "pk": True, "anchor_x": 4.65},
        {"name": "name", "x": 4.75, "y": 7.78, "w": 0.68, "h": 0.38, "pk": False, "anchor_x": 4.95},
        {"name": "description", "x": 5.42, "y": 7.78, "w": 0.95, "h": 0.38, "pk": False, "anchor_x": 5.30},
        {"name": "created_at", "x": 6.05, "y": 7.25, "w": 0.86, "h": 0.38, "pk": False, "anchor_x": 5.65},
    ]
    for att in proj_attrs:
        connect_attr(att["x"], att["y"], att["anchor_x"], y_top + 0.25)
        draw_attribute(att["x"], att["y"], att["w"], att["h"], att["name"], att["pk"])

    # 6.3 ASSESSMENT Attributes (Top)
    # Distinct top-edge anchors across ASSESSMENT [7.65 to 9.05]
    asm_attrs = [
        {"name": "assessment_id", "x": 7.32, "y": 7.25, "w": 1.10, "h": 0.38, "pk": True, "anchor_x": 7.80},
        {"name": "name", "x": 7.85, "y": 7.78, "w": 0.68, "h": 0.38, "pk": False, "anchor_x": 8.08},
        {"name": "target", "x": 8.35, "y": 7.78, "w": 0.70, "h": 0.38, "pk": False, "anchor_x": 8.35},
        {"name": "scope", "x": 8.85, "y": 7.78, "w": 0.70, "h": 0.38, "pk": False, "anchor_x": 8.62},
        {"name": "status", "x": 9.40, "y": 7.25, "w": 0.75, "h": 0.38, "pk": False, "anchor_x": 8.90},
    ]
    for att in asm_attrs:
        connect_attr(att["x"], att["y"], att["anchor_x"], y_top + 0.25)
        draw_attribute(att["x"], att["y"], att["w"], att["h"], att["name"], att["pk"])

    # 6.4 ATTACK_SURFACE Attributes (Top)
    # Distinct top-edge anchors across ATTACK_SURFACE [10.70 to 12.20]
    atk_attrs = [
        {"name": "surface_id", "x": 10.45, "y": 7.25, "w": 0.92, "h": 0.38, "pk": True, "anchor_x": 10.85},
        {"name": "path", "x": 11.05, "y": 7.78, "w": 0.68, "h": 0.38, "pk": False, "anchor_x": 11.20},
        {"name": "method", "x": 11.75, "y": 7.78, "w": 0.75, "h": 0.38, "pk": False, "anchor_x": 11.60},
        {"name": "auth_state", "x": 12.45, "y": 7.25, "w": 0.92, "h": 0.38, "pk": False, "anchor_x": 12.00},
    ]
    for att in atk_attrs:
        connect_attr(att["x"], att["y"], att["anchor_x"], y_top + 0.25)
        draw_attribute(att["x"], att["y"], att["w"], att["h"], att["name"], att["pk"])

    # 6.5 PENTEST_ACTION Attributes (1 Top, 2 Bottom)
    # action_id (above)
    connect_attr(1.85, 4.35, 1.85, y_bot + 0.25)
    draw_attribute(1.85, 4.35, 0.90, 0.38, "action_id", is_pk=True)
    # capability & tool (below)
    connect_attr(1.30, 2.05, 1.65, y_bot - 0.25)
    draw_attribute(1.30, 2.05, 0.95, 0.38, "capability", is_pk=False)

    connect_attr(1.85, 1.55, 2.05, y_bot - 0.25)
    draw_attribute(1.85, 1.55, 0.75, 0.38, "tool", is_pk=False)

    # 6.6 EVIDENCE Attributes (2 Top, 2 Bottom)
    # evidence_id & evidence_type (above)
    connect_attr(4.55, 4.35, 4.85, y_bot + 0.25)
    draw_attribute(4.55, 4.35, 0.96, 0.38, "evidence_id", is_pk=True)

    connect_attr(5.75, 4.35, 5.45, y_bot + 0.25)
    draw_attribute(5.75, 4.35, 1.02, 0.38, "evidence_type", is_pk=False)
    # timestamp & source (below)
    connect_attr(5.00, 1.35, 5.00, y_bot - 0.25)
    draw_attribute(5.00, 1.35, 0.95, 0.38, "timestamp", is_pk=False)

    connect_attr(5.80, 1.95, 5.35, y_bot - 0.25)
    draw_attribute(5.80, 1.95, 0.80, 0.38, "source", is_pk=False)

    # 6.7 FINDING Attributes (1 Top, 2 Bottom)
    # finding_id (placed to the left of identifies diamond)
    connect_attr(7.35, 4.35, 7.85, y_bot + 0.25)
    draw_attribute(7.35, 4.35, 0.95, 0.38, "finding_id", is_pk=True)
    # severity & confidence (below)
    connect_attr(7.75, 2.00, 8.10, y_bot - 0.25)
    draw_attribute(7.75, 2.00, 0.85, 0.38, "severity", is_pk=False)

    connect_attr(8.95, 2.00, 8.60, y_bot - 0.25)
    draw_attribute(8.95, 2.00, 0.95, 0.38, "confidence", is_pk=False)

    # 6.8 REPORT Attributes (2 Top, 2 Bottom)
    # report_id & report_type (above)
    connect_attr(10.85, 4.35, 11.15, y_bot + 0.25)
    draw_attribute(10.85, 4.35, 0.90, 0.38, "report_id", is_pk=True)

    connect_attr(12.05, 4.35, 11.75, y_bot + 0.25)
    draw_attribute(12.05, 4.35, 0.98, 0.38, "report_type", is_pk=False)
    # findings_count & generated_at (below)
    connect_attr(10.82, 1.95, 11.20, y_bot - 0.25)
    draw_attribute(10.82, 1.95, 1.08, 0.38, "findings_count", is_pk=False)

    connect_attr(12.08, 1.95, 11.70, y_bot - 0.25)
    draw_attribute(12.08, 1.95, 1.05, 0.38, "generated_at", is_pk=False)

    out_png = OUTPUT_DIR / "er_diagram_ares.png"
    out_pdf = OUTPUT_DIR / "er_diagram_ares.pdf"
    fig.savefig(out_png, bbox_inches="tight", dpi=300)
    fig.savefig(out_pdf, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Generated PNG: {out_png}")
    print(f"Generated PDF: {out_pdf}")


if __name__ == "__main__":
    generate_er_diagram()
