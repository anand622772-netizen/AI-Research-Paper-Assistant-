"""
Comprehensive verification test suite for AI Research Paper Assistant.
Tests all methodology modules, search APIs, plotting engine, and LaTeX generators.
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import DATA_DIR, OUTPUTS_DIR, SAMPLES_DIR, CONFERENCE_TEMPLATES
from modules.semantic_scholar import search_semantic_scholar, clean_bibtex_key, paper_to_bibtex, CURATED_PAPERS
from modules.llm_provider import llm_service
from modules.project_state import ProjectState
from modules.methodology.material import extract_research_insights
from modules.methodology.outline import generate_structured_outline
from modules.methodology.lit_review import synthesize_literature_review
from modules.methodology.section_writer import draft_paper_section
from modules.methodology.refinement import polish_academic_tone, simulate_peer_review, audit_citations_and_claims
from modules.plotting.studio import CHART_TEMPLATES, execute_plot_code, generate_latex_figure_snippet
from modules.latex.templates import render_latex_manuscript, markdown_to_latex
from modules.latex.bibtex_manager import deduplicate_bibtex, validate_bibtex_syntax
from modules.latex.compiler import check_local_latex_compilers, create_latex_package
from modules.final_paper.portal import audit_paper_health, export_as_markdown, export_as_html, generate_presentation_slides


class TestAIResearchPaperAssistant(unittest.TestCase):

    def setUp(self):
        self.project = ProjectState.create_empty_project(name="Test Paper Project", template="NeurIPS / ICLR")

    def test_semantic_scholar_search_and_bibtex(self):
        """Test search query, fallback handling, and BibTeX conversion."""
        res = search_semantic_scholar("Transformer Attention", limit=3)
        self.assertIn("papers", res)
        self.assertTrue(len(res["papers"]) > 0)
        
        first_paper = res["papers"][0]
        self.assertIn("title", first_paper)
        bib = paper_to_bibtex(first_paper)
        self.assertIn("@article", bib)
        self.assertIn("title", bib)

    def test_llm_provider_offline_engine(self):
        """Test that offline engine generates high-quality structured content without API keys."""
        resp = llm_service.generate("Generate paper outline", task_context="outline")
        self.assertIn("Introduction", resp)
        self.assertIn("Methodology", resp)

    def test_methodology_step1_material(self):
        """Test research insight extraction."""
        insights = extract_research_insights(
            papers=CURATED_PAPERS[:2],
            notes=["Test lab note: state dimension N=64 is optimal"],
            provider="offline"
        )
        self.assertIn("problem_statement", insights)
        self.assertIn("research_gap", insights)
        self.assertIn("proposed_contribution", insights)

    def test_methodology_step2_outline(self):
        """Test outline generator for different templates."""
        outline = generate_structured_outline(
            paper_title="Adaptive State Space Models",
            template_name="IEEE Transactions / Conference",
            insights={"problem_statement": "Efficiency issue"},
            provider="offline"
        )
        self.assertTrue(len(outline) >= 4)
        self.assertIn("title", outline[0])

    def test_methodology_step3_lit_review(self):
        """Test literature review synthesizer and comparative matrix."""
        res = synthesize_literature_review(
            papers=CURATED_PAPERS[:3],
            proposed_work_title="DSO Operator",
            research_gap="Quadratic attention overhead",
            provider="offline"
        )
        self.assertIn("synthesis_text", res)
        self.assertIn("matrix", res)
        self.assertTrue(len(res["matrix"]) > 0)

    def test_methodology_step4_section_writer(self):
        """Test section drafting with equations and algorithmic blocks."""
        draft = draft_paper_section(
            section_name="Proposed Methodology",
            paper_metadata=self.project["metadata"],
            outline_item=self.project["outline"][3],
            research_insights=self.project["research_materials"]["extracted_insights"],
            cited_papers=CURATED_PAPERS[:2],
            include_equations=True,
            provider="offline"
        )
        self.assertTrue(len(draft) > 100)
        self.assertTrue("\\begin{equation}" in draft or "equation" in draft.lower() or "\\mathbf" in draft)

    def test_methodology_step5_refinement(self):
        """Test peer review simulation and citation auditor."""
        sim = simulate_peer_review(
            paper_title=self.project["metadata"]["title"],
            abstract=self.project["sections"]["Abstract"],
            sections_summary="Summary of sections",
            provider="offline"
        )
        self.assertIn("reviewers", sim)
        self.assertTrue(len(sim["reviewers"]) >= 2)

        audit = audit_citations_and_claims(
            manuscript_text="As shown in \\cite{vaswani2017attention} and \\cite{unknown2099}.",
            bibtex_entries="@article{vaswani2017attention,\n  title={Attention}\n}"
        )
        self.assertIn("vaswani2017attention", audit["verified_in_bibtex"])
        self.assertIn("unknown2099", audit["missing_from_bibtex"])

    def test_methodology_step6_plotting_studio(self):
        """Test plotting code execution and export."""
        plots_dir = OUTPUTS_DIR / "test_plots"
        code = CHART_TEMPLATES["Latency vs Context Length (Scaling Curve)"]
        success, png_path, err = execute_plot_code(code, plots_dir, "test_latency_scaling")
        self.assertTrue(success, f"Plot error: {err}")
        self.assertTrue(Path(png_path).exists())

        latex_snippet = generate_latex_figure_snippet("test_latency_scaling.png", "Sample caption", "fig:sample")
        self.assertIn("\\begin{figure}", latex_snippet)
        self.assertIn("\\caption{Sample caption}", latex_snippet)

    def test_methodology_step7_latex_and_zip(self):
        """Test LaTeX assembly and ZIP bundle packaging."""
        tex = render_latex_manuscript(
            template_name="NeurIPS / ICLR",
            metadata=self.project["metadata"],
            abstract=self.project["sections"]["Abstract"],
            sections=self.project["sections"]
        )
        self.assertIn("\\documentclass", tex)
        self.assertIn("\\begin{document}", tex)
        self.assertIn("\\bibliography{references}", tex)

        pkg_dir, zip_path = create_latex_package(
            output_dir=OUTPUTS_DIR,
            main_tex=tex,
            bibtex_content="@article{vaswani2017attention, title={Attention}}",
            figures_list=[],
            project_name="unit_test_paper"
        )
        self.assertTrue(pkg_dir.exists())
        self.assertTrue(zip_path.exists())

    def test_methodology_step8_final_audit_and_exports(self):
        """Test paper health audit, markdown export, and HTML pre-print."""
        health = audit_paper_health(self.project)
        self.assertIn("score", health)
        self.assertIn("checklist", health)

        md = export_as_markdown(self.project)
        self.assertIn("# ", md)
        self.assertIn("## Abstract", md)

        html = export_as_html(self.project)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("abstract-box", html)


if __name__ == "__main__":
    unittest.main()
