function ListRending() {
    const messages = [
        { id: 1, role: "user", content: "안녕하세요." },
        { id: 2, role: "assistant", content: "무엇을 도와드릴까요?" },
        { id: 3, role: "assistant", content: "Local LLM에 대해 알려줘." },
        { id: 4, role: "assistant", content: "Local LLM 은...." },
    ];

    return (
        <main>
            {" "}
            <h1>메시지 목록</h1>{" "}
            {messages.map((message) => (
                <div key={message.id}>
                    {" "}
                    <strong>{message.role}</strong> {" "}
                    <span>{message.content}</span> {/* 옆으로 바로 출력 */}
                </div>
            ))}{" "}
        </main>
    );
}

export default ListRending;

// 그냥 복붙시 한 줄로 나옴 
// -> Prettier 설치 후 포멧터 적용 단축키 Shift + Alt + F로 바로 구조 맞게 짜줌.

// function ListRending() {
// const messages = [
// { id: 1, role: "user", content: "안녕하세요." },
// { id: 2, role: "assistant", content: "무엇을 도와드릴까요?" },
// ];

// return (
// <main>
// <h1>메시지 목록</h1>
// {messages.map((message) => (
// <div key={message.id}>
// <strong>{message.role}</strong>
// <p>{message.content}</p>
// </div>
// ))}
// </main>
// );
// }

// export default ListRending;