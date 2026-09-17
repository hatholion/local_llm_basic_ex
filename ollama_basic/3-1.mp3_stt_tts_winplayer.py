###############################################
# STT → Ollama → TTS
# 음성 파일 입력 → 텍스트
# → Ollama: 텍스트 질문 → 텍스트 답변
# → TTS: 텍스트 답변 → 음성 파일 생성 및 재생
#
# STT : faster-whisper
# TTS : edge-tts
#
# 설치:
# pip install ollama faster-whisper edge-tts pygame
###############################################

import asyncio              # 비동기(동시에 여러 작업을 기다리는) 처리를 위한 파이썬 표준 라이브러리. TTS 변환이 시간이 걸리는 작업이라 사용
import os
import time
from pathlib import Path

import ollama
from faster_whisper import WhisperModel  # 음성을 텍스트로 바꿔주는 STT 모델 클래스
import edge_tts                          # 텍스트를 음성으로 바꿔주는 TTS 라이브러리
import pygame


# =========================
# 기본 설정
# =========================

OLLAMA_MODEL = "exaone3.5:7.8b"      # 언어 모델
# 테스트가 무거우면 아래 모델로 먼저 확인
# OLLAMA_MODEL = "llama3.2:3b"

AUDIO_FILE = Path("./voice/voice1.mp3")       # 로딩할 오디오 파일 경로
OUTPUT_TTS_FILE = Path("./voice/answer.mp3")  # 답변 오디오 파일 저장 경로

# TTS : Text to Speech. STT : Speech to Text.

WHISPER_MODEL_SIZE = "base"    
# 음성 인식 모델 크기. 커질수록 인식 정확도는 올라가지만 속도는 느려지고 메모리도 더 필요함.
# tiny, base, small, medium, large-v3

WHISPER_DEVICE = "cpu"         
# STT 모델을 CPU로 돌릴지 GPU(cuda)로 돌릴지 설정.
# RTX 3080이면 "cuda" 사용 가능

WHISPER_COMPUTE_TYPE = "int8"
# 모델 내부 연산을 얼마나 '가볍게'(저정밀도) 할지 정하는 옵션. int8은 CPU에서 빠르고 메모리를 적게 씀.  
# cuda 사용 시 "float16" 권장

TTS_VOICE = "ko-KR-SunHiNeural" # TTS의 목소리를 선정.


# =========================
# STT 모델 로드
# =========================

print("STT 모델 로딩 중...")                # STT 모델을 메모리에 불러온다.

stt_model = WhisperModel(
    WHISPER_MODEL_SIZE,                   # 샘플 소리 파일을 읽는다.
    device=WHISPER_DEVICE,                # CPU로 STT 모델을 돌린다.
    compute_type=WHISPER_COMPUTE_TYPE     # int8로 연산.
)

print("STT 모델 로딩 완료")


# =========================
# 대화 히스토리
# =========================

messages = [
    {
        "role": "system",    # "system" 역할 = AI에게 미리 성격/규칙을 정해주는 지시문
        "content": (
            "너는 한국어로 간결하고 명확하게 답변하는 로컬 AI 비서다. "
            "사용자의 음성 질문을 텍스트로 변환한 내용을 바탕으로 자연스럽게 답변하라."
        )
    }
]
# 위 messeages에 대화가 진행될수록 사용자 질문(user)과 AI 답변(assistant)이 계속 추가되어 AI가 이전 대화 맥락을 기억한 채로 답할 수 있게 해줌.

# 함수는 "입력: 음성 파일 경로" → "출력: 인식된 텍스트" 역할을 함 (STT)
def transcribe_audio(audio_path: Path) -> str:
    """음성 파일을 텍스트로 변환한다."""

    if not audio_path.exists():
        raise FileNotFoundError(f"음성 파일을 찾을 수 없습니다: {audio_path}")

    print(f"\n음성 파일 읽는 중: {audio_path}")
    print("STT 변환 중...")

    segments, info = stt_model.transcribe(
        str(audio_path),
        language="ko",              # 한국어 음성임을 전달.
        beam_size=5                 # 후보를 5개까지 넓게 탐색해서 더 정확한 결과를 고르는 정밀도 옵션 (클수록 정확하지만 느려짐)
    )

    text = " ".join(segment.text.strip() for segment in segments).strip()

    return text


def ask_ollama(user_text: str) -> str:
    """Ollama 모델에 질문하고 답변을 받는다."""

    messages.append({
        "role": "user",
        "content": user_text
    })

    print("\nOllama 답변 생성 중...")

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        options={
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 512
        }
    )

    # ollama-python 버전에 따라 객체/딕셔너리 접근 모두 대비
    try:
        answer = response.message.content
    except AttributeError:
        answer = response["message"]["content"]

    answer = answer.strip()

    messages.append({
        "role": "assistant",
        "content": answer
    })

    return answer


async def text_to_speech(text: str, output_path: Path) -> None:
    """텍스트 답변을 음성 MP3 파일로 변환한다."""

    print("\nTTS 변환 중...")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    communicate = edge_tts.Communicate(
        text=text,
        voice=TTS_VOICE,
        rate="+0%",
        volume="+0%"
    )

    await communicate.save(str(output_path))

    print(f"TTS 파일 저장 완료: {output_path}")


def play_audio(audio_path: Path) -> None:
    """WSL2에서는 Windows 기본 플레이어로 MP3 파일을 연다."""

    if not audio_path.exists():
        raise FileNotFoundError(f"재생할 음성 파일을 찾을 수 없습니다: {audio_path}")

    print("\n음성 출력 중...")

    try:
        # WSL2 환경이면 Windows 경로로 변환 후 Windows 기본 플레이어 실행
        import subprocess

        linux_path = str(audio_path.resolve())
        windows_path = subprocess.check_output(
            ["wslpath", "-w", linux_path],
            text=True
        ).strip()

        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                f"Start-Process -FilePath '{windows_path}'"
            ],
            check=True
        )

        print(f"Windows 기본 플레이어로 재생 파일을 열었습니다: {windows_path}")

    except Exception as e:
        print("Windows 플레이어 실행에 실패했습니다.")
        print(e)

def main():
    print("\n파일 기반 음성 Ollama 앱 시작")

    try:
        # 1. 음성 파일 → 텍스트
        user_text = transcribe_audio(AUDIO_FILE)

        if not user_text:
            print("음성을 인식하지 못했습니다.")
            return

        print("\n사용자 음성 인식 결과:")
        print(user_text)

        # 2. 텍스트 → Ollama 답변
        answer = ask_ollama(user_text)

        print("\nAI 답변:")
        print(answer)

        # 3. 답변 텍스트 → 음성 파일
        asyncio.run(text_to_speech(answer, OUTPUT_TTS_FILE))

        # 4. 음성 출력
        play_audio(OUTPUT_TTS_FILE)

    except Exception as e:
        print(f"\n오류 발생: {type(e).__name__}")
        print(e)


if __name__ == "__main__":
    main()