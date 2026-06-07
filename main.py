import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.simulator import simulate_traffic_scenario
from pipeline.opensky import fetch_opensky
from ml.eta_model import train_eta_model, predict_eta
from ml.priority_model import train_priority_model, predict_priority
from optimizer.fcfs import fcfs_sequence, compute_metrics as fcfs_metrics
from optimizer.greedy import greedy_sequence, compute_metrics as greedy_metrics
from optimizer.genetic import genetic_sequence, compute_metrics as genetic_metrics


def run_pipeline(source="simulation", scenario="normal", save_csv=True):
    if source == "opensky":
        df = fetch_opensky()
        if df is None:
            print("⚠️ Fallback vers simulation...")
            df = simulate_traffic_scenario(scenario)
    else:
        df = simulate_traffic_scenario(scenario)

    if save_csv:
        os.makedirs("data/simulated", exist_ok=True)
        path = f"data/simulated/flights_{scenario}.csv"
        df.to_csv(path, index=False)
        print(f"✅ Sauvegardé → {path}")

    print(f"\n📊 {len(df)} vols générés:\n")
    print(df[["flight_id", "callsign", "aircraft_type", "category",
              "wake_class", "altitude_ft", "speed_kt", "eta_min", "priority"]].to_string(index=False))
    return df


def run_ml():
    print("\n🤖 Training ETA Model...")
    train_eta_model()
    print("\n🤖 Training Priority Model...")
    train_priority_model()


def run_inference(scenario="dense"):
    df = simulate_traffic_scenario(scenario)
    df["eta_predicted"]      = predict_eta(df)
    df["priority_predicted"] = predict_priority(df)
    print(f"\n📊 Résultats inference ({scenario}):\n")
    print(df[["flight_id", "callsign", "eta_min", "eta_predicted",
              "priority", "priority_predicted"]].to_string(index=False))
    return df


def run_optimizer(scenario="dense"):
    df = simulate_traffic_scenario(scenario)
    df["eta_predicted"]      = predict_eta(df)
    df["priority_predicted"] = predict_priority(df)

    fcfs    = fcfs_sequence(df)
    greedy  = greedy_sequence(df)
    genetic = genetic_sequence(df)

    m_fcfs    = fcfs_metrics(fcfs)
    m_greedy  = greedy_metrics(greedy)
    m_genetic = genetic_metrics(genetic)

    print(f"\n{'='*60}")
    print(f"📊 COMPARAISON ALGORITHMES — Scénario: {scenario.upper()}")
    print(f"{'='*60}")
    print(f"{'Métrique':<25} {'FCFS':>10} {'GREEDY':>10} {'GENETIC':>10}")
    print(f"{'-'*60}")
    print(f"{'Nb vols':<25} {m_fcfs['n_flights']:>10} {m_greedy['n_flights']:>10} {m_genetic['n_flights']:>10}")
    print(f"{'Total attente (min)':<25} {m_fcfs['total_wait_min']:>10} {m_greedy['total_wait_min']:>10} {m_genetic['total_wait_min']:>10}")
    print(f"{'Moy attente (min)':<25} {m_fcfs['avg_wait_min']:>10} {m_greedy['avg_wait_min']:>10} {m_genetic['avg_wait_min']:>10}")
    print(f"{'Séparation min (min)':<25} {m_fcfs['min_separation']:>10} {m_greedy['min_separation']:>10} {m_genetic['min_separation']:>10}")
    print(f"{'='*60}")

    print(f"\n📋 Séquence GREEDY:")
    print(greedy[["sequence_pos", "flight_id", "callsign", "wake_class",
                  "priority", "eta_min", "scheduled_eta"]].to_string(index=False))
    return fcfs, greedy, genetic


def run_api():
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="pipeline",
        choices=["pipeline", "train", "inference", "optimize", "api"])
    parser.add_argument("--source",   default="simulation",
        choices=["simulation", "opensky"])
    parser.add_argument("--scenario", default="normal",
        choices=["normal", "dense", "emergency"])
    args = parser.parse_args()

    if args.mode == "pipeline":
        run_pipeline(source=args.source, scenario=args.scenario)
    elif args.mode == "train":
        run_ml()
    elif args.mode == "inference":
        run_inference(scenario=args.scenario)
    elif args.mode == "optimize":
        run_optimizer(scenario=args.scenario)
    elif args.mode == "api":
        run_api()