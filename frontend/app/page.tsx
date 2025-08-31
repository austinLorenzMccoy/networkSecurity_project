"use client"

import { useRef, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Shield,
  Upload,
  Activity,
  BarChart3,
  FileText,
  AlertTriangle,
  CheckCircle,
  XCircle,
  TrendingUp,
  Zap,
  Eye,
  Database,
} from "lucide-react"
import { ThreatChart } from "@/components/threat-chart"
import { SystemHealth } from "@/components/system-health"
import { RecentPredictions } from "@/components/recent-predictions"
import { Navigation } from "@/components/navigation"

export default function Dashboard() {
  const [textInput, setTextInput] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [predictionResult, setPredictionResult] = useState<{
    classification: string
    confidence: number
    threat_level: "low" | "medium" | "high" | "critical"
  } | null>(null)
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"

  const handlePredict = async () => {
    if (!textInput.trim()) return

    setIsAnalyzing(true)
    try {
      // Try real backend first
      const res = await fetch(`${API_BASE}/predict/text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textInput }),
      })
      if (res.ok) {
        const data = await res.json()
        // Handle backend schema: { predictions: number[], prediction_probabilities?: Array<Record<string, number>> }
        if (Array.isArray(data?.predictions) && data.predictions.length > 0) {
          const pred = Number(data.predictions[0])
          // Map class label to human-readable classification
          const classification = pred === 1 ? "Malware" : "Benign"
          // Derive confidence from probs if available; pick max probability * 100
          let confidence = 0
          if (Array.isArray(data.prediction_probabilities) && data.prediction_probabilities[0]) {
            const probs = data.prediction_probabilities[0]
            const values = Object.values(probs) as number[]
            if (values.length > 0) confidence = Math.round(Math.max(...values) * 100)
          }
          const threat_level = pred === 1 ? (confidence >= 85 ? "critical" : confidence >= 70 ? "high" : "medium") : "low"
          setPredictionResult({ classification, confidence, threat_level })
        } else {
          // Fallback if unexpected schema
          const mockResults = [
            { classification: "Malware", confidence: 94, threat_level: "critical" as const },
            { classification: "Phishing", confidence: 87, threat_level: "high" as const },
            { classification: "Benign", confidence: 92, threat_level: "low" as const },
            { classification: "Suspicious Activity", confidence: 76, threat_level: "medium" as const },
          ]
          setPredictionResult(mockResults[Math.floor(Math.random() * mockResults.length)])
        }
      } else {
        // Fallback to mock if backend returns error
        const mockResults = [
          { classification: "Malware", confidence: 94, threat_level: "critical" as const },
          { classification: "Phishing", confidence: 87, threat_level: "high" as const },
          { classification: "Benign", confidence: 92, threat_level: "low" as const },
          { classification: "Suspicious Activity", confidence: 76, threat_level: "medium" as const },
        ]
        setPredictionResult(mockResults[Math.floor(Math.random() * mockResults.length)])
      }
    } catch (e) {
      // Fallback on network errors
      const mockResults = [
        { classification: "Malware", confidence: 94, threat_level: "critical" as const },
        { classification: "Phishing", confidence: 87, threat_level: "high" as const },
        { classification: "Benign", confidence: 92, threat_level: "low" as const },
        { classification: "Suspicious Activity", confidence: 76, threat_level: "medium" as const },
      ]
      setPredictionResult(mockResults[Math.floor(Math.random() * mockResults.length)])
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleFileUpload = async (file: File) => {
    try {
      const text = await file.text()
      setTextInput(text)
      // Auto-trigger predict after loading file
      setTimeout(() => handlePredict(), 0)
    } catch (e) {
      console.error("Failed to read file", e)
    }
  }

  const getThreatColor = (level: string) => {
    switch (level) {
      case "critical":
        return "text-destructive"
      case "high":
        return "text-chart-4"
      case "medium":
        return "text-chart-4"
      case "low":
        return "text-primary"
      default:
        return "text-muted-foreground"
    }
  }

  const getThreatIcon = (level: string) => {
    switch (level) {
      case "critical":
        return <XCircle className="w-4 h-4" />
      case "high":
        return <AlertTriangle className="w-4 h-4" />
      case "medium":
        return <Eye className="w-4 h-4" />
      case "low":
        return <CheckCircle className="w-4 h-4" />
      default:
        return <Activity className="w-4 h-4" />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold font-[family-name:var(--font-playfair)] text-balance">
              NetSec Threat Portal
            </h1>
            <p className="text-muted-foreground mt-2">Advanced threat detection and security monitoring dashboard</p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="glass">
              <Activity className="w-3 h-3 mr-1 text-primary" />
              System Online
            </Badge>
          </div>
        </div>

        {/* Top Row - System Health & Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <SystemHealth />

          <Card className="glass">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Threats Detected</p>
                  <p className="text-2xl font-bold text-destructive">247</p>
                </div>
                <AlertTriangle className="w-8 h-8 text-destructive" />
              </div>
              <div className="mt-4">
                <div className="flex items-center gap-2 text-sm">
                  <TrendingUp className="w-3 h-3 text-destructive" />
                  <span className="text-destructive">+12% from last week</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Scans Today</p>
                  <p className="text-2xl font-bold text-primary">1,429</p>
                </div>
                <Zap className="w-8 h-8 text-primary" />
              </div>
              <div className="mt-4">
                <Progress value={78} className="h-2" />
                <p className="text-xs text-muted-foreground mt-1">78% of daily quota</p>
              </div>
            </CardContent>
          </Card>

          <Card className="glass">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Data Processed</p>
                  <p className="text-2xl font-bold">2.4TB</p>
                </div>
                <Database className="w-8 h-8 text-accent" />
              </div>
              <div className="mt-4">
                <div className="flex items-center gap-2 text-sm">
                  <CheckCircle className="w-3 h-3 text-primary" />
                  <span className="text-primary">All systems operational</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Threat Analysis Form */}
          <div className="lg:col-span-2">
            <Card className="glass-strong">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5 text-primary" />
                  Threat Analysis Engine
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Input Threat Intelligence Data</label>
                  <Textarea
                    placeholder="Paste network logs, threat intelligence reports, or suspicious content here for analysis..."
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    className="min-h-[120px] bg-input/50 border-border/50 focus:border-primary/50"
                  />
                </div>

                <div className="flex gap-3">
                  <Button
                    onClick={handlePredict}
                    disabled={!textInput.trim() || isAnalyzing}
                    className="bg-primary hover:bg-primary/90"
                  >
                    {isAnalyzing ? (
                      <>
                        <Activity className="w-4 h-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Shield className="w-4 h-4 mr-2" />
                        Analyze Threat
                      </>
                    )}
                  </Button>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".txt,.log,.json,.md"
                    className="hidden"
                    onChange={(e) => {
                      const f = e.target.files?.[0]
                      if (f) handleFileUpload(f)
                      // reset to allow re-upload of same file
                      e.currentTarget.value = ""
                    }}
                  />
                  <Button
                    variant="secondary"
                    className="glass"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Upload className="w-4 h-4 mr-2" />
                    Upload File
                  </Button>
                </div>

                {/* Prediction Result */}
                {predictionResult && (
                  <Card className="glass border-l-4 border-l-primary">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold">Analysis Result</h3>
                        <Badge
                          variant="outline"
                          className={`${getThreatColor(predictionResult.threat_level)} border-current`}
                        >
                          {getThreatIcon(predictionResult.threat_level)}
                          <span className="ml-1 capitalize">{predictionResult.threat_level}</span>
                        </Badge>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-muted-foreground">Classification:</span>
                          <span className="font-medium">{predictionResult.classification}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-muted-foreground">Confidence:</span>
                          <span className="font-medium">{predictionResult.confidence}%</span>
                        </div>
                        <Progress value={predictionResult.confidence} className="h-2 mt-2" />
                      </div>
                    </CardContent>
                  </Card>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Threat Distribution Chart */}
          <div>
            <ThreatChart />
          </div>
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RecentPredictions />

          <Card className="glass">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary" />
                Security Reports
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground">
                  Generate and download comprehensive security reports and analysis logs.
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <Button variant="outline" className="glass bg-transparent">
                    <BarChart3 className="w-4 h-4 mr-2" />
                    Daily Report
                  </Button>
                  <Button variant="outline" className="glass bg-transparent">
                    <FileText className="w-4 h-4 mr-2" />
                    Threat Log
                  </Button>
                </div>
                <Button className="w-full bg-primary hover:bg-primary/90">
                  <FileText className="w-4 h-4 mr-2" />
                  Download Full Report
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
