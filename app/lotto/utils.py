import random


def generate_auto_numbers():
    """1~45 중 서로 다른 6개 숫자를 오름차순으로 반환"""
    numbers = random.sample(range(1, 46), 6)
    return sorted(numbers)


def validate_manual_numbers(numbers):
    """수동 입력 번호 유효성 검증
    
    Args:
        numbers: 정수 리스트 [n1, n2, n3, n4, n5, n6]
    
    Returns:
        (bool, str): (유효 여부, 메시지)
    """
    # 개수 체크
    if len(numbers) != 6:
        return False, "6개의 숫자를 모두 선택해야 합니다."
    
    # 중복 체크
    if len(set(numbers)) != 6:
        return False, "중복된 숫자가 있습니다."
    
    # 범위 체크
    for n in numbers:
        if not isinstance(n, int):
            return False, "숫자만 입력 가능합니다."
        if not (1 <= n <= 45):
            return False, f"{n}은(는) 범위를 벗어났습니다. 1~45 사이의 숫자만 입력하세요."
    
    return True, "OK"