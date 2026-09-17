# 실습 : image to text
from ollama import chat

IMAGE_PATH = "imgs/img01.jpg"
MODEL_NAME = "qwen3.5:9b"

response = chat(
    model=MODEL_NAME, # role
    messages=[        # role의 content
        {
            "role": "user",
            "content": """
이 이미지를 한국어로 설명해줘.

다음 형식으로 답변해줘.
1. 전체 장면
2. 주요 객체
3. 배경
4. 이미지에서 추론 가능한 상황
""",
            "images": [IMAGE_PATH], # image 경로 말고 사용자가 넣을 경우 ui 상에서 받은 걸 처리하는 과정을 백엔드에서 해야 함.
        }
    ],
    think=False,
    # stream=False, 
    stream = True, 
    # 일 경우 buffer에 쌓아서 한꺼번에 제시하지 않고 token, chunk 단위로 저장함. 
    # 그러므로, 출력도 chunk 단위로 화면에 찍히게 만들어야 함.
)

# print(response.message.content)

for chunk in response:
    print(chunk.message.content, end = "", flush = True)