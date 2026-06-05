class VedicDhvajankaDivisionService:
    @staticmethod
    def _flag_correction(flag_digits: list[int], quotient_digits: list[int], index: int):
        """
        Dhvajanka correction for current column:
        f1*q_i + f2*q_{i-1} + f3*q_{i-2} + ...
        """
        correction = 0
        terms = []
        for flag_pos, flag in enumerate(flag_digits, start=1):
            q_pos = index - (flag_pos - 1)
            if q_pos < 0:
                continue
            q_digit = quotient_digits[q_pos]
            term = flag * q_digit
            correction += term
            terms.append(f"{flag}x{q_digit}={term}")
        return correction, terms

    def calculate(self, dividend: int, divisor: int):
        if divisor == 0:
            raise ValueError("Division by zero is not allowed.")

        sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
        dividend_abs = abs(dividend)
        divisor_abs = abs(divisor)

        dividend_digits = [int(d) for d in str(dividend_abs)]
        divisor_digits = [int(d) for d in str(divisor_abs)]

        main_digit = divisor_digits[0]
        flag_digits = divisor_digits[1:]
        remainder_places = len(flag_digits)

        true_quotient, true_remainder = divmod(dividend_abs, divisor_abs)

        steps = [
            {
                "step": 1,
                "step_type": "Setup",
                "rule": "Paravartya Yojayet (Dhvajanka Sutra)",
                "calculation": (
                    f"Divisor {divisor_abs}: main digit={main_digit}, "
                    f"dhvajank={flag_digits if flag_digits else [0]}; "
                    f"remainder places={remainder_places}"
                ),
                "output": {
                    "main_digit": main_digit,
                    "dhvajank": flag_digits,
                    "remainder_places": remainder_places,
                },
            }
        ]

        if dividend_abs < divisor_abs:
            steps.append(
                {
                    "step": 2,
                    "step_type": "Finalize",
                    "rule": "Paravartya Yojayet (Dhvajanka Sutra)",
                    "calculation": (
                        f"Since {dividend_abs} < {divisor_abs}, quotient = 0 and remainder = {dividend_abs}"
                    ),
                    "output": {"quotient": 0, "remainder": dividend_abs},
                }
            )
            return {
                "result": 0,
                "remainder": dividend if dividend >= 0 else -dividend_abs,
                "steps": steps,
            }

        quotient_len = len(dividend_digits) - len(divisor_digits) + 1
        quotient_digits = []
        current_val = dividend_digits[0]

        for idx in range(quotient_len):
            q = current_val // main_digit
            r = current_val % main_digit
            quotient_digits.append(q)

            steps.append(
                {
                    "step": len(steps) + 1,
                    "step_type": "Division",
                    "rule": "Paravartya Yojayet (Dhvajanka Sutra)",
                    "calculation": (
                        f"Column {idx + 1}: {current_val} / {main_digit} -> "
                        f"q={q}, remainder={r}"
                    ),
                    "output": {"q_digit": q, "remainder": r, "partial_q": quotient_digits[:]}
                }
            )

            if idx == quotient_len - 1:
                break

            next_digit = dividend_digits[idx + 1]
            raw_next = r * 10 + next_digit
            correction, terms = self._flag_correction(flag_digits, quotient_digits, idx)
            adjusted = raw_next - correction

            # If adjusted becomes negative, reduce current q and recompute correction.
            while adjusted < 0 and quotient_digits[idx] > 0:
                quotient_digits[idx] -= 1
                q = quotient_digits[idx]
                r = current_val - (q * main_digit)
                raw_next = r * 10 + next_digit
                correction, terms = self._flag_correction(flag_digits, quotient_digits, idx)
                adjusted = raw_next - correction

            steps.append(
                {
                    "step": len(steps) + 1,
                    "step_type": "Dhvajanka correction",
                    "rule": "Paravartya Yojayet (Dhvajanka Sutra)",
                    "calculation": (
                        f"Next={raw_next}; correction="
                        f"{(' + '.join(terms)) if terms else '0'} => {correction}; "
                        f"adjusted={adjusted}"
                    ),
                    "output": {
                        "next_raw": raw_next,
                        "correction": correction,
                        "correction_terms": terms,
                        "adjusted": adjusted,
                    },
                }
            )

            current_val = adjusted

        raw_q = int("".join(str(d) for d in quotient_digits)) if quotient_digits else 0

        if flag_digits and quotient_digits:
            lead_q = quotient_digits[0]
            flag_products = [lead_q * flag for flag in flag_digits]
            trailing_digits = dividend_digits[1 : 1 + len(flag_digits)]
            steps.append(
                {
                    "step": len(steps) + 1,
                    "step_type": "Remainder correction",
                    "rule": "Paravartya Yojayet (Dhvajanka Sutra)",
                    "calculation": (
                        f"Sanshodhan: q1={lead_q}; dhvajank {flag_digits} -> products {flag_products}. "
                        f"Use these against trailing digits {trailing_digits} while forming final remainder."
                    ),
                    "output": {
                        "lead_quotient_digit": lead_q,
                        "dhvajank": flag_digits,
                        "flag_products": flag_products,
                        "trailing_digits": trailing_digits,
                    },
                }
            )

        if raw_q != true_quotient:
            # Keep mathematically exact quotient/remainder while still exposing Dhvajanka teaching steps.
            steps.append(
                {
                    "step": len(steps) + 1,
                    "step_type": "Normalization",
                    "rule": "Paravartya Yojayet (Dhvajanka Sutra)",
                    "calculation": (
                        f"Normalize to exact integer division: {dividend_abs} // {divisor_abs} = "
                        f"{true_quotient}, remainder {true_remainder}"
                    ),
                    "output": {
                        "dhvajanka_q": raw_q,
                        "normalized_q": true_quotient,
                        "normalized_r": true_remainder,
                    },
                }
            )

        signed_quotient = true_quotient * sign
        signed_remainder = true_remainder if dividend >= 0 else -true_remainder

        steps.append(
            {
                "step": len(steps) + 1,
                "step_type": "Finalize",
                "rule": "Paravartya Yojayet (Dhvajanka Sutra)",
                "calculation": (
                    f"Final: {dividend_abs} = {divisor_abs} x {true_quotient} + {true_remainder}; "
                    f"apply sign on quotient -> {signed_quotient}"
                ),
                "output": {"quotient": signed_quotient, "remainder": signed_remainder},
            }
        )

        return {
            "result": signed_quotient,
            "remainder": signed_remainder,
            "steps": steps,
        }


class VedicParavartyaYojayetDivisionService(VedicDhvajankaDivisionService):
    """Backward-compatible alias used by expression service imports."""
