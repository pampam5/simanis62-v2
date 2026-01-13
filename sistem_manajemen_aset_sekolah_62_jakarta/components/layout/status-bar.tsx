"use client"

import { Circle, Database, Wifi, Clock } from "lucide-react"
import { useEffect, useState } from "react"

interface StatusBarProps {
  user?: string
  school?: string
}

export function StatusBar({ user = "Admin", school = "SDN 62 Kota" }: StatusBarProps) {
  const [currentTime, setCurrentTime] = useState<string>("")

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      setCurrentTime(
        now.toLocaleTimeString("id-ID", {
          hour: "2-digit",
          minute: "2-digit",
        }),
      )
    }
    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="h-6 bg-muted border-t border-border flex items-center justify-between px-3 text-[11px] text-muted-foreground select-none shrink-0">
      {/* Left Section */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5">
          <Circle className="w-2 h-2 fill-green-500 text-green-500" />
          <span>Terhubung</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Database className="w-3 h-3" />
          <span>SQLite</span>
        </div>
      </div>

      {/* Center Section */}
      <div className="flex items-center gap-1.5">
        <span className="font-medium">{school}</span>
        <span className="text-muted-foreground/50">•</span>
        <span>{user}</span>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5">
          <Wifi className="w-3 h-3" />
          <span>Online</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Clock className="w-3 h-3" />
          <span>{currentTime}</span>
        </div>
      </div>
    </div>
  )
}
