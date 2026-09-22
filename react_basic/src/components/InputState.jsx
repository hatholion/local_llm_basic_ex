import { useState } from "react";

function InputState(){
    const [message, setMessage] = useState("")
    return (
        <main className = 'app'>
            <h1> 입력값 상태 관리 예제</h1>
            <input
            value = {message}
            onChange = {(event) => setMessage(event.target.value)}
            placeholder = '메세지를 입력하세요.'
            />

            <p> 입력한 메세지 : {message} </p>
            
        </main>


    )


}


export default InputState

// h1과 p는 HTML의 기본 태그.

// h1 (Heading 1)

// 문서의 제목이나 가장 중요한 제목을 나타내는 태그.
// h1부터 h6까지 있고, 숫자가 작을수록 더 크고 중요한 제목임 (h1이 제일 크고 중요함).
// 기본적으로 브라우저에서 크고 굵은 글씨로 표시.

// p (Paragraph)

// 문단, 즉 일반 텍스트 내용을 담는 태그.
// 줄바꿈과 여백이 자동으로 적용되는 평범한 텍스트 블록.