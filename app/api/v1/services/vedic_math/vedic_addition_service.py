class VedicAdditionService:
    @staticmethod
    def _num_to_digits(n: int):
        return [ord(ch) - 48 for ch in str(n)]

    @staticmethod
    def _pad_left(text: str, width: int):
        return " " * (width - len(text)) + text

    @staticmethod
    def _place_name(power: int):
        if power == 0:
            return "Ones"
        if power == 1:
            return "Tens"
        if power == 2:
            return "Hundreds"
        if power == 3:
            return "Thousands"
        return f"10^{power}"

    def calculate(self, numbers: list[int]) -> dict:
        nums = [int(n) for n in numbers]
        digits_list = [self._num_to_digits(abs(n)) for n in nums]
        max_len = max(len(d) for d in digits_list)
        stacked_lines = [self._pad_left("".join(str(d) for d in row), max_len) for row in digits_list]
        stacked = "\n".join(stacked_lines + ["-" * max_len])

        if any(n < 0 for n in nums):
            signed_total = sum(nums)
            return {
                "sum": signed_total,
                "steps": [
                    f"Step 1 - Signed addition: {' + '.join(str(n) for n in nums)} = {signed_total}",
                    f"Step 2 - Final result: {signed_total}",
                ],
                "stacked": stacked,
                "numbers": nums,
                "result_digits": [int(ch) for ch in str(abs(signed_total))],
            }

        padded_numbers = [str(abs(n)).zfill(max_len) for n in nums]
        steps = [f"Step 1 - Align numbers to {max_len} digits: {', '.join(padded_numbers)}"]
        running_total = 0
        detail_step = 2

        for index in range(max_len):
            power = max_len - index - 1
            place_value = 10 ** power
            place_digits = [int(text[index]) for text in padded_numbers]
            expanded = [digit * place_value for digit in place_digits]
            place_sum = sum(expanded)
            previous_total = running_total
            running_total += place_sum
            digit_sum = sum(place_digits)
            place_name = self._place_name(power)

            steps.append(f"Step {detail_step} - {place_name} place: {' + '.join(str(d) for d in place_digits)} = {digit_sum}")
            detail_step += 1

            expanded_line = " + ".join(str(value) for value in expanded)
            steps.append(f"Step {detail_step} - {place_name} value: {expanded_line} = {place_sum}")
            detail_step += 1

            steps.append(f"Step {detail_step} - Running total: {previous_total} + {place_sum} = {running_total}")
            detail_step += 1

        signed_total = sum(nums)
        steps.append(f"Step {detail_step} - Final result: {signed_total}")

        return {
            "sum": signed_total,
            "steps": steps,
            "stacked": stacked,
            "numbers": nums,
            "result_digits": [int(ch) for ch in str(abs(signed_total))],
        }
