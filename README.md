# QUtilities ⚛️🧩

**QUtilities** is a growing collection of quantum tools — built for experimenting, prototyping, and understanding.

This project started as a way to better understand quantum programming through code — and evolved into a library of practical building blocks. It’s where I collect the functions, gates, and tricks I find useful while navigating the noisy madness of quantum computing.

It’s built on [Qiskit](https://qiskit.org/), but shaped by curiosity.

---

## 🚀 Features

- ✅ **Quantum Fourier Transform (QFT)**
  - Forward & inverse modes
  - Approximate gate skipping
  - Bit-reversal swapping
  - Reusable as gate

- ✅ **Quantum Phase Estimation (QPE)**
  - Angle-based or unitary-based input
  - Configurable register size
  - Reusable gate export
  - Debug circuit visualization

- ✅ **QFT-Based Arithmetic**
  - `QFTAdder`: Draper-style QFT adder/subtractor
    - `target ± operand` logic (in-place)
    - Optional Fourier basis skipping
    - Fully unitary and reversible
  - `QFTMultiplier`: Repeated controlled additions for `target ± multiplicand × multiplier`
    - Fourier-domain accumulation logic
    - Fully quantum-coherent (supports superposition)
    - Supports subtraction (`inverse=True`)

- 📦 Built as installable package
- 🧪 Ready for integration and testing
- 🧠 More tools coming soon...

---

## 📦 Installation

```bash
git clone https://github.com/MarcusSkynet/qutilities.git
cd qutilities
pip install -e .
```

---

## 🔍 Usage Example

```python
from qutilities.qft import QFT
from qutilities.qpe import QPE, QPEGate
from qutilities.arithmetic.adders.qft_adder import QFTAdder
from qutilities.arithmetic.multipliers.qft_multiplier import QFTMultiplier
from qiskit import QuantumRegister

# QFT circuit
qft = QFT(num_qubits=4, do_swaps=True, debug=True)
circuit = qft.build()

# QPE using a simple angle
qpe = QPE(control_qubits=3, theta=0.125, debug=True)
qpe_circuit = qpe.build()

# QFTAdder
X = QuantumRegister(4, 'X')
A = QuantumRegister(3, 'A')
adder = QFTAdder(target=X, operand=A)
adder_circuit = adder.build()

# QFTMultiplier
M = QuantumRegister(3, 'M')
N = QuantumRegister(2, 'N')
Y = QuantumRegister(5, 'Y')
multiplier = QFTMultiplier(multiplicand=M, multiplier=N, target=Y)
mult_circuit = multiplier.build()
```

---

## 📁 Modules

```
qutilities/
├── qft/
│   ├── qft.py            # QFT + QFTGate
├── qpe/
│   ├── qpe.py            # QPE + QPEGate
├── arithmetic/
│   ├── adders/
│   │   └── qft_adder.py  # QFTAdder
│   ├── multipliers/
│   │   └── qft_multiplier.py  # QFTMultiplier
└── __init__.py
```

---

## 📜 License

Licensed under the Apache License 2.0.  
See [LICENSE](./LICENSE) for details.

---

## 🌊 Project

This library is part of the  
[**On Tides of Uncertainty**](https://github.com/MarcusSkynet/tides-of-uncertainty)  
— a personal journey into quantum computing, logic, and intuition.
