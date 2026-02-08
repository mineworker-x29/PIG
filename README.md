# PIG (Process Intelligence Graph) MVP

## 프로젝트 목표
각종 데이터와 이벤트 로그를 **Object-Centric Event Log(OCEL)** 형태로 변환한 뒤, Process Intelligence Graph(PIG)를 생성하고, 이를 LLM의 컨텍스트 레이어(Information Layer)로 활용 가능한지 검증한다.

## MVP 명세

### 1) 범위 (In Scope)
- 원천 데이터/로그 입력 디렉터리(`data/raw`)를 받는다.
- MVP 파이프라인 실행 시, 기본 event log/OCEL을 로드해 OC-DFG(`data/processed/oc_dfg.json`)와 기본 레포트(`data/processed/basic_report.md`)를 생성한다.
- CLI 엔트리포인트(`pig`)를 통해 최소 실행 경로를 제공한다.

### 2) 비범위 (Out of Scope)
- 실제 프로덕션 데이터 커넥터(ERP, DB, SaaS API) 연동
- 고급 프로세스 마이닝 알고리즘 및 대규모 그래프 최적화
- LLM 서빙/추론 파이프라인 통합

### 3) MVP 완료 기준 (Definition of Done)
- `scripts/bootstrap.sh`로 로컬 실행 환경이 구성된다.
- `scripts/run.sh` 또는 `make run`으로 OC-DFG/기본 레포트가 생성된다.
- README의 실행 절차만으로 신규 개발자가 5분 내 실행 가능하다.

## 프로젝트 구조

```text
.
├─ data/
│  ├─ raw/               # 원천 로그/데이터 입력 위치
│  └─ processed/         # 파이프라인 산출물
├─ scripts/
│  ├─ bootstrap.sh       # 가상환경 + 로컬 설치
│  └─ run.sh             # 기본 실행 스크립트
├─ src/pig/
│  ├─ main.py            # CLI 엔트리포인트
│  └─ pipeline.py        # 기본 데이터 로드 + OC-DFG/리포트 생성
├─ Makefile
└─ pyproject.toml
```

## 빠른 시작

### 방법 A) 스크립트 사용
```bash
./scripts/bootstrap.sh
./scripts/run.sh
```

### 방법 B) Make 사용
```bash
make setup
make run
```

실행 후 생성 파일:
- `data/processed/oc_dfg.json`
- `data/processed/basic_report.md`

## 다음 단계 제안
- 원천 시스템별 파서 모듈 추가 (`src/pig/connectors/*`)
- OCEL 검증 스키마/테스트 추가
- 그래프 생성 및 질의 API 레이어 설계
