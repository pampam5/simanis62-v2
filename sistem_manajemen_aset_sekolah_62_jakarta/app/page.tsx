import { DesktopShell } from "@/components/layout/desktop-shell"
import { Package, TrendingUp, AlertTriangle, CheckCircle2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function HomePage() {
  return (
    <DesktopShell>
      <div className="p-4 space-y-4">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-foreground">Dashboard</h1>
            <p className="text-xs text-muted-foreground">Selamat datang di SIMANIS62 V2 - Sistem Manajemen Aset</p>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-4 gap-3">
          <Card className="border shadow-none">
            <CardHeader className="p-3 pb-1">
              <CardTitle className="text-xs font-medium text-muted-foreground flex items-center gap-2">
                <Package className="w-3.5 h-3.5" />
                Total Aset
              </CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-0">
              <div className="text-2xl font-bold text-foreground">1,234</div>
              <p className="text-[11px] text-muted-foreground">+12 bulan ini</p>
            </CardContent>
          </Card>

          <Card className="border shadow-none">
            <CardHeader className="p-3 pb-1">
              <CardTitle className="text-xs font-medium text-muted-foreground flex items-center gap-2">
                <TrendingUp className="w-3.5 h-3.5" />
                Nilai Total
              </CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-0">
              <div className="text-2xl font-bold text-foreground">Rp 2.5M</div>
              <p className="text-[11px] text-muted-foreground">Perolehan 2024</p>
            </CardContent>
          </Card>

          <Card className="border shadow-none">
            <CardHeader className="p-3 pb-1">
              <CardTitle className="text-xs font-medium text-muted-foreground flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-green-600" />
                Kondisi Baik
              </CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-0">
              <div className="text-2xl font-bold text-green-600">1,180</div>
              <p className="text-[11px] text-muted-foreground">95.6% dari total</p>
            </CardContent>
          </Card>

          <Card className="border shadow-none">
            <CardHeader className="p-3 pb-1">
              <CardTitle className="text-xs font-medium text-muted-foreground flex items-center gap-2">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                Perlu Perhatian
              </CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-0">
              <div className="text-2xl font-bold text-amber-600">54</div>
              <p className="text-[11px] text-muted-foreground">Rusak ringan/berat</p>
            </CardContent>
          </Card>
        </div>

        {/* Placeholder Content */}
        <Card className="border shadow-none">
          <CardHeader className="p-3">
            <CardTitle className="text-sm font-medium">Aktivitas Terbaru</CardTitle>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="space-y-2">
              {[
                { action: "Penambahan aset baru", item: "Laptop ASUS ROG", time: "2 menit lalu" },
                { action: "Mutasi aset", item: "Proyektor Epson ke R.Guru", time: "15 menit lalu" },
                { action: "Update kondisi", item: "AC Daikin - Rusak Ringan", time: "1 jam lalu" },
                { action: "Penghapusan aset", item: "Printer Canon (rusak berat)", time: "2 jam lalu" },
              ].map((activity, i) => (
                <div key={i} className="flex items-center justify-between py-1.5 border-b border-border last:border-0">
                  <div>
                    <p className="text-xs font-medium text-foreground">{activity.action}</p>
                    <p className="text-[11px] text-muted-foreground">{activity.item}</p>
                  </div>
                  <span className="text-[11px] text-muted-foreground">{activity.time}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DesktopShell>
  )
}
