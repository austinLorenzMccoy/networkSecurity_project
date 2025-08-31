"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Activity, Server, Cpu, HardDrive } from "lucide-react"

export function SystemHealth() {
  return (
    <Card className="glass">
      <CardContent className="p-6">
        <div className="flex items-center gap-3 mb-4">
          <Activity className="w-5 h-5 text-primary" />
          <h3 className="font-semibold">System Health</h3>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Server className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm">API Status</span>
            </div>
            <Badge variant="outline" className="text-primary border-primary/50">
              Online
            </Badge>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm">CPU Usage</span>
            </div>
            <span className="text-sm font-medium">23%</span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <HardDrive className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm">Memory</span>
            </div>
            <span className="text-sm font-medium">1.2GB</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
