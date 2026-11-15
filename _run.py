"""
CAMAS clean runner — sets up logging before any other import.
Usage: python run.py [--max-queries N] [--mode baseline|camas|both] [--ablation] [--scalability]
"""
import sys
import logging

# Must happen before any other import
for h in logging.root.handlers[:]:
    logging.root.removeHandler(h)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("camas.log", mode="w"),
    ],
)

import argparse
import yaml
from pathlib import Path

logger = logging.getLogger("camas.run")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",      default="config/config.yaml")
    parser.add_argument("--max-queries", type=int, default=None)
    parser.add_argument("--mode",        choices=["baseline", "camas", "both"], default="both")
    parser.add_argument("--ablation",    action="store_true")
    parser.add_argument("--scalability", action="store_true")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    Path(config["experiment"]["results_dir"]).mkdir(parents=True, exist_ok=True)
    Path(config["experiment"]["visualization_dir"]).mkdir(parents=True, exist_ok=True)
    Path(config["experiment"]["database_path"]).parent.mkdir(parents=True, exist_ok=True)

    from experiments.runner import load_prompts, run_experiment
    from run_experiment import _generate_reports, _run_ablation, _run_scalability

    prompts = load_prompts(config["experiment"]["prompts_file"])

    modes = []
    if args.mode in ("both", "baseline"):
        modes.append("baseline")
    if args.mode in ("both", "camas"):
        modes.append("camas")

    run_ids = {}
    for mode in modes:
        logger.info("=" * 60)
        logger.info(f"Starting {mode.upper()} experiment")
        logger.info("=" * 60)
        run_ids[mode] = run_experiment(
            mode=mode, config=config, prompts=prompts,
            max_queries=args.max_queries,
        )
        logger.info(f"Completed {mode.upper()} → run_id={run_ids[mode]}")

    if modes:
        logger.info("Generating reports and visualizations...")
        _generate_reports(config, run_ids)

    if args.ablation:
        logger.info("Running ablation study...")
        _run_ablation(config, prompts, args.max_queries)

    if args.scalability:
        logger.info("Running scalability sweep...")
        _run_scalability(config, prompts)

    logger.info("=" * 60)
    logger.info("DONE")
    logger.info(f"  Reports:        {config['experiment']['results_dir']}/")
    logger.info(f"  Visualizations: {config['experiment']['visualization_dir']}/")
    logger.info(f"  Database:       {config['experiment']['database_path']}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
