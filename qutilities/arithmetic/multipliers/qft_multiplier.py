from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qutilities.qft import QFTGate
from qutilities.arithmetic.adders.qft_adder import QFTAdder

class QFTMultiplier:
    """
    Quantum Fourier Transform (QFT)-based multiplier.

    Performs the transformation:
        |Y⟩|M⟩|N⟩ → |Y ± M × N⟩|M⟩|N⟩
    where:
        - Y is the accumulator (result)
        - M is the multiplicand
        - N is the multiplier

    This operation is performed in the Fourier basis using controlled QFT adders.

    Notes
    -----
    This class accumulates phase rotations in the QFT domain and is fully quantum-coherent,
    supporting inputs in superposition. The logic scales linearly with the control register size,
    using repeated controlled additions for each binary-weighted contribution of N[i].
    When `inverse=True`, the operation becomes subtraction: Y ← Y − M × N.
    """
    def __init__(
        self,
        multiplicand: QuantumRegister, # Value to be multiplied (M)
        multiplier: QuantumRegister,   # Value controlling repetitions (N)
        target: QuantumRegister | None = None, # Accumulator (Y) : optional
        inverse: bool = False,
        skip_qft: bool = False,
        insert_barrier: bool = False,
        debug: bool = False,
        label: str | None = None,
    ):
        """
        Initialize a QFT-based multiplier instance.
    
        Parameters
        ----------
        multiplicand : QuantumRegister
            The register representing the multiplicand M (value to be added/subtracted repeatedly).
    
        multiplier : QuantumRegister
            The register representing the multiplier N (number of additions to apply).
    
        target : QuantumRegister, optional
            The result register Y. If not provided, a new one will be created of size len(M) + len(N).
    
        inverse : bool, optional
            If True, subtracts M instead of adding (Y ← Y − M × N). Default is False.
    
        skip_qft : bool, optional
            If True, assumes the target register is already in the Fourier basis. Default is False.
    
        debug : bool, optional
            If True, enables matplotlib drawing on build. Default is False.
    
        insert_barrier : bool, optional
            If True, inserts circuit barriers between QFT stages and controlled additions.
    
        label : str, optional
            Optional label used to name the resulting circuit.
        """
        """
        Initialize a QFT-based multiplier instance.
        
        Parameters
        ----------
        multiplicand : QuantumRegister
            The register representing the multiplicand M (value to be added/subtracted repeatedly).
        
        multiplier : QuantumRegister
            The register representing the multiplier N (controls the number of applications).
        
        target : QuantumRegister, optional
            The result register Y. If not provided, one is created of size len(M) + len(N).
        
        inverse : bool, optional
            If True, subtracts M instead of adding (Y ← Y − M × N). Default is False.
        
        skip_qft : bool, optional
            If True, assumes the target register is already in the Fourier basis.
        
        debug : bool, optional
            If True, displays the circuit diagram on build.
        
        insert_barrier : bool, optional
            If True, inserts circuit barriers between logical steps.
        
        label : str, optional
            Optional label for the circuit.
        """
        # Store user facing registers
        self.M_reg = multiplicand
        self.N_reg = multiplier

        # Determine required size for target register if not provided
        required_size = self.M_reg.size + self.N_reg.size
        if target is None:
            self.Y_reg = QuantumRegister(required_size, 'Y')
        else:
            if len(target) < required_size:
                raise ValueError(f'[!] Provided target register must be at least {required_size} qubits.')
            self.Y_reg = target

        # Flags
        self.inverse = inverse
        self.skip_qft = skip_qft
        self.debug = debug
        self.insert_barrier = insert_barrier
        self.label = label or ("|M×N⟩" if not inverse else "|M÷N⟩")

    def _create_circuit(self):
        """
        Initialize the internal QuantumCircuit using provided registers.
    
        Registers used:
        - Y (target): accumulator
        - M (multiplicand): value to be added
        - N (multiplier): controls repeated addition
        """
        self.multiplier_circuit = QuantumCircuit(self.Y_reg, self.M_reg, self.N_reg, name=self.label)

    def _debug_display(self):
        """
        If debug is True, show the final circuit using matplotlib.
        """
        if self.debug:
            from IPython.display import display
            display(self.multiplier_circuit.draw('mpl'))

    def _insert_barrier(self):
        """
        Insert a barrier if the `insert_barrier` flag is True.
        """
        if self.insert_barrier:
            self.multiplier_circuit.barrier()

    def _create_qft_gate(self):
        """
        Create the QFT gate for the target register Y.
        """
        return QFTGate(num_qubits=self.Y_reg.size).build()

    def _create_iqft_gate(self):
        """
        Create the inverse QFT gate for the target register Y.
        """
        return QFTGate(num_qubits=self.Y_reg.size, inverse=True).build()

    def _apply_qft(self):
        """
        Apply the QFT to the target register Y, unless skip_qft=True.
        """
        if self.skip_qft:
            return
        qft_gate = self._create_qft_gate()
        self.multiplier_circuit.append(qft_gate, self.Y_reg)
        self._insert_barrier()

    def _apply_iqft(self):
        """
        Apply the inverse QFT to the target register Y, unless skip_qft=True.
        """
        if self.skip_qft:
            return
        iqft_gate = self._create_iqft_gate()
        self.multiplier_circuit.append(iqft_gate, self.Y_reg)

    def _create_C_ADD(self):
        """
        Create a controlled QFT adder or subtractor:
            |Y⟩|M⟩ → |Y ± M⟩  (in Fourier basis), controlled on one qubit.

        The operation performed depends on `self.inverse`.

        Returns
        -------
        ControlledGate
            The controlled gate to apply conditionally on N[i].
        """
        adder_gate = QFTAdder(target=self.Y_reg, operand=self.M_reg, inverse=self.inverse, skip_qft=True).build().to_gate()
        return adder_gate.control()

    def _apply_C_ADD(self):
        """
        Apply controlled QFT additions to the accumulator Y based on the multiplier N.
    
        For each bit i of N:
            - If N[i] is |1⟩, apply the adder 2^i times to simulate binary-weighted addition.
            - This is done via repeated controlled application of the same gate.
    
        This phase-accumulation model is fully quantum-compatible and operates in the Fourier domain.
        """
        c_add_gate = self._create_C_ADD()
        
        for i in range(self.N_reg.size):
            for j in range(2**i):
                self.multiplier_circuit.append(c_add_gate, [self.N_reg[i]] + list(self.Y_reg) + list(self.M_reg))
            self._insert_barrier()

    def build(self):
        """
        Construct the full QFT-based multiplier circuit.
    
        Applies:
            1. QFT on target register Y
            2. Repeated controlled additions of M, controlled by bits of N
            3. Inverse QFT to return to the computational basis
    
        Returns
        -------
        QuantumCircuit
            The completed multiplier circuit implementing Y += M × N.
        """
        self._create_circuit()
        self._apply_qft()
        self._apply_C_ADD()
        self._apply_iqft()
        self._debug_display()

        return self.multiplier_circuit