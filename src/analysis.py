import os
import csv

import matplotlib.pyplot as plt


# -------------------------------------------------
# Load results
# -------------------------------------------------

def load_results(filename):

    results = []

    with open(
        filename,
        "r"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            results.append({
                "input_state": row["input_state"],
                "noise_type": row["noise_type"],
                "noise_probability": float(
                    row["noise_probability"]
                ),
                "fidelity": float(
                    row["fidelity"]
                )
            })

    return results


# -------------------------------------------------
# Plot one graph per input state
# -------------------------------------------------

def plot_state_results(
    results,
    state_name
):

    noise_types = [
        "bit_flip",
        "phase_flip",
        "depolarizing"
    ]

    plt.figure(
        figsize=(10, 6)
    )

    for noise_type in noise_types:

        data = [
            row
            for row in results
            if (
                row["input_state"] == state_name
                and
                row["noise_type"] == noise_type
            )
        ]

        probabilities = [
            row["noise_probability"]
            for row in data
        ]

        fidelities = [
            row["fidelity"]
            for row in data
        ]

        plt.plot(
            probabilities,
            fidelities,
            marker="o",
            label=noise_type.replace(
                "_",
                " "
            ).title()
        )

    plt.xlabel(
        "Noise Probability"
    )

    plt.ylabel(
        "Teleportation Fidelity"
    )

    plt.title(
        f"Quantum Teleportation Fidelity "
        f"under Noise — Input State {state_name}"
    )

    plt.ylim(
        0,
        1.05
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    filename = (
        state_name
        .replace("|", "")
        .replace(">", "")
        .replace("+", "plus")
        .replace("-", "minus")
    )

    output_file = (
        "results/plots/"
        f"fidelity_{filename}.png"
    )

    plt.savefig(
        output_file,
        dpi=300
    )

    plt.show()

    print(
        f"Plot saved: {output_file}"
    )


# -------------------------------------------------
# Plot average fidelity
# -------------------------------------------------

def plot_average_fidelity(results):

    noise_types = [
        "bit_flip",
        "phase_flip",
        "depolarizing"
    ]

    plt.figure(
        figsize=(10, 6)
    )

    for noise_type in noise_types:

        probabilities = []

        average_fidelities = []

        for probability in sorted(
            set(
                row["noise_probability"]
                for row in results
                if row["noise_type"] == noise_type
            )
        ):

            values = [
                row["fidelity"]
                for row in results
                if (
                    row["noise_type"] == noise_type
                    and
                    row["noise_probability"] == probability
                )
            ]

            probabilities.append(
                probability
            )

            average_fidelities.append(
                sum(values) / len(values)
            )

        plt.plot(
            probabilities,
            average_fidelities,
            marker="o",
            label=noise_type.replace(
                "_",
                " "
            ).title()
        )

    plt.xlabel(
        "Noise Probability"
    )

    plt.ylabel(
        "Average Teleportation Fidelity"
    )

    plt.title(
        "Average Quantum Teleportation Fidelity "
        "under Different Noise Models"
    )

    plt.ylim(
        0,
        1.05
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    output_file = (
        "results/plots/"
        "average_fidelity.png"
    )

    plt.savefig(
        output_file,
        dpi=300
    )

    plt.show()

    print(
        f"Plot saved: {output_file}"
    )


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":

    results_file = (
        "results/data/"
        "teleportation_fidelity_results.csv"
    )

    results = load_results(
        results_file
    )

    states = sorted(
        set(
            row["input_state"]
            for row in results
        )
    )

    os.makedirs(
        "results/plots",
        exist_ok=True
    )

    for state in states:

        if state != "none":

            plot_state_results(
                results,
                state
            )

    plot_average_fidelity(
        results
    )