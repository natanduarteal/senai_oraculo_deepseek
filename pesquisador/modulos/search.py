import requests
import os
from dotenv import load_dotenv

load_dotenv() 
api_key = os.environ.get("SERPER_API_KEY")
def search(theme):
    query = theme.replace(" ", "+")
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "q": f"{query} filetype:pdf"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    links = []
    if "organic" in data:
        for item in data["organic"]:
            link = item.get("link")
            if link and ".pdf" in link:
                links.append(link)
    return links

def donwload_pdfs(links, output_dir="data/raw"):
    os.makedirs(output_dir,exist_ok=True)
    archives=[]

    for i,link in enumerate(links):
        try:
            print(f"donwloading: {link}")
            response=requests.get(link,timeout=30)

            if response.status_code == 200 and "pdf" in response.headers.get("content-type", ""):
                archive_name= os.path.join(output_dir,f"archive_{i+1}.pdf")
                with open(archive_name,"wb") as f:
                    f.write(response.content)
                    archives.append(archive_name)
                    print(f"saved archive: {archive_name}")
            else:
                print("Non valid pdf")
        except Exception as e:
            print(f"issues with the link: {link} Error:{e}")
    return archives


if __name__ == "__main__":
    tema = "produção de metanol e impactos"
    pdf_links = search(tema)
    arquivos_baixados = donwload_pdfs(pdf_links)
    print("\nArquivos baixados:")
    for arq in arquivos_baixados:
        print(" -", arq)