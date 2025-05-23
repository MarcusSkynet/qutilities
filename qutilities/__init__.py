# This file is part of the on-tides-of-uncertainty project.
#
# (C) 2025 On Tides of Uncertainty
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module is part of **on-tides-of-uncertainty**, a Python toolkit for exploring
quantum computation through composable libraries, educational experiments, and
algorithmic prototyping.

Provides:
    - QFT / QFTGate: Modular Quantum Fourier Transform (QFT) circuit and reusable gate
    - QPE / QPEGate: Generalized Quantum Phase Estimation (QPE) with toy or custom unitary
    - Arithmetic: Tools for QFT-based arithmetic (e.g. QFTAdder)
"""

# === IMPORTS START ===
from . import arithmetic
from . import qft
from . import qpe
__all__ = ['arithmetic', 'qft', 'qpe']
# === IMPORTS END ===

__version__ = "0.2.0"