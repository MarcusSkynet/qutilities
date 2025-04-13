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

- 📦 Built as installable package
- 🧪 Ready for integration and testing
- 🧰 More tools coming soon...

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

# QFT circuit
qft = QFT(num_qubits=4, do_swaps=True, debug=True)
circuit = qft.build()

# QPE using a simple angle
qpe = QPE(control_qubits=3, theta=0.125, debug=True)
qpe_circuit = qpe.build()
```

Or as gates:

```python
from qutilities.qft import QFTGate
from qutilities.qpe import QPEGate

qft_gate = QFTGate(4).build()
qpe_gate = QPEGate(3, theta=0.125).build()
```

---

## 📁 Modules

```
qutilities/
├── qft/
│   ├── qft.py        # QFT + QFTGate
│   └── __init__.py
├── qpe/
│   ├── qpe.py        # QPE + QPEGate
│   └── __init__.py
├── __init__.py
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