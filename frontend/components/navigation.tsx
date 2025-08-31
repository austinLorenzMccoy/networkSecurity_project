"use client"

import { Shield, Home, FileText, Settings, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"

export function Navigation() {
  return (
    <nav className="border-b border-border/50 bg-card/80 backdrop-blur-xl">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Shield className="w-7 h-7 text-primary" />
              <span className="text-xl font-bold font-[family-name:var(--font-playfair)]">NetSec Portal</span>
            </div>
            <Badge variant="outline" className="ml-4">
              v1.2.0
            </Badge>
          </div>

          <div className="flex items-center gap-4">
            <Link href="/" className="inline-flex items-center gap-2 text-sm px-3 py-2 rounded-md hover:bg-accent/40">
              <Home className="w-4 h-4" />
              Dashboard
            </Link>
            <Link href="/reports" className="inline-flex items-center gap-2 text-sm px-3 py-2 rounded-md hover:bg-accent/40">
              <FileText className="w-4 h-4" />
              Reports
            </Link>
            <Link href="/settings" className="inline-flex items-center gap-2 text-sm px-3 py-2 rounded-md hover:bg-accent/40">
              <Settings className="w-4 h-4" />
              Settings
            </Link>
            <Button variant="outline" size="sm" className="gap-2 glass bg-transparent">
              <LogOut className="w-4 h-4" />
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
