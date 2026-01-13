import { Text } from "@/components/ui/text";

export function KIBPage() {
    return (
        <div className="flex flex-col h-full bg-[#F5F5F7] dark:bg-black">
            <div className="p-8">
                <Text variant="title-1" className="mb-2">Laporan KIB</Text>
                <Text variant="body" color="secondary">
                    Laporan Kartu Inventaris Barang (A, B, C, D, E, F).
                </Text>

                <div className="mt-8 p-12 border-2 border-dashed border-gray-300 rounded-xl flex items-center justify-center">
                    <Text variant="body" color="tertiary">Konten Laporan KIB akan segera hadir</Text>
                </div>
            </div>
        </div>
    );
}
