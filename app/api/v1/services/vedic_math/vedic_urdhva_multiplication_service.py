class VedicUrdhvaTirService:
    def calculate(self, a: int, b: int) -> dict:
        orig_a, orig_b = a, b

        # 🔹 Sign handling
        sign = 1
        if a < 0:   # agr nuber negative ho to usko positive banane ke liye sign ko 
            sign *= -1
            a = -a
        if b < 0:
            sign *= -1
            b = -b   

        # 🔹 Equal length banane ke liye padding
        len_a = len(str(a))
        len_b = len(str(b))
        max_len = max(len_a, len_b)

        a_str = str(a).zfill(max_len)
        b_str = str(b).zfill(max_len)

        # 🔹 Reverse arrays   # number ko reverse karne ke liye agr 2,3 hai to 32 ho jaye
        A = [int(d) for d in a_str][::-1]
        B = [int(d) for d in b_str][::-1]

        n = max_len
        carry = 0
        out_digits = []
        steps = []

        for k in range(2 * n - 1):
            pairs = []
            partial_sum = 0

            i_min = max(0, k - (n - 1))
            i_max = min(k, n - 1)

            for i in range(i_min, i_max + 1):
                j = k - i
                da, db = A[i], B[j]
                pairs.append((da, db))
                partial_sum += da * db

            total = partial_sum + carry
            digit = total % 10
            new_carry = total // 10

            products_expr = " + ".join(f"({da} × {db})" for da, db in pairs)
            values_expr = " + ".join(str(da * db) for da, db in pairs)

            if carry > 0:
                values_expr += f" + carry {carry}"

            step_line = (
                f"({k + 1}) {products_expr} = {values_expr} = {total} "
                f"→ write {digit}, carry {new_carry}"
            )

            steps.append(step_line)

            out_digits.append(digit)
            carry = new_carry

        # 🔹 Remaining carry
        while carry > 0:
            digit = carry % 10
            steps.append(f"(carry) {carry} → write {digit}")
            out_digits.append(digit)
            carry //= 10

        result = int("".join(map(str, reversed(out_digits)))) * sign

        steps.append(f"Output: {result}")

        return {
            "SUTRA": "URDHVA-TIRYAGBHYAM",
            "multiplicand": a_str,  
            "multiplier": b_str,   
            "steps": steps,
        }