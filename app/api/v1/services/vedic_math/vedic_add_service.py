from fastapi import HTTPException

class VedicAdditionCopyService:
    def calculate(self, numbers):
        # 1. Sabhi inputs ko string mein convert karna
        nums = []
        for n in numbers:
            nums.append(str(n))
        
        print(f"Calculating sum of: {nums}")
        
        # # Validation
        # if len(nums) < 2:
        #     raise HTTPException(status_code=400, detail="Kam se kam do numbers hone chahiye.")

        # Sabse pehle number ko base running total banana
        running_total = int(nums[0])
        print(f"Initial number (base total): {running_total}")
        steps_log = []
        
        # 2. Index 1 se lekar baaki saare numbers par ek-ek karke loop chalana
        for idx in range(1, len(nums)):
            num1_str = str(running_total)
            num2_str = nums[idx]
            
            steps_log.append(f"<span class='font-bold text-blue-700 text-lg'>Adding {num1_str} + {num2_str}</span>")
            counter=1
            # Dono numbers ko barabar length ka banane ke liye zero-padding
            max_len = max(len(num1_str), len(num2_str))
            num1_str = num1_str.zfill(max_len)
            num2_str = num2_str.zfill(max_len)
            
            # Har naye number ke addition ke liye temporary subtotal fresh shuru hoga
            sub_running_total = 0
            
            # Left to Right Loop (Place value extraction)
            for i in range(max_len):
                power = max_len - 1 - i
                multiplier = 10 ** power
                
                val1 = int(num1_str[i]) * multiplier
                val2 = int(num2_str[i]) * multiplier
                
                place_sum = val1 + val2
                prev_sub_total = sub_running_total
                sub_running_total += place_sum
                
                # Step details save karna
                steps_log.append(f"<span class='font-bold text-blue-700'>Step {counter}: Place Value </span> {val1} + {val2} = {place_sum}")
                counter+=1
                if prev_sub_total > 0:  # ye isliye hai ki pehle se koi prev_sub_total nahi hota hai  0 hota hai
                   steps_log.append(f"<span class='font-bold text-blue-700'>Step {counter}: Total place values</span> {prev_sub_total} + {place_sum} = {sub_running_total}")
                   counter+=1
                
                
            
            # Ek step khatam hone par final subtotal ko main running_total bana dena
            running_total = sub_running_total
            if idx == len(nums) - 1:
                steps_log.append(f"<span class='font-bold text-dark-700 text-xl'>OUTPUT: {running_total}</span>\n")
            # steps_log.append(f"Result after Step {idx}: {running_total}\n")

        # 3. Final response data taiyar karna
        return {
            "input_numbers": nums,
            "steps": steps_log,
            "final_output": running_total
        }
        
