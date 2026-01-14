/**
 * Dialog Konfirmasi Hapus Aset
 * Dengan validasi alasan minimal 20 karakter
 */

import { useState } from 'react';
import { Trash2, Loader2, AlertTriangle } from 'lucide-react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
} from '@/components/ui/dialog';
import { GlassButton } from '@/components/ui/glass-button';

import { Label } from '@/components/ui/label';
import { Text } from '@/components/ui/text';
import { asetService } from '@/services/aset-service';
import type { Aset } from '@/services/types';

interface DeleteConfirmDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    aset: Aset | null;
    onSuccess?: () => void;
}

const MIN_REASON_LENGTH = 20;

export function DeleteConfirmDialog({ open, onOpenChange, aset, onSuccess }: DeleteConfirmDialogProps) {
    const [reason, setReason] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleDelete = async () => {
        if (!aset) return;

        setError(null);

        if (reason.trim().length < MIN_REASON_LENGTH) {
            setError(`Alasan penghapusan minimal ${MIN_REASON_LENGTH} karakter`);
            return;
        }

        setIsSubmitting(true);
        try {
            await asetService.delete(aset.id, reason.trim());
            setReason('');
            onOpenChange(false);
            onSuccess?.();
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Gagal menghapus aset';
            setError(message);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleClose = () => {
        setReason('');
        setError(null);
        onOpenChange(false);
    };

    const remainingChars = MIN_REASON_LENGTH - reason.trim().length;
    const isValid = remainingChars <= 0;

    return (
        <Dialog open={open} onOpenChange={handleClose}>
            <DialogContent className="max-w-md">
                <DialogHeader>
                    <div className="flex items-center gap-3">
                        <div className="p-2 rounded-full bg-red-500/10">
                            <AlertTriangle className="h-6 w-6 text-red-500" />
                        </div>
                        <div>
                            <DialogTitle>Hapus Aset</DialogTitle>
                            <DialogDescription>Tindakan ini tidak dapat dibatalkan</DialogDescription>
                        </div>
                    </div>
                </DialogHeader>

                <div className="space-y-4 py-4">
                    {aset && (
                        <div className="p-3 rounded-lg bg-[var(--color-hover)]">
                            <Text variant="subhead" color="secondary">Aset yang akan dihapus:</Text>
                            <Text variant="body" className="font-medium">{aset.nama_barang}</Text>
                            <Text variant="caption-1" color="tertiary">{aset.kode_barang}</Text>
                        </div>
                    )}

                    {error && (
                        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                            <Text variant="subhead" className="text-red-500">{error}</Text>
                        </div>
                    )}

                    <div className="space-y-2">
                        <Label htmlFor="reason">Alasan Penghapusan *</Label>
                        <textarea
                            id="reason"
                            className="w-full min-h-[100px] p-3 rounded-lg border border-[var(--separator)] bg-[var(--color-hover)] text-[var(--text-primary)] placeholder:text-[var(--text-tertiary)] focus:outline-none focus:ring-2 focus:ring-[var(--accent-blue)] resize-none"
                            placeholder="Jelaskan alasan penghapusan aset ini..."
                            value={reason}
                            onChange={(e) => {
                                setReason(e.target.value);
                                setError(null);
                            }}
                        />
                        <Text variant="caption-1" color={isValid ? 'secondary' : 'tertiary'}>
                            {isValid
                                ? `✓ ${reason.trim().length} karakter`
                                : `Minimal ${remainingChars} karakter lagi`}
                        </Text>
                    </div>
                </div>

                <DialogFooter>
                    <GlassButton type="button" variant="ghost" onClick={handleClose} disabled={isSubmitting}>
                        Batal
                    </GlassButton>
                    <GlassButton
                        type="button"
                        variant="primary"
                        className="bg-red-500 hover:bg-red-600"
                        onClick={handleDelete}
                        disabled={isSubmitting || !isValid}
                    >
                        {isSubmitting ? (
                            <><Loader2 className="h-4 w-4 animate-spin" />Menghapus...</>
                        ) : (
                            <><Trash2 className="h-4 w-4" />Hapus Aset</>
                        )}
                    </GlassButton>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
