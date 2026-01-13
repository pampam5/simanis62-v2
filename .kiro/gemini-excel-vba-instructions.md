# Panduan Penggunaan Gemini Excel VBA

Tools `gemini-excel-vba` yang ada di folder `tools` Anda adalah sebuah **Excel Add-in (VBA)**, bukan sebuah MCP Server. Oleh karena itu, tools ini tidak bisa ditambahkan ke `mcp.json` untuk dijalankan oleh AI Agent secara otomatis. Tools ini dirancang untuk dijalankan langsung di dalam Microsoft Excel oleh Anda.

## Cara Menginstall ke Excel

Berikut adalah langkah-langkah untuk mengaktifkannya di Excel Anda:

1.  **Dapatkan API Key Google Gemini**:
    *   Buka [Google AI Studio](https://aistudio.google.com/apikey).
    *   Buat API Key baru dan salin kuncinya.

2.  **Buka Excel**:
    *   Buka file Excel baru atau yang sudah ada.
    *   Tekan `Alt + F11` untuk membuka **VBA Editor**.

3.  **Import Module**:
    *   Di VBA Editor, klik kanan pada **VBAProject (Nama File Anda)** -> **Import File...**.
    *   Arahkan ke folder `d:\simanis62-v2\tools\gemini-excel-vba\src`.
    *   Import file-file berikut satu per satu:
        *   `Dictionary.cls`
        *   `JsonConverter.bas`
        *   `mGemini.bas`
        *   `mGeminiDemo.bas` (Opsional, untuk contoh)

4.  **Masukkan API Key**:
    *   Buka modul `mGemini` yang baru saja diimport.
    *   Cari baris kode: `Const GEMINI_API_KEY As String = "YOUR_API_KEY"`
    *   Ganti `"YOUR_API_KEY"` dengan API Key yang Anda dapatkan di langkah 1.

5.  **Gunakan Gemini di Excel**:
    *   **Rumus**: Ketik `=AskGemini("Pertanyaan Anda")` di dalam sel Excel.
    *   **Macro**: Tekan `Alt + F8`, pilih `Gemini`, lalu klik **Run**.

Tools ini sangat berguna untuk analisis data manual langsung di spreadsheet Anda!
