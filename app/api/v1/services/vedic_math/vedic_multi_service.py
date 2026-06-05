from fastapi import HTTPException

from .vedic_urdhva_multiplication_service import VedicUrdhvaTirService
from .vedic_add_service import VedicAdditionCopyService
from .vedic_subct_service import VedicSubctService


class VedicMultiService:

    def __init__(self):
        self._multiplication = VedicUrdhvaTirService()
        self._addition = VedicAdditionCopyService()
        self._subtraction = VedicSubctService()

    def mul(self,nums):
        return self._multiplication.calculate(a=nums[0],b=nums[1])
    
    def add_nested_steps(self,cal_type,title,data):
        result={
            "type": cal_type,
            "title":title,
        }

        if cal_type == "addition":
            result["add"]=data
        elif cal_type == "subtraction":
            result["sub"]=data
        else:
            result["mul"]=data
        
        return result

    def calculate(self,numbers):
        # print(f"Calculating product of: {numbers}")
        num_str=[]
        for n in numbers:
            num_str.append(str(n))
        
        print(f"Calculating product of: {num_str}")
        
        counter=1
        total=num_str[0]
        steps=[]
        for i in range(1,len(num_str)):
            num1_str=str(total)
            num2_str=num_str[i]

            steps.append(f"<span class='font-bold text-blue-700 text-lg'>Multiplying {num1_str} * {num2_str}</span>")
            max_value = max(
                        int(num1_str),
                        int(num2_str)
                    )

            max_len=max(len(num1_str),len(num2_str))
            num1_str=num1_str.zfill(max_len)
            num2_str=num2_str.zfill(max_len)

            theoretical_base=0

            if max_len==1:
                theoretical_base=10
            else:
                theoretical_base=10**(max_len-1)

            print(f"theoretical_base={theoretical_base}")

            zero_digit_count=len(str(theoretical_base)) - 1  #ye use hoga rhs me ki theoritical me kitne zero hai utne hi

            print(f"zero_digit_count={zero_digit_count}")
           

            multipliers=range(1,11)

            base=[]

            for m in multipliers:
                value=theoretical_base*m
                base.append(value)
            print(f"base={base}")

            def working_base_closeness(base):
                return abs(max_value-base)
            
            working_base=min(base,key=working_base_closeness)

            factor=working_base//theoretical_base
            print(f"working_base={working_base} factor={factor}")


            steps.append(
                f"<span class='font-bold text-blue-700'>Base Selection:</span>"
                
                # f"<span class='font-bold text-blue-700'>"
                # f"Determine the base by taking the higher value among the two numbers."
                # f"</span>"
                
                # f"<span class='font-bold text-blue-700'>"
                # f"Larger operand base family gives:</span> "
                
                f"<span class='font-bold text-blue-700'> Theoretical Base </span> = {theoretical_base}, "
                f"<span class='font-bold text-blue-700'>Working Base </span> = {working_base}"
            )
       

            if factor == 1:
                steps.append(f"<span class='font-bold text-blue-700'>Step {counter}:working base is same as theoretical base.</span>")
                counter+=1
            else:
                steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: working base </span>  {theoretical_base} x {factor}")
                counter += 1

            complement1=int(num1_str)-working_base
            complement2=int(num2_str)-working_base

            steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: complements:</span>{num1_str} - {working_base} = {complement1}, {num2_str} - {working_base} = {complement2}")

            counter+=1

            steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: L.H.S. Methods: </span>")
            counter+=1

            if complement1 >= 0:
                op1 = "+"
                cross_sub_add2 = int(num2_str) + complement1
            else:
                op1 = "-"
                cross_sub_add2 = int(num2_str) - abs(complement1)


            if complement2 >= 0:
                op2 = "+"
                cross_sub_add1 = int(num1_str) + complement2
            else:
                op2 = "-"
                cross_sub_add1 = int(num1_str) - abs(complement2)

            nums1 = [int(num1_str), abs(complement2)]
            nums2 = [int(num2_str), abs(complement1)]


            service1=self._addition if op2 == "+" else self._subtraction
            service2=self._addition if op1 == "+" else self._subtraction

            add_sub1=service1.calculate(nums1)
            add_sub2=service2.calculate(nums2)


            steps.append(
                f"<span class='font-bold text-blue-700'>&nbsp;&nbsp;Method 1 (Cross Subtraction & Addition): </span> "
                f"{num1_str} {op2} {abs(complement2)}"
            )
            # steps.append(add_sub1.get("steps", []))

            steps.append(
                self.add_nested_steps(
                    "addition" if op2 == "+" else "subtraction",
                    "add_details" if op2 == "+" else "sub_details",
                    add_sub1.get("steps", [])
                )
            )


            steps.append(
                f"<span class='font-bold text-blue-700'>&nbsp;&nbsp;Method 2 (Cross Subtraction & Addition): </span> "
                f"{num2_str} {op1} {abs(complement1)}"
            )
            # steps.append(add_sub2.get("steps", []))

            steps.append(
                self.add_nested_steps(
                    "addition" if op1 == "+" else "subtraction",
                    "add_details" if op1 == "+" else "sub_details",
                    add_sub2.get("steps", [])
                )
            )

            
            if factor == 1:
                steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: Adjusted L.H.S.</span> {cross_sub_add1}")
                counter+=1
            else:
                steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: Adjusted L.H.S. to theoretical base</span>:{cross_sub_add1} x {factor} ")
                counter+=1

                multiplywithurdhva=self.mul([cross_sub_add1,factor])
                steps.append(self.add_nested_steps("multiplication","multi_details",multiplywithurdhva.get("steps", [])))
                # steps.append(multiplywithurdhva)
            
            left_part=cross_sub_add1*factor



            # rhs starts


            steps.append(f"<span class='font-bold text-blue-700'>Step {counter}: R.H.S.:</span> ({complement1}) x ({complement2})")
            counter+=1

            multiplywithurdhva=self.mul([complement1,complement2])
            steps.append(self.add_nested_steps("multiplication","multi_details",multiplywithurdhva.get("steps", [])))
            # steps.append(multiplywithurdhva)


            right_part = complement1 * complement2

            if right_part > 0:
                    if right_part >= theoretical_base:
                        carry = right_part // theoretical_base   #quotent upar wala part yha par carry calculation isliye kar rahe hain ki agar rhs theoretical base se bada hai toh uske jitne bhi digits hai utne ko rhs me rakhna hai aur baaki ko lhs me carry karna hai
                        remainder = right_part % theoretical_base  # ye reminder ke liye hai yani ki jitna theoretical base me zero hoga utna last a digt nikalna hai right part se aur uske baaki jitne bhi digit bachege wo carry me add karna hai lhs me

                        steps.append(
                            f"<span class=' text-blue-700'>Step {counter} - Right-part rule:  theoretical base </span> {theoretical_base} <span class=' text-blue-700'>has </span> {zero_digit_count} <span class=' text-blue-700'>zero(s), so keep only last </span> {zero_digit_count} <span class=' text-blue-700'>digit(s) on RHS and carry the remaining part to LHS.</span>"
                            
                        )
                        counter+=1


                        steps.append(
                                f"<span class=' text-blue-700'>Step {counter} - LHS Carry Addition: </span> {left_part} + {carry} = {left_part + carry}"
                            )
                        
                        counter+=1

                        right_part = remainder   # ab yha par bacha hua jo hai wo rhs ban gaya 
                        left_part += carry  # and yha par carry ka addition ho rha hai lhs me
                        counter+=1
                    else:
                        # ye wala hai ki agr jaise ki theoritical base hai 100 and rhs aay 58 amd do digit hume trhs se chhodne hai but rhs already do hi digit ka hai toh koi carry nahi hoga aur rhs wahi rahega and lhs bhi same rahega
                        steps.append(
                                f"<span class=' text-blue-700'>Step {counter} - Right-part rule:  theoretical base </span> {theoretical_base} <span class=' text-blue-700'>has </span> {zero_digit_count} <span class=' text-blue-700'>zero(s), so RHS must keep exactly </span> {zero_digit_count} <span class=' text-blue-700'>digit(s). </span>"
                                f"<span class=' text-blue-700'>Since </span> {right_part} <span class=' text-blue-700'>already fits, carry = 0 and RHS = </span> {right_part:0{zero_digit_count}d}"
                            )
                        counter+=1
            else:
                #ye wala hai agr rhs negative aa rha hai toh hum usko positive me convert karenge aur uske corresponding base se subtract karenge aur usko rhs banayenge aur lhs me borrow karenge
                deficit = -right_part   # ye wala part hai ki agr value negative ho to usko positive banaa taki carrya nd remainer nikal
                borrow_blocks = deficit // theoretical_base
                remainder = deficit % theoretical_base
                steps.append(
                    f"<span class=' text-blue-700'>Step {counter} - Negative RHS rule:  RHS is </span> {right_part}.<span class=' text-blue-700'>Since RHS cannot be negative, Use real base </span> {theoretical_base}; <span class=' text-blue-700'>subtract |RHS| from base and borrow 1 from LHS. </span>"
                )

                counter+=1

                if remainder == 0:
                    #ye wala part agr rhs me value like base 100 hai and rhs me -200 aa rha hai toh iska matlab hai ki rhs me 2 block ka deficit hai aur remainder zero hai toh humko base se zero subtract karna hai aur borrow me 2 block borrow karna hai but rhs zero hai iskliye isko bse se minus nahi kar rhe hai bs bacha hua borrow lhs se minus karke comnind kar de rhe hain
                    right_part = 0
                    total_borrow = borrow_blocks
                    steps.append(
                        f"<span class=' text-blue-700'>Step {counter} - Exact base multiple deficit: </span> |RHS| = {deficit} = {borrow_blocks} x {theoretical_base},<span class=' text-blue-700'> so RHS </span> = {right_part}<span class=' text-blue-700'> and LHS borrow  </span> = {total_borrow}"
                    )
                    counter+=1
                else:
                    right_part = theoretical_base - remainder   # agr -minus me ho valuto to theoritical bse se reminer ko minus karte hai 
                    total_borrow = borrow_blocks + 1
                    steps.append(
                        f"<span class=' text-blue-700'> Step {counter} - Base subtraction: </span> {theoretical_base} - {remainder} = {right_part}; <span class=' text-blue-700'> Total LHS Borrow </span> = 1 + {borrow_blocks} = {total_borrow}"
                    )
                    counter+=1

                
                subtractons = self._subtraction.calculate(
                    [left_part, total_borrow]
                )

                steps.append(
                    f"<span class=' text-blue-700'>Step {counter} - LHS After Borrow:</span> {left_part} - {total_borrow} = {left_part - total_borrow}"
                )
                counter+=1

                steps.append(
                    self.add_nested_steps(
                        "subtraction",
                        "subtract_details",
                        subtractons.get("steps", [])
                    )
              )

                left_part -= total_borrow


            steps.append(f"<span class=' text-blue-700'>Step {counter} COMBINED LEFT AND RIGHT :</span> ({left_part}|{right_part})\n")
            counter+=1

            total=f"{left_part}{right_part}"
            steps.append(f"<span class='font-bold text-dark-700 text-xl'>OUTPUT: {total}</span>\n") 
        
        return {
            "steps": steps,
            "final_output": total
        }