import requests
import base64
import json

file_path = f"G:\Il mio Drive\ChatScriptShit\shit_reports\Shit_Tracker_31_3.pdf"
TOKEN = "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"
git_name = "pdf_cacatorio.pdf"

def upload_to_github_api(file_path,git_name, token, branch="main"):
       
        repo_owner="Hrdo0"
        repo_name="cacatorio.github.io"
        
        with open(file_path, "rb") as file:
            content = file.read()

        # 2. GitHub vuole il contenuto codificato in Base64
        content_base64 = base64.b64encode(content).decode("utf-8")

        # 3. Prepariamo l'URL per l'API di GitHub
        
        file_name_in_repo = git_name
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name_in_repo}"

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Se esiste ottengo sha 'sha' 

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
    

    upload_to_github_api(file_path=file_path,git_name=git_name,token=TOKEN)