from qiskit import QuantumCircuit, QuantumRegister
from qutilities.qft import QFT, QFTGate
from math import pi

class QFTAdder:
    """
    QFTAdder: Draper-style Quantum Fourier Transform Adder

    This class implements an in-place quantum adder using the QFT algorithm proposed by
    T.G. Draper in "Addition on a Quantum Computer", arXiv:quant-ph/0008033.

    It performs quantum addition or subtraction:
        X ← X ± A
    where the result is stored in-place in register X, and A acts as a constant operand.

    Parameters
    ----------
    target : QuantumRegister
        Register that holds the input and receives the result (i.e., the accumulator).
        Must be at least one qubit longer than `operand` to handle overflow.

    operand : QuantumRegister
        Input register (ancilla) holding the constant value, used for addition or subtraction.

    inverse : bool, default=False
        If True, performs subtraction (target ← target - operand) instead of addition.

    skip_qft : bool, default=False
        If True, assumes the `target` is already in Fourier basis and skips QFT/IQFT steps.

    label : str, optional
        Optional name for the circuit.

    debug : bool, default=False
        If True, displays the circuit with matplotlib when built.

    insert_barrier : bool, default=False
        If True, inserts visual barriers between logical blocks.

    Example
    -------
    >>> X = QuantumRegister(4, 'X')
    >>> A = QuantumRegister(3, 'A')
    >>> adder = QFTAdder(X=X, A=A, inverse=False)
    >>> qc = adder.build()

    References
    ----------
    - T.G. Draper, "Addition on a Quantum Computer", arXiv:quant-ph/0008033
      https://arxiv.org/abs/quant-ph/0008033
    """
    def __init__(self, 
                 target: QuantumRegister,
                 operand: QuantumRegister,
                 inverse=False, 
                 skip_qft=False,                 
                 label: str | None = None,
                 debug: bool = False,
                 insert_barrier: bool = False):

        if target is None or operand is None:
            raise ValueError("Both target and operand registers must be provided.")
            
        
        if target.size <= operand.size:
            raise ValueError("[!] Target register must be at least one qubit longer than operand register, to hold overflow.")
        
        self.X_reg = target
        self.A_reg = operand
        self.subtract = inverse
        self.skip_qft = skip_qft
        self.label = label or ('|X-A⟩' if self.subtract else '|X+A⟩')
        self.debug = debug
        self.insert_barrier = insert_barrier

    def _create_circuit(self):
        """
        Create the underlying QuantumCircuit object, using provided external registers.
        """
        self.adder_circuit = QuantumCircuit(self.X_reg, self.A_reg, name=self.label)

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
        Create and return a QFT gate on the X register.

        Returns
        -------
        Gate
            QFT gate object to be applied on register X.
        """
        return QFTGate(num_qubits=self.X_reg.size).build()

    def _create_iqft_gate(self):
        """
        Create and return an inverse QFT gate on the X register.

        Returns
        -------
        Gate
            Inverse QFT gate object to be applied on register X.
        """
        return QFTGate(num_qubits=self.X_reg.size, inverse=True).build()

    def _apply_qft(self):
        """
        Apply the QFT to the X register unless skipping is enabled.
        """
        if self.skip_qft:
            return
        qft_gate = self._create_qft_gate()
        self.adder_circuit.append(qft_gate, self.X_reg)
        self._insert_barrier()

    def _apply_iqft(self):
        """
        Apply the inverse QFT to the X register unless skipping is enabled.
        """
        if self.skip_qft:
            return
        iqft_gate = self._create_iqft_gate()
        self.adder_circuit.append(iqft_gate, self.X_reg)

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
        Apply a single controlled phase rotation from A[control_idx] to X[target_idx].

        Parameters
        ----------
        control_idx : int
            Index of the control qubit in register A.
        target_idx : int
            Index of the target qubit in register X.
        """
        distance = target_idx - control_idx
        angle = self._encode_angle(distance)
        self.adder_circuit.cp(angle, self.A_reg[control_idx], self.X_reg[target_idx])

    def _apply_phase_kickbacks(self):
        """
        Apply all necessary Draper-style CP gates from register A to X.
        For each A[i], apply CP to X[i..n], followed by a barrier (if enabled).
        """
        for control_qubit in range(self.A_reg.size):
            for target_qubit in range(control_qubit, self.X_reg.size):
                self._apply_phase_kick(control_qubit, target_qubit)
            self._insert_barrier()

    def build(self):
        """
        Construct and return the full Draper QFT adder circuit.

        Returns
        -------
        QuantumCircuit
            A complete quantum circuit implementing X ± A → X.
        """
        self._create_circuit()
        self._apply_qft()
        self._apply_phase_kickbacks()
        self._apply_iqft()
        self._debug_display()
        return self.adder_circuit
