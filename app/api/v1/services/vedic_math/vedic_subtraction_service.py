class VedicSubtractionService:
    @staticmethod
    def _pad_left(text: str, width: int):
        return " " * (width - len(text)) + text

    @staticmethod
    def _is_power_of_ten(value: int):
        return value > 0 and str(value)[0] == "1" and set(str(value)[1:]) <= {"0"}

    @staticmethod
    def _rule_guide(minuend: int, subtrahend: int, chosen_rule: str):
        return [
            "Rule Guide 1 - Nikhilam Navatashcaramam Dashatah: use when the upper number is exactly 10, 100, 1000, ... and the lower number is smaller.",
            "Rule Guide 2 - Nikhilam Navatashcaramam Dashatah: use when subtraction can be done through complement from base 10, 100, 1000, ... .",
            "Rule Guide 3 - Direct subtraction: use when signed numbers are involved or a complement-based shortcut is not suitable.",
            f"Rule Guide 4 - For {minuend} - {subtrahend}, selected rule = {chosen_rule}",
        ]

    @staticmethod
    def _subtract_from_power_of_ten(minuend: int, subtrahend: int):
        width = len(str(minuend))
        subtrahend_text = str(subtrahend).zfill(width)
        result_digits = []
        presentation_steps = [
            f"Rule - Nikhilam Navatashcaramam Dashatah: since minuend = {minuend}, subtract each digit of {subtrahend_text} from 9 and the last digit from 10"
        ]
        steps = []

        for index, digit_text in enumerate(subtrahend_text):
            digit = int(digit_text)
            if index == width - 1:
                adjusted = 10 - digit
                calculation = f"Last from 10: 10 - {digit} = {adjusted}"
                rule_name = "Nikhilam Navatashcaramam Dashatah"
            else:
                adjusted = 9 - digit
                calculation = f"All from 9: 9 - {digit} = {adjusted}"
                rule_name = "Nikhilam Navatashcaramam Dashatah"

            result_digits.append(str(adjusted))
            steps.append(
                {
                    "rule": rule_name,
                    "calculation": calculation,
                    "output": int("".join(result_digits)),
                }
            )
            presentation_steps.append(
                f"Rule - {calculation}; partial result = {''.join(result_digits)}"
            )

        result = int("".join(result_digits))
        presentation_steps.append(
            f"Rule - Final result by Nikhilam Navatashcaramam Dashatah = {result}"
        )
        return result, steps, presentation_steps, "Nikhilam Navatashcaramam Dashatah"

    def _subtract_pair(self, minuend: int, subtrahend: int):
        if self._is_power_of_ten(minuend) and 0 <= subtrahend <= minuend:
            return self._subtract_from_power_of_ten(minuend, subtrahend)

        result, steps, presentation_steps = self._subtract_pair_nikhilam(minuend, subtrahend)
        return result, steps, presentation_steps, "Nikhilam Navatashcaramam Dashatah"

    @staticmethod
    def _subtract_pair_nikhilam(minuend: int, subtrahend: int):
        width = max(len(str(abs(minuend))), len(str(abs(subtrahend))))
        base = 10 ** width
        complement = base - subtrahend
        interim = minuend + complement
        presentation_steps = [
            f"Rule - Base selection: max digits = {width}, so base = 10^{width} = {base}",
            f"Rule - Nikhilam complement: {base} - {subtrahend} = {complement}",
            f"Rule - Add complement: {minuend} + {complement} = {interim}",
        ]

        steps = [
            {
                "rule": "Nikhilam Navatashcaramam Dashatah",
                "calculation": f"Base = 10^{width} = {base}",
                "output": base,
                "breakdown": [f"max digits = {width}", f"10^{width} = {base}"],
            },
            {
                "rule": "Nikhilam Navatashcaramam Dashatah",
                "calculation": f"Complement = {base} - {subtrahend} = {complement}",
                "output": complement,
                "breakdown": [
                    f"Subtrahend = {subtrahend}",
                    f"Base - Subtrahend = {base} - {subtrahend}",
                ],
            },
            {
                "rule": "Nikhilam Navatashcaramam Dashatah",
                "calculation": f"{minuend} + {complement} = {interim}",
                "output": interim,
                "breakdown": [
                    f"Minuend = {minuend}",
                    f"Complement = {complement}",
                ],
            },
            {
                "rule": "Nikhilam Navatashcaramam Dashatah",
                "calculation": f"Overflow check: {interim} >= {base} -> {interim >= base}",
                "output": interim >= base,
            },
        ]
        presentation_steps.append(
            f"Rule - Overflow check: {interim} >= {base} -> {interim >= base}"
        )

        if interim >= base:
            result = interim - base
            steps.append(
                {
                    "rule": "Nikhilam Navatashcaramam Dashatah",
                    "calculation": f"{interim} - {base} = {result}",
                    "output": result,
                    "breakdown": [
                        "Overflow present, so discard base once.",
                        f"Final pair result = {result}",
                    ],
                }
            )
            presentation_steps.append(
                f"Rule - Discard base once: {interim} - {base} = {result}"
            )
            return result, steps, presentation_steps

        result = -(base - interim)
        steps.append(
            {
                "rule": "Nikhilam Navatashcaramam Dashatah",
                "calculation": f"-({base} - {interim}) = {result}",
                "output": result,
                "breakdown": [
                    f"Base - interim = {base} - {interim} = {base - interim}",
                    f"Apply negative sign -> {result}",
                ],
            }
        )
        presentation_steps.append(
            f"Rule - Negative balance: {base} - {interim} = {base - interim}, so result = {result}"
        )
        return result, steps, presentation_steps

    def calculate(self, numbers: list[int]) -> dict:
        nums = [int(n) for n in numbers]
        final_difference = nums[0] - sum(nums[1:])

        max_num = max(abs(n) for n in nums)
        max_len = len(str(max_num))
        stacked_lines = [self._pad_left(str(abs(n)), max_len) for n in nums]
        stacked = "\n".join(stacked_lines + ["-" * max_len])
        rules_used = []

        steps = [
            {
                "step": 1,
                "rule": "Nikhilam Navatashcaramam Dashatah",
                "calculation": f"Start from {nums[0]} and subtract each next number.",
                "numbers": nums,
                "output": nums[0],
            }
        ]
        running_value = nums[0]
        step_segments = []
        for index, subtrahend in enumerate(nums[1:], start=1):
            if running_value >= 0 and subtrahend >= 0:
                pair_result, pair_steps, pair_presentation_steps, rule_used = self._subtract_pair(running_value, subtrahend)
                rules_used.append(rule_used)
                steps.append(
                    {
                        "step": len(steps) + 1,
                        "rule": rule_used,
                        "calculation": f"Pair {index}: {running_value} - {subtrahend}",
                        "output": running_value,
                        "breakdown": [
                            f"Current running value = {running_value}",
                            f"Current subtrahend = {subtrahend}",
                        ],
                    }
                )
                pair_segment = [
                    f"Apply {rule_used} on pair {index}: {running_value} - {subtrahend}",
                    *pair_presentation_steps,
                ]

                for pair_step in pair_steps:
                    steps.append(
                        {
                            "step": len(steps) + 1,
                            **pair_step,
                        }
                    )
                running_value = pair_result
                pair_segment.append(f"Running result after pair {index} = {running_value}")
                step_segments.extend(pair_segment)
            else:
                direct = running_value - subtrahend
                rules_used.append("Direct subtraction")
                steps.append(
                    {
                        "step": len(steps) + 1,
                        "rule": "Direct subtraction",
                        "calculation": f"{running_value} - {subtrahend} = {direct}",
                        "output": direct,
                        "breakdown": [
                            "Signed fallback path",
                            f"Updated running value = {direct}",
                        ],
                    }
                )
                step_segments.append(
                    f"Direct subtraction rule on pair {index}: {running_value} - {subtrahend} = {direct}"
                )
                running_value = direct

        steps.append(
            {
                "step": len(steps) + 1,
                "rule": "Nikhilam Navatashcaramam Dashatah",
                "calculation": f"Result = {final_difference}",
                "output": final_difference,
            }
        )
        guide = self._rule_guide(nums[0], nums[1] if len(nums) > 1 else 0, rules_used[0] if rules_used else "Direct subtraction")
        presentation_steps = guide + [f"Step 1 - Start subtraction with {nums[0]}"]

        for index, item in enumerate(step_segments, start=2):
            presentation_steps.append(f"Step {index} - {item}")

        presentation_steps.append(
            f"Step {len(step_segments) + 2} - Final subtraction result = {final_difference}"
        )

        return {
            "difference": final_difference,
            "primary_rule": rules_used[0] if rules_used else "Direct subtraction",
            "rules_used": rules_used,
            "available_rules": guide[:3],
            "steps": steps,
            "presentation_steps": presentation_steps,
            "stacked": stacked,
            "numbers": nums,
            "result_digits": [int(ch) for ch in str(abs(final_difference))],
        }
