import { MacOSTitleBarCompact } from "@/components/layout/macos-title-bar";
import { Text } from "@/components/ui/text";

export function AssetsPage() {
    return (
        <div className="flex flex-col h-full bg-[#F5F5F7] dark:bg-black">
            <div className="p-8">
                <h1 className="text-2xl font-semibold mb-2 text-gray-900 dark:text-white">Daftar Aset</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                    Kelola seluruh aset daerah di sini.
                </p>

                <div className="mt-8 p-12 border-2 border-dashed border-gray-300 rounded-xl flex items-center justify-center">
                    <p className="text-gray-400">Konten Daftar Aset akan segera hadir</p>
                </div>
            </div>
        </div>
    );
}
