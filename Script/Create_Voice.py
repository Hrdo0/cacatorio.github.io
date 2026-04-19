
from google import genai
from google.genai import types # Importiamo anche i tipi per la configurazione
import edge_tts
import asyncio
import os
import requests
import json
import base64







'''
Nome: it-IT-GiuseppeMultilingualNeural - Genere: Male
Nome: it-IT-DiegoNeural - Genere: Male
Nome: it-IT-ElsaNeural - Genere: Female
Nome: it-IT-IsabellaNeural - Genere: Female
'''

sub_prompt = '''
La seguente è una classifica cacatoria, ogni numero corrisponde al numero di cacate che ha fatto una persona nell'arco di un mese,commentala come se fossi un telecronista sportivo particolarmente scurrile e colorito. Il testo che mi restituirai verrà dato in pasto ad un text-to-speech quindi non usare emoji e non essere particolarmente prolisso, non usare termini inglesi e non usare simboli come "*" o "#":\n
'''
classifica = '''
Lellino : 64
 giulia Zizzania : 36
Antonio : 32
Maria Frittatina : 19
 Martina Stinga : 17
 Peppe DR : 17
 Massimiliano : 16
 Mota : 15
Erika : 12
 Peppe Catalano : 12
 Dario : 10
 Gian : 6
 Giulia Aprea : 4
 Valerio : 2
 Roberto Ripa : 1
 '''

def list_my_models(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print("MODELLI DISPONIBILI PER LA TUA CHIAVE:")
        for m in models:
            
            print(f"- {m['name'].split('/')[-1]}")
    else:
        print(f"Errore nel recupero lista: {response.status_code}")


def get_comment_from_gemini(prompt: str) -> str:
    def get_api_key():
        with open("key.txt", "r") as f:
            return f.read().strip()
    # gemini-2.5-flash 
    api_key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        if response.status_code == 200:
            #sTRUTTURA RISPOSTA
            return response_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Errore {response.status_code}: {response_json.get('error', {}).get('message', 'Errore')}"
            
    except Exception as e:
        return f"Errore: {e}"


async def parla_pro(testo: str, voce: str = "it-IT-GiuseppeNeural") -> None:
    communicate = edge_tts.Communicate(testo, voce)
    await communicate.save(r"shit_files\audio_cacatorio.mp3")

    #riproduce
    os.system(r"shit_files\audio_cacatorio.mp3")

def upload_to_github_api(file_path,git_name, branch="main"):
        token = "TOKEN_GIT" #DISABLED FOR GIT PUSH
        repo_owner=""
        repo_name=""
        
        with open(file_path, "rb") as file:
            content = file.read()

        # GitHub vuole il contenuto codificato in Base64
        content_base64 = base64.b64encode(content).decode("utf-8")

        # make url
        
        file_name_in_repo = git_name
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name_in_repo}"

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Se esiste ottengo 'sha' 

        response = requests.get(url, headers=headers)
        sha = ""
        if response.status_code == 200:
            sha = response.json().get("sha", "")

        
        data = {
            "message": "Update automatico via script",
            "content": content_base64,
            "branch": branch
        }
        if sha:
            data["sha"] = sha # Necessario se il file esiste già

        # Invio PUT
        put_response = requests.put(url, headers=headers, data=json.dumps(data))

        if put_response.status_code in [200, 201]:
            print(f"File '{file_name_in_repo}' caricato con successo!")
        else:
            print(f"Errore: {put_response.json()}")


if __name__ == "__main__":
    '''
    it-IT-GiuseppeMultilingualNeural - Genere: Male
    it-IT-DiegoNeural - Genere: Male
    it-IT-ElsaNeural - Genere: Female
    it-IT-IsabellaNeural - Genere: Female
    '''
    prompt = "Dimmi quattro parole"
    #prompt = sub_prompt+classifica
    testo = get_comment_from_gemini(prompt=prompt)
    print(testo)
    asyncio.run(parla_pro(testo, "it-IT-GiuseppeMultilingualNeural"))
    #upload_to_github_api(file_path="audio_cacatorio.mp3",git_name="audio_cacatorio.mp3")
