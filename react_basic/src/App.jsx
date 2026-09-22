// import { useState } from 'react'
// import heroImg from './assets/hero.png'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import './App.css'

import Header from "./components/Header.jsx" // 컴포넌트 가져와서 아래에서 렌더링
import Greeting from "./components/Greeting.jsx"
import Counter from "./components/Counter.jsx"
import InputState from "./components/InputState.jsx"
import ListRending from "./components/ListRending.jsx"
import ConditionalRending from "./components/ConditionalRending.jsx"
import UseEffectRender from "./components/UseEffectRender.jsx"
import OllamaChat from "./components/OllamaChat.jsx"

function App() {
  // const [count, setCount] = useState(0)
  // javascript 영역
  const title = '헬로 리엑트' // 변수 처리

  return (
    <>
      {/* 데이터 랜더링 영역. 브라우저에서 이루어짐. 코드를 수행해서 return 받음. */}
      <OllamaChat />
      <UseEffectRender />
      <ConditionalRending />
      <ListRending />
      <InputState />
      <Counter />
      <Greeting name='joy' age='30' />
      {/* 자식은 부모에게서 변하는 값을 받음. component에 lendering할 값을 자식에게 전달. */}
      {/* html 태그는 , 할 필요 X */}
      <Header />
      <h1>{title}</h1>
    </>
  )
}

export default App
