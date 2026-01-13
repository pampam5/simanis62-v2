"use client"

import { useState } from "react"
import { Minus, Square, X, Minimize2 } from "lucide-react"

interface TitleBarProps {
  title?: string
}

export function TitleBar({ title = "SIMANIS62 V2" }: TitleBarProps) {
  const [isMaximized, setIsMaximized] = useState(false)

  // In a real Tauri app, these would call Tauri window APIs
  const handleMinimize = () => {
    // window.__TAURI__?.window.appWindow.minimize()
  }

  const handleMaximize = () => {
    setIsMaximized(!isMaximized)
    // window.__TAURI__?.window.appWindow.toggleMaximize()
  }

  const handleClose = () => {
    // window.__TAURI__?.window.appWindow.close()
  }

  return (
    <div data-tauri-drag-region className="h-8 bg-primary flex items-center justify-between select-none shrink-0">
      {/* App Icon & Title */}
      <div className="flex items-center gap-2 px-3" data-tauri-drag-region>
        <div className="w-4 h-4 bg-primary-foreground/90 rounded-sm flex items-center justify-center">
          <span className="text-[10px] font-bold text-primary">S</span>
        </div>
        <span className="text-xs font-medium text-primary-foreground/90">{title}</span>
      </div>

      {/* Window Controls */}
      <div className="flex h-full">
        <button
          onClick={handleMinimize}
          className="h-full w-11 flex items-center justify-center hover:bg-primary-foreground/10 transition-colors"
          aria-label="Minimize"
        >
          <Minus className="w-3.5 h-3.5 text-primary-foreground/90" />
        </button>
        <button
          onClick={handleMaximize}
          className="h-full w-11 flex items-center justify-center hover:bg-primary-foreground/10 transition-colors"
          aria-label={isMaximized ? "Restore" : "Maximize"}
        >
          {isMaximized ? (
            <Minimize2 className="w-3 h-3 text-primary-foreground/90" />
          ) : (
            <Square className="w-3 h-3 text-primary-foreground/90" />
          )}
        </button>
        <button
          onClick={handleClose}
          className="h-full w-11 flex items-center justify-center hover:bg-red-500 transition-colors"
          aria-label="Close"
        >
          <X className="w-3.5 h-3.5 text-primary-foreground/90" />
        </button>
      </div>
    </div>
  )
}
