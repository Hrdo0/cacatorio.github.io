import datetime
import time
import json
import calendar

def rimuovi_chiavi_vuote_da_lista(lista_diz):
  """
  Rimuove le chiavi con valori vuoti da una lista di dizionari.

  Args:
    lista_diz: Una lista di dizionari.

  Returns:
    Nessun valore, modifica i dizionari nella lista per riferimento.
  """
  chiavi_da_rimuovere = set()

  for dizionario in lista_diz:
    for chiave in dizionario.keys():
      valori_vuoti = True
      for diz in lista_diz:
        if diz[chiave]:
          valori_vuoti = False
          break

      if valori_vuoti:
        chiavi_da_rimuovere.add(chiave)

  for dizionario in lista_diz:
    for chiave in chiavi_da_rimuovere:
      del dizionario[chiave]

def getMonthsBetween(data_inizio, data_fine)-> list[str]:
    # nomi_mesi = [
    #     "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    #     "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
    # ]
    if data_inizio > data_fine:
        raise ValueError("Start date cannot be after end date")

    data_corrente = data_inizio
    months = []

    while data_corrente <= data_fine:
        month_name = data_corrente.strftime("%B")
        if month_name not in months:
            months.append(month_name)
        if data_corrente.month == 12:
            data_corrente = data_corrente.replace(year=data_corrente.year + 1, month=1)
        else:
            data_corrente = data_corrente.replace(month=data_corrente.month + 1)

    return months

def getMonthDates(month, year=None) -> list[str]:
    if year is None:
        year = datetime.datetime.now().year
    
    nomi_mesi = [
        "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
        "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
    ]
    month_names = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
    
    if isinstance(month, int):
        month_idx = month
    elif isinstance(month, str):
        if month in nomi_mesi:
            month_idx = nomi_mesi.index(month) + 1
        elif month in month_names:
            month_idx = month_names.index(month) + 1
        else:
            return []
    else:
        raise ValueError("Valore mese non valido")

    _, last_day = calendar.monthrange(year, month_idx)
    dates = []
    for day in range(1, last_day + 1):
        # yr_short prende le ultime due cifre dell'anno (es: 24, 25, 26)
        yr_short = str(year)[-2:]
        # Formattazione dd/mm/yy per combaciare con la chat
        date_str = f"{day:02d}/{month_idx:02d}/{yr_short}"
        dates.append(date_str)

    return dates

def clean_shitter_name(shitter):
    if "Hrdo" in shitter:
        return "Valerio"
    elif "Claudia" in shitter:
        return "Claudia"
    elif " Lorenza" in shitter:
        return "Lorenza"
    elif " AntoFritto" in shitter:
        return "Antonio"
    elif "334 987 5975" in shitter:
        return " Meme"
    elif "rob" in shitter:
        return "Roberto Ripa"
    elif "389 443 6330" in shitter:
        return "Ilario"
    elif "351 651 4520" in shitter:
        return "Giorgio"
    elif "351 651 4520" in shitter:
        return "Valentina"
    elif "342 562 2135" in shitter:
        return "Giulia Zizzania"
    elif "334 165 1870" in shitter:
        return "Raffaele"
    elif "333 654 3573" in shitter:
        return "Sblorc"
    elif "Mothi" in shitter:
        return "Martina Stinga"
    elif "Sarrr" in shitter:
        return "Sara Gargiulo"
    elif "Peppe Google " in shitter:
        return "Peppe Catalano"
    elif "379 178 3015" in shitter: 
        return "Simone"
    elif "Cipiciappola" in shitter: 
        return "Erika"
    elif "Maria" in shitter: 
        return "Maria Frittatina"
    elif "Catello" in shitter: 
        return "Lellino"
    else:
        return shitter

def merge_dictionaries(*input_dicts):
    merged_dict = {}
    for d in list(input_dicts):
        for key, value in d.items():
            if key not in merged_dict:
                merged_dict[key] = value
            else:
                if isinstance(merged_dict[key], list) and isinstance(value, list):
                    merged_dict[key].extend(value)
    return merged_dict

def isDateTimeInRange(datetime_str:str, data_inizio:datetime, data_fine:datetime, mode:str) ->bool: 
    try:
        date_object = string2DateTime(datetime_str)
        if mode == "pm":
            if date_object.month == 1:
                date_object = date_object.replace(year=date_object.year-1, month=12)
            else:
                date_object = date_object.replace(month=date_object.month - 1)
        
        return data_inizio <= date_object <= data_fine
    except:
        return False

def getCalendarRange():
    y = datetime.datetime.now().year
    mode ="1"
    current_time = datetime.datetime.now()
    if mode == "1":
        month = current_time.month
        day = current_time.day
        data_inizio = datetime.datetime(y,month,1)
        data_fine = datetime.datetime(y,month,day)
    else:
        data_inizio = input("Inserisci data iniziale dd/mm\n")
        day,month= data_inizio.split("/")
        data_inizio = datetime.datetime(y,int(month),int(day))
        data_fine = input("Inserisci data finale dd/mm/yy\n")
        day,month= data_fine.split("/")
        data_fine = datetime.datetime(y,int(month),int(day))

    return data_inizio, data_fine

def getMonthFromDatetime(data : datetime , name = True):
    mesi_inglesi = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November","December"]
    mese= data.month
    if name == True:   
        return mesi_inglesi[mese - 1]
    else:
        return mese

def string2DateTime(stringa_data_ora):
    fmts = ["%d/%m/%y %H:%M", "%d/%m/%Y %H:%M", "%d/%m/%y, %H:%M", "%d/%m/%Y, %H:%M"]
    for fmt in fmts:
        try:
            return datetime.datetime.strptime(stringa_data_ora, fmt)
        except:
            continue
    
    parti = stringa_data_ora.replace(",","").split("/")
    giorno = int(parti[0])
    mese = int(parti[1])
    anno_stringa = parti[2].split()[0]
    if len(anno_stringa) == 2:
        anno = int(anno_stringa) + 2000
    else:
        anno = int(anno_stringa)
    try:
        ora_min = parti[2].split()[1].split(":")
        ora = int(ora_min[0])
        minuti = int(ora_min[1])
    except:
        ora = 0
        minuti = 0
    return datetime.datetime(anno, mese, giorno, ora, minuti)

'''
This code was written by Valerio Accardo, 
all rights on the shit that will be monitored 
belong to him and him alone
'''
if __name__ == "__main__":
    data_inizio = datetime.datetime(2025,1,1)
    data_fine = datetime.datetime(2025,1,30)
    print(getMonthsBetween(data_inizio,data_fine))