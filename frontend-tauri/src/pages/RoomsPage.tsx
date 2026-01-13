import { Text } from "@/components/ui/text";

export function RoomsPage() {
    return (
        <div className="flex flex-col h-full bg-[#F5F5F7] dark:bg-black">
            <div className="p-8">
                <Text variant="title-1" className="mb-2">Ruangan</Text>
                <Text variant="body" color="secondary">
                    Daftar ruangan dan lokasi aset.
                </Text>

                <div className="mt-8 p-12 border-2 border-dashed border-gray-300 rounded-xl flex items-center justify-center">
                    <Text variant="body" color="tertiary">Konten Ruangan akan segera hadir</Text>
                </div>
            </div>
        </div>
    );
}
