import {
  Package,
  DollarSign,
  CheckCircle,
  AlertCircle,
  Plus,
  Download,
  Database,
  Search,
  ArrowLeftRight
} from 'lucide-react';
import { GlassButton, GlassInput, Text, AnimatedCard, PageTransition, FadeIn, StaggerContainer, StaggerItem } from '@/components/ui';
import { StatusBadge } from '@/components/ui/status-badge';
import { KondisiBadge } from '@/components/ui/kondisi-badge';

export function DashboardPage() {
  const stats = [
    {
      label: 'Total Aset',
      value: '1,234',
      icon: Package,
      color: 'text-[var(--accent-blue)]',
      bgColor: 'bg-[var(--color-info-bg)]'
    },
    {
      label: 'Kondisi Baik',
      value: '1,089',
      icon: CheckCircle,
      color: 'text-[var(--accent-green)]',
      bgColor: 'bg-[var(--color-success-bg)]'
    },
    {
      label: 'Kondisi Rusak',
      value: '145',
      icon: AlertCircle,
      color: 'text-[var(--accent-red)]',
      bgColor: 'bg-[var(--color-error-bg)]'
    },
    {
      label: 'Total Nilai',
      value: 'Rp 15.5M',
      icon: DollarSign,
      color: 'text-[var(--accent-green)]',
      bgColor: 'bg-[var(--color-success-bg)]'
    },
  ];

  const recentAssets = [
    { nama: 'Laptop Dell Latitude 5520', kode: '02.06.01.0001', status: 'Aktif' as const, kondisi: 'Baik' as const },
    { nama: 'Proyektor Epson EB-X51', kode: '02.06.02.0015', status: 'Baru' as const, kondisi: 'Baik' as const },
    { nama: 'AC Daikin 2PK', kode: '02.06.03.0008', status: 'Mutasi' as const, kondisi: 'Rusak Ringan' as const },
    { nama: 'Printer HP LaserJet Pro', kode: '02.06.01.0042', status: 'Rusak' as const, kondisi: 'Rusak Berat' as const },
  ];

  const activities = [
    { text: 'Admin menambah aset Laptop Dell', time: '5 menit lalu', icon: Plus },
    { text: 'Admin mengubah status aset', time: '1 jam lalu', icon: CheckCircle },
    { text: 'Admin mutasi aset ke Ruang Lab', time: '2 jam lalu', icon: ArrowLeftRight },
    { text: 'Admin export laporan KIB B', time: '3 jam lalu', icon: Download },
  ];

  const quickActions = [
    { label: 'Tambah Aset', icon: Plus },
    { label: 'Export Laporan', icon: Download },
    { label: 'Backup Database', icon: Database },
  ];

  return (
    <PageTransition className="p-4 sm:p-6 lg:p-8 space-y-6 lg:space-y-8">
      {/* Header */}
      <FadeIn>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <Text variant="large-title" as="h1">
              Dashboard
            </Text>
          </div>

          <div className="flex flex-wrap gap-3">
            <GlassButton variant="secondary" size="md">
              <Download className="h-4 w-4" />
              Export Laporan
            </GlassButton>
            <GlassButton variant="primary" size="md">
              <Plus className="h-4 w-4" />
              Tambah Aset
            </GlassButton>
          </div>
        </div>
      </FadeIn>

      {/* Stats Cards - Responsive Grid */}
      <StaggerContainer className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        {stats.map((stat, index) => (
          <StaggerItem key={stat.label}>
            <AnimatedCard
              delay={index * 0.1}
              className="p-4 lg:p-6 relative overflow-hidden"
            >
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <Text variant="footnote" color="secondary" className="uppercase tracking-wide">
                    {stat.label}
                  </Text>
                  <Text variant="large-title" className="font-bold">
                    {stat.value}
                  </Text>
                </div>

                <div className={`p-3 rounded-xl ${stat.bgColor}`}>
                  <stat.icon className={`h-7 w-7 ${stat.color}`} />
                </div>
              </div>
            </AnimatedCard>
          </StaggerItem>
        ))}
      </StaggerContainer>

      {/* Search Section - Moved to top for better UX */}
      <FadeIn delay={0.3}>
        <AnimatedCard delay={0.3} hover={false} className="p-4">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <GlassInput
                placeholder="Cari aset berdasarkan nama, kode, atau merk..."
                className="pl-10 w-full"
              />
            </div>
            <GlassButton variant="primary" size="md" className="sm:w-auto w-full">
              Cari
            </GlassButton>
          </div>
        </AnimatedCard>
      </FadeIn>

      {/* Content Grid - Responsive */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 items-start">
        {/* Recent Assets - Takes 3 columns on xl screens */}
        <FadeIn delay={0.4} className="xl:col-span-3">
          <AnimatedCard delay={0.4} hover={false} className="p-5">
            <div className="flex items-center justify-between mb-4">
              <Text variant="title-3" as="h2">
                Aset Terbaru
              </Text>
              <GlassButton variant="ghost" size="md">
                Lihat Semua
              </GlassButton>
            </div>

            {/* Mini Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[var(--separator)]">
                    <th className="text-left py-2 px-3 text-[14px] font-semibold uppercase tracking-wide text-[var(--text-tertiary)]">
                      Nama Barang
                    </th>
                    <th className="text-left py-2 px-3 text-[14px] font-semibold uppercase tracking-wide text-[var(--text-tertiary)]">
                      Kode
                    </th>
                    <th className="text-left py-2 px-3 text-[14px] font-semibold uppercase tracking-wide text-[var(--text-tertiary)]">
                      Status
                    </th>
                    <th className="text-left py-2 px-3 text-[14px] font-semibold uppercase tracking-wide text-[var(--text-tertiary)]">
                      Kondisi
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {recentAssets.map((asset, index) => (
                    <tr
                      key={asset.kode}
                      className="border-b border-[var(--separator)] last:border-0 hover:bg-[var(--color-hover)] transition-colors"
                      style={{ animationDelay: `${0.5 + index * 0.1}s` }}
                    >
                      <td className="py-2.5 px-3">
                        <Text variant="body" className="font-medium">
                          {asset.nama}
                        </Text>
                      </td>
                      <td className="py-2.5 px-3">
                        <Text variant="subhead" color="secondary" className="font-mono">
                          {asset.kode}
                        </Text>
                      </td>
                      <td className="py-2.5 px-3">
                        <StatusBadge status={asset.status} />
                      </td>
                      <td className="py-2.5 px-3">
                        <KondisiBadge kondisi={asset.kondisi} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </AnimatedCard>
        </FadeIn>

        {/* Sidebar - Quick Actions & Recent Activity */}
        <FadeIn delay={0.5} className="space-y-4">
          {/* Quick Actions - Compact */}
          <AnimatedCard delay={0.5} hover={false} className="p-4">
            <Text variant="headline" as="h2" className="mb-3">
              Quick Actions
            </Text>

            <div className="space-y-2">
              {quickActions.map((action) => (
                <GlassButton
                  key={action.label}
                  variant="secondary"
                  size="md"
                  className="w-full justify-start"
                >
                  <action.icon className="h-4 w-4" />
                  {action.label}
                </GlassButton>
              ))}
            </div>
          </AnimatedCard>

          {/* Recent Activity - Compact */}
          <AnimatedCard delay={0.6} hover={false} className="p-4">
            <Text variant="headline" as="h2" className="mb-3">
              Aktivitas Terbaru
            </Text>

            <div className="space-y-2">
              {activities.map((activity, index) => (
                <div
                  key={index}
                  className="flex items-start gap-2 p-1.5 rounded-lg hover:bg-[var(--color-hover)] transition-colors"
                >
                  <div className="p-1.5 rounded-md bg-[var(--color-info-bg)] shrink-0">
                    <activity.icon className="h-4 w-4 text-[var(--accent-blue)]" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <Text variant="body" className="line-clamp-1">
                      {activity.text}
                    </Text>
                    <Text variant="subhead" color="tertiary">
                      {activity.time}
                    </Text>
                  </div>
                </div>
              ))}
            </div>
          </AnimatedCard>
        </FadeIn>
      </div>
    </PageTransition>
  );
}
