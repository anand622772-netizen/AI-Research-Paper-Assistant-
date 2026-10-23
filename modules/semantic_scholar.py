"""
Semantic Scholar & ArXiv API integration module for AI Research Paper Assistant.
Provides academic literature search, metadata extraction, BibTeX generation,
and fallback capabilities.
"""

import json
import logging
import re
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional
import requests

logger = logging.getLogger(__name__)

SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper"
ARXIV_API_URL = "http://export.arxiv.org/api/query"

# Curated fallback papers for offline or rate-limited environments
CURATED_PAPERS: List[Dict[str, Any]] = [
    {
        "paperId": "vaswani2017attention",
        "title": "Attention Is All You Need",
        "authors": [{"name": "Ashish Vaswani"}, {"name": "Noam Shazeer"}, {"name": "Niki Parmar"}, {"name": "Jakob Uszkoreit"}, {"name": "Llion Jones"}, {"name": "Aidan N. Gomez"}, {"name": "Lukasz Kaiser"}, {"name": "Illia Polosukhin"}],
        "year": 2017,
        "venue": "NeurIPS 2017",
        "citationCount": 115000,
        "influentialCitationCount": 18500,
        "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.",
        "url": "https://arxiv.org/abs/1706.03762",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/1706.03762.pdf"},
        "fieldsOfStudy": ["Computer Science", "Artificial Intelligence"],
        "externalIds": {"ArXiv": "1706.03762", "DOI": "10.48550/arXiv.1706.03762"}
    },
    {
        "paperId": "devlin2018bert",
        "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "authors": [{"name": "Jacob Devlin"}, {"name": "Ming-Wei Chang"}, {"name": "Kenton Lee"}, {"name": "Kristina Toutanova"}],
        "year": 2018,
        "venue": "NAACL 2019",
        "citationCount": 78000,
        "influentialCitationCount": 11200,
        "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks.",
        "url": "https://arxiv.org/abs/1810.04805",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/1810.04805.pdf"},
        "fieldsOfStudy": ["Computer Science", "Computation and Language"],
        "externalIds": {"ArXiv": "1810.04805"}
    },
    {
        "paperId": "brown2020language",
        "title": "Language Models are Few-Shot Learners",
        "authors": [{"name": "Tom B. Brown"}, {"name": "Benjamin Mann"}, {"name": "Nick Ryder"}, {"name": "Melanie Subbiah"}, {"name": "Jared Kaplan"}, {"name": "Prafulla Dhariwal"}, {"name": "Arvind Neelakantan"}, {"name": "Pranav Shyam"}, {"name": "Girish Sastry"}, {"name": "Amanda Askell"}, {"name": "Dario Amodei"}],
        "year": 2020,
        "venue": "NeurIPS 2020",
        "citationCount": 38000,
        "influentialCitationCount": 6500,
        "abstract": "Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While also applied to architectures with hundreds of millions of parameters, this paradigm still requires task-specific fine-tuning datasets of thousands of examples. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art fine-tuning approaches. We train GPT-3, an autoregressive language model with 175 billion parameters.",
        "url": "https://arxiv.org/abs/2005.14165",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/2005.14165.pdf"},
        "fieldsOfStudy": ["Computer Science", "Artificial Intelligence"],
        "externalIds": {"ArXiv": "2005.14165"}
    },
    {
        "paperId": "lewis2020retrieval",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "authors": [{"name": "Patrick Lewis"}, {"name": "Ethan Perez"}, {"name": "Aleksandra Piktus"}, {"name": "Fabio Petroni"}, {"name": "Vladimir Karpukhin"}, {"name": "Naman Goyal"}, {"name": "Heinrich Küttler"}, {"name": "Mike Lewis"}, {"name": "Wen-tau Yih"}, {"name": "Tim Rocktäschel"}, {"name": "Sebastian Riedel"}, {"name": "Douwe Kiela"}],
        "year": 2020,
        "venue": "NeurIPS 2020",
        "citationCount": 6500,
        "influentialCitationCount": 980,
        "abstract": "Large pre-trained language models store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to precisely access and manipulate knowledge is still limited. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) models which combine pre-trained parametric and non-parametric memory for language generation.",
        "url": "https://arxiv.org/abs/2005.11401",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/2005.11401.pdf"},
        "fieldsOfStudy": ["Computer Science", "Computation and Language"],
        "externalIds": {"ArXiv": "2005.11401"}
    },
    {
        "paperId": "ouyang2022instructgpt",
        "title": "Training language models to follow instructions with human feedback",
        "authors": [{"name": "Long Ouyang"}, {"name": "Jeff Wu"}, {"name": "Xu Jiang"}, {"name": "Diogo Almeida"}, {"name": "Carroll L. Wainwright"}, {"name": "Pamela Mishkin"}, {"name": "Chong Zhang"}, {"name": "Sandhini Agarwal"}, {"name": "Katarina Slama"}, {"name": "Alex Ray"}, {"name": "John Schulman"}, {"name": "Jacob Hilton"}, {"name": "Fraser Kelton"}, {"name": "Luke Miller"}, {"name": "Maddie Simens"}, {"name": "Amanda Askell"}, {"name": "Peter Welinder"}, {"name": "Paul Christiano"}, {"name": "Jan Leike"}, {"name": "Ryan Lowe"}],
        "year": 2022,
        "venue": "NeurIPS 2022",
        "citationCount": 8900,
        "influentialCitationCount": 1600,
        "abstract": "Making language models bigger does not inherently make them better at following a user's intent. Large models can generate untruthful, toxic, or simply unhelpful outputs. In this paper, we show an avenue for aligning language models with user intent on a wide range of tasks by fine-tuning with human feedback (RLHF).",
        "url": "https://arxiv.org/abs/2203.02155",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/2203.02155.pdf"},
        "fieldsOfStudy": ["Computer Science", "Machine Learning"],
        "externalIds": {"ArXiv": "2203.02155"}
    },
    {
        "paperId": "ho2020ddpm",
        "title": "Denoising Diffusion Probabilistic Models",
        "authors": [{"name": "Jonathan Ho"}, {"name": "Ajay Jain"}, {"name": "Pieter Abbeel"}],
        "year": 2020,
        "venue": "NeurIPS 2020",
        "citationCount": 14200,
        "influentialCitationCount": 2400,
        "abstract": "We present high quality image synthesis results using diffusion probabilistic models, a class of latent variable models inspired by considerations from nonequilibrium thermodynamics. Our best results are obtained by training on a weighted variational bound designed according to a novel connection between diffusion models and denoising score matching with Langevin dynamics.",
        "url": "https://arxiv.org/abs/2006.11239",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/2006.11239.pdf"},
        "fieldsOfStudy": ["Computer Science", "Machine Learning"],
        "externalIds": {"ArXiv": "2006.11239"}
    },
    {
        "paperId": "touvron2023llama",
        "title": "LLaMA: Open and Efficient Foundation Language Models",
        "authors": [{"name": "Hugo Touvron"}, {"name": "Thibaut Lavril"}, {"name": "Gautier Izacard"}, {"name": "Xavier Martinet"}, {"name": "Marie-Anne Lachaux"}, {"name": "Timothée Lacroix"}, {"name": "Baptiste Rozière"}, {"name": "Naman Goyal"}, {"name": "Eric Hambro"}, {"name": "Faisal Azhar"}, {"name": "Aurelien Rodriguez"}, {"name": "Armand Joulin"}, {"name": "Edouard Grave"}, {"name": "Guillaume Lample"}],
        "year": 2023,
        "venue": "arXiv preprint",
        "citationCount": 12400,
        "influentialCitationCount": 1950,
        "abstract": "We introduce LLaMA, a collection of foundation language models ranging from 7B to 65B parameters. We train our models on trillions of tokens, and show that it is possible to train state-of-the-art models using publicly available datasets exclusively, without resorting to proprietary or inaccessible datasets.",
        "url": "https://arxiv.org/abs/2302.13971",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/2302.13971.pdf"},
        "fieldsOfStudy": ["Computer Science", "Computation and Language"],
        "externalIds": {"ArXiv": "2302.13971"}
    },
    {
        "paperId": "dao2022flashattention",
        "title": "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness",
        "authors": [{"name": "Tri Dao"}, {"name": "Daniel Y. Fu"}, {"name": "Stefano Ermon"}, {"name": "Atri Rudra"}, {"name": "Christopher Ré"}],
        "year": 2022,
        "venue": "NeurIPS 2022",
        "citationCount": 3100,
        "influentialCitationCount": 540,
        "abstract": "Transformers are slow and memory-hungry on long sequences, since the time and memory complexity of self-attention are quadratic in sequence length. Approximate attention methods have attempted to address this, but often trade off model quality. We propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce memory reads/writes between GPU HBM and SRAM.",
        "url": "https://arxiv.org/abs/2205.14135",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/2205.14135.pdf"},
        "fieldsOfStudy": ["Computer Science", "Hardware and Architecture"],
        "externalIds": {"ArXiv": "2205.14135"}
    }
]


