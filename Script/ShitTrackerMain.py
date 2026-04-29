import datetime
from Bathroom import Bathroom, Chat
from ShitGraph import createPdf
import traceback
import asyncio
from Create_Voice import upload_to_github_api,get_comment_from_gemini,parla_pro




sub_prompt = '''
La seguente è una classifica cacatoria, ogni numero corrisponde al numero di cacate che ha fatto una persona nell'arco di un mese,commentala come se fossi un telecronista sportivo particolarmente scurrile e colorito, usa un sacco di parolacce ed eufemismi relativi al gabinetto. 
Attenzione perchè questo mese è molto particolare, questo mese la vittoria non se la aggiudicherà colui il quale avrà fatto piu cacate bensi il criterio rimarrà segreto fino a domani
Il testo che mi restituirai verrà dato in pasto ad un text-to-speech quindi non usare emoji e non essere particolarmente prolisso, non usare termini inglesi e non usare simboli come "*" o "#":\n
'''

UPLOAD_GIT_FLAG = True

if __name__ == "__main__":
    # DATETIME.DATETIME(ANNO , MESE, GIORNO)
    data_inizio  = datetime.datetime(year = 2026, month = 4, day = 1)
    data_fine =  datetime.datetime(year = 2026, month = 4, day = 29)# datetime.datetime.now()
    print("Inizializzazione Chat...")
    try:
        chat = Chat("Script/Chat WhatsApp con cacatorio.txt")
        bathroom = Bathroom(data_inizio=data_inizio, data_fine=data_fine, chat=chat)
        
        print("Analyzing data (Flush)...")
        bathroom.flush()
        classifica = bathroom.getClassifica()
        
        print("Generating JSON...")
        bathroom.createShitRegister()
        bathroom.createShitRegisterGlobal()
        
        print("\n--- CLASSIFICA ATTUALE ---")
        print(bathroom.getClassifica())
        
        print("...Sto Generando il PDF...")
        createPdf(bathroom,data_inizio,data_fine,upload = UPLOAD_GIT_FLAG)
        
        if UPLOAD_GIT_FLAG:
            
            testo = get_comment_from_gemini(prompt=sub_prompt+classifica)
            print(testo)
            asyncio.run(parla_pro(testo, "it-IT-DiegoNeural"))
            #upload_to_github_api(file_path="audio_cacatorio.mp3",git_name="audio_cacatorio.mp3")

    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except Exception as e:
        print(f"Si è verificato un errore imprevisto: {e}")
        traceback.print_exc()


        