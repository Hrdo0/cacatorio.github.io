
#from google import genai
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
Lellino : 77
 giulia Zizzania : 45
Antonio : 39
Maria Frittatina : 22
Martina Stinga : 22
 Massimiliano : 21
 Peppe DR : 21
 Mota : 20
Erika : 13
Peppe Catalano : 12
 Dario : 12
 Giulia Aprea : 10
Valerio : 6
 Gian : 6
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
        with open(r"C:\Users\valer\OneDrive\Documenti\GitHub\cacatorio.github.io\Script\api_key.txt", "r") as f:
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
    prompt = '''Signori, signore, che spettacolo! Qui siamo in diretta per la classifica cacatoria del mese, e vi dico già che c'è stato un vero e proprio terremoto nel gabinetto!

Il campione indiscusso, il Re della tazza, Lellino! Settantasette scariche, settantasette bombe, ha polverizzato la concorrenza! Un uragano intestinale che ha lasciato tutti a bocca aperta e chiappe strette!

Sul secondo gradino del podio, si piazza Giulia Zizzania, con 45 sgasate di tutto rispetto. Ha cercato di tenere il ritmo, ma Lellino è un altro pianeta! E che dire di Antonio? Trentanove scariche, ha lottato con le unghie e con i denti per la zona podio, ma ha dovuto cedere il passo!

Poi abbiamo un bel gruppo compatto, una mischia furibonda! Maria Frittatina e Martina Stinga, un pari merito a 22 che sa di spareggio. Poco dietro, Massimiliano e Peppe DR, a 21, si sono dati battaglia per un punto, quasi gomito a gomito nel cesso! Mota, lì vicino a 20, si è difeso con onore, ma è rimasto staccato dal treno che contava.

Erika con 13 ha cercato di farsi vedere, ma è rimasta nelle retrovie. Peppe Catalano e Dario, un altro pari merito a 12, si sono accontentati di un piazzamento senza infamia e senza lode. Giulia Aprea, a quota 10, ha provato qualche allungo, ma non ha mai impensierito i primi!

E veniamo alle note dolenti, ai fantasmi del gabinetto! Valerio e Gian, a quota 6, hanno fatto il minimo sindacale, direi quasi... una cacata a settimana, che tristezza! Ma il cucchiaio di legno, il premio per la svogliatezza, va a lui: Roberto Ripa! Signori, UNA CACATA! UN'UNICA SCARICA IN UN MESE INTERO! Ma cos'hai mangiato, sassi? Dormivi sulla tazza? Una performance così imbarazzante che ci si chiede se abbia capito le regole del gioco!

Insomma, Lellino domina incontrastato, mentre per Roberto Ripa ci vuole un corso accelerato di igiene e alimentazione! Che mese, amici! Alla prossima scarica!'''
    #prompt = sub_prompt+classifica
    #testo = get_comment_from_gemini(prompt=prompt)
    testo = prompt
    print(testo)
    asyncio.run(parla_pro(testo, "it-IT-GiuseppeMultilingualNeural"))
    #upload_to_github_api(file_path="audio_cacatorio.mp3",git_name="audio_cacatorio.mp3")
