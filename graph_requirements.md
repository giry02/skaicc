# 실시간 데이터 연동 그래프 구현 요건 (Live Data Graph Specs)

사용자께서 요청하신 **'이전 달 대비 사용량 비교 그래프'** (참조: `giry02.dothome.co.kr`)를 AICC 환경에서 구현하기 위한 기술 명세입니다.

## 1. UI/UX 목표
*   상담사가 "이번 달 데이터 사용량은..." 이라고 말하는 순간,
*   화면의 그래프 막대가 애니메이션과 함께 상승하여 시각적 몰입도 제공.
*   **고려사항**: 폰트 크기 확대(Silver Mode)는 레이아웃 깨짐 방지를 위해 **'반응형 뷰포트(Viewport) 확대'** 방식이나 **'큰 글씨 전용 테마'**로 접근해야 함. (단순 CSS zoom 지양)

## 2. 데이터 연동 규격 (Data Specs)
솔루션에서 TTS와 함께 아래 메타데이터를 내려줘야 합니다.

### (1) 데이터 패킷 (JSON)
*   **시점**: 해당 시나리오 진입 시 (또는 상담 시작 시 미리 로드)
*   **구조**:
    ```json
    {
      "usage_data": {
        "prev_month": 120,  // 전월 사용량 (GB)
        "curr_month": 145,  // 당월 사용량 (GB)
        "limit": 200        // 요금제 한도
      },
      "bill_data": {
        "prev_bill": 35000,
        "curr_bill": 38500
      }
    }
    ```

### (2) 트리거 이벤트 (Trigger Event)
*   **목적**: "말하는 타이밍"에 맞춰 그래프를 움직이게 함.
*   **방식**: TTS 스트림 내 시간 정보(Time Marker) 또는 별도 소켓 이벤트.
    *   `Event: ANIMATE_GRAPH_USAGE` (사용량 그래프 시작)
    *   `Event: ANIMATE_GRAPH_BILL` (요금 그래프 시작)

## 3. 솔루션 요청 사항 (To Solution Provider)
> "화면의 그래프는 더미(Dummy) 이미지가 아니라, 고객의 실제 데이터를 반영해야 합니다. 상담 중 **실시간으로 개인화 데이터(Personalized Data)**를 던져줄 수 있는 API 인터페이스를 열어주십시오."
