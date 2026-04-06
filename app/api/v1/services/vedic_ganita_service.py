from .vedic_math.vedic_addition_service import VedicAdditionService
from .vedic_math.vedic_multiplication_service import VedicUrdhvaTiryagbhyamService
from .vedic_math.vedic_subtraction_service import VedicSubtractionService


class VedicGanitaService:
    def __init__(self):
        self._addition = VedicAdditionService()
        self._subtraction = VedicSubtractionService()
        self._multiplication = VedicUrdhvaTiryagbhyamService()

    def add(self, nums):
        return self._addition.calculate(nums)

    def subtract(self, nums):
        return self._subtraction.calculate(nums)

    def urdhva_tiryagbhyam(self, a: int, b: int) -> dict:
        return self._multiplication.calculate(a, b)

    def multiplication(self, a: int, b: int) -> dict:
        return self._multiplication.calculate(a, b)

    def ekadhikena_purvena(self, n: int) -> dict:
        if str(n)[-1] != "5":
            return {
                "number": n,
                "error": "This sutra applies best to numbers ending with 5.",
            }

        prefix = int(str(n)[:-1])
        step1 = prefix * (prefix + 1)
        result = int(f"{step1}25")

        return {
            "number": n,
            "steps": [
                {
                    "step": 1,
                    "description": f"Take prefix {prefix} and multiply by one more ({prefix + 1}).",
                    "calculation": f"{prefix} x {prefix + 1} = {step1}",
                },
                {
                    "step": 2,
                    "description": "Append 25 as fixed suffix for numbers ending in 5.",
                    "calculation": f"{step1} || 25 = {result}",
                },
            ],
            "result": result,
        }

    def nikhilam_navatashcaramam_dashatah(self, a: int, b: int) -> dict:
        orig_a, orig_b = a, b
        max_len = max(len(str(abs(a))), len(str(abs(b))))
        base = 10 ** max_len

        da = a - base
        db = b - base
        left = a + db
        right = da * db
        right_str = str(abs(right)).zfill(max_len)
        right_display = f"-{right_str}" if right < 0 else right_str
        result = left * base + right

        return {
            "multiplicand": orig_a,
            "multiplier": orig_b,
            "base": base,
            "steps": [
                {
                    "step": 1,
                    "description": f"Nearest base is {base}.",
                    "calculation": f"Base = {base}",
                },
                {
                    "step": 2,
                    "description": "Find deviations from base.",
                    "calculation": f"{a} - {base} = {da}, {b} - {base} = {db}",
                },
                {
                    "step": 3,
                    "description": "Cross adjust to get left part.",
                    "calculation": f"{a} + ({db}) = {left}",
                },
                {
                    "step": 4,
                    "description": "Multiply deviations to get right part.",
                    "calculation": f"{da} x {db} = {right}",
                },
                {
                    "step": 5,
                    "description": "Join left and right parts.",
                    "calculation": f"({left} x {base}) + ({right_display}) = {result}",
                },
            ],
            "result": result,
        }
