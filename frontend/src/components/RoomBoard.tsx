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
  const bookings = room.bookings ?? []
  const isBooked = bookings.length > 0
  return (
    <div className={`w-52 rounded-xl border p-4 border-t-4 ${
      isBooked
        ? 'border-t-red-400 bg-red-50'
        : 'border-t-green-400 bg-green-50'
    }`}>
      <p className="font-bold text-sm text-center">{room.name}</p>
      <p className="text-xs text-gray-400 mt-1 text-center">{room.id}</p>
      <p className="text-xs text-gray-500 text-center">容納 {room.capacity} 人</p>
      {isBooked ? (
        <div className="mt-2 space-y-1.5 text-left">
          {bookings.map(b => (
            <div key={b.id} className="text-xs bg-white/70 rounded p-1.5 border border-red-100">
              <p className="font-semibold text-red-500">🔴 {b.start_time}~{b.end_time}</p>
              <p className="text-gray-600">{b.user_name}・與會 {b.attendees} 人</p>
              <p className="text-red-400">{b.meeting_name}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-2 font-semibold text-sm text-green-600 text-center">🟢 目前無預約</p>
      )}
    </div>
  )
}
