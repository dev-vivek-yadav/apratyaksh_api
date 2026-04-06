from decimal import Decimal
import re

from .vedic_addition_service import VedicAdditionService
from .vedic_division_service import VedicParavartyaYojayetDivisionService
from .vedic_multiplication_service import VedicUrdhvaTiryagbhyamService
from .vedic_subtraction_service import VedicSubtractionService


class VedicExpressionService:
    _BINARY_EXPR = re.compile(r"^\s*([+-]?\d+)\s*([+\-*/xX÷])\s*([+-]?\d+)\s*$")

    def __init__(self):
        self._addition = VedicAdditionService()
        self._subtraction = VedicSubtractionService()
        self._multiplication = VedicUrdhvaTiryagbhyamService()
        self._division = VedicParavartyaYojayetDivisionService()

    @staticmethod
    def _normalize_number(value):
        if isinstance(value, Decimal):
            if value == value.to_integral_value():
                return int(value)
            return float(value)
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value

    @staticmethod
    def _format_number(value):
        if isinstance(value, Decimal):
            text = format(value, "f")
            if "." in text:
                text = text.rstrip("0").rstrip(".")
            return "0" if text in {"", "-0"} else text
        return str(value)

    def _separate_numbers_and_operator(self, expression: str):
        match = self._BINARY_EXPR.match(expression)
        if not match:
            raise ValueError("For now only two-number expressions are supported, e.g. 12+5")

        left = int(match.group(1))
        operator = match.group(2).replace("x", "*").replace("X", "*").replace("÷", "/")
        right = int(match.group(3))
        return left, operator, right

    def calculate(self, expression: str) -> dict:
        print(f"Calculating expression: {expression}")
        left, operator, right = self._separate_numbers_and_operator(expression)
        normalized_expression = f"{left} {operator} {right}"

        if operator == "+":
            result = self._normalize_number(Decimal(left) + Decimal(right))
            print(f"Addition result: {result}")
            details = self._addition.calculate([left, right]).get("steps", [])
            sutra = "Left-to-Right Vedic addition"
        elif operator == "-":
            result = self._normalize_number(Decimal(left) - Decimal(right))
            details = self._subtraction.calculate([left, right]).get("steps", [])
            sutra = "Nikhilam Navatashcaramam Dashatah"
        elif operator == "*":
            result = self._normalize_number(Decimal(left) * Decimal(right))
            details = self._multiplication.calculate(left, right).get("steps", [])
            sutra = "Nikhilam Sutra"
        elif operator == "/":
            if right == 0:
                raise ValueError("Division by zero is not allowed.")
            result = self._normalize_number(Decimal(left) / Decimal(right))
            details = self._division.calculate(left, right).get("steps", [])
            sutra = "Paravartya Yojayet"
        else:
            raise ValueError(f"Unsupported operator '{operator}'")

        step = {
            "step": 1,
            "sutra": sutra,
            "operation": normalized_expression,
            "before": normalized_expression,
            "after": self._format_number(result),
            "explanation": f"{normalized_expression} = {self._format_number(result)}",
            "result_after_step": result,
            "details": details,
        }

        return {
            "expression": expression,
            "normalized_expression": normalized_expression,
            "result": result,
            "steps": [step],
        }