# 🎓 AI Research Paper Assistant

An end-to-end, academic-grade AI research paper portal and manuscript authoring platform built with **Python 3.11/3.13**, **Streamlit**, **OpenAI & Google Gemini**, and **Semantic Scholar API**.

---

## 🚀 Key Features & Working Methodology

The platform provides a complete academic workflow mirroring the real-world scientific paper development process:

```
[1. Paper Portal] ──> [2. Research Material] ──> [3. Paper Outline] ──> [4. Literature Review]
                                                                                │
[8. Final Paper & Export] <── [7. LaTeX Studio] <── [6. Plots Studio] <── [5. Section Writing]
```

### 1. 🔍 Research Paper Portal (Semantic Scholar & ArXiv API)
- Real-time querying against millions of papers using the **Semantic Scholar Graph API** and **ArXiv API**.
- Filter by topic, author, year range, and venue.
- Automatic **BibTeX generation** with clean citation keys.
- Direct links to open-access PDFs and publisher DOIs.
- 1-click **Add to Research Material** bookmarking.

### 2. 📚 Methodology Step 1: Research Material & Hypothesis Hub
- Curated literature repository linked directly to your active project.
- Upload / edit experimental lab notes, hypotheses, and preliminary observations.
- **AI-driven Research Insights**: Automatically extracts the formal **Problem Statement**, **Research Gap**, **Core Novel Contribution**, and **Recommended Benchmark Datasets**.

### 3. 📐 Methodology Step 2: Outline Generator & Structural Hierarchy
- Template presets matching top publication venues:
  - **NeurIPS / ICLR**
  - **IEEE Transactions / Conference**
  - **ACM SIGCONF**
  - **Nature / Scientific Reports**
  - **Standard Academic Article**
- AI-synthesized section-by-section outline with objectives, bullet points, target word counts, and completion statuses.
- Interactive outline editor: add, delete, and reorder sections.

### 4. 🔬 Methodology Step 3: Literature Review & Comparative Matrix
- Synthesizes related work narrative with proper in-text citation keys (e.g. `\cite{vaswani2017attention}`).
- **Comparative Analysis Matrix**: Interactive tabular comparison of prior art (Method, Benchmark, Pros, Cons, Citation Keys).
- Built-in **BibTeX Repository (`references.bib`)** with automatic deduplication and syntax validation.

### 5. ✍️ Methodology Step 4: Academic Section Writing Studio
- Context-aware generation conditioned on paper title, outline objectives, lab notes, and cited references.
- Selectable writing tones: *Formal Academic*, *Rigorous Theoretical*, *Empirical Focus*, *Concise Letter*.
- LaTeX equations support (`\begin{equation} ... \end{equation}`).
- Algorithmic pseudo-code generation (`\begin{algorithmic}`).
- Publication table generation with `booktabs` formatting.
- Live dual-pane Markdown/LaTeX preview with real-time word counting.

### 6. ✨ Methodology Step 5: Refinement, Academic Polish & Peer Review
- **Tone & Clarity Polisher**: Enhances precision, eliminates colloquialisms, and balances active/passive voice.
- **Simulated 3-Reviewer Committee (NeurIPS/IEEE Criterion)**:
  - Reviewer 1 (Theoretical Specialist)
  - Reviewer 2 (Empirical & Systems Specialist)
  - Meta-Reviewer Synthesis
  - Scores (Soundness, Presentation, Novelty, Overall 1-10) with actionable revision critiques.
- **Citation & Claim Auditor**: Flags unsupported claims and verifies that all `\cite{}` keys exist in `references.bib`.

### 7. 📊 Methodology Step 6: Publication Plots & Visuals Studio
- Pre-configured publication chart templates:
  - Inference Latency Scaling Curve (log-scale)
  - Multi-Task Benchmark Accuracy Comparison
  - Discretization / Hyperparameter Heatmap
  - Training Loss Convergence with Confidence Intervals
- Interactive Python code editor & runner (Matplotlib, Seaborn).
- High-resolution export (300 DPI PNG, vector PDF).
- Auto-generates ready-to-copy `\begin{figure}` LaTeX code with captions and labels.

### 8. 📑 Methodology Step 7: LaTeX Studio & Manuscript Compiler
- Full LaTeX manuscript assembly for NeurIPS, IEEEtran, ACM, and Standard Article classes.
- Live `main.tex` code editor.
- **Overleaf & LaTeX ZIP Packager**: Bundles `main.tex`, `references.bib`, figure files, `compile.bat`, `Makefile`, and `README.txt`.
- Local PDF compiler detection (`pdflatex`, `tectonic`).

### 9. 🚀 Methodology Step 8: Final Paper Audit & Export Portal
- **Submission Readiness Score** (0-100%) with automated checklist (abstract word limit, section completeness, citation resolution, figure checks).
- Multi-format exports:
  - Download Complete Overleaf ZIP Package
  - Download Full Manuscript Markdown (`.md`)
  - Download Academic HTML Pre-print (`.html`)
  - Download BibTeX Database (`.bib`)
- **Conference Spotlight Slide Deck Generator**: Generates a 6-slide presentation script with speaker delivery notes.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.11 / 3.13 |
| **User Interface** | Streamlit |
| **AI / LLMs** | Google Gemini (`google-genai`), OpenAI (`openai`), and Offline Academic Mock Engine |
| **Literature Search** | Semantic Scholar Graph API & ArXiv XML API |
| **Plotting & Visuals** | Matplotlib, Seaborn, Plotly |
| **Manuscript Engine** | LaTeX (`pdflatex`, `tectonic`, Overleaf ZIP) |
| **Data & Configuration** | JSON, `.env` (`python-dotenv`) |

---

## 📦 Installation & Setup

### 1. Clone or Navigate to Project
```bash
cd C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional)
Copy `.env.example` to `.env` and configure your keys:
```bash
cp .env.example .env
```
*(Note: If you do not have API keys, the application seamlessly runs using the built-in **Offline Academic Engine** with zero setup!)*

### 4. Launch the Web Application
```bash
python -m streamlit run app.py
```
Or double-click `run_app.bat` on Windows.
