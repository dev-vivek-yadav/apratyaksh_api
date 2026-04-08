# from .vedic_addition_service import VedicAdditionService
from .vedic_urdhva_multiplication_service import VedicUrdhvaTirService

class VedicUrdhvaTiryagbhyamService:

    # def __init__(self):
    #     self._addition = VedicAdditionService()

    def __init__(self):
        self._addition = VedicUrdhvaTirService()

    def mul(self,nums):
        return self._addition.calculate(a=nums[0],b=nums[1])

    # def add(self, nums):
    #     return self._addition.calculate(nums)

    def _select_bases(self, a: int, b: int):
        # Use larger operand as the anchor, as shown in mixed-size examples.
        anchor = max(a, b)
        digits = len(str(anchor))
        theoretical_base = 10 if digits == 1 else 10 ** (digits - 1)

        multipliers = range(1, 11)
        working_base = min(
            (theoretical_base * m for m in multipliers),
            key=lambda base: abs(anchor - base),
        )
        factor = working_base // theoretical_base
        return theoretical_base, working_base, factor

    def calculate(self, a: int, b: int) -> dict:
        orig_a, orig_b = a, b

        sign = 1
        if a < 0:
            sign *= -1
            a = -a
        if b < 0:
            sign *= -1
            b = -b

        steps = []

        theoretical_base, working_base, factor = self._select_bases(a, b)
        n = len(str(theoretical_base)) - 1

        dev_a = a - working_base
        dev_b = b - working_base

        sign_a = "+" if dev_a >= 0 else ""
        sign_b = "+" if dev_b >= 0 else ""

        steps.append(
            f"Step 1 - Determine the base by taking the higher value among the two numbers"

                f" 1.1 Base Selection: Larger operand base family gives theoretical base = {theoretical_base}, working base = {working_base}"

        )

        if factor == 1:
            steps.append("Step 2 - Base Factor: Working base equals theoretical base")
        else:
            steps.append(
                f"Step 2 - Base Factor: working base = {theoretical_base} x {factor}"
            )

        steps.append(
            f"Step 3 - Complement: {a} - {working_base} = {sign_a}{dev_a}, "
            f"{b} - {working_base} = {sign_b}{dev_b}"
        )
        
        # add_number=self.add([a,b])
        # print(add_number)
        
        # print(multiplywithurdhva)
        cross_left = a + dev_b
        cross_left = a + dev_b
        alt_cross_left = b + dev_a
        lhs_via_sum = (a + b) - working_base
        lhs_via_base_complements = working_base + dev_a + dev_b
        adjusted_left = cross_left * factor

        op_with_b_comp = "-" if dev_b < 0 else "+"
        op_with_a_comp = "-" if dev_a < 0 else "+"

        steps.append("Step 4 - L.H.S. (4 Methods):")
        steps.append(
            f"(1) Cross subtraction/addition: {a} {op_with_b_comp} {abs(dev_b):0{n}d} = {cross_left}"
        )
        steps.append(
            f"(2) Cross subtraction/addition: {b} {op_with_a_comp} {abs(dev_a):0{n}d} = {alt_cross_left}"
        )
        steps.append(
            f"(3) Add numbers then subtract working base: ({a} + {b}) - {working_base} = {lhs_via_sum}"
        )
        # steps.append(add_number)
        steps.append(
            f"(4) Working base with complements: {working_base} + ({sign_a}{dev_a}) + ({sign_b}{dev_b}) = {lhs_via_base_complements}"
        )
        steps.append(f"Step 5 - Raw L.H.S. = {cross_left}")

        if factor == 1:
            steps.append(f"Step 6 - Adjusted L.H.S. = {adjusted_left}")
        else:
            multiplywithurdhva=self.mul([cross_left,factor])
            steps.append(
                f"Step 6 - Adjusted L.H.S. to theoretical base: {cross_left} x {factor}"
            )
            steps.append(multiplywithurdhva)

        right_product = dev_a * dev_b
        steps.append(
            f"Step 7 - R.H.S.: ({sign_a}{dev_a}) x ({sign_b}{dev_b})"
        )
        multiply7steps=self.mul([dev_a,dev_b])
        steps.append(multiply7steps)


        left_part = adjusted_left
        right_part = right_product

        if right_part >= theoretical_base:
            carry = right_part // theoretical_base
            remainder = right_part % theoretical_base

            steps.append(
                f"Step 8 - Right-part rule: theoretical base {theoretical_base} has {n} zero(s), so keep only last {n} digit(s) on RHS and carry the remaining part to LHS."
                
            )

            steps.append(
                f"Step 9 - Carry Addition: {left_part} + {carry} = {left_part + carry}"
            )

            right_part = remainder
            left_part += carry

            steps.append(
                f"Step 10 - Normalized: Left = {left_part}, Right = {right_part:0{n}d}"
            )
        elif right_part < 0:
            deficit = -right_part
            borrow_blocks = deficit // theoretical_base
            remainder = deficit % theoretical_base

            steps.append(
                f"Step 8 - Negative RHS rule: RHS is {right_part}.Since RHS cannot be negative, Use real base {theoretical_base}; subtract |RHS| from base and borrow 1 from LHS."
            )

            if remainder == 0:
                right_part = 0
                total_borrow = borrow_blocks
                steps.append(
                    f"Step 9 - Exact base multiple deficit: |RHS| = {deficit} = {borrow_blocks} x {theoretical_base}, so RHS = {right_part:0{n}d} and LHS borrow = {total_borrow}"
                )
            else:
                right_part = theoretical_base - remainder
                total_borrow = borrow_blocks + 1
                steps.append(
                    f"Step 9 - Base subtraction: {theoretical_base} - {remainder} = {right_part:0{n}d}; total LHS borrow = 1 + {borrow_blocks} = {total_borrow}"
                )

            steps.append(
                f"Step 10 - LHS after borrow: {left_part} - {total_borrow} = {left_part - total_borrow}"
            )
            left_part -= total_borrow
        else:
            steps.append(
                f"Step 8 - Right-part rule: theoretical base {theoretical_base} has {n} zero(s), so RHS must keep exactly {n} digit(s). "
                f"Since {right_part} already fits, carry = 0 and RHS = {right_part:0{n}d}"
            )

        unsigned_result = (left_part * theoretical_base) + right_part
        steps.append(
            f"Step 11 - Combine: ({left_part} | {right_part:0{n}d}) = {unsigned_result}"
        )

        result = unsigned_result * sign

        if sign < 0:
            steps.append("Step 12 - Apply sign adjustment")

        steps.append(f"Final Answer: {result}")

        return {
            "multiplicand": orig_a,
            "multiplier": orig_b,
            "steps": steps,
            "result": result,
        }