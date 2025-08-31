"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Clock, AlertTriangle, CheckCircle, XCircle, Eye } from "lucide-react"

const recentPredictions = [
  {
    id: 1,
    description: "Suspicious login attempt detected",
    classification: "Benign",
    threat_level: "low",
    timestamp: "2 minutes ago",
    confidence: 92,
  },
  {
    id: 2,
    description: "Ransomware signature identified",
    classification: "Malware",
    threat_level: "critical",
    timestamp: "5 minutes ago",
    confidence: 96,
  },
  {
    id: 3,
    description: "Email credential harvesting attempt",
    classification: "Phishing",
    threat_level: "high",
    timestamp: "12 minutes ago",
    confidence: 87,
  },
  {
    id: 4,
    description: "Unusual network traffic pattern",
    classification: "Suspicious",
    threat_level: "medium",
    timestamp: "18 minutes ago",
    confidence: 74,
  },
]

const getThreatColor = (level: string) => {
  switch (level) {
    case "critical":
      return "text-destructive border-destructive/50"
    case "high":
      return "text-chart-4 border-chart-4/50"
    case "medium":
      return "text-chart-4 border-chart-4/50"
    case "low":
      return "text-primary border-primary/50"
    default:
      return "text-muted-foreground border-border"
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
      return <Clock className="w-4 h-4" />
  }
}

export function RecentPredictions() {
  return (
    <Card className="glass">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="w-5 h-5 text-primary" />
          Recent Predictions
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {recentPredictions.map((prediction) => (
            <div
              key={prediction.id}
              className="flex items-start justify-between p-3 rounded-lg bg-card/50 border border-border/50"
            >
              <div className="flex-1">
                <p className="text-sm font-medium mb-1">{prediction.description}</p>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <Clock className="w-3 h-3" />
                  {prediction.timestamp}
                  <span>•</span>
                  <span>{prediction.confidence}% confidence</span>
                </div>
              </div>
              <div className="flex flex-col items-end gap-1">
                <Badge variant="outline" className={`${getThreatColor(prediction.threat_level)} text-xs`}>
                  {getThreatIcon(prediction.threat_level)}
                  <span className="ml-1 capitalize">{prediction.threat_level}</span>
                </Badge>
                <span className="text-xs font-medium">{prediction.classification}</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
