import { useEffect, useState } from 'react'
import type { Room } from '../types'

export default function RoomBoard() {
  const [rooms, setRooms] = useState<Room[]>([])

  const fetchRooms = async () => {
    const res = await fetch('/rooms')
    const data: Room[] = await res.json()
    setRooms(data)
  }

  useEffect(() => {
    fetchRooms()
    const timer = setInterval(fetchRooms, 3000)
    return () => clearInterval(timer)
  }, [])

  return (
    <section className="w-full max-w-3xl bg-white rounded-2xl shadow p-6">
      <h2 className="text-lg font-semibold text-blue-600 mb-4">企業行政會議室看板</h2>
      <div className="flex flex-wrap gap-4 justify-around">
        {rooms.map(room => (
          <RoomCard key={room.id} room={room} />
        ))}
      </div>
    </section>
  )
}

function RoomCard({ room }: { room: Room }) {
  const isBooked = room.status === 'Booked'
  return (
    <div className={`w-44 rounded-xl border p-4 text-center border-t-4 ${
      isBooked
        ? 'border-t-red-400 bg-red-50'
        : 'border-t-green-400 bg-green-50'
    }`}>
      <p className="font-bold text-sm">{room.name}</p>
      <p className="text-xs text-gray-400 mt-1">{room.id}</p>
      <p className="text-xs text-gray-500">容納 {room.capacity} 人</p>
      {isBooked ? (
        <div className="mt-2 text-red-500 text-sm">
          <p className="font-semibold">🔴 {room.booked_by}</p>
          {room.meeting_name && <p className="text-xs text-red-400 mt-0.5">{room.meeting_name}</p>}
        </div>
      ) : (
        <p className="mt-2 font-semibold text-sm text-green-600">🟢 空閒中</p>
      )}
    </div>
  )
}
