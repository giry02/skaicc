# SK Broadband AICC 멀티모달 솔루션 연동 규격 요청서 (v1.0)

**수신**: ACP 솔루션 담당자 귀하
**발신**: SK Broadband AICC 멀티모달 개발팀
**날짜**: 2024.10.24

---

## 1. 개요 (Overview)
본 문서는 SK Broadband AICC 멀티모달(보이는 상담) 서비스의 고도화를 위해 필요한 **Web Client(화면)와 AICC Solution(음성/제어) 간의 연동 규격**을 정의합니다.
성공적인 '음성-화면 동기화' 경험을 위해 아래 명시된 항목들에 대한 기술 지원 및 API/Socket 인터페이스 제공을 요청합니다.

## 2. 핵심 연동 아키텍처 (Architecture)
*   **통신 방식**: **WebSocket** (선호) 또는 Server-Sent Events (SSE)
    *   *Note*: 실시간성(Latency < 200ms) 보장을 위해 Polling 방식은 지양합니다.
*   **데이터 포맷**: JSON

---

## 3. 상세 요구사항 (Technical Requirements)

### 3.1 Voice-Screen Interaction (음성-화면 상호작용)

| 항목 | 이벤트명(예시) | 설명 및 요구사항 |
| :--- | :--- | :--- |
| **VAD Status** | `SPEECH_START` / `END` | 고객 발화 시작/종료를 실시간 트리거로 전송. (화면 Listen 모드 전환용) |
| **Audio Level** | `AUDIO_LEVEL` | 고객 음성의 데시벨(dB) 스트림. (파동/Wave 애니메이션 구현용) |
| **Barge-in** | `BARGE_IN_DETECTED` | **[Critical]** 고객이 말을 끊었음(Interruption)을 알리는 신호. <br> 수신 즉시 클라이언트는 **재생 중인 TTS와 화면 애니메이션을 강제 중단**해야 함. |
| **Barge-in Info** | `BARGE_IN_METADATA` | TTS 재생 시작 후 몇 ms 시점에 끊겼는지(`offset_ms`) 정보 포함. (시나리오 최적화 분석용) |
| **Real-time STT**| `STT_PARTIAL_RESULT` | 완성된 문장이 아닌, **인식 중인 텍스트 스트림** 전송. <br> *활용: "요금..." -> "요금 납부..." 실시간 자막 표시* |

### 3.2 Contents Sync & Data Injection (동기화 및 데이터 주입)

| 항목 | 이벤트명(예시) | 설명 및 요구사항 |
| :--- | :--- | :--- |
| **TTS Sync** | `TTS_MARKER` | 오디오 스트림 내 특정 구간(Timestamp)에 대한 메타데이터 마커 포함. <br> *활용: TTS가 "버튼을 누르세요"라고 할 때 정확히 버튼 Highlight 처리.* |
| **Data Injection**| `DATA_PAYLOAD` | 상담 시나리오에 필요한 **개인화 데이터(JSON)**를 실시간 주입. <br> **[필수 데이터 예시 - 사용량 그래프]** <br> `{ "usage": { "prev": 120, "curr": 145 }, "bill": { "prev": 35000, "curr": 38500 } }` |
| **Graph Trigger** | `ANIMATE_GRAPH` | 봇의 발화 타이밍에 맞춰 그래프(Chart) 상승 애니메이션을 시작하라는 트리거 신호. |

### 3.3 Call Lifecycle (통화 생명주기) **[Critical]**

솔루션이 PBX(교환기) 내부에 위치함에 따라, 웹 클라이언트가 통화 상태를 독립적으로 인지할 수 없습니다. 따라서 아래 생명주기 이벤트를 명시적으로 전송해야 합니다.

*   **요청사항**: 교환기 단선(Hang-up) 시 **1초 이내**에 웹소켓 이벤트 전송.
*   **Event**: `CALL_ENDED`
*   **Payload**: `{ "reason": "user_hangup" | "system_error" | "normal_end" }`
*   **질의**: 현재 귀사 솔루션은 상위 교환기의 단선 신호를 **SIP BYE 패킷**으로 감지합니까, 아니면 **API 콜백** 방식입니까? (안정적인 감지 방식에 대한 확답 필요)

### 3.4 Bidirectional Interaction (양방향 소통)

*   **Touch-to-Voice**: 웹 화면의 버튼 클릭을 봇이 인지하고 음성으로 반응해야 함.
    *   *Interface*: `BotSDK.sendEvent("BUTTON_CLICKED", payload)` 형태의 SDK 함수 지원 필요.
*   **Secure Input**: PCI-DSS 준수를 위한 보안 키패드 모드 진입 커맨드 (`SECURE_INPUT_MODE`).
    *   해당 모드 진입 시 STT(마이크)는 차단되고, 입력값은 결제 모듈로 직접 전송되어야 함.

### 3.5 Context & Reliability (환경 및 안정성)

*   **Network Quality**: 클라이언트의 네트워크 상태(Weak Signal)를 감지하여 전송 (`NETWORK_QUALITY`).
    *   *활용*: 신호 약함 시, 고용량 리소스 로딩 중단 및 텍스트 위주 UI(Lite Mode)로 자동 전환.
*   **Session Restore**: 브라우저 재실행 시 `SESSION_ID`를 통해 기존 대화 컨텍스트 복구 지원.

---

## 4. 맺음말
위 요구사항은 SK브로드밴드의 차별화된 고객 경험을 위해 필수적인 항목들입니다.
기존 제공되는 API 명세서(ICD)와 본 요청사항 간의 차이점을 분석(Gap Analysis)하여,
**가능한 항목 / 커스터마이징 필요 항목 / 불가능 항목**을 구분해 회신 주시면 감사하겠습니다.

빠른 시일 내에 실무 미팅을 통해 구체적인 연동 방식을 협의하기를 희망합니다.
