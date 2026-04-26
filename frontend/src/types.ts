export type RoomStatus = 'Available' | 'Booked'

export interface Room {
  id: string
  name: string
  capacity: number
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
