export type RoomStatus = 'Available' | 'Booked'

export interface Booking {
  id: number
  user_name: string
  meeting_name: string
  attendees: number
  start_time: string
  end_time: string
}

export interface Room {
  id: string
  name: string
  capacity: number
  bookings: Booking[]
  // 向後相容欄位（由最近一筆預約導出）
  status: RoomStatus
  booked_by: string | null
  meeting_name: string | null
}

export type MessageRole = 'user' | 'agent' | 'tool'

export interface Message {
  id: number
  role: MessageRole
  content: string
}

export type Phase = '1' | '2' | '3'
