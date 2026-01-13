import { useState } from "react"
import { TitleBar } from "./title-bar"
import { Sidebar } from "./sidebar"
import { StatusBar } from "./status-bar"

interface DesktopShellProps {
    children: React.ReactNode
}

export function DesktopShell({ children }: DesktopShellProps) {
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

    return (
        <div className="h-screen w-screen flex flex-col overflow-hidden bg-background">
            {/* Title Bar */}
            <TitleBar />

            {/* Main Content Area */}
            <div className="flex-1 flex overflow-hidden">
                {/* Sidebar */}
                <Sidebar collapsed={sidebarCollapsed} onCollapsedChange={setSidebarCollapsed} />

                {/* Content */}
                <main className="flex-1 overflow-auto bg-background">{children}</main>
            </div>

            {/* Status Bar */}
            <StatusBar />
        </div>
    )
}
