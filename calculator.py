def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b

def power(a, b):
    return a ** b

def modulo(a, b):
    if b == 0:
        raise ValueError("0으로 나머지를 구할 수 없습니다.")
    return a % b

def calculator():
    print("=== 간단한 계산기 ===")
    print("연산자: + - * / ** %")

    while True:
        expr = input("\n계산식을 입력하세요 (예: 3 + 5, 2 ** 8) 또는 'q'로 종료: ").strip()
        if expr.lower() == 'q':
            print("종료합니다.")
            break

        try:
            a, op, b = expr.split()
            a, b = float(a), float(b)

            if op == '+':
                result = add(a, b)
            elif op == '-':
                result = subtract(a, b)
            elif op == '*':
                result = multiply(a, b)
            elif op == '/':
                result = divide(a, b)
            elif op == '**':
                result = power(a, b)
            elif op == '%':
                result = modulo(a, b)
            else:
                print("지원하지 않는 연산자입니다.")
                continue

            print(f"결과: {result}")
        except ValueError as e:
            print(f"오류: {e}")
        except Exception:
            print("올바른 형식으로 입력해주세요. (예: 3 + 5)")

if __name__ == "__main__":
    calculator()
