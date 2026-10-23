# AI Research Paper Assistant - Configuration & Environment Setup
import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
SAMPLES_DIR = PROJECT_ROOT / "sample_data"

DATA_DIR.mkdir(exist_ok=True, parents=True)
OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)
SAMPLES_DIR.mkdir(exist_ok=True, parents=True)

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

# Sync Streamlit secrets to environment if deployed on Streamlit Cloud
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for k, v in st.secrets.items():
            if k not in os.environ and isinstance(v, str):
                os.environ[k] = v
except Exception:
    pass

# LLM Providers Configuration
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")

# Academic conference & journal template definitions
CONFERENCE_TEMPLATES = {
    "NeurIPS / ICLR": {
        "class": "article",
        "doc_style": "neurips",
        "description": "Leading machine learning conference layout with 2-column or 1-column single-blind/double-blind formatting.",
        "sections": [
            "Abstract",
            "Introduction",
            "Related Work",
            "Theoretical Framework & Methodology",
            "Empirical Experiments & Results",
            "Ablation Studies & Discussion",
            "Broader Impact & Ethical Considerations",
            "Conclusion & Future Work"
        ]
    },
    "IEEE Transactions / Conference": {
        "class": "IEEEtran",
        "doc_style": "ieeetran",
        "description": "Standard IEEE two-column technical format with roman numerals and standard IEEE citation style.",
        "sections": [
            "Abstract",
            "Introduction",
            "System Architecture & Problem Formulation",
            "Proposed Algorithm / Methodology",
            "Performance Evaluation & Simulation",
            "Comparative Analysis & Discussion",
            "Conclusion and Acknowledgments"
        ]
    },
    "ACM SIGCONF": {
        "class": "acmart",
        "doc_style": "acm",
        "description": "Association for Computing Machinery conference format with CCS concepts and ACM keywords.",
        "sections": [
            "Abstract",
            "Introduction",
            "Background & Motivation",
            "Design & Implementation",
            "Evaluation",
            "Related Work",
            "Threats to Validity",
            "Conclusion"
        ]
    },
    "Nature / Scientific Reports": {
        "class": "article",
        "doc_style": "nature",
        "description": "Interdisciplinary scientific style with narrative introduction, direct results, discussion, and separated detailed methods.",
        "sections": [
            "Abstract",
            "Introduction",
            "Results",
            "Discussion",
            "Methods & Data Availability",
            "References"
        ]
    },
    "Standard Academic Article": {
        "class": "article",
        "doc_style": "generic",
        "description": "Universal LaTeX article format with modern typography, microtype, booktabs, and amsmath.",
        "sections": [
            "Abstract",
            "Introduction",
            "Literature Review",
            "Proposed Framework",
            "Experimental Setup & Results",
            "Discussion",
            "Conclusion"
        ]
    }
}
