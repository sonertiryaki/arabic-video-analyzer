from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime
import os


def create_excel(video_name: str, analysis_results: list):
    """
    Analiz sonuçlarından Excel dosyası oluşturur
    """

    wb = Workbook()
    ws = wb.active
    ws.title = "Analiz Sonuçları"

    # --------------------------------------------------
    # BAŞLIKLAR
    # --------------------------------------------------
    headers = [
        "Orijinal Arapça",
        "Harekesi Temizlenmiş Arapça",
        "Türkçe Anlam"
    ]

    header_font = Font(bold=True)

    ws.append(headers)
    for cell in ws[1]:
        cell.font = header_font

    # --------------------------------------------------
    # SATIRLAR
    # --------------------------------------------------
    for item in analysis_results:
        ws.append([
            item.get("arabic", ""),
            item.get("arabic_normalized", ""),
            item.get("turkish", "")
        ])

    # --------------------------------------------------
    # SÜTUN GENİŞLİKLERİ
    # --------------------------------------------------
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 40
    ws.column_dimensions["C"].width = 50

    # --------------------------------------------------
    # DOSYA ADI
    # --------------------------------------------------
    safe_video_name = video_name.replace(" ", "_").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{safe_video_name}_{timestamp}.xlsx"
    output_path = os.path.join("/tmp", file_name)

    wb.save(output_path)

    print(f"📁 Excel oluşturuldu: {output_path}")

    return output_path
