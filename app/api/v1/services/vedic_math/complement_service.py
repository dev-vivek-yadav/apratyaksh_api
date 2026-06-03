from winsound import MB_ICONQUESTION


class ComplementService:

    def calculate_complement(self, num1, num2):

        print(f"Calculating complement of {num1} and {num2}")

        first_num = int(num1)
        second_num = int(num2)

        steps = []

        num1_str = str(first_num)
        num2_str = str(second_num)



        zero_count = len(num1_str) - 1

        # Jitne zero base me hain utne hi digits lenge
        real_calc_digit = num2_str[-zero_count:]
        
        # Agar digits kam hain to left padding
        real_calc_digit = real_calc_digit.zfill(zero_count)
        result = ""
        counter = 1

        

        for idx in range(len(real_calc_digit)):

            digit = int(real_calc_digit[idx])

            # Last digit -> subtract from 10
            if idx == len(real_calc_digit) - 1:
                value = 10 - digit

                steps.append(
                    f"<span class='font-bold text-blue-700'>Step {counter}:</span> "
                    f"10 - {digit} = {value}"
                )
            else:
                value = 9 - digit

                steps.append(
                    f"<span class='font-bold text-blue-700'>Step {counter}:</span> "
                    f"9 - {digit} = {value}"
                )

            result += str(value)
            counter += 1

        complement = int(result)

        steps.append(
            f"<span class='font-bold text-green-700'>Complement = {complement}</span>"
        )

        return {
            "steps": steps,
            "final_output": complement
        }