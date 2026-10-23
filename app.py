"""
AI Research Paper Assistant - Main Streamlit Application
A complete end-to-end academic research paper portal and authoring workflow.
"""

import os
import json
import io
import shutil
from pathlib import Path
import streamlit as st
import pandas as pd

# Internal modules
from config import PROJECT_ROOT, DATA_DIR, OUTPUTS_DIR, SAMPLES_DIR, CONFERENCE_TEMPLATES
from modules.semantic_scholar import search_semantic_scholar, CURATED_PAPERS, paper_to_bibtex
from modules.llm_provider import llm_service
from modules.project_state import ProjectState
from modules.methodology.material import extract_research_insights
from modules.methodology.outline import generate_structured_outline
from modules.methodology.lit_review import synthesize_literature_review
from modules.methodology.section_writer import draft_paper_section
from modules.methodology.refinement import polish_academic_tone, simulate_peer_review, audit_citations_and_claims
from modules.plotting.studio import CHART_TEMPLATES, execute_plot_code, generate_latex_figure_snippet
from modules.latex.templates import render_latex_manuscript
from modules.latex.bibtex_manager import deduplicate_bibtex, validate_bibtex_syntax
from modules.latex.compiler import check_local_latex_compilers, create_latex_package, attempt_local_compile
from modules.final_paper.portal import audit_paper_health, export_as_markdown, export_as_html, generate_presentation_slides

