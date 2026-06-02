import { useState } from "react"
import { apiGet } from "./api"
import "./App.css"

function App() {
  const [message, setMessage] = useState("")

  async function testApi() {
    const data = await apiGet("/api/ping/")
    setMessage(data.message)
  }

  return (
    <main style={{ padding: 32 }}>
      <h1>Django + React + EB</h1>
      <button onClick={testApi}>API 테스트</button>
      <p>응답: {message}</p>
    </main>
  )
}

export default App