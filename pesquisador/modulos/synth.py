import re
import google.generativeai as genai

def tech_generator(resume, theme):
    # Limpeza dos textos
    clean_resume = []
    for t in resume:
        t_clean = re.sub(r"(archive_\d+)", "", t)  # remove tags de arquivo
        t_clean = re.sub(r"\n+", "\n", t_clean)    # remove quebras de linha extras
        clean_resume.append(t_clean.strip())

    joined = "\n".join(clean_resume)  # mantém quebras de linha

    # Modelo
    module = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt reforçado para instruções obrigatórias
    prompt = f"""
Você é um pesquisador técnico. Com base nos textos abaixo, elabore um relatório técnico coeso sobre o tema '{theme}'.

REGRAS OBRIGATÓRIAS (siga rigorosamente):
1. Todo título principal que estiver marcado como '##' deve ser substituído por '$' e deve ser centralizado, o '$' deverá estar apenas no inicio como sinalização.
2. Todo subtítulo que estiver marcado como '###' (ou '##' secundário) deve ser substituído por '#' e alinhado à esquerda,o '#' deverá estar apenas no inicio como sinalização.
3. Subtópicos iniciados com '*' ou '**' devem ser preservados, e o negrito '**' deve ser mantido.
4. Não altere nenhuma outra estrutura do texto.
5. Escreva de forma formal e científica, mantendo a estrutura de títulos, subtítulos e negrito.
6. Integre citações simuladas no formato (Autor, Ano) quando possível.
7. Todo texto normal (não título ou subtítulo) deve ser mantido como parágrafo corrido, respeitando as quebras de linha existentes.

TEXTOS PARA INTEGRAÇÃO:
{joined}

OUTPUT:
- Use '$' apenas para títulos principais.
- Use '#' apenas para subtítulos.
- Preserve '*' e '**' nos subtópicos.
- Não faça outras alterações nos marcadores.
"""

    try:
        resposta = module.generate_content(prompt)
        return resposta.text
    except Exception as e:
        print(f"❌ Error in generation: {e}")
        return ""
