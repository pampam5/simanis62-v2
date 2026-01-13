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
import {
    GlassButton,
    GlassInput,
    Text,
    PageTransition,
    FadeIn,
} from '@/components/ui';
// We need to export MacOS components from ui/index.ts or import directly
// Since I haven't updated ui/index.ts to export MacOSCards/Table yet, I might need to update that first or import from specific files.
// Let's assume I will update ui/index.ts shortly or use specific imports for now.
// Actually, better to check ui/index.ts. I saw it earlier, it had many files but I didn't verify exports.
// I will import from specific files to be safe, then clean up.
// Wait, I should assume I can import from '@/components/ui' if I update the index.
// I'll stick to specific file imports for the new components to avoid errors if index isn't updated.
import { MacOSStatCard, MacOSStatsGrid, MacOSSectionCard, MacOSActivityItem } from '@/components/ui/macos-cards';
import { MacOSTable, MacOSTableHeader, MacOSTableHead, MacOSTableBody, MacOSTableRow, MacOSTableCell, MacOSTableBadge } from '@/components/ui/macos-table';

export function MacOSDashboardPage() {
    const stats = [
        {
            label: 'Total Aset',
            value: '1,234',
            icon: Package,
            trend: { value: 12, label: 'vs last month' }
        },
        {
            label: 'Kondisi Baik',
            value: '1,089',
            icon: CheckCircle,
            iconColor: 'text-[#34C759]',
            iconBgColor: 'bg-[#34C759]/10',
            trend: { value: 5, label: 'vs last month' }
        },
        {
            label: 'Kondisi Rusak',
            value: '145',
            icon: AlertCircle,
            iconColor: 'text-[#FF3B30]',
            iconBgColor: 'bg-[#FF3B30]/10',
            trend: { value: -2, label: 'vs last month' }
        },
        {
            label: 'Total Nilai',
            value: 'Rp 15.5M',
            icon: DollarSign,
            iconColor: 'text-[#FF9500]',
            iconBgColor: 'bg-[#FF9500]/10',
            trend: { value: 8, label: 'vs last month' }
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
        <PageTransition className="p-6 lg:p-8 space-y-8 max-w-[1600px] mx-auto">
            {/* Header */}
            <FadeIn>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div>
                        <Text variant="large-title" as="h1" className="font-bold tracking-tight">
                            Dasbor
                        </Text>
                        <Text variant="body" color="secondary" className="mt-1">
                            Selamat datang kembali di Simanis Asset Management
                        </Text>
                    </div>

                    <div className="flex flex-wrap gap-3">
                        <GlassButton variant="secondary" size="md">
                            <Download className="h-4 w-4" />
                            Ekspor
                        </GlassButton>
                        <GlassButton variant="primary" size="md" className="shadow-lg shadow-blue-500/20">
                            <Plus className="h-4 w-4" />
                            Aset Baru
                        </GlassButton>
                    </div>
                </div>
            </FadeIn>

            {/* Stats Grid */}
            <MacOSStatsGrid>
                {stats.map((stat, index) => (
                    <MacOSStatCard
                        key={stat.label}
                        label={stat.label}
                        value={stat.value}
                        icon={stat.icon}
                        iconColor={stat.iconColor}
                        iconBgColor={stat.iconBgColor}
                        trend={stat.trend}
                        delay={index * 0.1}
                    />
                ))}
            </MacOSStatsGrid>

            {/* Search Bar - Full Width Glass */}
            <FadeIn delay={0.3}>
                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-tertiary z-10" />
                    <GlassInput
                        className="pl-12 h-12 text-lg rounded-xl shadow-sm bg-white/50 backdrop-blur-xl border-black/5"
                        placeholder="Search assets, locations, or reference codes..."
                    />
                    <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-2">
                        <div className="px-2 py-1 rounded-md bg-black/5 text-xs text-secondary font-medium">⌘K</div>
                    </div>
                </div>
            </FadeIn>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 items-start">
                {/* Recent Assets Table */}
                <FadeIn delay={0.4} className="xl:col-span-3">
                    <MacOSSectionCard
                        title="Aset Terbaru"
                        subtitle="Pembaruan inventaris terkini"
                        action={
                            <GlassButton variant="ghost" size="sm" className="text-blue-500 hover:text-blue-600">
                                Lihat Semua
                            </GlassButton>
                        }
                        className="min-h-[400px]"
                    >
                        <MacOSTable className="shadow-none border-0 bg-transparent">
                            <MacOSTableHeader className="bg-transparent border-b border-black/5">
                                <MacOSTableRow>
                                    <MacOSTableHead>Nama Aset</MacOSTableHead>
                                    <MacOSTableHead>Kode</MacOSTableHead>
                                    <MacOSTableHead>Status</MacOSTableHead>
                                    <MacOSTableHead>Kondisi</MacOSTableHead>
                                </MacOSTableRow>
                            </MacOSTableHeader>
                            <MacOSTableBody>
                                {recentAssets.map((asset, i) => (
                                    <MacOSTableRow key={i} onClick={() => { }} className="cursor-pointer hover:bg-black/5">
                                        <MacOSTableCell className="font-medium">{asset.nama}</MacOSTableCell>
                                        <MacOSTableCell mono className="text-secondary">{asset.kode}</MacOSTableCell>
                                        <MacOSTableCell>
                                            <MacOSTableBadge variant={asset.status === 'Aktif' || asset.status === 'Baru' ? 'success' : 'warning'}>
                                                {asset.status}
                                            </MacOSTableBadge>
                                        </MacOSTableCell>
                                        <MacOSTableCell>
                                            <MacOSTableBadge variant={asset.kondisi === 'Baik' ? 'info' : 'error'}>
                                                {asset.kondisi}
                                            </MacOSTableBadge>
                                        </MacOSTableCell>
                                    </MacOSTableRow>
                                ))}
                            </MacOSTableBody>
                        </MacOSTable>
                    </MacOSSectionCard>
                </FadeIn>

                {/* Sidebar - Actions & Activity */}
                <FadeIn delay={0.5} className="space-y-6">
                    <MacOSSectionCard
                        title="Quick Actions"
                        className="p-5"
                    >
                        <div className="space-y-3">
                            {quickActions.map((action) => (
                                <GlassButton
                                    key={action.label}
                                    variant="secondary"
                                    className="w-full justify-start h-11 text-base shadow-sm"
                                >
                                    <div className="p-1.5 rounded-md bg-blue-50 text-blue-600 mr-2">
                                        <action.icon className="h-4 w-4" />
                                    </div>
                                    {action.label}
                                </GlassButton>
                            ))}
                        </div>
                    </MacOSSectionCard>

                    <MacOSSectionCard
                        title="Aksi Cepat"
                        className="p-5"
                    >
                        <div className="space-y-3">
                            {quickActions.map((action) => (
                                <GlassButton
                                    key={action.label}
                                    variant="secondary"
                                    className="w-full justify-start h-11 text-base shadow-sm"
                                >
                                    <div className="p-1.5 rounded-md bg-blue-50 text-blue-600 mr-2">
                                        <action.icon className="h-4 w-4" />
                                    </div>
                                    {action.label}
                                </GlassButton>
                            ))}
                        </div>
                    </MacOSSectionCard>

                    <MacOSSectionCard
                        title="Aktivitas"
                        className="p-5"
                    >
                        <div className="space-y-4">
                            {activities.map((activity, i) => (
                                <MacOSActivityItem
                                    key={i}
                                    title={activity.text}
                                    time={activity.time}
                                />
                            ))}
                        </div>
                    </MacOSSectionCard>
                </FadeIn>
            </div>
        </PageTransition>
    );
}
