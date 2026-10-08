from qiskit_aer.noise import pauli_error, depolarizing_error


def create_noise_instruction(noise_type, probability):
    """
    Create a quantum noise instruction.

    The noise is applied explicitly to Bob's entangled
    qubit during the teleportation channel.

    Parameters
    ----------
    noise_type : str
        "bit_flip", "phase_flip", "depolarizing", or "none"

    probability : float
        Noise probability between 0 and 1.
    """

    if noise_type == "none":
        return None

    if not 0 <= probability <= 1:
        raise ValueError(
            "Noise probability must be between 0 and 1."
        )

    # -------------------------------------------------
    # Bit flip
    # -------------------------------------------------

    if noise_type == "bit_flip":

        error = pauli_error([
            ("X", probability),
            ("I", 1 - probability)
        ])

        return error.to_instruction()

    # -------------------------------------------------
    # Phase flip
    # -------------------------------------------------

    if noise_type == "phase_flip":

        error = pauli_error([
            ("Z", probability),
            ("I", 1 - probability)
        ])

        return error.to_instruction()

    # -------------------------------------------------
    # Depolarizing
    # -------------------------------------------------

    if noise_type == "depolarizing":

        error = depolarizing_error(
            probability,
            1
        )

        return error.to_instruction()

    raise ValueError(
        f"Unknown noise type: {noise_type}"
    )