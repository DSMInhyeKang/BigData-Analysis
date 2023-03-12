#https://eknowhow.kr/적금이자-계산법-공식/

print("[대마뱅크]")
print("좌*익님, 자유적금이 만기되어 알려드립니다.")

principal = float(input("원금 : ").replace(',', ''))
monthly_amount = principal / 12

interest_rate = 0.024
interest_taxation_rate = 0.154
tax_free_interest = 0 
interest_taxation = 0
sum = 0

for i in reversed(range(1, 13)):
    tax_free_interest += int(monthly_amount * interest_rate * i / 12)

interest_taxation = int(tax_free_interest * interest_taxation_rate)
sum = int(principal) + tax_free_interest - interest_taxation

print(f'세전이자 : {tax_free_interest:,}원')
print(f'이자과세(15.4%) : {interest_taxation:,}원')
print(f'세후 수령액 : {sum:,}원')
