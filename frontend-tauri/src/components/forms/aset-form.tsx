/**
 * Form Tambah/Edit Aset KIB B
 * Sesuai dengan format BPAD DKI Jakarta
 */

import { useState, useEffect } from 'react';
import { Save, Loader2 } from 'lucide-react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
} from '@/components/ui/dialog';
import { GlassButton } from '@/components/ui/glass-button';
import { GlassInput } from '@/components/ui/glass-input';
import { Label } from '@/components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import { Text } from '@/components/ui/text';
import { asetService } from '@/services/aset-service';
import { ruanganService } from '@/services/ruangan-service';
import type { Aset, AsetCreate, AsetUpdate, Ruangan, KategoriKIB, Kondisi, AsalUsul } from '@/services/types';

interface AsetFormProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    aset?: Aset | null;
    onSuccess?: () => void;
}

const KONDISI_OPTIONS: Kondisi[] = ['Baik', 'Kurang Baik', 'Rusak Berat'];
const ASAL_USUL_OPTIONS: AsalUsul[] = ['Pembelian', 'Hibah', 'Sumbangan', 'Produksi'];
const KATEGORI_KIB_OPTIONS: KategoriKIB[] = ['A', 'B', 'C', 'D', 'E', 'F'];

export function AsetForm({ open, onOpenChange, aset, onSuccess }: AsetFormProps) {
    const isEdit = !!aset;

    const [formData, setFormData] = useState({
        kode_barang: '',
        nama_barang: '',
        nomor_register: 1,
        kategori_kib: 'B' as KategoriKIB,
        tahun_perolehan: new Date().getFullYear(),
        asal_usul: 'Pembelian' as AsalUsul,
        harga: 0,
        kondisi: 'Baik' as Kondisi,
        keterangan: '',
        ruangan_id: '',
        satuan: 'Unit',
        merk: '',
        tipe: '',
    });

    const [ruanganList, setRuanganList] = useState<Ruangan[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (open) {
            loadRuangan();
        }
    }, [open]);

    useEffect(() => {
        if (aset && open) {
            setFormData({
                kode_barang: aset.kode_barang,
                nama_barang: aset.nama_barang,
                nomor_register: aset.nomor_register,
                kategori_kib: aset.kategori_kib,
                tahun_perolehan: aset.tahun_perolehan,
                asal_usul: aset.asal_usul,
                harga: aset.harga,
                kondisi: aset.kondisi,
                keterangan: aset.keterangan || '',
                ruangan_id: aset.ruangan_id,
                satuan: 'Unit',
                merk: '',
                tipe: '',
            });
        } else if (!aset && open) {
            setFormData({
                kode_barang: '',
                nama_barang: '',
                nomor_register: 1,
                kategori_kib: 'B',
                tahun_perolehan: new Date().getFullYear(),
                asal_usul: 'Pembelian',
                harga: 0,
                kondisi: 'Baik',
                keterangan: '',
                ruangan_id: '',
                satuan: 'Unit',
                merk: '',
                tipe: '',
            });
        }
    }, [aset, open]);

    const loadRuangan = async () => {
        setIsLoading(true);
        try {
            const list = await ruanganService.getAllForDropdown();
            setRuanganList(list);
        } catch (err) {
            console.error('Failed to load ruangan:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleChange = (field: string, value: string | number) => {
        setFormData(prev => ({ ...prev, [field]: value }));
        setError(null);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setIsSubmitting(true);

        try {
            if (!formData.kode_barang.trim()) {
                throw new Error('Kode barang wajib diisi');
            }
            if (!formData.nama_barang.trim()) {
                throw new Error('Nama barang wajib diisi');
            }
            if (!formData.ruangan_id) {
                throw new Error('Ruangan wajib dipilih');
            }

            if (isEdit && aset) {
                const updateData: AsetUpdate = {
                    nama_barang: formData.nama_barang,
                    kondisi: formData.kondisi,
                    keterangan: formData.keterangan || undefined,
                    ruangan_id: formData.ruangan_id,
                    harga: formData.harga,
                };
                await asetService.update(aset.id, updateData);
            } else {
                const createData: AsetCreate = {
                    kode_barang: formData.kode_barang,
                    nama_barang: formData.nama_barang,
                    nomor_register: formData.nomor_register,
                    kategori_kib: formData.kategori_kib,
                    tahun_perolehan: formData.tahun_perolehan,
                    asal_usul: formData.asal_usul,
                    harga: formData.harga,
                    kondisi: formData.kondisi,
                    keterangan: formData.keterangan || undefined,
                    ruangan_id: formData.ruangan_id,
                };
                await asetService.create(createData);
            }

            onOpenChange(false);
            onSuccess?.();
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Gagal menyimpan aset';
            setError(message);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>{isEdit ? 'Edit Aset' : 'Tambah Aset Baru'}</DialogTitle>
                    <DialogDescription>
                        {isEdit ? 'Ubah data aset yang sudah ada' : 'Isi form berikut untuk menambah aset baru'}
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {error && (
                        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                            <Text variant="subhead" className="text-red-500">{error}</Text>
                        </div>
                    )}

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="kode_barang">Kode Barang *</Label>
                            <GlassInput
                                id="kode_barang"
                                placeholder="XX.XX.XX.XXXX"
                                value={formData.kode_barang}
                                onChange={(e) => handleChange('kode_barang', e.target.value)}
                                disabled={isEdit}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="nama_barang">Nama Barang *</Label>
                            <GlassInput
                                id="nama_barang"
                                placeholder="Nama barang"
                                value={formData.nama_barang}
                                onChange={(e) => handleChange('nama_barang', e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                        <div className="space-y-2">
                            <Label>Kategori KIB</Label>
                            <Select value={formData.kategori_kib} onValueChange={(v) => handleChange('kategori_kib', v)} disabled={isEdit}>
                                <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    {KATEGORI_KIB_OPTIONS.map((k) => (<SelectItem key={k} value={k}>KIB {k}</SelectItem>))}
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="tahun_perolehan">Tahun Perolehan</Label>
                            <GlassInput id="tahun_perolehan" type="number" min={1900} max={new Date().getFullYear()} value={formData.tahun_perolehan} onChange={(e) => handleChange('tahun_perolehan', parseInt(e.target.value))} disabled={isEdit} />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="nomor_register">No. Register</Label>
                            <GlassInput id="nomor_register" type="number" min={1} value={formData.nomor_register} onChange={(e) => handleChange('nomor_register', parseInt(e.target.value))} disabled={isEdit} />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Ruangan *</Label>
                            <Select value={formData.ruangan_id} onValueChange={(v) => handleChange('ruangan_id', v)}>
                                <SelectTrigger className="w-full"><SelectValue placeholder="Pilih ruangan" /></SelectTrigger>
                                <SelectContent>
                                    {ruanganList.map((r) => (<SelectItem key={r.id} value={r.id}>{r.nama_ruangan} ({r.kode_ruangan})</SelectItem>))}
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label>Asal Usul</Label>
                            <Select value={formData.asal_usul} onValueChange={(v) => handleChange('asal_usul', v)} disabled={isEdit}>
                                <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    {ASAL_USUL_OPTIONS.map((a) => (<SelectItem key={a} value={a}>{a}</SelectItem>))}
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="harga">Harga (Rp) *</Label>
                            <GlassInput id="harga" type="number" min={0} value={formData.harga} onChange={(e) => handleChange('harga', parseInt(e.target.value) || 0)} />
                        </div>
                        <div className="space-y-2">
                            <Label>Kondisi</Label>
                            <Select value={formData.kondisi} onValueChange={(v) => handleChange('kondisi', v)}>
                                <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    {KONDISI_OPTIONS.map((k) => (<SelectItem key={k} value={k}>{k}</SelectItem>))}
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="keterangan">Keterangan</Label>
                        <GlassInput id="keterangan" placeholder="Keterangan tambahan (opsional)" value={formData.keterangan} onChange={(e) => handleChange('keterangan', e.target.value)} />
                    </div>

                    <DialogFooter className="pt-4">
                        <GlassButton type="button" variant="ghost" onClick={() => onOpenChange(false)} disabled={isSubmitting}>Batal</GlassButton>
                        <GlassButton type="submit" variant="primary" disabled={isSubmitting}>
                            {isSubmitting ? (<><Loader2 className="h-4 w-4 animate-spin" />Menyimpan...</>) : (<><Save className="h-4 w-4" />{isEdit ? 'Simpan' : 'Tambah'}</>)}
                        </GlassButton>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
