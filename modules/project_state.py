"""
Project state manager for AI Research Paper Assistant.
Handles persistence, JSON export/import, default structures, and sample research projects.
"""

import os
import json
import uuid
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

class ProjectState:
    @staticmethod
    def create_empty_project(name: str = "New Research Project", template: str = "NeurIPS / ICLR") -> Dict[str, Any]:
        """Creates a brand new blank research paper project."""
        proj_id = str(uuid.uuid4())[:8]
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        default_outline = [
            {"id": "sec_abstract", "title": "Abstract", "level": 1, "objective": "Synthesize problem, method, and empirical gains in <= 250 words.", "bullet_points": ["Context & core bottleneck", "Proposed method", "Key quantitative result"], "target_words": 200, "status": "Drafted"},
            {"id": "sec_intro", "title": "1. Introduction", "level": 1, "objective": "Establish research problem, state hypothesis, and list explicit contributions.", "bullet_points": ["Motivation in foundation models", "Limitations of current linear/quadratic operators", "Our 3 primary contributions"], "target_words": 900, "status": "Drafted"},
            {"id": "sec_related", "title": "2. Related Work", "level": 1, "objective": "Contextualize within recent literature and contrast against baselines.", "bullet_points": ["Attention approximations", "State-space models (SSMs)", "Hardware-aware algorithms"], "target_words": 800, "status": "Drafted"},
            {"id": "sec_method", "title": "3. Proposed Methodology", "level": 1, "objective": "Formulate mathematical framework, algorithms, and theoretical proofs.", "bullet_points": ["Discretization operator", "Selective gating mechanism", "Fused kernel implementation", "Complexity analysis"], "target_words": 1400, "status": "Drafted"},
            {"id": "sec_exp", "title": "4. Empirical Evaluation", "level": 1, "objective": "Present benchmark results, baselines, and rigorous ablation studies.", "bullet_points": ["Evaluation benchmarks & setups", "Main accuracy vs latency comparisons", "Ablation on state dimensions", "Long sequence memory scaling"], "target_words": 1200, "status": "Drafted"},
            {"id": "sec_disc", "title": "5. Discussion & Limitations", "level": 1, "objective": "Discuss theoretical implications, deployment constraints, and ethical impact.", "bullet_points": ["Hardware specificity", "Generalization limits", "Compute sustainability"], "target_words": 600, "status": "Drafted"},
            {"id": "sec_conclusion", "title": "6. Conclusion", "level": 1, "objective": "Summarize conclusions and provide forward-looking directions.", "bullet_points": ["Summary of validated findings", "Future multimodal extensions"], "target_words": 300, "status": "Drafted"}
        ]

        return {
            "id": proj_id,
            "project_name": name,
            "created_at": now,
            "updated_at": now,
            "template": template,
            "metadata": {
                "title": "Scalable Selective State-Space Neural Operators for Sub-Quadratic Sequence Modeling",
                "authors": [
                    {"name": "Alex Mercer", "affiliation": "Stanford AI Lab", "email": "amercer@stanford.edu"},
                    {"name": "Elena Rostova", "affiliation": "MIT CSAIL", "email": "erostova@mit.edu"}
                ],
                "keywords": ["State-Space Models", "Transformers", "Hardware-Aware AI", "Deep Learning", "Efficiency"],
                "subject_class": "I.2.7 [Artificial Intelligence]: Natural Language Processing",
                "target_conference": "NeurIPS 2026"
            },
            "research_materials": {
                "saved_papers": [],
                "user_notes": [
                    "Empirical finding: Standard attention hits VRAM limit at sequence length L=16k on A100 80GB.",
                    "Hypothesis: Discretizing continuous SSMs with input-dependent step sizes preserves selective associative recall while maintaining O(L) time.",
                    "Baseline comparisons: FlashAttention-2, Mamba-1, Transformer-XL, RWKV-5."
                ],
                "extracted_insights": {
                    "problem_statement": "Dense quadratic self-attention introduces severe IO memory bottlenecks on extended sequences, limiting context windows and real-time inference throughput.",
                    "research_gap": "Current linear attention methods sacrifice associative recall, while existing state-space models suffer from synchronization barriers across distributed accelerators.",
                    "proposed_contribution": "A fused selective state-space operator that synchronizes IO-aware memory access with continuous discretization bounds, achieving 2.4x throughput speedup without accuracy degradation.",
                    "benchmark_datasets": ["Long Range Arena (LRA)", "GLUE Benchmark", "Pile-10k Token Evaluation", "ImageNet-1K Tokenized"]
                }
            },
            "outline": default_outline,
            "literature_review": {
                "synthesis_text": "",
                "matrix": [
                    {"author_year": "Vaswani et al. (2017)", "method": "Transformer Attention", "benchmark": "WMT'14 Translation", "pros": "High associative expressivity, parallel training", "cons": "Quadratic O(L^2) memory and compute barrier", "citation_key": "vaswani2017attention"},
                    {"author_year": "Dao et al. (2022)", "method": "FlashAttention", "benchmark": "BERT / GPT Scaling", "pros": "Hardware IO-aware tiling, no intermediate HBM writes", "cons": "Fundamental computational complexity remains O(L^2)", "citation_key": "dao2022flashattention"},
                    {"author_year": "Gu et al. (2023)", "method": "Mamba SSM", "benchmark": "LRA, Pile Language Modeling", "pros": "Linear O(L) scan, strong language modeling", "cons": "Kernel synchronization latency on multi-GPU nodes", "citation_key": "gu2023mamba"}
                ],
                "bibtex_entries": ""
            },
            "sections": {
                "Abstract": "Deep neural architectures operating on extensive sequence contexts suffer from quadratic memory bottlenecks and hardware memory traffic saturation. In this paper, we propose the Dynamic Selective Operator (DSO), an IO-aware structured state-space model that bridges continuous dynamical system formulation with fused GPU kernel execution. By adapting discretization step sizes dynamically conditioned on input tokens and leveraging hardware-conscious SRAM tiling, DSO achieves strictly sub-quadratic O(L log L) computation and linear O(L) memory footprint. On comprehensive evaluations including Long Range Arena and multi-benchmark language modeling, DSO achieves up to 2.4x inference speedup and a 42% reduction in peak activation memory compared to FlashAttention-2, while matching or exceeding the downstream accuracy of standard transformer baselines. Our theoretical proofs establish bounded variance and exponential convergence for the discretized transition operator.",
                "1. Introduction": "Large-scale sequence modeling has revolutionized machine intelligence across natural language comprehension, multimodal perception, and computational biology \\cite{vaswani2017attention, brown2020language}. At the foundation of these successes lies the self-attention mechanism, which affords unconstrained pairwise token interaction across sequence dimensions. However, this expressive freedom comes at a prohibitive cost: the standard attention operation scales quadratically, $\\mathcal{O}(L^2)$, with respect to sequence length $L$.\n\nAs modern application domains increasingly demand extended contextual horizons—such as analyzing entire repositories of source code, multi-hour video streams, and long clinical records—the quadratic computational and memory burden becomes an insurmountable bottleneck \\cite{dao2022flashattention}. In response, two primary research paradigms have gained traction: hardware-optimized attention execution and sub-quadratic recurrent or state-space models (SSMs).\n\nDespite promising developments, existing SSM approaches face critical performance compromises. Specifically, linear continuous-time formulations frequently suffer from information degradation in long-range associative recall tasks when compared against dense attention. Furthermore, contemporary GPU architectures are memory-bandwidth constrained rather than compute-bound; algorithmic improvements that do not explicitly account for GPU SRAM versus High Bandwidth Memory (HBM) hierarchies often fail to yield tangible wall-clock speedups in distributed deployment environments.\n\nTo overcome these dual challenges, this paper introduces the **Dynamic Selective Operator (DSO)**. DSO synthesizes continuous state-space dynamics with input-dependent discretization and IO-aware GPU kernel execution. Our primary contributions are summarized as follows:\n\n1. **Theoretical Formulation**: We derive a continuous-time state-space operator equipped with input-dependent parameter discretization and formally prove exponential stability and bounded state variance under arbitrary bounded sequence inputs.\n2. **Hardware-Conscious Kernel Implementation**: We engineer a custom fused parallel scan kernel implemented in Triton, which co-locates intermediate activations inside on-chip SRAM, eliminating redundant HBM round-trips and lowering activation memory by 42%.\n3. **Extensive Empirical Validation**: Across synthetic associative recall benchmarks, the Long Range Arena (LRA) suite, and autoregressive language modeling, DSO outperforms both FlashAttention-2 and baseline state-space architectures, delivering up to 2.4x latency speedups while preserving model capacity.",
                "2. Related Work": "Our work builds upon rich lineages in efficient transformer architectures, structured state-space systems, and hardware-accelerated deep learning algorithms.\n\n### Efficient Attention Approximations\nEfforts to mitigate the quadratic complexity of multi-head self-attention have explored sparse patterns, low-rank factorizations, and linear kernel approximations \\cite{vaswani2017attention, devlin2018bert}. While linear attention variants reduce nominal complexity to $\\mathcal{O}(L)$, they commonly experience catastrophic forgetting in needle-in-a-haystack tasks due to uncompressed state saturation.\n\n### Structured State-Space Models\nDrawing inspiration from linear dynamical systems, structured state-space models map continuous inputs $u(t) \\in \\mathbb{R}$ to outputs $y(t) \\in \\mathbb{R}$ through hidden representations $x(t) \\in \\mathbb{R}^N$. Recent architectures establish strong foundations for linear-time sequence modeling. However, their reliance on static parameters constrains their capacity to dynamically filter out irrelevant tokens from input streams.\n\n### Hardware-Aware Optimization\nModern deep learning accelerators exhibit pronounced disparities between arithmetic throughput (TFLOPs) and memory bandwidth (TB/s). As demonstrated by \\cite{dao2022flashattention}, optimizing algorithm execution for the GPU memory hierarchy yields dramatic wall-clock accelerations. Our proposed framework marries IO-aware memory tiling with dynamic state transitions, preventing memory traffic stalls during both forward and backward passes.",
                "3. Proposed Methodology": "In this section, we present the mathematical foundation and architectural realization of the Dynamic Selective Operator (DSO).\n\n## Problem Formulation\nLet $\\mathbf{X} = [x_1, x_2, \\dots, x_L]^T \\in \\mathbb{R}^{L \\times d}$ represent an input sequence of length $L$ with feature dimensionality $d$. We consider a continuous-time linear time-invariant (LTI) state-space system defined by differential equations:\n\\begin{align}\nh'(t) &= \\mathbf{A} h(t) + \\mathbf{B} x(t) \\\\\ny(t) &= \\mathbf{C} h(t) + \\mathbf{D} x(t)\n\\end{align}\nwhere $h(t) \\in \\mathbb{R}^N$ denotes the hidden state vector, $\\mathbf{A} \\in \\mathbb{R}^{N \\times N}$ is the evolution matrix, and $\\mathbf{B}, \\mathbf{C}$ are projection operators.\n\n## Input-Dependent Discretization\nTo process discrete tokens $x_t$, we discretize the system using a dynamic time step $\\Delta_t$ computed directly from the current token input:\n\\begin{equation}\n\\Delta_t = \\text{softplus}\\left(\\mathbf{W}_\\Delta x_t + b_\\Delta\\right)\n\\end{equation}\nApplying zero-order hold (ZOH) discretization yields the recurrence:\n\\begin{equation}\nh_t = \\mathbf{\\bar{A}}_t h_{t-1} + \\mathbf{\\bar{B}}_t x_t, \\quad y_t = \\mathbf{C}_t h_t + \\mathbf{D} x_t\n\\end{equation}\nwhere:\n\\begin{equation}\n\\mathbf{\\bar{A}}_t = \\exp(\\Delta_t \\mathbf{A}), \\quad \\mathbf{\\bar{B}}_t = (\\Delta_t \\mathbf{A})^{-1} (\\mathbf{\\bar{A}}_t - \\mathbf{I}) \\cdot (\\Delta_t \\mathbf{B})\n\\end{equation}\n\n## Algorithmic Complexity\nThrough our fused associative scan implementation, the entire state sequence $\\{h_1, \\dots, h_L\\}$ is computed in $\\mathcal{O}(L)$ sequential steps during autoregressive generation and in $\\mathcal{O}(L \\log L)$ parallel work during forward training passes, requiring strictly $\\mathcal{O}(L)$ activation memory.",
                "4. Empirical Evaluation": "We conduct extensive experiments across diverse synthetic and real-world modalities to evaluate model capacity, inference latency, and memory scaling.\n\n## Benchmark Datasets and Setup\nAll models are evaluated under uniform hardware conditions using 8x NVIDIA A100 (80GB SXM4) GPUs interconnected via NVLink. Datasets include:\n1. **Long Range Arena (LRA)**: Standard benchmark testing long-context capability across sequence lengths from 1k to 16k tokens.\n2. **Language Modeling on The Pile**: Measuring validation perplexity on open-domain text corpora.\n\n## Primary Performance Comparison\nTable 1 details the comparative performance of DSO against competitive baselines.\n\n\\begin{table}[htbp]\n\\centering\n\\caption{Downstream Performance and Inference Latency on Long-Context Benchmarks. Latency measured at batch size 16, sequence length 8192 on an NVIDIA A100 GPU.}\n\\label{tab:main_results}\n\\begin{tabular}{lcccc}\n\\toprule\n\\textbf{Model Architecture} & \\textbf{LRA Avg Score (\\%)} & \\textbf{Validation PPL} & \\textbf{Latency (ms)} & \\textbf{Peak VRAM (GB)} \\\\\n\\midrule\nStandard Transformer \\cite{vaswani2017attention} & 58.4 & 18.2 & 142.6 & 74.2 \\\\\nFlashAttention-2 \\cite{dao2022flashattention} & 64.1 & 16.9 & 68.4 & 38.1 \\\\\nMamba SSM & 67.8 & 16.5 & 41.2 & 22.4 \\\\\n\\textbf{DSO (Ours)} & \\textbf{71.2} & \\textbf{15.8} & \\textbf{28.5} & \\textbf{16.8} \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nAs observed in Table 1, DSO achieves the highest average score on the Long Range Arena (71.2%) while cutting inference latency to 28.5 ms, representing a 2.4x speedup over FlashAttention-2.",
                "5. Discussion & Limitations": "The experimental outcomes corroborate our core hypothesis: combining continuous-time state-space dynamics with input-dependent discretization and IO-aware kernel fusion enables superior sequence modeling without quadratic penalties.\n\n### Limitations\nWhile DSO shows exceptional performance on sequence lengths up to 32k tokens, extreme contexts ($L > 128k$) require distributed parallel scans across multi-node topologies, which introduces communication overheads currently bound by inter-node InfiniBand latencies.\n\n### Ethical and Broader Impacts\nBy reducing training compute and inference power consumption by more than 50% relative to dense transformer models, DSO contributes towards sustainable, environmentally responsible machine intelligence deployment.",
                "6. Conclusion": "In this work, we introduced the Dynamic Selective Operator (DSO), a hardware-conscious state-space framework for high-throughput sub-quadratic sequence modeling. Theoretical proofs establish convergence and numerical stability, while extensive benchmark evaluations confirm substantial empirical gains in both accuracy and inference efficiency. Future investigations will extend DSO to cross-modal vision-language transformers and embodied robotics control."
            },
            "refinement": {
                "tone_score": 92,
                "academic_vocabulary_density": "8.4%",
                "peer_reviews": [
                    {
                        "reviewer": "Reviewer 1 (Expert in Efficient Architectures)",
                        "rating": "8/10 (Strong Accept)",
                        "feedback": "The theoretical formulation is elegant and mathematically sound. The IO-aware Triton kernel yields tangible speedups over FlashAttention-2. Table 1 results are very convincing.",
                        "action_items": ["Include standard deviation over 3 seeds in Table 1", "Clarify bfloat16 numerical stability"]
                    },
                    {
                        "reviewer": "Reviewer 2 (Expert in State-Space Systems)",
                        "rating": "7/10 (Accept)",
                        "feedback": "A very solid paper. The input-dependent discretization resolves the associative recall limitation of classical SSMs effectively.",
                        "action_items": ["Add citation to S4 and H3 precursors in Related Work", "Discuss multi-node scaling constraints"]
                    }
                ],
                "checklist": {
                    "abstract_word_count_ok": True,
                    "all_citations_in_bibtex": True,
                    "all_equations_numbered": True,
                    "tables_booktabs_formatted": True,
                    "figures_high_dpi": True
                }
            },
            "figures": [
                {
                    "id": "fig_latency_scaling",
                    "title": "Inference Latency vs Sequence Length",
                    "caption": "Inference Latency (ms) comparison across sequence lengths from 512 to 16,384 tokens. DSO exhibits linear scaling, outperforming quadratic attention baselines.",
                    "label": "fig:latency_scaling",
                    "chart_type": "line",
                    "filename": "fig_latency_scaling.png",
                    "latex_snippet": "\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=0.85\\columnwidth]{fig_latency_scaling.png}\n\\caption{Inference Latency (ms) comparison across sequence lengths from 512 to 16,384 tokens. DSO exhibits linear scaling, outperforming quadratic attention baselines.}\n\\label{fig:latency_scaling}\n\\end{figure}"
                },
                {
                    "id": "fig_ablation_accuracy",
                    "title": "Ablation on State Dimension vs Accuracy",
                    "caption": "Downstream accuracy trade-off as state dimension N varies from 8 to 128 across three benchmark tasks.",
                    "label": "fig:ablation_accuracy",
                    "chart_type": "bar",
                    "filename": "fig_ablation_accuracy.png",
                    "latex_snippet": "\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=0.85\\columnwidth]{fig_ablation_accuracy.png}\n\\caption{Downstream accuracy trade-off as state dimension N varies from 8 to 128 across three benchmark tasks.}\n\\label{fig:ablation_accuracy}\n\\end{figure}"
                }
            ],
            "latex": {
                "custom_preamble": "% Custom academic packages\n\\usepackage{microtype}\n\\usepackage{booktabs}\n\\usepackage{nicefrac}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n\\usepackage{graphicx}\n\\usepackage{subcaption}\n\\usepackage{algorithm}\n\\usepackage{algorithmic}\n\\usepackage{hyperref}\n",
                "compiled_tex": "",
                "bibtex_content": ""
            }
        }

    @staticmethod
    def save_project(project_data: Dict[str, Any], filepath: Path) -> bool:
        """Saves project to JSON file."""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            project_data["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            return False

    @staticmethod
    def load_project(filepath: Path) -> Optional[Dict[str, Any]]:
        """Loads project from JSON file."""
        try:
            if not filepath.exists():
                return None
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
