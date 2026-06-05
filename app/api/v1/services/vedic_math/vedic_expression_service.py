from decimal import Decimal
import re


from .vedic_add_service import VedicAdditionCopyService
from .vedic_division_service import VedicParavartyaYojayetDivisionService
# from .vedic_multiplication_service import VedicUrdhvaTiryagbhyamService
from .vedic_multi_service import VedicMultiService
# from .vedic_subtraction_service import VedicSubtractionService
from .vedic_subct_service import VedicSubctService


class VedicExpressionService:
    _BINARY_EXPR = re.compile(r"^\s*([+-]?\d+)\s*([+\-*/xX÷])\s*([+-]?\d+)\s*$")

    def __init__(self):
        self._addition = VedicAdditionCopyService()
        self._subtraction = VedicSubctService()
        self._multiplication = VedicMultiService()
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
        numbers = list(map(int, re.findall(r'\d+', expression)))
        operators = re.findall(r'[+\-*/xX÷]', expression)

        operators = [
            op.replace("x", "*").replace("X", "*").replace("÷", "/")
            for op in operators
        ]
        return numbers, operators

    def calculate(self, expression: str) -> dict:
        print(f"Calculating expression: {expression}")

        numbers, operators = self._separate_numbers_and_operator(expression)

        if not numbers or not operators:
            raise ValueError("Invalid expression format.")

        # abhi sirf same operator expressions support kar rahe hain
        if len(set(operators)) != 1:
            raise ValueError("Mixed operators are not supported yet.")

        operator = operators[0]

        if operator == "+":
            details = self._addition.calculate(numbers).get("steps", [])
            sutra = "Left-to-Right Vedic addition"

        elif operator == "-":
            result = self._subtraction.calculate(numbers)

            details = result.get("steps", [])
            sutra = "Nikhilam Navatashcaramam Dashatah"

        # elif operator == "*":
        #     result = numbers[0]

        #     for num in numbers[1:]:
        #         result = self._multiplication.calculate(result, num)

        #     details = result.get("steps", [])
        #     sutra = "Nikhilam Sutra"

        elif operator == "*":
            
            result = self._multiplication.calculate(numbers)

            details = result.get("steps", [])
            sutra = "Nikhilam Sutra"

        elif operator == "/":
            result = numbers[0]

            for num in numbers[1:]:
                if num == 0:
                    raise ValueError("Division by zero is not allowed.")

                result = self._division.calculate(result, num)

            details = result.get("steps", [])
            sutra = "Paravartya Yojayet"

        else:
            raise ValueError(f"Unsupported operator '{operator}'")

        step = {
            "step": 1,
            "sutra": sutra,
            "details": details,
        }

        return {
            "expression": expression,
            "steps": [step],
        }