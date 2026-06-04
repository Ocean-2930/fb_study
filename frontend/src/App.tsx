import { useState } from "react"
import { apiPost } from "./api"
import "./App.css"

function App() {
  const [text, setText] = useState("")
  const [message, setMessage] = useState("")
  const [isSending, setIsSending] = useState(false)

  async function sendMessage() {
    setIsSending(true)
    setMessage("")

    try {
      const data = await apiPost<{ text: string }>("/api/message/", { text })
      setMessage(data.message)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "API request failed")
    } finally {
      setIsSending(false)
    }
  }

  return (
    <main className="app">
      <h1>Django + React + EB</h1>
      <div className="message-form">
        <input
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="String to send"
        />
        <button onClick={sendMessage} disabled={isSending || text.trim().length === 0}>
          {isSending ? "Sending..." : "Send"}
        </button>
      </div>
      <p>Response: {message}</p>
    </main>
  )
}

export default App
