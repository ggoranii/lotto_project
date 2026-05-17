# 🎰 Django Lotto Project

Django와 Docker를 활용하여 개발한 6/45 로또 웹 서비스 프로젝트입니다.

일반 사용자는 복권 구매 및 당첨 확인 기능을 사용할 수 있으며, 관리자는 추첨 실행 및 판매 통계 기능을 관리할 수 있습니다.

---

# 📌 프로젝트 소개

본 프로젝트는 Django 기반의 웹 애플리케이션으로, 실제 로또 시스템과 유사한 기능을 구현하는 것을 목표로 개발되었습니다.

Docker Multi-Container 환경을 사용하여 서비스 환경을 구성하였으며, 사용자 기능과 관리자 기능을 분리하여 설계하였습니다.

---

# 🛠️ 개발 환경

| 항목 | 내용 |
|---|---|
| Backend | Django 4.2.7 |
| Language | Python 3.11 |
| Database | SQLite3 |
| Container | Docker |
| Orchestration | Docker Compose |
| Frontend | HTML, CSS |
| Version Control | GitHub |

---

# 📂 프로젝트 구조

```bash
lotto_project/
├── accounts/
├── lotto/
├── config/
├── templates/
├── static/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

# 👤 사용자 기능

## ✅ 회원 기능
- 회원가입
- 로그인
- 로그아웃

---

## 🎫 복권 구매 기능

### 자동 번호 구매
- 랜덤 번호 자동 생성
- 1~45 숫자 중 중복 없이 생성

### 수동 번호 구매
- 사용자가 직접 번호 입력
- 번호 유효성 검사 수행

---

## 📋 구매 내역 조회
- 사용자의 구매 기록 확인
- 회차별 결과 확인 가능

---

## 🏆 당첨 결과 확인
- 당첨 번호 확인
- 등수 확인

---

# 👨‍💼 관리자 기능

## 🎲 추첨 실행
- 회차별 추첨 진행
- 당첨번호 자동 생성

---

## 📊 판매 내역 확인
- 전체 판매량 조회
- 자동/수동 구매 통계
- 사용자별 구매량 확인

---

## 🏅 당첨자 확인
- 회차별 당첨자 조회
- 등수별 결과 확인

---

# 🗄️ 데이터베이스 구조

## LottoDrawing
추첨 회차 정보를 저장하는 모델

| 필드명 | 설명 |
|---|---|
| round_no | 회차 번호 |
| num1~num6 | 당첨 번호 |
| bonus | 보너스 번호 |
| draw_date | 추첨 날짜 |

---

## LottoTicket
사용자 복권 구매 정보를 저장하는 모델

| 필드명 | 설명 |
|---|---|
| user | 구매 사용자 |
| num1~num6 | 구매 번호 |
| purchase_type | 자동/수동 |
| purchase_date | 구매 날짜 |
| drawing | 연결 회차 |
| rank | 당첨 등수 |

---

# ⚙️ 실행 방법

## 1️⃣ 프로젝트 Clone

```bash
git clone https://github.com/ggoranii/lotto_project.git
cd lotto_project
```

---

## 2️⃣ Docker 실행

```bash
docker-compose up --build
```

---

## 3️⃣ Django Migration

```bash
docker-compose exec web python manage.py migrate
```

---

## 4️⃣ 관리자 계정 생성

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 5️⃣ 서버 접속

```text
http://localhost:8000
```

관리자 페이지:

```text
http://localhost:8000/admin
```

---

# 🧩 주요 구현 기능

## 🎲 자동 번호 생성 알고리즘

```python
import random

def generate_auto_numbers():
    return sorted(random.sample(range(1, 46), 6))
```

---

## 🏆 당첨 판정 알고리즘

| 조건 | 등수 |
|---|---|
| 6개 일치 | 1등 |
| 5개 + 보너스 | 2등 |
| 5개 일치 | 3등 |
| 4개 일치 | 4등 |
| 3개 일치 | 5등 |

---

# 🐳 Docker 구성

본 프로젝트는 Docker Multi-Container 환경으로 구성되었습니다.

## 구성 요소
- Django Web Container
- Database Container
- Nginx Container

---

# 🚨 문제 해결 과정

## NoReverseMatch 오류 해결

### 문제
```text
Reverse for 'admin_drawing' not found
```

### 원인
`urls.py`에 관리자 URL 등록이 누락됨

### 해결
```python
path('manage/drawing/', views.admin_drawing, name='admin_drawing')
```

---

## Django Admin URL 충돌 해결

### 문제
`/admin/drawing/` 경로가 Django Admin과 충돌

### 해결
관리자 커스텀 URL을 `/manage/`로 변경

---

# 🧪 테스트 결과

| 테스트 항목 | 결과 |
|---|---|
| 회원가입 | 성공 |
| 로그인 | 성공 |
| 자동 구매 | 성공 |
| 수동 구매 | 성공 |
| 추첨 기능 | 성공 |
| 판매 통계 | 성공 |
| Docker 실행 | 성공 |

---

# 🔗 GitHub Repository

https://github.com/ggoranii/lotto_project

---

# 📌 향후 개선 사항

- PostgreSQL 적용
- Redis 캐시 서버 추가
- REST API 개발
- 반응형 UI 개선
- Kubernetes 배포 환경 구축

---

# 👨‍💻 개발자

- GitHub: https://github.com/ggoranii

---