# Page Configuration
st.set_page_config(
    page_title="AI Research Paper Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Academic Aesthetics
st.markdown("""
<style>
    .main-header {
        font-family: 'Georgia', serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.92rem;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 4px;
        background-color: #e0f2fe;
        color: #0369a1;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "project" not in st.session_state:
    sample_file = SAMPLES_DIR / "sample_project.json"
    loaded = ProjectState.load_project(sample_file) if sample_file.exists() else None
    if loaded:
        st.session_state.project = loaded
    else:
        st.session_state.project = ProjectState.create_empty_project()

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

proj = st.session_state.project

# -------------------------------------------------------------
# SIDEBAR: Configuration & Project Management
# -------------------------------------------------------------
with st.sidebar:
    st.title("🎓 Paper Assistant")
    st.caption("End-to-End Academic Authoring Suite")
    
    st.markdown("---")
    st.subheader("📁 Project Management")
    proj_name = st.text_input("Project Name", value=proj.get("project_name", "Research Project"))
    proj["project_name"] = proj_name

    selected_template = st.selectbox(
        "Venue / LaTeX Template",
        options=list(CONFERENCE_TEMPLATES.keys()),
        index=list(CONFERENCE_TEMPLATES.keys()).index(proj.get("template", "NeurIPS / ICLR")) if proj.get("template") in CONFERENCE_TEMPLATES else 0
    )
    proj["template"] = selected_template

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("💾 Save Project", use_container_width=True):
            save_path = DATA_DIR / f"{proj.get('id', 'proj')}.json"
            if ProjectState.save_project(proj, save_path):
                st.success("Project Saved!")
    with col_s2:
        if st.button("🔄 Reset Demo", use_container_width=True):
            sample_file = SAMPLES_DIR / "sample_project.json"
            if sample_file.exists():
                st.session_state.project = ProjectState.load_project(sample_file)
                st.rerun()

    # Import / Export JSON
    with st.expander("📂 Import / Export Project JSON"):
        json_str = json.dumps(proj, indent=2)
        st.download_button(
            "⬇️ Export JSON",
            data=json_str,
            file_name=f"{proj['project_name'].lower().replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )
        uploaded_json = st.file_uploader("Upload Project JSON", type=["json"])
        if uploaded_json is not None:
            try:
                data = json.load(uploaded_json)
                st.session_state.project = data
                st.success("Project loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading JSON: {e}")

    st.markdown("---")
    st.subheader("⚙️ AI & LLM Settings")

    provider_choice = st.selectbox(
        "LLM Engine",
        options=["Offline Academic Engine (Instant / Zero-Cost)", "Google Gemini", "OpenAI"],
        index=0
    )

    api_key_input = ""
    model_choice = "default"
    if provider_choice == "Google Gemini":
        api_key_input = st.text_input("Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
        model_choice = st.selectbox("Gemini Model", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-pro", "gemini-1.5-flash"])
    elif provider_choice == "OpenAI":
        api_key_input = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
        model_choice = st.selectbox("OpenAI Model", ["gpt-4o-mini", "gpt-4o", "o1-mini", "gpt-3.5-turbo"])
    else:
        st.info("💡 Running Offline Engine: Generates complete, rigorous academic manuscripts without API keys or token costs.")

    s2_key = st.text_input("Semantic Scholar Key (Optional)", value=os.getenv("SEMANTIC_SCHOLAR_API_KEY", ""), type="password")

    st.markdown("---")
    compilers_status = check_local_latex_compilers()
    has_latex = any(compilers_status.values())
    st.markdown(f"**Local LaTeX Engine:** {'✅ Detected (' + ', '.join([k for k, v in compilers_status.items() if v]) + ')' if has_latex else '⚠️ None (Overleaf ZIP ready)'}")


# -------------------------------------------------------------
# MAIN APP HEADER & WORKFLOW TABS
# -------------------------------------------------------------
st.markdown('<div class="main-header">🎓 AI Research Paper Assistant</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Working Manuscript: <strong>{proj.get("metadata", {}).get("title", "Untitled Manuscript")}</strong> | Target: <strong>{proj.get("template")}</strong></div>', unsafe_allow_html=True)

# 8 Methodology Steps + Search Portal Tabs
tabs = st.tabs([
    "🔍 1. Paper Portal",
    "📚 2. Research Material",
    "📐 3. Paper Outline",
    "🔬 4. Literature Review",
    "✍️ 5. Section Writing",
    "✨ 6. Refinement & Review",
    "📊 7. Plots & Visuals",
    "📑 8. LaTeX Manuscript",
    "🚀 9. Final Paper & Export"
])


# =============================================================
# TAB 1: LITERATURE SEARCH PORTAL
# =============================================================
with tabs[0]:
    st.subheader("🔍 Research Paper Portal (Semantic Scholar & ArXiv)")
    st.write("Discover peer-reviewed literature, inspect abstracts, copy BibTeX citations, and collect relevant papers into your working research material.")

    col_q1, col_q2, col_q3 = st.columns([3, 1, 1])
    with col_q1:
        search_query = st.text_input("Search Topics, Authors, or DOI / ArXiv ID", value="State Space Models for Long Context Sequence Modeling")
    with col_q2:
        year_filter = st.selectbox("Year Range", ["All Years", "2023-2026", "2020-2023", "2015-2020"])
    with col_q3:
        search_limit = st.slider("Max Results", min_value=5, max_value=25, value=10)

    if st.button("🔎 Search Academic Literature", type="primary"):
        with st.spinner("Querying Semantic Scholar & ArXiv..."):
            yr = None
            if year_filter == "2023-2026": yr = "2023-2026"
            elif year_filter == "2020-2023": yr = "2020-2023"
            elif year_filter == "2015-2020": yr = "2015-2020"
            
            res = search_semantic_scholar(
                query=search_query,
                api_key=s2_key or None,
                limit=search_limit,
                year_range=yr
            )
            st.session_state.search_results = res.get("papers", [])
            st.success(f"Retrieved {len(st.session_state.search_results)} papers via {res.get('source')}!")

    # Display Search Results
    if st.session_state.search_results:
        st.markdown(f"### Found Papers ({len(st.session_state.search_results)})")
        for idx, paper in enumerate(st.session_state.search_results):
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin-top:0; color:#1e40af;">{paper.get('title', 'Untitled')}</h4>
                    <span class="badge">📅 {paper.get('year', 'N/A')}</span>
                    <span class="badge">🏛️ {paper.get('venue') or 'Academic Venue'}</span>
                    <span class="badge">🌟 {paper.get('citationCount', 0):,} Citations</span>
                    <span class="badge">⚡ {paper.get('influentialCitationCount', 0):,} Influential</span>
                    <p style="margin-top:8px; margin-bottom:6px; font-size:0.9rem; color:#475569;">
                        <strong>Authors:</strong> {', '.join([a.get('name', '') for a in paper.get('authors', [])][:5])}
                    </p>
                    <p style="font-size:0.88rem; color:#334155; line-height:1.45;">
                        {paper.get('abstract', 'No abstract available.')[:380]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)

                col_b1, col_b2, col_b3 = st.columns([1.5, 1.5, 2])
                with col_b1:
                    is_saved = any(p.get("paperId") == paper.get("paperId") for p in proj["research_materials"]["saved_papers"])
                    if is_saved:
                        st.button(f"✅ Saved to Project", key=f"saved_{idx}", disabled=True)
                    else:
                        if st.button(f"➕ Add to Research Material", key=f"add_{idx}"):
                            proj["research_materials"]["saved_papers"].append(paper)
                            # Also add bibtex
                            bib = paper.get("bibtex", paper_to_bibtex(paper))
                            cur_bib = proj["literature_review"].get("bibtex_entries", "")
                            proj["literature_review"]["bibtex_entries"] = deduplicate_bibtex(f"{cur_bib}\n\n{bib}")
                            st.success(f"Added '{paper.get('title')[:30]}...' to Research Material!")
                            st.rerun()

                with col_b2:
                    with st.popover("📜 View BibTeX"):
                        st.code(paper.get("bibtex", paper_to_bibtex(paper)), language="latex")

                with col_b3:
                    if paper.get("url"):
                        st.link_button("🌐 Open Publisher / ArXiv", paper["url"])


# =============================================================
# TAB 2: RESEARCH MATERIAL HUB (Step 1)
# =============================================================
with tabs[1]:
    st.subheader("📚 Methodology Step 1: Research Material & Hypothesis Hub")
    st.write("Curate your references, experimental notes, baseline models, and let AI extract the core problem statement, research gap, and contributions.")

    col_m1, col_m2 = st.columns([1, 1])

    with col_m1:
        st.markdown("#### 📑 Curated Literature Library")
        saved_papers = proj["research_materials"].get("saved_papers", [])
        if not saved_papers:
            st.info("No papers added yet. Search papers in Tab 1 or click below to populate curated seminal papers.")
            if st.button("📥 Import Seminal Baseline Papers"):
                for cp in CURATED_PAPERS[:4]:
                    proj["research_materials"]["saved_papers"].append(cp)
                    cur_bib = proj["literature_review"].get("bibtex_entries", "")
                    proj["literature_review"]["bibtex_entries"] = deduplicate_bibtex(f"{cur_bib}\n\n{cp.get('bibtex', paper_to_bibtex(cp))}")
                st.success("Loaded 4 seminal papers!")
                st.rerun()
        else:
            for idx, sp in enumerate(saved_papers):
                with st.expander(f"{idx+1}. {sp.get('title')} ({sp.get('year')})"):
                    st.write(f"**Authors:** {', '.join([a.get('name', '') for a in sp.get('authors', [])])}")
                    st.write(f"**Abstract:** {sp.get('abstract', '')}")
                    if st.button(f"🗑️ Remove Paper", key=f"del_p_{idx}"):
                        proj["research_materials"]["saved_papers"].pop(idx)
                        st.rerun()

        st.markdown("#### 📝 Laboratory & Experimental Notes")
        current_notes = "\n".join(proj["research_materials"].get("user_notes", []))
        notes_input = st.text_area("Lab Notes, Hypotheses & Observations (1 per line)", value=current_notes, height=180)
        if st.button("💾 Update Notes"):
            proj["research_materials"]["user_notes"] = [line.strip() for line in notes_input.split("\n") if line.strip()]
            st.success("Notes saved!")

    with col_m2:
        st.markdown("#### 🤖 Automated Research Insights & Gap Analysis")
        if st.button("⚡ Extract Insights & Research Gap", type="primary", use_container_width=True):
            with st.spinner("Synthesizing problem statement and novelty gap..."):
                extracted = extract_research_insights(
                    papers=proj["research_materials"].get("saved_papers", []),
                    notes=proj["research_materials"].get("user_notes", []),
                    provider=provider_choice,
                    model=model_choice,
                    api_key=api_key_input
                )
                proj["research_materials"]["extracted_insights"] = extracted
                st.success("Insights synthesized successfully!")
                st.rerun()

        insights = proj["research_materials"].get("extracted_insights", {})
        
        prob = st.text_area("Problem Statement", value=insights.get("problem_statement", ""), height=100)
        insights["problem_statement"] = prob
        
        gap = st.text_area("Identified Research Gap", value=insights.get("research_gap", ""), height=100)
        insights["research_gap"] = gap

        contrib = st.text_area("Proposed Novel Contribution", value=insights.get("proposed_contribution", ""), height=120)
        insights["proposed_contribution"] = contrib

        st.markdown("**Recommended Benchmarks & Baselines:**")
        st.write(", ".join([f"`{b}`" for b in insights.get("benchmark_datasets", [])]))


# =============================================================
# TAB 3: OUTLINE ARCHITECT (Step 2)
# =============================================================
with tabs[2]:
    st.subheader("📐 Methodology Step 2: Paper Outline & Structural Architecture")
    st.write("Plan your paper structure based on the chosen conference standard. Set section targets, objectives, and bullet points.")

    col_o1, col_o2 = st.columns([1, 2])
    with col_o1:
        st.markdown("#### Outline Generator")
        st.write(f"**Target Venue:** `{proj.get('template')}`")
        if st.button("🤖 Generate Structured Outline", type="primary", use_container_width=True):
            with st.spinner("Architecting paper outline tailored to venue..."):
                new_outline = generate_structured_outline(
                    paper_title=proj.get("metadata", {}).get("title", "Manuscript"),
                    template_name=proj.get("template", "NeurIPS / ICLR"),
                    insights=proj["research_materials"].get("extracted_insights", {}),
                    provider=provider_choice,
                    model=model_choice,
                    api_key=api_key_input
                )
                proj["outline"] = new_outline
                st.success("Generated structured outline!")
                st.rerun()

        st.markdown("---")
        st.markdown("#### Paper Metadata")
        proj_title = st.text_input("Paper Title", value=proj.get("metadata", {}).get("title", ""))
        proj["metadata"]["title"] = proj_title

        keywords_str = st.text_input("Keywords (comma separated)", value=", ".join(proj.get("metadata", {}).get("keywords", [])))
        proj["metadata"]["keywords"] = [k.strip() for k in keywords_str.split(",") if k.strip()]

    with col_o2:
        st.markdown("#### Interactive Section Hierarchy")
        outline = proj.get("outline", [])
        total_planned_words = sum(sec.get("target_words", 0) for sec in outline)
        st.caption(f"Total Target Word Count: **{total_planned_words:,} words** across **{len(outline)} sections**")

        for idx, sec in enumerate(outline):
            with st.expander(f"{sec.get('title', 'Section')} ({sec.get('target_words', 0)} words)"):
                col_e1, col_e2 = st.columns([3, 1])
                with col_e1:
                    new_t = st.text_input("Title", value=sec.get("title", ""), key=f"ot_{idx}")
                    sec["title"] = new_t
                    new_obj = st.text_input("Objective", value=sec.get("objective", ""), key=f"oo_{idx}")
                    sec["objective"] = new_obj
                    bullets_txt = st.text_area("Key Points to Cover", value="\n".join(sec.get("bullet_points", [])), key=f"ob_{idx}", height=80)
                    sec["bullet_points"] = [b.strip() for b in bullets_txt.split("\n") if b.strip()]
                with col_e2:
                    new_tw = st.number_input("Target Words", value=sec.get("target_words", 500), step=50, key=f"ow_{idx}")
                    sec["target_words"] = new_tw
                    if st.button("🗑️ Delete", key=f"odel_{idx}"):
                        outline.pop(idx)
                        st.rerun()

        if st.button("➕ Add Custom Section"):
            outline.append({
                "id": f"sec_custom_{len(outline)+1}",
                "title": f"Custom Section {len(outline)+1}",
                "level": 1,
                "objective": "Address customized technical evaluation.",
                "bullet_points": ["Key technical concept"],
                "target_words": 600,
                "status": "Not Started"
            })
            st.rerun()


# =============================================================
# TAB 4: LITERATURE REVIEW SYNTHESIZER (Step 3)
# =============================================================
with tabs[3]:
    st.subheader("🔬 Methodology Step 3: Literature Review & Comparative Matrix")
    st.write("Synthesize Related Work with formal in-text citation keys and construct a multi-dimensional comparative analysis matrix.")

    col_lr1, col_lr2 = st.columns([1.2, 1])
    with col_lr1:
        st.markdown("#### Related Work Synthesis Narrative")
        if st.button("🤖 Synthesize Related Work with Citations", type="primary"):
            with st.spinner("Synthesizing comparative literature review..."):
                lit_res = synthesize_literature_review(
                    papers=proj["research_materials"].get("saved_papers", []),
                    proposed_work_title=proj.get("metadata", {}).get("title", "Manuscript"),
                    research_gap=proj["research_materials"].get("extracted_insights", {}).get("research_gap", ""),
                    provider=provider_choice,
                    model=model_choice,
                    api_key=api_key_input
                )
                proj["literature_review"]["synthesis_text"] = lit_res["synthesis_text"]
                if lit_res.get("matrix"):
                    proj["literature_review"]["matrix"] = lit_res["matrix"]
                if lit_res.get("bibtex_entries"):
                    cur_b = proj["literature_review"].get("bibtex_entries", "")
                    proj["literature_review"]["bibtex_entries"] = deduplicate_bibtex(f"{cur_b}\n\n{lit_res['bibtex_entries']}")
                
                # Update Section in manuscript
                proj["sections"]["2. Related Work"] = lit_res["synthesis_text"]
                st.success("Literature Review synthesized and inserted into manuscript draft!")
                st.rerun()

        synth_text = st.text_area("Related Work Draft (Markdown/LaTeX with \\cite{...})", value=proj["literature_review"].get("synthesis_text", proj["sections"].get("2. Related Work", "")), height=350)
        proj["literature_review"]["synthesis_text"] = synth_text
        proj["sections"]["2. Related Work"] = synth_text

    with col_lr2:
        st.markdown("#### Comparative Analysis Matrix")
        matrix_data = proj["literature_review"].get("matrix", [])
        if matrix_data:
            df_matrix = pd.DataFrame(matrix_data)
            st.dataframe(df_matrix, use_container_width=True, hide_index=True)
        else:
            st.info("Matrix is currently empty. Synthesize literature above to populate.")

        st.markdown("#### 📚 BibTeX Citation Repository (`references.bib`)")
        cur_bibtex = st.text_area("BibTeX Entries", value=proj["literature_review"].get("bibtex_entries", ""), height=220)
        proj["literature_review"]["bibtex_entries"] = cur_bibtex
        
        col_b_chk1, col_b_chk2 = st.columns(2)
        with col_b_chk1:
            if st.button("🧹 Clean & Deduplicate BibTeX"):
                deduped = deduplicate_bibtex(cur_bibtex)
                proj["literature_review"]["bibtex_entries"] = deduped
                st.success("BibTeX Deduplicated!")
                st.rerun()
        with col_b_chk2:
            is_valid, b_errs = validate_bibtex_syntax(cur_bibtex)
            if is_valid:
                st.caption("✅ BibTeX Syntax Valid")
            else:
                st.caption(f"⚠️ {len(b_errs)} syntax issue(s)")


# =============================================================
# TAB 5: SECTION WRITING STUDIO (Step 4)
# =============================================================
with tabs[4]:
    st.subheader("✍️ Methodology Step 4: Academic Section Writing Studio")
    st.write("Context-aware draft generation with LaTeX equations, algorithmic pseudocode, and publication tables.")

    # Select which section to write/edit
    section_options = list(proj["sections"].keys())
    if not section_options:
        section_options = ["Abstract", "1. Introduction", "2. Related Work", "3. Proposed Methodology", "4. Empirical Evaluation", "5. Discussion & Limitations", "6. Conclusion"]

    selected_sec = st.selectbox("Select Manuscript Section to Draft / Edit", options=section_options)
    
    col_w1, col_w2 = st.columns([1, 1.4])
    with col_w1:
        st.markdown("#### Generation Controls")
        writing_tone = st.selectbox(
            "Academic Tone Style",
            ["Formal Academic (Top-tier Conference)", "Rigorous Theoretical & Mathematical", "Empirical & Experimental Focus", "Concise Letter Style"]
        )

        col_tog1, col_tog2, col_tog3 = st.columns(3)
        with col_tog1:
            inc_eq = st.checkbox("LaTeX Equations", value=True)
        with col_tog2:
            inc_alg = st.checkbox("Algorithm Block", value=("Method" in selected_sec))
        with col_tog3:
            inc_tab = st.checkbox("Booktabs Table", value=("Evaluation" in selected_sec or "Result" in selected_sec))

        target_w = st.slider("Target Words for this Section", min_value=150, max_value=2000, value=750, step=50)

        # Matched outline item
        matched_outline = None
        for o in proj.get("outline", []):
            if o.get("title", "").lower() in selected_sec.lower():
                matched_outline = o
                break

        if st.button(f"🤖 Draft '{selected_sec}' with AI", type="primary", use_container_width=True):
            with st.spinner(f"Drafting {selected_sec} with academic rigor..."):
                draft = draft_paper_section(
                    section_name=selected_sec,
                    paper_metadata=proj.get("metadata", {}),
                    outline_item=matched_outline or {"target_words": target_w, "objective": f"Address {selected_sec}"},
                    research_insights=proj["research_materials"].get("extracted_insights", {}),
                    cited_papers=proj["research_materials"].get("saved_papers", []),
                    tone=writing_tone,
                    include_equations=inc_eq,
                    include_algorithms=inc_alg,
                    include_tables=inc_tab,
                    provider=provider_choice,
                    model=model_choice,
                    api_key=api_key_input
                )
                proj["sections"][selected_sec] = draft
                st.success(f"Drafted '{selected_sec}'!")
                st.rerun()

        # Word count metric
        current_content = proj["sections"].get(selected_sec, "")
        words_count = len(current_content.split())
        st.metric("Section Word Count", f"{words_count:,} words", delta=f"{words_count - target_w} vs target")

    with col_w2:
        st.markdown(f"#### Live Editor: `{selected_sec}`")
        edited_content = st.text_area("Draft Content (Markdown & LaTeX Math)", value=proj["sections"].get(selected_sec, ""), height=450)
        proj["sections"][selected_sec] = edited_content

        with st.expander("👁️ Rendered Math & Text Preview"):
            st.markdown(edited_content)


# =============================================================
# TAB 6: REFINEMENT & REVIEW (Step 5)
# =============================================================
with tabs[5]:
    st.subheader("✨ Methodology Step 5: Refinement, Academic Polish & Peer Review")
    st.write("Polish writing style, run simulated NeurIPS/IEEE peer reviews, and audit citations against hallucinated references.")

    refine_mode = st.radio("Refinement Tool", ["Simulated Peer Review Committee", "Tone & Clarity Polish", "Citation & Claim Auditor"], horizontal=True)

    if refine_mode == "Simulated Peer Review Committee":
        st.markdown("#### ⚖️ Simulated 3-Reviewer Panel (NeurIPS / IEEE Criterion)")
        if st.button("🚀 Run Peer Review Simulation", type="primary"):
            with st.spinner("Reviewer 1, Reviewer 2, and Meta-Reviewer evaluating submission..."):
                all_secs = "\n\n".join([f"## {k}\n{v}" for k, v in proj["sections"].items()])
                pr_res = simulate_peer_review(
                    paper_title=proj.get("metadata", {}).get("title", ""),
                    abstract=proj["sections"].get("Abstract", ""),
                    sections_summary=all_secs,
                    venue=proj.get("template", "NeurIPS / IEEE"),
                    provider=provider_choice,
                    model=model_choice,
                    api_key=api_key_input
                )
                proj["refinement"]["simulated_reviews"] = pr_res
                st.success("Peer Review Complete!")
                st.rerun()

        reviews_data = proj["refinement"].get("simulated_reviews")
        if reviews_data:
            st.markdown(f"### Overall Outcome: **{reviews_data.get('overall_recommendation', 'Accept')}**")
            rev_cols = st.columns(len(reviews_data.get("reviewers", [])))
            for i, r in enumerate(reviews_data.get("reviewers", [])):
                with rev_cols[i]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>{r.get('reviewer')}</h4>
                        <span class="badge">Rating: {r.get('score')}</span>
                        <span class="badge">Soundness: {r.get('soundness')}</span>
                        <span class="badge">Novelty: {r.get('novelty')}</span>
                        <p style="margin-top:10px; font-size:0.92rem;">{r.get('summary')}</p>
                        <strong>Strengths:</strong>
                        <ul>{''.join([f'<li>{s}</li>' for s in r.get('strengths', [])])}</ul>
                        <strong>Actionable Critiques:</strong>
                        <ul>{''.join([f'<li>{w}</li>' for w in r.get('weaknesses', [])])}</ul>
                    </div>
                    """, unsafe_allow_html=True)

            with st.container():
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #16a34a;">
                    <h4>📋 Meta-Reviewer Synthesis</h4>
                    <p>{reviews_data.get('meta_review', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Click 'Run Peer Review Simulation' to receive structured scores and critiques.")

    elif refine_mode == "Tone & Clarity Polish":
        st.markdown("#### ✍️ Academic Tone & Scholarly Polish")
        sec_to_polish = st.selectbox("Select Section to Polish", list(proj["sections"].keys()))
        polish_focus = st.selectbox("Focus Area", ["Tone & Academic Authority", "Conciseness & Fluff Elimination", "Clarity & Logical Flow"])

        if st.button(f"✨ Polish '{sec_to_polish}'", type="primary"):
            with st.spinner(f"Polishing {sec_to_polish}..."):
                res_polish = polish_academic_tone(
                    text=proj["sections"].get(sec_to_polish, ""),
                    focus=polish_focus,
                    provider=provider_choice,
                    model=model_choice,
                    api_key=api_key_input
                )
                proj["refinement"]["last_polished"] = res_polish
                st.success("Polishing report generated!")
                st.rerun()

        last_pol = proj["refinement"].get("last_polished")
        if last_pol:
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown("#### Original Draft")
                st.text_area("Original", value=proj["sections"].get(sec_to_polish, ""), height=300, disabled=True)
            with col_p2:
                st.markdown("#### Polished Academic Version")
                st.text_area("Polished Result", value=last_pol.get("polished_text", ""), height=300)
                if st.button("✅ Replace Original with Polished Version"):
                    proj["sections"][sec_to_polish] = last_pol.get("polished_text", "")
                    st.success("Updated manuscript section!")
                    st.rerun()

    elif refine_mode == "Citation & Claim Auditor":
        st.markdown("#### 🔍 Citation & Claim Auditor")
        all_text = "\n\n".join(proj["sections"].values())
        bib_text = proj["literature_review"].get("bibtex_entries", "")
        audit_res = audit_citations_and_claims(all_text, bib_text)

        col_a1, col_a2, col_a3 = st.columns(3)
        col_a1.metric("Citations in Manuscript", audit_res["total_citations_found"])
        col_a2.metric("Verified in BibTeX", len(audit_res["verified_in_bibtex"]))
        col_a3.metric("Unresolved Keys", len(audit_res["missing_from_bibtex"]), delta=-len(audit_res["missing_from_bibtex"]))

        if audit_res["missing_from_bibtex"]:
            st.error(f"⚠️ Missing BibTeX entries for cited keys: {', '.join(audit_res['missing_from_bibtex'])}")
        else:
            st.success("✅ All citations used in manuscript have corresponding BibTeX entries!")

        if audit_res["warnings"]:
            for w in audit_res["warnings"]:
                st.warning(w)


# =============================================================
# TAB 7: PLOTS & VISUALS STUDIO (Step 6)
# =============================================================
with tabs[6]:
    st.subheader("📊 Methodology Step 6: Publication Plots & Visuals Studio")
    st.write("Generate publication-grade figures (300 DPI PNG, vector PDF) using Matplotlib and Seaborn, and generate LaTeX `\\begin{figure}` snippets.")

    col_v1, col_v2 = st.columns([1, 1.2])

    with col_v1:
        st.markdown("#### 🎨 Publication Chart Templates")
        selected_plot_template = st.selectbox("Select Preset Academic Chart", list(CHART_TEMPLATES.keys()))
        
        plot_code = st.text_area("Python Plotting Code (Matplotlib / Seaborn)", value=CHART_TEMPLATES[selected_plot_template], height=320)

        fig_name_base = st.text_input("Figure ID / Filename", value="fig_generated_plot")
        fig_caption = st.text_input("Figure Caption", value="Downstream latency scaling comparison under varying sequence lengths.")
        fig_label = st.text_input("LaTeX Label", value=f"fig:{fig_name_base}")

        if st.button("🚀 Render & Export Figure", type="primary", use_container_width=True):
            plots_dir = OUTPUTS_DIR / "plots"
            success, png_path, err = execute_plot_code(plot_code, plots_dir, fig_name_base)
            if success:
                st.session_state.last_rendered_plot = {
                    "png_path": png_path,
                    "filename": f"{fig_name_base}.png",
                    "caption": fig_caption,
                    "label": fig_label,
                    "code": plot_code
                }
                # Also save to project figures
                existing = [f for f in proj["figures"] if f.get("id") == fig_name_base]
                if not existing:
                    proj["figures"].append({
                        "id": fig_name_base,
                        "title": selected_plot_template,
                        "caption": fig_caption,
                        "label": fig_label,
                        "filename": f"{fig_name_base}.png",
                        "latex_snippet": generate_latex_figure_snippet(f"{fig_name_base}.png", fig_caption, fig_label)
                    })
                st.success("Figure rendered and saved at 300 DPI!")
                st.rerun()
            else:
                st.error(f"Plot execution failed: {err}")

    with col_v2:
        st.markdown("#### 🖼️ Figure Preview & LaTeX Integration")
        # Check if we have a rendered plot
        plots_dir = OUTPUTS_DIR / "plots"
        rendered = getattr(st.session_state, "last_rendered_plot", None)
        
        # Fallback to pre-generated plot if none just rendered
        display_img_path = None
        if rendered and Path(rendered["png_path"]).exists():
            display_img_path = rendered["png_path"]
            curr_caption = rendered["caption"]
            curr_label = rendered["label"]
            curr_fname = rendered["filename"]
        elif (plots_dir / "fig_latency_scaling.png").exists():
            display_img_path = str(plots_dir / "fig_latency_scaling.png")
            curr_caption = "Inference Latency (ms) comparison across sequence lengths from 512 to 16,384 tokens."
            curr_label = "fig:latency_scaling"
            curr_fname = "fig_latency_scaling.png"

        if display_img_path and Path(display_img_path).exists():
            st.image(display_img_path, caption=curr_caption, use_container_width=True)
            
            # Download buttons
            col_d1, col_d2 = st.columns(2)
            with open(display_img_path, "rb") as f_img:
                col_d1.download_button("⬇️ Download High-Res PNG (300 DPI)", data=f_img.read(), file_name=curr_fname, mime="image/png", use_container_width=True)
            
            pdf_path = Path(display_img_path).with_suffix(".pdf")
            if pdf_path.exists():
                with open(pdf_path, "rb") as f_pdf:
                    col_d2.download_button("⬇️ Download Vector PDF", data=f_pdf.read(), file_name=pdf_path.name, mime="application/pdf", use_container_width=True)

            st.markdown("#### 📑 Ready-to-Copy LaTeX Figure Block")
            latex_fig_code = generate_latex_figure_snippet(curr_fname, curr_caption, curr_label)
            st.code(latex_fig_code, language="latex")
        else:
            st.info("Render a chart on the left to see the high-resolution preview and LaTeX snippet.")


# =============================================================
# TAB 8: LATEX STUDIO & MANUSCRIPT (Step 7)
# =============================================================
with tabs[7]:
    st.subheader("📑 Methodology Step 7: LaTeX Studio & Manuscript Compiler")
    st.write("Full modular LaTeX compilation engine supporting IEEEtran, NeurIPS, ACM, and Standard Article formats.")

    # Render full LaTeX
    assembled_latex = render_latex_manuscript(
        template_name=proj.get("template", "NeurIPS / ICLR"),
        metadata=proj.get("metadata", {}),
        abstract=proj["sections"].get("Abstract", ""),
        sections=proj["sections"],
        custom_preamble=proj.get("latex", {}).get("custom_preamble", "")
    )
    proj["latex"]["compiled_tex"] = assembled_latex

    col_lx1, col_lx2 = st.columns([1.5, 1])
    with col_lx1:
        st.markdown("#### 📝 Live `main.tex` Source Code")
        edited_latex = st.text_area("LaTeX Source Code", value=assembled_latex, height=520)
        proj["latex"]["compiled_tex"] = edited_latex

    with col_lx2:
        st.markdown("#### 📦 Packaging & Compilation Hub")
        st.write(f"**Target Template:** `{proj.get('template')}`")

        # Compile Package Button
        if st.button("📦 Build Overleaf & LaTeX ZIP Package", type="primary", use_container_width=True):
            pkg_dir, zip_file = create_latex_package(
                output_dir=OUTPUTS_DIR,
                main_tex=proj["latex"]["compiled_tex"],
                bibtex_content=proj["literature_review"].get("bibtex_entries", ""),
                figures_list=proj.get("figures", []),
                project_name=proj.get("project_name", "paper")
            )
            st.session_state.last_zip_path = str(zip_file)
            st.session_state.last_pkg_dir = str(pkg_dir)
            st.success(f"Built LaTeX package: {zip_file.name}")
            st.rerun()

        last_zip = getattr(st.session_state, "last_zip_path", None)
        if last_zip and Path(last_zip).exists():
            with open(last_zip, "rb") as fz:
                st.download_button(
                    "⬇️ Download Overleaf ZIP Bundle",
                    data=fz.read(),
                    file_name=Path(last_zip).name,
                    mime="application/zip",
                    use_container_width=True
                )

        st.markdown("---")
        st.markdown("#### ⚡ Local PDF Compilation")
        st.caption("Checks for pdflatex or tectonic on system.")
        if st.button("🔨 Compile to PDF Locally", use_container_width=True):
            last_pkg = getattr(st.session_state, "last_pkg_dir", None)
            if not last_pkg or not Path(last_pkg).exists():
                pkg_dir, _ = create_latex_package(
                    output_dir=OUTPUTS_DIR,
                    main_tex=proj["latex"]["compiled_tex"],
                    bibtex_content=proj["literature_review"].get("bibtex_entries", ""),
                    figures_list=proj.get("figures", []),
                    project_name=proj.get("project_name", "paper")
                )
                last_pkg = str(pkg_dir)

            success_c, pdf_p, c_log = attempt_local_compile(Path(last_pkg))
            if success_c and pdf_p and pdf_p.exists():
                st.success("PDF Compiled Successfully!")
                with open(pdf_p, "rb") as fp:
                    st.download_button("⬇️ Download main.pdf", data=fp.read(), file_name="main.pdf", mime="application/pdf")
            else:
                st.warning("Local compiler output / status:")
                st.code(c_log[:500] if c_log else "No local compiler detected.")
                st.info("💡 You can upload the generated ZIP directly to Overleaf for 1-click cloud PDF compilation!")


# =============================================================
# TAB 9: FINAL PAPER & EXPORT PORTAL (Step 8)
# =============================================================
with tabs[8]:
    st.subheader("🚀 Methodology Step 8: Final Paper Audit & Export Portal")
    st.write("Comprehensive publication readiness check, multi-format export, and conference presentation slide deck generator.")

    col_fp1, col_fp2 = st.columns([1, 1.2])

    with col_fp1:
        st.markdown("#### 🩺 Submission Readiness Audit")
        health = audit_paper_health(proj)

        st.metric("Readiness Score", f"{health['score']}%", delta="Camera Ready" if health["score"] >= 85 else "Revisions Needed")

        for item in health["checklist"]:
            st.markdown(f"{'✅' if item['passed'] else '⚠️'} **{item['name']}**<br><small style='color:#64748b;'>{item['detail']}</small>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📤 Multi-Format Exports")
        
        md_content = export_as_markdown(proj)
        st.download_button("⬇️ Download Full Manuscript (.md)", data=md_content, file_name=f"{proj['project_name'].lower().replace(' ', '_')}.md", mime="text/markdown", use_container_width=True)

        html_content = export_as_html(proj)
        st.download_button("⬇️ Download Academic HTML Pre-print (.html)", data=html_content, file_name=f"{proj['project_name'].lower().replace(' ', '_')}.html", mime="text/html", use_container_width=True)

        bib_content = proj["literature_review"].get("bibtex_entries", "")
        st.download_button("⬇️ Download References (.bib)", data=bib_content, file_name="references.bib", mime="text/plain", use_container_width=True)

    with col_fp2:
        st.markdown("#### 🎤 Conference Spotlight Slide Deck")
        st.caption("Generate a 6-slide presentation script for your conference spotlight/oral.")

        if st.button("🤖 Generate Spotlight Slide Deck", type="primary", use_container_width=True):
            with st.spinner("Generating conference slide deck script..."):
                deck = generate_presentation_slides(
                    project_data=proj,
                    provider=provider_choice,
                    model=model_choice,
                    api_key=api_key_input
                )
                proj["refinement"]["slide_deck"] = deck
                st.success("Slide Deck Generated!")
                st.rerun()

        deck_content = proj["refinement"].get("slide_deck", "")
        if deck_content:
            st.markdown(deck_content)
            st.download_button("⬇️ Download Slides Script (.md)", data=deck_content, file_name="conference_presentation.md", mime="text/markdown")
        else:
            st.info("Click 'Generate Spotlight Slide Deck' to synthesize your conference oral presentation script.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:0.85rem;'>AI Research Paper Assistant • Built for NeurIPS, IEEE, ACM & Nature Submissions • Python 3.11/3.13 & Streamlit</p>", unsafe_allow_html=True)
