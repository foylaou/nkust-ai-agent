import { useEffect, useRef, useState } from 'react'
import type { Message, Phase } from '../types'

const PHASES: { value: Phase; label: string }[] = [
  { value: '1', label: '階段一：Local Agent' },
  { value: '2', label: '階段二：MCP Power' },
  { value: '3', label: '階段三：Multi-Agent' },
]

interface Props {
  phase: Phase
  onPhaseChange: (p: Phase) => void
}

let msgCounter = 0
const nextId = () => ++msgCounter

export default function ChatBox({ phase, onPhaseChange }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    { id: nextId(), role: 'agent', content: '您好！我是您的 AI 行政助手。' },
  ])
  const [input, setInput] = useState('')
  const [streaming, setStreaming] = useState(false)
  const [waitingForAgent, setWaitingForAgent] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const agentIdRef = useRef<number | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handlePhaseChange = (p: Phase) => {
    onPhaseChange(p)
    setMessages(prev => [
      ...prev,
      { id: nextId(), role: 'agent', content: `[系統] 已切換至階段 ${p}。` },
    ])
  }

  const handleReset = async () => {
    await fetch('/reset', { method: 'POST' })
    setMessages([{ id: nextId(), role: 'agent', content: '✅ 已重置所有資料。' }])
  }

  const sendMessage = async () => {
    const text = input.trim()
    if (!text || streaming) return
    setInput('')
    setMessages(prev => [...prev, { id: nextId(), role: 'user', content: text }])
    setStreaming(true)
    setWaitingForAgent(true)
    agentIdRef.current = null

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, phase }),
      })

      const reader = res.body!.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        const lines = decoder.decode(value).split('\n').filter(l => l.trim())
        for (const line of lines) {
          try {
            const data = JSON.parse(line) as { type: string; content: string }

            if (data.type === 'log') {
              // 工具 log 直接 append，不影響 agent 泡泡
              setMessages(prev => [...prev, { id: nextId(), role: 'tool', content: data.content }])
            } else if (data.type === 'delta') {
              if (agentIdRef.current === null) {
                // 第一個 delta 才建立 agent 泡泡，確保排在所有 log 之後
                const id = nextId()
                agentIdRef.current = id
                setWaitingForAgent(false)
                setMessages(prev => [...prev, { id, role: 'agent', content: data.content }])
              } else {
                const id = agentIdRef.current
                setMessages(prev =>
                  prev.map(m => m.id === id ? { ...m, content: m.content + data.content } : m)
                )
              }
            } else if (data.type === 'error') {
              setWaitingForAgent(false)
              setMessages(prev => [...prev, { id: nextId(), role: 'agent', content: `❌ 錯誤：${data.content}` }])
            }
          } catch {
            // skip malformed chunk
          }
        }
      }
    } catch (e) {
      setWaitingForAgent(false)
      setMessages(prev => [...prev, { id: nextId(), role: 'agent', content: `連線失敗：${e}` }])
    } finally {
      setStreaming(false)
      setWaitingForAgent(false)
    }
  }

  return (
    <section className="w-full max-w-3xl bg-white rounded-2xl shadow p-6 flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-blue-600">🤖 AI 行政助手</h2>
        <button
          onClick={handleReset}
          className="text-xs bg-gray-500 hover:bg-gray-600 text-white px-3 py-1.5 rounded-lg"
        >
          重置 Demo
        </button>
      </div>

      {/* Phase selector */}
      <div className="bg-gray-100 rounded-xl px-4 py-3 flex items-center gap-3">
        <span className="text-sm text-gray-600">🚀 切換階段：</span>
        <select
          value={phase}
          onChange={e => handlePhaseChange(e.target.value as Phase)}
          className="text-sm border border-gray-300 rounded-lg px-2 py-1 outline-none"
        >
          {PHASES.map(p => (
            <option key={p.value} value={p.value}>{p.label}</option>
          ))}
        </select>
      </div>

      {/* Chat messages */}
      <div className="h-96 overflow-y-auto flex flex-col gap-2 bg-gray-50 rounded-xl p-4">
        {messages.map(msg => <ChatMessage key={msg.id} msg={msg} />)}
        {waitingForAgent && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="輸入指令..."
          disabled={streaming}
          className="flex-1 border border-gray-300 rounded-xl px-4 py-2 text-sm outline-none focus:border-blue-400 disabled:bg-gray-100"
        />
        <button
          onClick={sendMessage}
          disabled={streaming}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white px-5 py-2 rounded-xl text-sm font-semibold"
        >
          發送
        </button>
      </div>
    </section>
  )
}

function ChatMessage({ msg }: { msg: Message }) {
  if (msg.role === 'user') {
    return (
      <div className="self-end max-w-[80%] bg-blue-600 text-white px-4 py-2 rounded-2xl rounded-br-sm text-sm whitespace-pre-wrap">
        {msg.content}
      </div>
    )
  }
  if (msg.role === 'tool') {
    return (
      <div className="self-center w-[90%] bg-yellow-50 border border-yellow-200 text-yellow-800 font-mono text-xs px-3 py-2 rounded-xl text-center">
        {msg.content}
      </div>
    )
  }
  return (
    <div className="self-start max-w-[80%] bg-gray-200 text-gray-800 px-4 py-2 rounded-2xl rounded-bl-sm text-sm whitespace-pre-wrap">
      {msg.content}
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="self-start flex gap-1 bg-gray-200 px-4 py-3 rounded-2xl">
      {[0, 1, 2].map(i => (
        <span
          key={i}
          className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce"
          style={{ animationDelay: `${i * 0.2}s` }}
        />
      ))}
    </div>
  )
}
