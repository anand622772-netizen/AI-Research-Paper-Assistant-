"""
Initializes sample project data and pre-renders baseline publication figures.
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.project_state import ProjectState
from modules.plotting.studio import execute_plot_code, CHART_TEMPLATES
from config import OUTPUTS_DIR, SAMPLES_DIR

def initialize():
    # 1. Create sample project JSON
    sample_proj = ProjectState.create_empty_project(
        name="Scalable Selective State-Space Neural Operators",
        template="NeurIPS / ICLR"
    )
    
    sample_path = SAMPLES_DIR / "sample_project.json"
    ProjectState.save_project(sample_proj, sample_path)
    print(f"Sample project saved to {sample_path}")

    # 2. Pre-generate sample figures
    plots_dir = OUTPUTS_DIR / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    code_scaling = CHART_TEMPLATES["Latency vs Context Length (Scaling Curve)"]
    success1, path1, err1 = execute_plot_code(code_scaling, plots_dir, "fig_latency_scaling")
    print(f"Figure 1 generated: {success1}, Path: {path1}, Error: {err1}")

    code_ablation = CHART_TEMPLATES["Benchmark Performance Comparison (Bar Chart)"]
    success2, path2, err2 = execute_plot_code(code_ablation, plots_dir, "fig_ablation_accuracy")
    print(f"Figure 2 generated: {success2}, Path: {path2}, Error: {err2}")

if __name__ == "__main__":
    initialize()
