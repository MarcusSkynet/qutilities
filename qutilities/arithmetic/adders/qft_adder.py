from qiskit import QuantumCircuit, QuantumRegister
from qutilities.qft import QFT, QFTGate
from math import pi

class QFTAdder:
    """
    QFTAdder: Draper-style Quantum Fourier Transform Adder

    This class implements an in-place quantum adder using the QFT algorithm proposed by
    T.G. Draper in "Addition on a Quantum Computer", arXiv:quant-ph/0008033.

    It performs addition (or subtraction) of two quantum registers:
        A ← A ± B
    where the result is stored in-place in register A.

    Key Features
    ------------
    - Pure QFT-based addition/subtraction
    - Internal or external QuantumRegister support
    - Optional QFT skipping (for composite arithmetic)
    - Optional barriers for circuit segmentation
    - Debug mode with auto-visualization

    Example Usage
    -------------
    >>> adder = QFTAdder(num_qubits=3, subtract=True, debug=True)
    >>> qc = adder.build()
    >>> qc.draw('mpl')

    Or with custom registers:
    >>> A = QuantumRegister(4, 'A')
    >>> B = QuantumRegister(3, 'B')
    >>> adder = QFTAdder(A=A, B=B)
    >>> circuit = adder.build()

    Parameters
    ----------
    num_qubits : int, default=0
        Number of qubits in register B. Register A will be created with num_qubits + 1.
        Ignored if external registers A and B are provided.
    subtract : bool, default=False
        If True, performs subtraction (A - B). Otherwise, performs addition (A + B).
    skip_qft : bool, default=False
        If True, assumes register A is already in the QFT basis and skips QFT/iQFT steps.
    A : QuantumRegister, optional
        External quantum register to use as A. Must be one qubit longer than B.
    B : QuantumRegister, optional
        External quantum register to use as B.
    label : str, optional
        Name for the circuit. Defaults to "|A+B⟩" or "|A-B⟩" depending on mode.
    debug : bool, default=False
        If True, renders the circuit after building.
    insert_barrier : bool, default=False
        If True, inserts barriers between logical blocks for visual clarity.

    Returns
    -------
    QuantumCircuit
        A quantum circuit performing QFT-based A ± B → A.

    References
    ----------
    - T.G. Draper, "Addition on a Quantum Computer", arXiv:quant-ph/0008033
      https://arxiv.org/abs/quant-ph/0008033
    """
    def __init__(self, num_qubits: int = 0, subtract=False, skip_qft=False,
                 A: QuantumRegister | None = None,
                 B: QuantumRegister | None = None,
                 label: str | None = None,
                 debug: bool = False,
                 insert_barrier: bool = False):

        if A is not None and B is not None:
            if A.size != B.size + 1:
                raise ValueError("[!] Register A must be one qubit longer than register B, to hold overflow.")
            self.A_reg = A
            self.B_reg = B
            self.num_qubits = B.size
            self.owns_registers = False
        elif A is not None or B is not None:
            raise ValueError("[!] Both registers A and B must be provided.")
        else:
            self.num_qubits = num_qubits
            self.A_reg = QuantumRegister(self.num_qubits + 1, 'A')
            self.B_reg = QuantumRegister(self.num_qubits, 'B')
            self.owns_registers = True

        self.subtract = subtract
        self.skip_qft = skip_qft
        self.label = label or ('|A-B⟩' if subtract else '|A+B⟩')
        self.debug = debug
        self.insert_barrier = insert_barrier

    def _create_circuit(self):
        """
        Create the underlying QuantumCircuit object, using internal or external registers.
        """
        if self.owns_registers:
            self.adder_circuit = QuantumCircuit(self.A_reg, self.B_reg, name=self.label)
        else:
            registers = []
            for register in [self.A_reg, self.B_reg]:
                if register not in registers:
                    registers.append(register)
            self.adder_circuit = QuantumCircuit(*registers, name=self.label)

    def _debug_display(self):
        """
        Display the current state of the circuit using matplotlib if debug mode is enabled.
        """
        if self.debug:
            from IPython.display import display
            display(self.adder_circuit.draw('mpl'))

    def _insert_barrier(self):
        """
        Insert a barrier across all registers if enabled.
        """
        if self.insert_barrier:
            self.adder_circuit.barrier()

    def _create_qft_gate(self):
        """
        Create and return a QFT gate on the A register.

        Returns
        -------
        Gate
            QFT gate object to be applied on register A.
        """
        return QFTGate(num_qubits=self.A_reg.size).build()

    def _create_iqft_gate(self):
        """
        Create and return an inverse QFT gate on the A register.

        Returns
        -------
        Gate
            Inverse QFT gate object to be applied on register A.
        """
        return QFTGate(num_qubits=self.A_reg.size, inverse=True).build()

    def _apply_qft(self):
        """
        Apply the QFT to the A register unless skipping is enabled.
        """
        if self.skip_qft:
            return
        qft_gate = self._create_qft_gate()
        self.adder_circuit.append(qft_gate, self.A_reg)
        self._insert_barrier()

    def _apply_iqft(self):
        """
        Apply the inverse QFT to the A register unless skipping is enabled.
        """
        if self.skip_qft:
            return
        iqft_gate = self._create_iqft_gate()
        self.adder_circuit.append(iqft_gate, self.A_reg)

    def _encode_angle(self, distance: int) -> float:
        """
        Compute the Draper phase angle based on the qubit distance.
        The angle is negated if subtraction mode is enabled.

        Parameters
        ----------
        distance : int
            Distance between target and control qubit indices.

        Returns
        -------
        float
            The encoded phase angle in radians.
        """
        angle = pi / (2 ** distance)
        return -angle if self.subtract else angle

    def _apply_phase_kick(self, control_idx: int, target_idx: int):
        """
        Apply a single controlled phase rotation from B[control_idx] to A[target_idx].

        Parameters
        ----------
        control_idx : int
            Index of the control qubit in register B.
        target_idx : int
            Index of the target qubit in register A.
        """
        distance = target_idx - control_idx
        angle = self._encode_angle(distance)
        self.adder_circuit.cp(angle, self.B_reg[control_idx], self.A_reg[target_idx])

    def _apply_phase_kickbacks(self):
        """
        Apply all necessary Draper-style CP gates from register B to A.
        For each B[i], apply CP to A[i..n], followed by a barrier (if enabled).
        """
        for control_qubit in range(self.B_reg.size):
            for target_qubit in range(control_qubit, self.A_reg.size):
                self._apply_phase_kick(control_qubit, target_qubit)
            self._insert_barrier()
        self._debug_display()

    def build(self):
        """
        Construct and return the full Draper QFT adder circuit.

        Returns
        -------
        QuantumCircuit
            A complete quantum circuit implementing A ± B → A.
        """
        self._create_circuit()
        self._apply_qft()
        self._apply_phase_kickbacks()
        self._apply_iqft()
        self._debug_display()
        return self.adder_circuit
