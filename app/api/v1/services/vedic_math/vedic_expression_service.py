from decimal import Decimal
import re

from .vedic_addition_service import VedicAdditionService
from .vedic_division_service import VedicParavartyaYojayetDivisionService
from .vedic_multiplication_service import VedicUrdhvaTiryagbhyamService
from .vedic_subtraction_service import VedicSubtractionService


class VedicExpressionService:
    _STEP_PREFIX = re.compile(r"^Step\s+\d+\s+-\s+")

    def __init__(self):
        self._addition = VedicAdditionService()
        self._subtraction = VedicSubtractionService()
        self._multiplication = VedicUrdhvaTiryagbhyamService()
        self._division = VedicParavartyaYojayetDivisionService()

    @staticmethod
    def _format_number(value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, Decimal):
            text = format(value, "f")
            if "." in text:
                text = text.rstrip("0").rstrip(".")
            return "0" if text in {"", "-0"} else text
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return f"{value:.8f}".rstrip("0").rstrip(".")
        return str(value)

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
    def _integer_value(value):
        if isinstance(value, int):
            return value
        if isinstance(value, Decimal) and value == value.to_integral_value():
            return int(value)
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return None

    @classmethod
    def _to_decimal(cls, value):
        if isinstance(value, Decimal):
            return value
        if isinstance(value, int):
            return Decimal(value)
        if isinstance(value, float):
            return Decimal(str(value))
        return Decimal(str(value))

    @classmethod
    def _fractional_places(cls, value):
        text = cls._format_number(value)
        if "." not in text:
            return 0
        return len(text.split(".", 1)[1])

    @classmethod
    def _fixed_scale_text(cls, value, scale):
        decimal_value = cls._to_decimal(value)
        if scale == 0:
            return cls._format_number(decimal_value)
        return format(decimal_value, f".{scale}f")

    @classmethod
    def _scale_numbers(cls, *values):
        scale = max(cls._fractional_places(value) for value in values)
        factor = 10 ** scale
        scaled_values = [int(cls._to_decimal(value) * factor) for value in values]
        aligned_values = [cls._fixed_scale_text(value, scale) for value in values]
        return scale, factor, aligned_values, scaled_values

    @classmethod
    def _scaled_to_display(cls, value, scale):
        if scale == 0:
            return str(value)
        return cls._format_number(Decimal(value) / (Decimal(10) ** scale))

    @classmethod
    def _detail_entry(cls, step, rule, calculation, output):
        return {
            "step": step,
            "rule": rule,
            "calculation": calculation,
            "output": output,
        }

    @classmethod
    def _renumber_details(cls, details):
        renumbered = []
        next_step = 1

        for detail in details:
            if isinstance(detail, dict):
                updated = dict(detail)
                if "step" in updated:
                    updated["step"] = next_step
                if "step_num" in updated:
                    updated["step_num"] = next_step
                renumbered.append(updated)
                next_step += 1
                continue

            if isinstance(detail, str) and cls._STEP_PREFIX.match(detail):
                renumbered.append(cls._STEP_PREFIX.sub(f"Step {next_step} - ", detail, count=1))
                next_step += 1
                continue

            renumbered.append(detail)

        return renumbered

    def _can_use_vedic_decimal_method(self, *values):
        return all(self._to_decimal(value) >= 0 for value in values)

    @staticmethod
    def _non_zero_sign(value):
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0

    def _decimal_alignment_details(self, aligned_values, scaled_values, scale):
        return [
            self._detail_entry(
                1,
                "Decimal alignment",
                f"Align decimal places to {scale} digits: {aligned_values[0]} -> {scaled_values[0]}, {aligned_values[1]} -> {scaled_values[1]}",
                {
                    "aligned_operands": aligned_values,
                    "scaled_operands": scaled_values,
                },
            )
        ]

    def _decimal_placement_detail(self, scaled_result, scale):
        return self._detail_entry(
            1,
            "Decimal placement",
            f"Place decimal back {scale} digits from the right: {scaled_result} -> {self._scaled_to_display(scaled_result, scale)}",
            self._scaled_to_display(scaled_result, scale),
        )

    def _sign_application_detail(self, value):
        return self._detail_entry(
            1,
            "Sign application",
            f"Apply negative sign to the magnitude result: -{abs(value)}",
            value,
        )

    def _signed_addition_bundle(self, a, b):
        scale, _, aligned_values, scaled_values = self._scale_numbers(a, b)
        scaled_a, scaled_b = scaled_values
        details = []

        if scale > 0:
            details.extend(self._decimal_alignment_details(aligned_values, scaled_values, scale))

        if scaled_a == 0 or scaled_b == 0 or self._non_zero_sign(scaled_a) == self._non_zero_sign(scaled_b):
            abs_a = abs(scaled_a)
            abs_b = abs(scaled_b)
            details.append(
                self._detail_entry(
                    1,
                    "Left-to-Right Vedic addition",
                    f"Add magnitudes using Left-to-Right Vedic addition: {abs_a} + {abs_b}",
                    {"scaled_operation": f"{abs_a} + {abs_b}"},
                )
            )
            details.extend(self._addition.calculate([abs_a, abs_b]).get("steps", []))
            scaled_result = abs_a + abs_b
            result_sign = -1 if scaled_a < 0 and scaled_b < 0 else 1

            if result_sign < 0 and scaled_result != 0:
                scaled_result = -scaled_result
                details.append(self._sign_application_detail(scaled_result))

            if scale > 0:
                details.append(self._decimal_placement_detail(scaled_result, scale))

            return ("Left-to-Right Vedic addition", self._renumber_details(details))

        abs_a = abs(scaled_a)
        abs_b = abs(scaled_b)
        if abs_a >= abs_b:
            larger = abs_a
            smaller = abs_b
            result_sign = 1 if scaled_a > 0 else -1
        else:
            larger = abs_b
            smaller = abs_a
            result_sign = 1 if scaled_b > 0 else -1

        sub_data = self._subtraction.calculate([larger, smaller])
        details.append(
            self._detail_entry(
                1,
                sub_data.get("primary_rule", "Direct subtraction"),
                f"Signed addition becomes subtraction of magnitudes: {larger} - {smaller}",
                {"scaled_operation": f"{larger} - {smaller}"},
            )
        )
        details.extend(sub_data.get("steps", []))
        scaled_result = sub_data.get("difference", larger - smaller)

        if result_sign < 0 and scaled_result != 0:
            scaled_result = -scaled_result
            details.append(self._sign_application_detail(scaled_result))

        if scale > 0:
            details.append(self._decimal_placement_detail(scaled_result, scale))

        return (sub_data.get("primary_rule", "Direct subtraction"), self._renumber_details(details))

    @staticmethod
    def _tokens_to_expression(tokens):
        parts = []
        for idx, token in enumerate(tokens):
            if isinstance(token, (int, float)) and token < 0 and idx > 0:
                parts.append(f"({VedicExpressionService._format_number(token)})")
            else:
                parts.append(VedicExpressionService._format_number(token))
        return " ".join(parts)

    def _tokenize_expression(self, expression: str):
        expr = expression.replace(" ", "").replace("÷", "/").replace("x", "*").replace("X", "*")
        if not expr:
            raise ValueError("Expression cannot be empty.")

        tokens = []
        i = 0
        expect_number = True

        while i < len(expr):    
            ch = expr[i]
            if expect_number:
                sign = 1
                if ch in "+-":
                    sign = -1 if ch == "-" else 1
                    i += 1
                    if i >= len(expr):
                        raise ValueError("Expression cannot end with a unary sign.")
                    ch = expr[i]

                if not ch.isdigit():
                        raise ValueError("Only integers with operators +, -, *, / are supported.")

                start = i
                while i < len(expr) and expr[i].isdigit():
                    i += 1
                tokens.append(sign * int(expr[start:i]))
                expect_number = False
            else:
                if ch not in "+-*/":
                    raise ValueError("Only +, -, *, / operators are supported.")
                tokens.append(ch)
                i += 1
                expect_number = True

        if expect_number:
            raise ValueError("Expression cannot end with an operator.")

        return tokens

    def _addition_details(self, a, b):
        a_int = self._integer_value(a)
        b_int = self._integer_value(b)
        if a_int is not None and b_int is not None and a_int >= 0 and b_int >= 0:
            return self._addition.calculate([a_int, b_int]).get("steps", [])

        _, details = self._signed_addition_bundle(a, b)
        if details:
            return details

        result = a + b
        return [
            {
                "step": 1,
                "rule": "Left-to-Right Vedic addition",
                "calculation": f"{self._format_number(a)} + {self._format_number(b)} = {self._format_number(result)}",
                "output": self._normalize_number(result),
            }
        ]

    def _subtraction_bundle(self, a, b):
        a_int = self._integer_value(a)
        b_int = self._integer_value(b)
        if a_int is not None and b_int is not None and a_int >= 0 and b_int >= 0:
            sub_data = self._subtraction.calculate([a_int, b_int])
            return (
                sub_data.get("primary_rule", "Direct subtraction"),
                sub_data.get("steps", []),
            )

        if self._can_use_vedic_decimal_method(a, b):
            scale, _, aligned_values, scaled_values = self._scale_numbers(a, b)
            if scale > 0:
                scaled_a, scaled_b = scaled_values
                sub_data = self._subtraction.calculate(scaled_values)
                details = [
                    *self._decimal_alignment_details(aligned_values, scaled_values, scale),
                    self._detail_entry(
                        2,
                        sub_data.get("primary_rule", "Direct subtraction"),
                        f"Apply {sub_data.get('primary_rule', 'Direct subtraction')} on aligned integers: {scaled_a} - {scaled_b}",
                        {"scaled_operation": f"{scaled_a} - {scaled_b}"},
                    ),
                ]
                details.extend(sub_data.get("steps", []))

                details.append(self._decimal_placement_detail(sub_data.get("difference"), scale))
                return (sub_data.get("primary_rule", "Direct subtraction"), self._renumber_details(details))

        signed_sutra, signed_details = self._signed_addition_bundle(a, -self._to_decimal(b))
        if signed_details:
            transformed_details = [
                self._detail_entry(
                    1,
                    "Subtraction transform",
                    f"Convert subtraction to signed addition: {self._format_number(a)} - {self._format_number(b)} = {self._format_number(a)} + ({self._format_number(-self._to_decimal(b))})",
                    {"transformed_operation": f"{self._format_number(a)} + ({self._format_number(-self._to_decimal(b))})"},
                ),
                *signed_details,
            ]
            return (signed_sutra, self._renumber_details(transformed_details))

        result = a - b
        return (
            "Direct subtraction",
            [
                "Rule Guide 1 - Nikhilam Navatashcaramam Dashatah: use when the upper number is exactly 10, 100, 1000, ... and the lower number is smaller.",
                "Rule Guide 2 - Nikhilam Navatashcaramam Dashatah: use when subtraction can be done through complement from base 10, 100, 1000, ... .",
                "Rule Guide 3 - Direct subtraction: use when signed numbers are involved or a complement-based shortcut is not suitable.",
                f"Rule Guide 4 - For {self._format_number(a)} - {self._format_number(b)}, selected rule = Direct subtraction",
                f"Step 1 - Direct subtraction rule: {self._format_number(a)} - {self._format_number(b)} = {self._format_number(result)}",
            ],
        )

    def _multiplication_details(self, a, b):
        a_int = self._integer_value(a)
        b_int = self._integer_value(b)
        if a_int is not None and b_int is not None:
            mul_data = self._multiplication.calculate(a_int, b_int)
            return mul_data.get("steps", [])

        scale_a = self._fractional_places(a)
        scale_b = self._fractional_places(b)
        scaled_a = int(self._to_decimal(a) * (10 ** scale_a))
        scaled_b = int(self._to_decimal(b) * (10 ** scale_b))
        scale_total = scale_a + scale_b
        mul_data = self._multiplication.calculate(scaled_a, scaled_b)
        details = []

        if scale_total > 0:
            details.append(
                self._detail_entry(
                    1,
                    "Decimal alignment",
                    f"Convert operands to integers for Nikhilam Sutra: {self._fixed_scale_text(a, scale_a)} -> {scaled_a}, {self._fixed_scale_text(b, scale_b)} -> {scaled_b}",
                    {
                        "scaled_operands": [scaled_a, scaled_b],
                        "fractional_places": [scale_a, scale_b],
                    },
                )
            )

        details.append(
            self._detail_entry(
                1,
                "Nikhilam Sutra",
                f"Apply Nikhilam Sutra on integers: {scaled_a} x {scaled_b}",
                {"scaled_operation": f"{scaled_a} x {scaled_b}"},
            )
        )
        details.extend(mul_data.get("steps", []))

        if scale_total > 0:
            details.append(self._decimal_placement_detail(mul_data.get("result"), scale_total))

        return self._renumber_details(details)

    def _division_details(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")

        a_int = self._integer_value(a)
        b_int = self._integer_value(b)
        if a_int is not None and b_int is not None:
            return self._division.calculate(a_int, b_int).get("steps", [])

        scale = max(self._fractional_places(a), self._fractional_places(b))
        scaled_a = int(self._to_decimal(a) * (10 ** scale))
        scaled_b = int(self._to_decimal(b) * (10 ** scale))
        division_data = self._division.calculate(scaled_a, scaled_b)
        details = []

        if scale > 0:
            details.append(
                self._detail_entry(
                    1,
                    "Decimal alignment",
                    f"Scale dividend and divisor equally to preserve quotient: {self._fixed_scale_text(a, scale)} -> {scaled_a}, {self._fixed_scale_text(b, scale)} -> {scaled_b}",
                    {
                        "scaled_dividend": scaled_a,
                        "scaled_divisor": scaled_b,
                        "scale": scale,
                    },
                )
            )

        details.extend(division_data.get("steps", []))
        return self._renumber_details(details)

    def calculate(self, expression: str) -> dict:
        tokens = self._tokenize_expression(expression)
        normalized_expression = self._tokens_to_expression(tokens)
        working_tokens = tokens[:]
        all_steps = []
        step_no = 1

        idx = 1
        while idx < len(working_tokens) - 1:
            if working_tokens[idx] not in {"*", "/"}:
                idx += 2
                continue

            left = working_tokens[idx - 1]
            operator = working_tokens[idx]
            right = working_tokens[idx + 1]
            before_expr = self._tokens_to_expression(working_tokens)
            if operator == "*":
                product = self._normalize_number(self._to_decimal(left) * self._to_decimal(right))
                sutra = "Nikhilam Sutra"
                operation_label = f"{self._format_number(left)} * {self._format_number(right)}"
                explanation = f"{operation_label} = {self._format_number(product)}"
                details = self._multiplication_details(left, right)
            else:
                if right == 0: 
                    raise ValueError("Division by zero is not allowed.")
                product = self._normalize_number(self._to_decimal(left) / self._to_decimal(right))
                sutra = "Paravartya Yojayet"
                operation_label = f"{self._format_number(left)} / {self._format_number(right)}"
                explanation = f"{operation_label} = {self._format_number(product)}"
                details = self._division_details(left, right)

            working_tokens = working_tokens[: idx - 1] + [product] + working_tokens[idx + 2 :]
            after_expr = self._tokens_to_expression(working_tokens)

            all_steps.append(
                {
                    "step": step_no,
                    "sutra": sutra,
                    "operation": operation_label,
                    "before": before_expr,
                    "after": after_expr,
                    "explanation": explanation,
                    "result_after_step": product,
                    "details": details,
                }
            )
            step_no += 1
            idx = 1

        while len(working_tokens) > 1:
            left = working_tokens[0]
            operator = working_tokens[1]
            right = working_tokens[2]
            before_expr = self._tokens_to_expression(working_tokens)

            if operator == "+":
                new_value = self._normalize_number(self._to_decimal(left) + self._to_decimal(right))
                sutra, details = self._signed_addition_bundle(left, right)
                explanation = f"{self._format_number(left)} + {self._format_number(right)} = {self._format_number(new_value)}"
            elif operator == "-":
                new_value = self._normalize_number(self._to_decimal(left) - self._to_decimal(right))
                sutra, details = self._subtraction_bundle(left, right)
                explanation = f"{self._format_number(left)} - {self._format_number(right)} = {self._format_number(new_value)}"
            else:
                raise ValueError(f"Unsupported operator '{operator}' in expression.")

            new_value = self._normalize_number(new_value)

            working_tokens = [new_value] + working_tokens[3:]
            after_expr = self._tokens_to_expression(working_tokens)

            all_steps.append(
                {
                    "step": step_no,
                    "sutra": sutra,
                    "operation": f"{self._format_number(left)} {operator} {self._format_number(right)}",
                    "before": before_expr,
                    "after": after_expr,
                    "explanation": explanation,
                    "result_after_step": new_value,
                    "details": details,
                }
            )
            step_no += 1

        return {
            "expression": expression,
            "normalized_expression": normalized_expression,
            "result": self._normalize_number(working_tokens[0]),
            "steps": all_steps,
        }