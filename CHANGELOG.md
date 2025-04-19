# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2025-04-19

### Added
- `QFTAdder`: Draper-style Quantum Fourier Transform adder supporting addition and subtraction
- Arithmetic module structure: `arithmetic.adders.qft_adder` integrated into main API
- Optional register injection, QFT skipping, debug drawing, and barrier control
- Benchmarks comparing custom vs native QFT adder on simulators and hardware

### Changed
- Renamed `qft_qubits` to `num_qubits` in `QFTGate` to align with standard terminology
- Updated root `__init__.py` to expose arithmetic tools via unified API
- Generalized docstrings and module index for extensibility

### Notes
- First public-facing addition of arithmetic tools
- Internal refactors maintain backward compatibility for QFT/QPE users

---

## [0.1.0] - 2025-04-12

### Added
- Initial public release of `qutilities`
- `QFT` class for building Quantum Fourier Transform circuits
- `QFTGate` class for exporting QFT as a reusable gate
- `QPE` class supporting both angle-based and unitary-based phase estimation
- `QPEGate` class for exporting QPE as a reusable gate
- Gate approximation, debug visualization, and barrier toggles
- Installation via `pyproject.toml`, GitHub documentation, and `.gitignore`