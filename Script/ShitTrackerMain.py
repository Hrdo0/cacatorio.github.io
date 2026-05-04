import datetime
from Bathroom import Bathroom, Chat
from ShitGraph import createPdf
import traceback
import asyncio
from Create_Voice import upload_to_github_api,get_comment_from_gemini,parla_pro




# sub_prompt = '''
# La seguente è una classifica cacatoria, ogni numero corrisponde al numero di cacate che ha fatto una persona nell'arco di un mese,commentala come se fossi un telecronista sportivo particolarmente scurrile e colorito, usa un sacco di parolacce ed eufemismi relativi al gabinetto. 
# Attenzione perchè questo mese è molto particolare, questo mese la vittoria non se la aggiudicherà colui il quale avrà fatto piu cacate bensi il criterio rimarrà segreto fino a domani
# Il testo che mi restituirai verrà dato in pasto ad un text-to-speech quindi non usare emoji e non essere particolarmente prolisso, non usare termini inglesi e non usare simboli come "*" o "#":\n
# '''

sub_prompt = '''
La seguente è una classifica cacatoria, ogni numero corrisponde al numero di cacate che ha fatto una persona. Questo mese il criterio di premiazione è rimasto segreto fino alla fine ed ora dobbiamo rivelarlo assieme al vincitore che si porta a casa il grande premio dell'ediziona pasquale. 
Il criterio è : NUMERO DI CACATE EFFETTUATE TRA LE 17 E LE 17.59. 
I risultati sono i seguenti, annunciali partendo dal fondo della classifica e metti molta mooolta enfasi nel rivelare il vincitore come se fossi un telecronista sportivo particolarmente scurrile e colorito, usa un sacco di parolacce ed eufemismi relativi al gabinetto. 
Il testo che mi restituirai verrà dato in pasto ad un text-to-speech quindi non usare emoji e non essere particolarmente prolisso, non usare termini inglesi e non usare simboli come "*" o "#":\n

Lellino : 6
 giulia Zizzania : 6
Antonio : 4
Martina Stinga : 1
 Massimiliano : 5
Maria Frittatina : 0
 Mota : 0
 Peppe DR : 1
Peppe Catalano : 4
Valerio : 1
Erika : 1
 Dario : 1
 Giulia Aprea : 1
La Julia : 1
'''
PROMPT = sub_prompt
UPLOAD_GIT_FLAG = True

if __name__ == "__main__":
    # DATETIME.DATETIME(ANNO , MESE, GIORNO)
    data_inizio  = datetime.datetime(year = 2026, month = 4, day = 1)
    data_fine =  datetime.datetime(year = 2026, month = 4, day = 30)# datetime.datetime.now()
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
            
            testo = get_comment_from_gemini(prompt=PROMPT)
            print(testo)
            asyncio.run(parla_pro(testo, "it-IT-DiegoNeural"))
            #upload_to_github_api(file_path="audio_cacatorio.mp3",git_name="audio_cacatorio.mp3")

    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except Exception as e:
        print(f"Si è verificato un errore imprevisto: {e}")
        traceback.print_exc()


        