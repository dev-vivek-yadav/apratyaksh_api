class GanitaService:

    @staticmethod
    def _num_to_digits(n: int):
        return [ord(ch) - 48 for ch in str(n)]

    @staticmethod
    def _pad_left(s: str, width: int):
        return " " * (width - len(s)) + s

    def add(self, nums):
        digits_list = [self._num_to_digits(abs(int(n))) for n in nums]
        max_len = max(len(d) for d in digits_list)
        stacked_lines = [self._pad_left(''.join(str(d) for d in dlist), max_len) for dlist in digits_list]
        separator = "-" * max_len
        stacked = "\n".join(stacked_lines + [separator])
        rev_digits = [d[::-1] for d in digits_list]
        steps = []
        result_digits = []
        carry = 0
        for i in range(max_len):
            col = []
            for rd in rev_digits:
                col.append(rd[i] if i < len(rd) else 0)
            total = 0
            for d in col:
                for _ in range(d):
                    total += 1
            for _ in range(carry):
                total += 1

            digit = total % 10
            new_carry = total // 10

            place_name = f"Place {10**i}" if i < 6 else f"10^{i}"
            steps.append(
                f"{place_name}: digits {col} + Last carry({carry}) = {total} → digit={digit}, new carry={new_carry}"
            )

            result_digits.append(str(digit))
            carry = new_carry

        if carry:
            while carry > 0:
                result_digits.append(str(carry % 10))
                carry //= 10
            steps.append("Carry added to the remaining places.")

        result_str = "".join(result_digits[::-1])
        return {
            'sum': int(result_str),
            'steps': steps,
            'stacked': stacked,
            'numbers': nums,
            'result_digits': [int(ch) for ch in result_str]
        }

    def subtract(self, nums):
        # Convert numbers to int
        nums = [int(n) for n in nums]

        # Find the actual result first (for sign correction)
        final_difference = nums[0] - sum(nums[1:])

        # Work with absolute values for digit-by-digit steps
        max_num = max(abs(n) for n in nums)
        max_len = len(str(max_num))

        # Create stacked representation
        stacked_lines = [self._pad_left(str(abs(n)), max_len) for n in nums]
        separator = "-" * max_len
        stacked = "\n".join(stacked_lines + [separator])

        # Reverse digits for column-wise subtraction
        rev_digits = [[int(d) for d in str(abs(n))[::-1]] for n in nums]

        result_digits = rev_digits[0][:]
        steps = []

        # Sequential subtraction
        for idx, sub_digits in enumerate(rev_digits[1:], start=1):
            borrow = 0
            new_result = []

            for i in range(max_len):
                d1 = result_digits[i] if i < len(result_digits) else 0
                d2 = sub_digits[i] if i < len(sub_digits) else 0

                effective = d1 - borrow
                step_info = f"{['Ones','Tens','Hundreds','Thousands'][i] if i < 4 else f'10^{i}'} place: "

                if effective < d2:
                    effective += 10
                    borrow = 1
                    step_info += f"borrow needed → ({d1}-previous borrow) = {effective-10}, adjust to {effective}, then {effective} - {d2} = {effective - d2}"
                else:
                    borrow = 0
                    step_info += f"({d1}-previous borrow) = {effective}, then {effective} - {d2} = {effective - d2}"

                digit = effective - d2
                new_result.append(digit)
                steps.append(step_info)

            result_digits = new_result

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        return {
            "difference": final_difference,
            "steps": steps,
            "stacked": stacked,
            "numbers": nums,
            "result_digits": [int(ch) for ch in str(abs(final_difference))]
        }

    def urdhva_tiryagbhyam(self,a: int, b: int) -> dict:
        """
        Multiply two integers using the Vedic 'Vertical & Crosswise' method,
        storing each step (including carries) in a dictionary.
        Returns a dictionary containing the steps and the final product.
        """
        orig_a, orig_b = a, b

        # Handle sign first
        sign = 1
        if a < 0:
            sign *= -1
            a = -a
        if b < 0:
            sign *= -1
            b = -b

        # Split into digits (least-significant first)
        A = [int(ch) for ch in str(a)][::-1]
        B = [int(ch) for ch in str(b)][::-1]
        n, m = len(A), len(B)

        steps = []
        carry = 0
        out_digits = []

        # There are (n + m - 1) diagonals/steps
        for k in range(n + m - 1):
            # Collect digit-pairs that lie on the k-th diagonal (from the right)
            pairs = []
            s = 0
            # i is index in A, j in B, both from LSD (right) side
            i_min = max(0, k - (m - 1))
            i_max = min(k, n - 1)
            for i in range(i_min, i_max + 1):
                j = k - i
                da, db = A[i], B[j]
                pairs.append((da, db))
                s += da * db

            # Describe step type (single product = vertical, multiple = crosswise)
            step_type = "Vertical" if len(pairs) == 1 else "Crosswise"

            total = s + carry
            digit = total % 10
            new_carry = total // 10

            products_str = " + ".join(f"{da}×{db}" for da, db in pairs)
            step_info = {
                "step_num": k + 1,
                "step_type": step_type,
                "products": products_str,
                "carry_in": carry,
                "total": total,
                "digit": digit,
                "carry_out": new_carry
            }
            steps.append(step_info)

            out_digits.append(digit)
            carry = new_carry

        # Flush any remaining carry
        step_num = n + m
        while carry > 0:
            digit = carry % 10
            next_carry = carry // 10
            step_info = {
                "step_num": step_num,
                "step_type": "Final carry",
                "products": None,
                "carry_in": carry,
                "total": carry,
                "digit": digit,
                "carry_out": next_carry
            }
            steps.append(step_info)

            out_digits.append(digit)
            carry = next_carry
            step_num += 1

        # Build final number
        result = int("".join(str(d) for d in reversed(out_digits))) * sign
        return {
            "multiplicand": orig_a,
            "multiplier": orig_b,
            "steps": steps,
            "result": result
        }


    def ekadhikena_purvena(self, n: int) -> dict:
        """
        Square of numbers ending with 9 using the Vedic 'Ekadhikena Purvena' sutra.
        Stores step-by-step explanation in a dictionary.
        """
        if str(n)[-1] != "5":
            return {
                "number": n,
                "error": "This sutra applies best to numbers ending with 5."
            }

        orig_n = n
        prefix = int(str(n)[:-1])  # all digits except last
        last_digit = 5

        # Step 1: multiply prefix with one more than itself
        step1 = prefix * (prefix + 1)

        # Step 2: suffix is always 9^2 = 81
        step2 = last_digit * last_digit

        # Combine results
        result = int(f"{step1}{step2}")

        return {
            "number": orig_n,
            "steps": [
                {
                    "step": 1,
                    "description": f"Take prefix {prefix} and multiply by one more than itself ({prefix+1}).",
                    "calculation": f"{prefix} × {prefix+1} = {step1}"
                },
                {
                    "step": 2,
                    "description": "Square of 5 is 25 (fixed suffix).",
                    "calculation": "5 × 5 = 25"
                },
                {
                    "step": 3,
                    "description": "Join the results of step 1 and step 2.",
                    "calculation": f"{step1} || 25 = {result}"
                }
            ],
            "result": result
        }

    def nikhilam_navatashcaramam_dashatah(self, a: int, b: int) -> dict:
        orig_a, orig_b = a, b
        if a>b:
            a,b = b,a
        return {
            "a": a,
            "b": b,
        }




        # Choose nearest base (10, 100, 1000...)
        max_len = max(len(str(abs(a))), len(str(abs(b))))
        base = 10 ** max_len

        # Deficiencies (how much less than base)
        da = a - base
        db = b - base

        # Step 1: Cross addition/subtraction
        left = a + db  # or b + da

        # Step 2: Multiply deficiencies
        right = da * db

        width = len(str(base))
        right_str = str(right).zfill(width)

        result = int(f"{left}{right_str}")

        return {
            "multiplicand": orig_a,
            "multiplier": orig_b,
            "base": base,
            "steps": [
                {
                    "step": 1,
                    "description": f"Nearest base is {base}.",
                    "calculation": f"Base = {base}"
                },
                {
                    "step": 2,
                    "description": f"Find deficiencies from base.",
                    "calculation": f"{a} − {base} = {da},  {b} − {base} = {db}"
                },
                {
                    "step": 3,
                    "description": "Cross subtract one deficiency.",
                    "calculation": f"{a} + ({db}) = {left}  OR  {b} + ({da}) = {left}"
                },
                {
                    "step": 4,
                    "description": "Multiply the deficiencies.",
                    "calculation": f"{da} × {db} = {right}"
                },
                {
                    "step": 5,
                    "description": "Combine left and right parts.",
                    "calculation": f"{left} || {right_str} = {result}"
                }
            ],
            "result": result
        }


