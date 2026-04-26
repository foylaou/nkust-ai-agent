import { useState } from 'react'
import RoomBoard from './components/RoomBoard'
import ChatBox from './components/ChatBox'
import type { Phase } from './types'

export default function App() {
  const [phase, setPhase] = useState<Phase>('1')

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center px-4 py-8 gap-6">
      <h1 className="text-2xl font-bold text-blue-600">🏢 NKUST AI Agent Suite</h1>
      <RoomBoard />
      <ChatBox phase={phase} onPhaseChange={setPhase} />
    </div>
  )
}
