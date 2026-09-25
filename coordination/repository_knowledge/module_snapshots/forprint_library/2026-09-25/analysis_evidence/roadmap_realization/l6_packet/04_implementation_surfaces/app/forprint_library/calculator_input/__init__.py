"""Calculator input projection contract for ForPrint Library.

This package exposes a read-only, deterministic Library projection for downstream
Calculator consumption. It does not implement prices or import Calculator code.
"""

from forprint_library.calculator_input.contract import (
    CalculatorInputContractError,
    CalculatorInputEnvelope,
    CalculatorInputErrorType,
    CalculatorReferenceIds,
    ValidationSnapshot,
    build_calculator_input,
)

__all__ = [
    "CalculatorInputContractError",
    "CalculatorInputEnvelope",
    "CalculatorInputErrorType",
    "CalculatorReferenceIds",
    "ValidationSnapshot",
    "build_calculator_input",
]
