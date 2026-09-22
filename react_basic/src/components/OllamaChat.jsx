// 사용자가 메시지를 입력하면 FastAPI 백엔드(/chat)를 통해 Ollama 모델에게 질문을 보내고,
//  응답을 받아서 화면에 보여주는 간단한 챗봇 UI

import { useState, useEffect } from "react";
import axios from "axios";
const CHAT_URL = "http://localhost:8000/chat";
const MODELS_URL = "http://localhost:8000/models";

function OllamaChat() {
    // 입력값, 응답 결과, 로딩 상태, 오류 메시지를 상태로 관리한다.
    const [message, setMessage] = useState(""); // 입력창에 쓴 텍스트
    const [answer, setAnswer] = useState(null); // 서버에서 받은 응답 객체
    const [isLoading, setIsLoading] = useState(false); // 요청 진행 중인지 여부
    const [errorMessage, setErrorMessage] = useState(""); // 에러 메시지

    const [model, setModel] = useState("");            // 현재 선택된 모델
    const [modelList, setModelList] = useState([]);    // 서버에서 받아온 모델 목록
    const [isModelLoading, setIsModelLoading] = useState(true); // 목록 불러오는 중 여부

    useEffect(() => {
        const fetchModels = async () => {
            try {
                const response = await axios.get(MODELS_URL);
                const models = response.data.models || [];
                setModelList(models);
                if (models.length > 0) {
                    setModel(models[0]);
                }
            } catch (error) {
                console.error(error);
                setErrorMessage("모델 목록을 불러오지 못했습니다.");
            } finally {
                setIsModelLoading(false);
            }
        };
        fetchModels();
    }, []);

    const handleSend = async () => {
        if (!message.trim()) {
            alert("메시지를 입력하세요.");
            return;
        }

        setIsLoading(true);
        setErrorMessage("");
        setAnswer(null);

        try {
            const response = await axios.post(CHAT_URL, {
                message: message,
                model: model,
                system_prompt: "너는 초보자를 돕는 AI 강사다.",
                temperature: 0.7,
                top_p: 0.9,
                num_predict: 256,
            });

            const data = response.data;
            console.log(data);
            setAnswer(data);
        } catch (error) {
            console.error(error);
            setErrorMessage("서버 요청 중 오류가 발생했습니다.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="app">
            <h1>Ollama Chat</h1>

            <section>
                <label htmlFor="model-select">모델 선택: </label>
                {isModelLoading ? (
                    <span>모델 목록 불러오는 중...</span>
                ) : (
                    <select
                        id="model-select"
                        value={model}
                        onChange={(event) => setModel(event.target.value)}
                        disabled={isLoading}
                    >
                        {modelList.map((m) => (
                            <option key={m} value={m}>
                                {m}
                            </option>
                        ))}
                    </select>
                )}
            </section>

            <section>
                <textarea
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                    placeholder="메시지를 입력하세요."
                    rows={5}
                />
                <br />
                <button onClick={handleSend} disabled={isLoading}>
                    {isLoading ? "응답 생성 중..." : "전송"}
                </button>
            </section>

            <section>
                <h2>응답</h2>
                {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
                {isLoading ? (
                    <p>Ollama 가 응답을 생성하고 있습니다.</p>
                ) : (
                    answer && (
                        <>
                            <p>{answer.model}</p>
                            <p>{answer.message}</p>
                            <p>{answer.elapsed_time}</p>
                        </>
                    )
                )}
            </section>
        </main>
    );
}

export default OllamaChat;