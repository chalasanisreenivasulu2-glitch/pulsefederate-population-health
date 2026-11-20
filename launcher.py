"""PulseFederate single-binary entry point."""
import argparse, sys, glob, os
from pathlib import Path


def cmd_simulate(args):
    from backend.app.domain.models import TrainingConfig
    from backend.app.ml.datasets import load_csv
    from backend.app.services.simulation import FederatedSimulator
    data_dir = Path(args.data_dir)
    paths = sorted(glob.glob(str(data_dir / "*.csv")))
    if len(paths) < 2:
        sys.exit(f"Need >=2 CSVs in {data_dir}")
    sites = {}
    for p in paths:
        sid = os.path.splitext(os.path.basename(p))[0]
        (Xtr, ytr), (Xva, yva), _ = load_csv(p)
        sites[sid] = {"X_train": Xtr, "y_train": ytr, "X_val": Xva, "y_val": yva}
    sim = FederatedSimulator(sites, TrainingConfig(rounds=args.rounds))
    result = sim.run()
    for r in result.rounds:
        print(f"round {r.round}: acc={r.aggregated_accuracy:.3f} loss={r.aggregated_loss:.3f} fairness={r.fairness_score:.3f}")
    print(f"\
final accuracy: {result.final_accuracy:.3f}")


def main():
    p = argparse.ArgumentParser(prog="pulsefederate")
    sub = p.add_subparsers(dest="role", required=True)
    m = sub.add_parser("simulate")
    m.add_argument("--data-dir", default="data/partitions")
    m.add_argument("--rounds", type=int, default=5)
    m.set_defaults(func=cmd_simulate)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()