def clean_bibtex_key(author_str: str, year: Any, title: str) -> str:
    """Generate a clean BibTeX key e.g. 'vaswani2017attention'."""
    last_name = "author"
    if author_str:
        # Get first author's last name
        first_author = author_str.split(",")[0].strip()
        parts = first_author.split(" ")
        last_name = re.sub(r"[^a-zA-Z]", "", parts[-1]).lower()
        if not last_name:
            last_name = "author"
    
    yr = str(year) if year else "2024"
    
    # First key word of title
    title_words = [w.lower() for w in re.findall(r"[a-zA-Z]{3,}", title)]
    kw = title_words[0] if title_words else "paper"
    return f"{last_name}{yr}{kw}"


def paper_to_bibtex(paper: Dict[str, Any]) -> str:
    """Format a paper dictionary into a valid standard BibTeX string."""
    authors = paper.get("authors", [])
    if isinstance(authors, list):
        if authors and isinstance(authors[0], dict):
            author_str = " and ".join([a.get("name", "Unknown") for a in authors])
        elif authors and isinstance(authors[0], str):
            author_str = " and ".join(authors)
        else:
            author_str = "Unknown Authors"
    else:
        author_str = str(authors)

    title = paper.get("title", "Untitled Manuscript")
    year = paper.get("year", "2024")
    venue = paper.get("venue") or "arXiv preprint"
    key = clean_bibtex_key(author_str, year, title)
    
    doi = ""
    external_ids = paper.get("externalIds") or {}
    if isinstance(external_ids, dict) and "DOI" in external_ids:
        doi = f"  doi = {{{external_ids['DOI']}}},\n"
    elif "doi" in paper and paper["doi"]:
        doi = f"  doi = {{{paper['doi']}}},\n"

    url_entry = ""
    if paper.get("url"):
        url_entry = f"  url = {{{paper['url']}}},\n"

    bibtex = f"""@article{{{key},
  title = {{{{{title}}}}},
  author = {{{author_str}}},
  journal = {{{venue}}},
  year = {{{year}}},
{doi}{url_entry}  eprint = {{{paper.get('paperId', '')}}}
}}"""
    return bibtex


