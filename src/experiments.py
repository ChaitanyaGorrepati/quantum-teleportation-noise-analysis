import os
import csv

from qiskit_aer import AerSimulator
from qiskit.quantum_info import state_fidelity

from teleportation import (
    create_teleportation_circuit,
    INPUT_STATES
)


# -------------------------------------------------
# Experiment configuration
# -------------------------------------------------

NOISE_TYPES = [
    "bit_flip",
    "phase_flip",
    "depolarizing"
]


NOISE_LEVELS = [
    0.00,
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50
]


# -------------------------------------------------
# Run one simulation
# -------------------------------------------------

def calculate_fidelity(
    state_name,
    noise_type,
    probability
):
    """
    Simulate teleportation and calculate
    the fidelity between Alice's original
    state and Bob's final state.
    """

    circuit = create_teleportation_circuit(
        state_name=state_name,
        noise_type=noise_type,
        noise_probability=probability
    )

    simulator = AerSimulator(
        method="density_matrix"
    )

    result = simulator.run(
        circuit
    ).result()

    bob_state = result.data(0)["bob_state"]

    target_state = INPUT_STATES[state_name]

    fidelity = state_fidelity(
        target_state,
        bob_state
    )

    return float(fidelity)


# -------------------------------------------------
# Run all experiments
# -------------------------------------------------

def run_all_experiments():

    os.makedirs(
        "results/data",
        exist_ok=True
    )

    output_file = (
        "results/data/"
        "teleportation_fidelity_results.csv"
    )

    rows = []

    print("\n")
    print("=" * 60)
    print("QUANTUM TELEPORTATION FIDELITY EXPERIMENT")
    print("=" * 60)

    for state_name, input_state in INPUT_STATES.items():

        print(f"\nInput state: {state_name}")
        print("-" * 40)

        # -------------------------------------------------
        # Ideal baseline
        # -------------------------------------------------

        fidelity = calculate_fidelity(
           state_name,
            "none",
            0.0
        )

        rows.append({
            "input_state": state_name,
            "noise_type": "none",
            "noise_probability": 0.0,
            "fidelity": fidelity
        })

        print(
            f"No noise -> Fidelity = "
            f"{fidelity:.6f}"
        )

        # -------------------------------------------------
        # Noisy experiments
        # -------------------------------------------------

        for noise_type in NOISE_TYPES:

            print(
                f"\nNoise model: {noise_type}"
            )

            for probability in NOISE_LEVELS:

                fidelity = calculate_fidelity(
                    state_name,
                    noise_type,
                    probability
                )

                rows.append({
                    "input_state": state_name,
                    "noise_type": noise_type,
                    "noise_probability": probability,
                    "fidelity": fidelity
                })

                print(
                    f"p = {probability:.2f}"
                    f" -> Fidelity = "
                    f"{fidelity:.6f}"
                )

    # -------------------------------------------------
    # Save CSV
    # -------------------------------------------------

    with open(
        output_file,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "input_state",
                "noise_type",
                "noise_probability",
                "fidelity"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print("\n")
    print("=" * 60)
    print("EXPERIMENTS COMPLETED")
    print("=" * 60)

    print(
        f"\nResults saved to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":
    run_all_experiments()