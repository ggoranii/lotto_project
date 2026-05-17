import random


def generate_auto_numbers():
    """1~45 중 서로 다른 6개 숫자를 오름차순으로 반환"""
    numbers = random.sample(range(1, 46), 6)
    return sorted(numbers)


def validate_manual_numbers(numbers):
    """수동 입력 번호 유효성 검증"""
    if len(numbers) != 6:
        return False, "6개의 숫자를 모두 선택해야 합니다."
    if len(set(numbers)) != 6:
        return False, "중복된 숫자가 있습니다."
    for n in numbers:
        if not isinstance(n, int):
            return False, "숫자만 입력 가능합니다."
        if not (1 <= n <= 45):
            return False, f"{n}은(는) 범위를 벗어났습니다. 1~45 사이의 숫자만 입력하세요."
    return True, "OK"


def perform_drawing():
    """추첨 실행: 당첨번호 6개 + 보너스 1개 생성
    
    Returns:
        tuple: (당첨번호 리스트, 보너스 번호)
    """
    # 1~45 중 7개를 한 번에 뽑음 (서로 다른 숫자)
    numbers = random.sample(range(1, 46), 7)
    winning_numbers = sorted(numbers[:6])  # 앞 6개를 당첨번호로
    bonus_number = numbers[6]  # 마지막 1개를 보너스로
    return winning_numbers, bonus_number


def check_rank(ticket_numbers, winning_numbers, bonus_number):
    """티켓의 등수 판정
    
    Args:
        ticket_numbers: 티켓의 6개 번호 (리스트)
        winning_numbers: 당첨 번호 6개 (리스트)
        bonus_number: 보너스 번호 1개 (정수)
    
    Returns:
        int or None: 등수 (1~5) 또는 None (낙첨)
    """
    ticket_set = set(ticket_numbers)
    winning_set = set(winning_numbers)
    
    match_count = len(ticket_set & winning_set)  # 일치하는 번호 개수
    has_bonus = bonus_number in ticket_set       # 보너스 일치 여부
    
    if match_count == 6:
        return 1  # 1등: 6개 모두 일치
    elif match_count == 5 and has_bonus:
        return 2  # 2등: 5개 + 보너스
    elif match_count == 5:
        return 3  # 3등: 5개 일치
    elif match_count == 4:
        return 4  # 4등: 4개 일치
    elif match_count == 3:
        return 5  # 5등: 3개 일치
    else:
        return None  # 낙첨