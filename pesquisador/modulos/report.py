import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

def generate_report(file_path, tema, output_dir="outputs/reports"):
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"{tema.replace(' ', '_')}_report.pdf")


    doc = SimpleDocTemplate(report_path, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elements = []


    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MainTitle', fontSize=20, leading=24, alignment=1, spaceAfter=12))
    
  
    if 'Bullet' not in styles:
        styles.add(ParagraphStyle(name='Bullet', fontSize=11, leftIndent=1*cm, leading=14, spaceAfter=4, alignment=4))
    else:
        styles['Bullet'].fontSize = 11
        styles['Bullet'].leftIndent = 1*cm
        styles['Bullet'].leading = 14
        styles['Bullet'].spaceAfter = 4
        styles['Bullet'].alignment = 4

    styles.add(ParagraphStyle(name='SubTitle', fontSize=14, leading=16, spaceAfter=8, leftIndent=0))
    styles.add(ParagraphStyle(name='NormalJustify', fontSize=11, leading=14, alignment=4))

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

    
        if line.startswith("$"):
            text = line[1:].strip()
            text = re.sub(r"\$(.*?)\$", r"<i>\1</i>", text)  
            text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)  
            elements.append(Paragraph(text, styles['MainTitle']))
            continue

        if line.startswith("#"):
            text = line[1:].strip()
            text = re.sub(r"\$(.*?)\$", r"<i>\1</i>", text)
            text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
            elements.append(Paragraph(text, styles['SubTitle']))
            continue

        if line.startswith("*"):
            text = line[1:].strip()
            text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
            text = re.sub(r"\$(.*?)\$", r"<i>\1</i>", text)
            elements.append(Paragraph(text, styles['Bullet']))
        else:
            text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            text = re.sub(r"\$(.*?)\$", r"<i>\1</i>", text)
            elements.append(Paragraph(text, styles['NormalJustify']))

        elements.append(Spacer(1,4))

    doc.build(elements)
    print(f"Relatório salvo em: {report_path}")


# TESTADOR INTERNO
if __name__ == "__main__":
    synth_path = "data/processed/synth_report.txt"
    if not os.path.exists(synth_path):
        print(f"Arquivo não encontrado: {synth_path}")
    else:
        generate_report(file_path=synth_path, tema="Python", output_dir="outputs/reports")
        print("Teste interno concluído, PDF gerado.")
