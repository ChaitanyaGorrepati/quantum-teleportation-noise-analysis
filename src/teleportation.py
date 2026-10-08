from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from noise_models import create_noise_instruction


# -------------------------------------------------
# Input states
# -------------------------------------------------

INPUT_STATES = {
    "|0>": Statevector.from_label("0"),
    "|1>": Statevector.from_label("1"),
    "|+>": Statevector.from_label("+"),
    "|->": Statevector.from_label("-"),

    # Y-basis states
    "|+i>": Statevector([1, 1j]) / (2 ** 0.5),
    "|-i>": Statevector([1, -1j]) / (2 ** 0.5)
}


def prepare_input_state(qc, state_name):
    """
    Prepare Alice's input state on qubit 0.

    |0>  = |0>
    |1>  = X|0>
    |+>  = H|0>
    |->  = X followed by H
    |+i> = H followed by S
    |-i> = H followed by Sdg
    """

    if state_name == "|0>":
        pass

    elif state_name == "|1>":
        qc.x(0)

    elif state_name == "|+>":
        qc.h(0)

    elif state_name == "|->":
        qc.x(0)
        qc.h(0)

    elif state_name == "|+i>":
        qc.h(0)
        qc.s(0)

    elif state_name == "|-i>":
        qc.h(0)
        qc.sdg(0)

    else:
        raise ValueError(
            f"Unknown input state: {state_name}"
        )


def create_teleportation_circuit(
    state_name,
    noise_type="none",
    noise_probability=0.0
):
    """
    Create a quantum teleportation circuit.

    Qubit 0: Alice's input state
    Qubit 1: Alice's Bell-pair qubit
    Qubit 2: Bob's Bell-pair qubit
    """

    qc = QuantumCircuit(3, 2)

    # -------------------------------------------------
    # Step 1: Prepare Alice's input state
    # -------------------------------------------------

    prepare_input_state(
        qc,
        state_name
    )

    # -------------------------------------------------
    # Step 2: Create Bell pair
    # -------------------------------------------------

    qc.h(1)
    qc.cx(1, 2)

    # -------------------------------------------------
    # Step 3: Apply channel noise to Bob's qubit
    # -------------------------------------------------

    noise_instruction = create_noise_instruction(
        noise_type,
        noise_probability
    )

    if noise_instruction is not None:

        qc.append(
            noise_instruction,
            [2]
        )

    # -------------------------------------------------
    # Step 4: Alice's Bell-state measurement
    # -------------------------------------------------

    qc.cx(0, 1)
    qc.h(0)

    # -------------------------------------------------
    # Step 5: Measure Alice's qubits
    # -------------------------------------------------

    qc.measure(0, 0)
    qc.measure(1, 1)

    # -------------------------------------------------
    # Step 6: Bob's conditional corrections
    # -------------------------------------------------

    # X correction
    with qc.if_test((qc.clbits[1], True)):
        qc.x(2)

    # Z correction
    with qc.if_test((qc.clbits[0], True)):
        qc.z(2)

    # -------------------------------------------------
    # Step 7: Save Bob's final density matrix
    # -------------------------------------------------

    qc.save_density_matrix(
        [2],
        label="bob_state"
    )

    return qc


if __name__ == "__main__":

    circuit = create_teleportation_circuit(
        state_name="|+i>"
    )

    print(circuit)