import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()  # lê o .env
api_key = os.environ.get("OPENAI_API_KEY")

genai.configure(api_key=api_key)

def analisar_texto(texto, prompt_extra=""):
    prompt = f"""
    Leia o texto abaixo e gere uma análise crítica e resumida.
    Foque em causas, consequências e relações científicas.
    {prompt_extra}

    Texto:
    {texto[:12000]}  # limitar tamanho para caber no contexto
    """
    modelo = genai.GenerativeModel("gemini-2.5-flash-lite")
    resposta = modelo.generate_content(prompt)
    return resposta.text
