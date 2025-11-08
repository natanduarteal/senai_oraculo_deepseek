from modulos.search import search, donwload_pdfs
from modulos.pdf_reader import pdf_reader
from modulos.gemini import analisar_texto
from modulos.synth import tech_generator
from modulos.report import generate_report
import os
def limpar_pastas(*pastas):
    for pasta in pastas:
        if os.path.exists(pasta):
            for arquivo in os.listdir(pasta):
                caminho = os.path.join(pasta, arquivo)
                try:
                    os.remove(caminho)
                    print(f"Removido: {caminho}")
                except Exception as e:
                    print(f"Não foi possível remover {caminho}: {e}")

def main():
    theme = input("digite seu tema:")

   
    limpar_pastas("data/raw", "data/processed")
    os.makedirs("data/processed", exist_ok=True)

    print("Buscando PDFs...")
    pdf_links = search(theme)
    if not pdf_links:
        print("Nenhum PDF encontrado")
        return


    print("Baixando PDFs...")
    pdf_files = donwload_pdfs(pdf_links)
    if not pdf_files:
        print("Falha no download dos PDFs")
        return
    print(f"{len(pdf_files)} PDFs baixados.")


    print("\nGerando resumo com Gemini...")
    resumo_total = ""
    for path in pdf_files:
        texto_bruto = pdf_reader(path)
        if texto_bruto.strip():
            resumo = analisar_texto(texto_bruto)
            resumo_total += resumo + "\n\n"

    if not resumo_total.strip():
        print("Nenhum resumo gerado!")
        return

  
    gemini_path = os.path.join("data/processed", "final_report.txt")
    with open(gemini_path, "w", encoding="utf-8") as f:
        f.write(resumo_total)
    print(f"Resumo do Gemini salvo em {gemini_path}")

  
    print("\n Processando síntese com Synth...")
    with open(gemini_path, "r", encoding="utf-8") as f:
        resumo_texto = f.read()

    synth_text = tech_generator(resumo_texto, theme)
    synth_path = os.path.join("data/processed", "synth_report.txt")
    with open(synth_path, "w", encoding="utf-8") as f:
        f.write(synth_text)
    print(f"Síntese do Synth salva em {synth_path}")


    print("\nGerando relatório PDF final...")
    generate_report(
        file_path=synth_path,
        tema=theme,               
        output_dir="outputs/reports"
    )
    print("Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