def search_semantic_scholar(
    query: str,
    api_key: Optional[str] = None,
    limit: int = 10,
    year_range: Optional[str] = None,
    fields_of_study: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Search papers using Semantic Scholar API with fallback to arXiv and curated set.
    """
    if not query.strip():
        return {"papers": [], "total": 0, "source": "empty_query"}

    headers = {"User-Agent": "AIResearchPaperAssistant/1.0"}
    if api_key:
        headers["x-api-key"] = api_key

    params = {
        "query": query,
        "limit": min(limit, 30),
        "fields": "paperId,title,abstract,authors,year,citationCount,influentialCitationCount,venue,url,openAccessPdf,fieldsOfStudy,publicationTypes,externalIds"
    }
    if year_range:
        params["year"] = year_range
    if fields_of_study:
        params["fieldsOfStudy"] = ",".join(fields_of_study)

    try:
        resp = requests.get(SEMANTIC_SCHOLAR_SEARCH_URL, params=params, headers=headers, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            papers = data.get("data", [])
            for p in papers:
                p["bibtex"] = paper_to_bibtex(p)
                p["source"] = "semantic_scholar"
            return {"papers": papers, "total": data.get("total", len(papers)), "source": "semantic_scholar"}
        else:
            logger.warning(f"Semantic Scholar API returned {resp.status_code}. Attempting arXiv fallback.")
    except Exception as e:
        logger.warning(f"Semantic Scholar search error: {e}. Attempting arXiv fallback.")

    # Try ArXiv API Fallback
    arxiv_result = search_arxiv(query, limit=limit)
    if arxiv_result.get("papers"):
        return arxiv_result

    # Fallback to local curated matching
    matched = []
    q_lower = query.lower()
    for cp in CURATED_PAPERS:
        if (q_lower in cp["title"].lower() or 
            any(q_lower in a.get("name", "").lower() for a in cp.get("authors", [])) or
            q_lower in cp.get("abstract", "").lower() or
            any(w in cp["title"].lower() for w in q_lower.split())):
            paper_copy = dict(cp)
            paper_copy["bibtex"] = paper_to_bibtex(paper_copy)
            paper_copy["source"] = "curated_library"
            matched.append(paper_copy)

    if not matched:
        # Return top curated papers if no exact keyword match
        matched = [dict(p) for p in CURATED_PAPERS[:limit]]
        for p in matched:
            p["bibtex"] = paper_to_bibtex(p)
            p["source"] = "curated_library"

    return {"papers": matched, "total": len(matched), "source": "curated_library (offline/rate-limit fallback)"}


def search_arxiv(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search papers using ArXiv public XML API."""
    try:
        clean_q = urllib.parse.quote(query)
        url = f"{ARXIV_API_URL}?search_query=all:{clean_q}&start=0&max_results={limit}&sortBy=relevance&sortOrder=descending"
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return {"papers": [], "total": 0, "source": "arxiv_failed"}

        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        
        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            id_tag = entry.find("atom:id", ns)
            published = entry.find("atom:published", ns)
            
            authors_list = []
            for author in entry.findall("atom:author", ns):
                name_elem = author.find("atom:name", ns)
                if name_elem is not None and name_elem.text:
                    authors_list.append({"name": name_elem.text.strip()})
            
            raw_title = title.text.replace("\n", " ").strip() if title is not None and title.text else "Untitled"
            raw_abstract = summary.text.replace("\n", " ").strip() if summary is not None and summary.text else ""
            paper_id = id_tag.text.split("/abs/")[-1] if id_tag is not None and id_tag.text else "unknown"
            year = int(published.text[:4]) if published is not None and published.text else 2024
            
            paper = {
                "paperId": f"arxiv_{paper_id}",
                "title": raw_title,
                "abstract": raw_abstract,
                "authors": authors_list,
                "year": year,
                "citationCount": 0,
                "influentialCitationCount": 0,
                "venue": "arXiv preprint",
                "url": f"https://arxiv.org/abs/{paper_id}",
                "openAccessPdf": {"url": f"https://arxiv.org/pdf/{paper_id}.pdf"},
                "fieldsOfStudy": ["Computer Science"],
                "externalIds": {"ArXiv": paper_id},
                "source": "arxiv"
            }
            paper["bibtex"] = paper_to_bibtex(paper)
            papers.append(paper)
            
        return {"papers": papers, "total": len(papers), "source": "arxiv"}
    except Exception as e:
        logger.warning(f"ArXiv query failed: {e}")
        return {"papers": [], "total": 0, "source": "arxiv_error"}
