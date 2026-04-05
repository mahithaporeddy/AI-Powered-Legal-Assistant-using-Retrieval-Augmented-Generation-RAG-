import { useState } from "react"

function App() {

  const [message, setMessage] = useState("")
  const [chat, setChat] = useState([])
  const [loading, setLoading] = useState(false)

  async function sendMessage() {

    if (!message.trim()) return

    const userMessage = message

    setChat(prev => [...prev, { type: "user", text: userMessage }])

    setMessage("")
    setLoading(true)

    const response = await fetch("http://127.0.0.1:8000/chat", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        user_message: userMessage
      })

    })

    const data = await response.json()

    setChat(prev => [...prev, { type: "ai", text: data.reply }])

    setLoading(false)
  }


  function handleKeyPress(e) {

    if (e.key === "Enter") {
      sendMessage()
    }

  }


  function clearChat() {

    setChat([])

  }


  return (

    <div style={styles.container}>

      <div style={styles.header}>

        AI Chatbot

        <button onClick={clearChat} style={styles.clearBtn}>
          Clear
        </button>

      </div>


      <div style={styles.chatBox}>

        {chat.map((msg, index) => (

          <div
            key={index}
            style={
              msg.type === "user"
                ? styles.userBubble
                : styles.aiBubble
            }
          >

            {msg.text}

          </div>

        ))}

        {loading && (

          <div style={styles.aiBubble}>
            typing...
          </div>

        )}

      </div>


      <div style={styles.inputArea}>

        <input

          style={styles.input}

          value={message}

          onChange={(e) => setMessage(e.target.value)}

          onKeyDown={handleKeyPress}

          placeholder="Ask something..."

        />

        <button
          style={styles.button}
          onClick={sendMessage}
        >

          Send

        </button>

      </div>

    </div>

  )

}

export default App



const styles = {

  container: {

    height: "100vh",

    display: "flex",

    flexDirection: "column",

    fontFamily: "Arial",

    backgroundColor: "#f0f2f5"

  },

  header: {

    padding: "15px",

    backgroundColor: "#202123",

    color: "white",

    display: "flex",

    justifyContent: "space-between"

  },

  chatBox: {

    flex: 1,

    padding: "20px",

    overflowY: "scroll"

  },

  userBubble: {

    backgroundColor: "#4CAF50",

    color: "white",

    padding: "10px",

    borderRadius: "10px",

    margin: "10px",

    maxWidth: "60%",

    alignSelf: "flex-end"

  },

  aiBubble: {

    backgroundColor: "white",

    padding: "10px",

    borderRadius: "10px",

    margin: "10px",

    maxWidth: "60%",

    border: "1px solid #ddd"

  },

  inputArea: {

    display: "flex",

    padding: "10px",

    backgroundColor: "white",

    borderTop: "1px solid #ddd"

  },

  input: {

    flex: 1,

    padding: "10px",

    borderRadius: "5px",

    border: "1px solid gray"

  },

  button: {

    marginLeft: "10px",

    padding: "10px",

    backgroundColor: "#202123",

    color: "white",

    border: "none",

    borderRadius: "5px"

  },

  clearBtn: {

    backgroundColor: "#444",

    color: "white",

    border: "none",

    padding: "5px 10px",

    borderRadius: "5px"

  }

}