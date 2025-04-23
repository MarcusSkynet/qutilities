# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] - 2025-04-23

### Added
- Introduced `QFTMultiplier` class for quantum-coherent multiplication in the Fourier basis.
  - Performs `|Y⟩|M⟩|N⟩ → |Y ± M × N⟩|M⟩|N⟩`
  - Parameters: `multiplicand`, `multiplier`, optional `target`
  - Flags: `inverse`, `skip_qft`, `insert_barrier`, `debug`
  - Modular helper methods: `_create_qft_gate`, `_create_iqft_gate`, `_apply_qft`, `_apply_C_ADD`, `_debug_display`
  - Internally composes `QFTAdder` as a controlled operation
  - Ready for use as a composable quantum `Gate` (unitary)

### Changed
- Finalized `QFTAdder` interface and documentation:
  - Replaced parameters `X` and `A` with clearer names: `target`, `operand`
  - Aligned internal naming (`X_reg`, `A_reg`) with symbolic math
  - Updated docstrings to match public API (`target`, `operand`) and clarify semantics:
    - Overflow constraint on `target`
    - Subtraction toggle via `inverse`
    - Label behavior and debugging support

- Refined import structure throughout:
  - Switched from circular top-level imports to clean absolute submodule references
  - Avoided triggering package `__init__` during submodule loading (fixes ImportError)

### Notes
- All arithmetic logic is fully quantum-compatible: coherent, reversible, and superposition-safe
- Style and architecture now align with `QFTGate` and `QPE` module conventions

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