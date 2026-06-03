from fastapi import HTTPException

from .vedic_add_service import VedicAdditionCopyService
from .complement_service import ComplementService


class VedicSubctService:

    def __init__(self):
        self._complement_service = ComplementService()
        self._addition = VedicAdditionCopyService()

    def add_nested_steps(self,cal_type,title,data):
        result={
            "type": cal_type,
            "title":title,
        }

        if cal_type == "complement":
            result["complement"]=data
        else:
            result["add"]=data
        return result

    def _is_basenumber(self, num):
        number_str = str(num)

        return number_str.startswith("1") and set(number_str[1:]) == {"0"}

    def calculate(self, numbers):


        nums = [str(n) for n in numbers]

        first_num = int(nums[0])
        steps = []

        for i in range(1, len(nums)):

            num1_str = str(first_num)
            num2_str = nums[i]

            # Find bigger and smaller number
            isnegative= False
            if int(num1_str) > int(num2_str):
                bigger = num1_str
                smaller = num2_str
            else:
                bigger = num2_str
                smaller = num1_str
                isnegative = True

            # Check if bigger number is a base number
            if self._is_basenumber(bigger):

                zero_count = len(bigger) - 1

                #jitna zero hoga  utne hi digit smaller me hona chahaiye isliye ki hum last ke jitne digit se subtraction karenge utne hi digit ka result nikal ke uske aage jitne zero hai utne zero laga denge
                real_calc_digit = smaller[-zero_count:]


                # zero padding
                real_calc_digit = real_calc_digit.zfill(
                    zero_count
                )
                
                steps.append(
                    f"<span class='font-bold text-blue-700 text-lg'>Subtracting: {num1_str} - {num2_str}</span>"
                )

                result = ""
                counter = 1

                for idx in range(len(real_calc_digit)):

                    digit = int(real_calc_digit[idx])

                    # Last digit -> subtract from 10
                    if idx == len(real_calc_digit) - 1:
                        value = 10 - digit
                        steps.append(
                            f"<span class='font-bold text-blue-700'>Step</span> {counter}: 10 - {digit} = {value}"
                        )
                    else:
                        value = 9 - digit
                        steps.append(
                            f"<span class='font-bold text-blue-700'>Step</span> {counter}: 9 - {digit} = {value}"
                        )

                    counter += 1
                    result += str(value)

                # Update running total
                if isnegative:
                    first_num = -int(result)
                else:
                    first_num = int(result)

                
                if  len(nums) >2:

                     steps.append(f"<span class='font-bold text-blue-700'>After first subtraction: {first_num}</span>")

            else:
                steps.append(
                    f"<span class='font-bold text-blue-700 text-lg'>Subtracting: {num1_str} - {num2_str}</span>"
                )
                counter=1
                # Agar bigger number base number nahi hai, toh normal subtraction kar dena
                # first_num = int(num1_str) - int(num2_str)
                max_len=max(len(num1_str),len(num2_str))
                num1_str=num1_str.zfill(max_len)
                num2_str=num2_str.zfill(max_len)

                base=10**max_len
                complement=base-int(num2_str)
                complement_data = self._complement_service.calculate_complement(base, num2_str)
                steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: complement </span> {base}-{num2_str}")
                counter+=1

                steps.append(
                    self.add_nested_steps(
                        "complement",
                        "complement_details",
                        complement_data.get("steps",[])
                        )
                )


               
                minuend_result=int(num1_str)+complement

                addition = self._addition.calculate(
                    [num1_str, str(complement)]
                )

                steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: Adding complement to the minuend: </span> {num1_str} + {complement}")
                counter+=1

                steps.append(
                    self.add_nested_steps(
                        "addition",
                        "add_details",
                        addition.get("steps", [])
                    )
              )

                if minuend_result >= base:
                    first_num=minuend_result - base
                    steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: Since the sum after complement addition </span> {minuend_result} <span class='font-bold text-blue-700'>is greater than the base</span> {base}, <span class='font-bold text-blue-700'>subtract the base: </span>{minuend_result} - {base} = {first_num}")
                    
                    # steps.append(f"<span class='font-bold text-emerald-700 text-xl'>OUTPUT: {first_num}</span>")
                else:
                    first_num=minuend_result-base
                    steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: Since the sum after complement addition </span> {minuend_result} <span class='font-bold text-blue-700'>is smaller than the base</span> {base}, <span class='font-bold text-blue-700'>so subtract the intermediate result from the base: </span>{minuend_result} - {base} = {first_num}")

        steps.append(f"<span class='font-bold text-dark-700 text-xl'>OUTPUT: {first_num}</span>")


                



        return {
            "input_numbers": nums,
            "steps": steps,
            "final_output": first_num
        }