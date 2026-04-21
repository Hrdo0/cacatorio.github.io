import Shitter
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import json
from matplotlib.backends.backend_pdf import PdfPages
import datetime
from Bathroom import Bathroom, Chat, SHITTER_THRESHOLD
from miscellaneous import *
import os
import numpy as np
import scipy.stats as stats
import requests
import base64
import json


class ShitGraph():
    
    def __init__(self, shitter):
        self.shitter = shitter
        
    def getShitter(self):
        return self.shitter.getName()
    def getXvalues(self):
        return self.x_values
    def getYvalues(self):
        return self.y_values

    def addGraph2Pdf(self,pdf):
        pass

class GaussianChart(ShitGraph):

    def __init__(self, bathroom: Bathroom,data_inizio,data_fine):
        self.shitter_names = []
        self.shitter_counts = []
        
        for shitter in bathroom.getShitters():
            
            if len([shit for shit in shitter.getShits() if data_inizio <=shit.getDateTime(string=False)<= data_fine]) < SHITTER_THRESHOLD:
                continue
            
            self.shitter_names.append(shitter.getName())
            shits = shitter.getShits()
            self.shitter_counts.append(len([shit for shit in shits if data_inizio <=shit.getDateTime(string=False)<= data_fine]))
             

        self.counts_array = np.array(self.shitter_counts)
        
        #  Media (mu) Deviazione Standard (sigma)
        if len(self.counts_array) > 0:
            self.mu = np.mean(self.counts_array)
            self.sigma = np.std(self.counts_array)
        else:
            self.mu = 0
            self.sigma = 1
       #gestion caso limite
        if self.sigma == 0:
            self.sigma = 1.0
    def addGraph2Pdf(self, pdf):
        if not self.shitter_counts: return
        
    
        if not self.shitter_counts: return
        
        # Usa il figsize standard (6.4, 4.8 è il default di matplotlib)
        fig, ax = plt.subplots(figsize=(6.4, 4.8)) 
        # Riduciamo l'area del grafico per far stare la tabella a destra MA dentro la pagina
        plt.subplots_adjust(left=0.1, right=0.65, top=0.9)
        
        x_min, x_max = min(self.counts_array) - 20, max(self.counts_array) + 20
        x_axis = np.linspace(x_min, x_max, 500)
        y_axis = stats.norm.pdf(x_axis, self.mu, self.sigma)
        
        ax.plot(x_axis, y_axis, color='gray', linestyle='--', alpha=0.3)
        ax.fill_between(x_axis, y_axis, alpha=0.05, color='gray')
        ax.axvline(self.mu, color='red', linestyle=':', alpha=0.4)
        
        
        colormap = plt.colormaps['tab10']
        data_list = []
        for i, (name, count) in enumerate(zip(self.shitter_names, self.shitter_counts)):
            if count < SHITTER_THRESHOLD:
                continue

            data_list.append({
                'name': name, 
                'count': count, 
                'dist': abs(count - self.mu), 
                'color': colormap(i % 10)
            })
        
        # Ordino cacatori per distanza dalla media 
        data_sorted = sorted(data_list, key=lambda x: x['dist'])

        # --- DISEGNO  GAUSSIANA ---
        
        plot_order = sorted(data_list, key=lambda x: x['count'])
        for i, entry in enumerate(plot_order):
            y_pos = stats.norm.pdf(entry['count'], self.mu, self.sigma)
            
            # Punto sulla curva
            ax.plot(entry['count'], y_pos, marker='o', markersize=6, color=entry['color'], zorder=5)
            
            # Targhetta 
            y_levels = [25, 45, 65, 85, 105]
            current_y_off = y_levels[i % len(y_levels)]
            
            ax.annotate(f"{entry['name']} ({entry['count']})", 
                        xy=(entry['count'], y_pos),
                        xytext=(0, current_y_off), 
                        textcoords='offset points',
                        ha='center', va='bottom',
                        fontsize=7, fontweight='bold',
                        color=entry['color'],
                        bbox=dict(boxstyle="round,pad=0.2", fc='white', ec=entry['color'], alpha=0.8),
                        arrowprops=dict(arrowstyle='-', color=entry['color'], alpha=0.2))

        # --- CREAZIONE TABELLA  ---
        table_data = [["CACATORE", "CACATE"]]
        table_data.append(["MEDIA GLOBALE", f"{self.mu:.2f}"]) # Riferimento media
        
        for entry in data_sorted:
            table_data.append([entry['name'], str(entry['count'])])

        # Posizionamento tabella
        the_table = ax.table(cellText=table_data, 
                     colWidths=[0.4, 0.2], 
                     cellLoc='center', 
                     loc='right',
                     bbox=[1.1, 0.05, 0.5, 0.9])
        
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(8)
        
        # Coloriamo i nomi nella tabella per matching visivo
        for i, entry in enumerate(data_sorted):
            # riga i+2 (0 header, 1 media globale)
            the_table[(i + 2, 0)].get_text().set_color(entry['color'])
            the_table[(i + 2, 0)].get_text().set_weight('bold')

        # Estetica finale
        ax.set_title("GAUSSIANA CACATORIA", fontsize=12)
        ax.set_xlabel("CACATE")
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_ylim(0, max(y_axis) * 2.5) # Spazio per le targhette

        pdf.savefig(fig)
        plt.close()
    
    
class ShitTracker(ShitGraph):
    
    def __init__(self,shitter:Shitter):
        self.x_values= []
        self.y_values = []
        self.average = []
        self.stats = ""
        self.cm = ""

        with open("shitRegister.json","r") as file:
            shitRegister = json.load(file)
            
        self.shitter = shitter
        available_months = list(shitRegister["ByDateFormat"].keys())
        current_month = available_months[-1]
        self.cm = current_month
        
        try:
            previous_month = available_months[-2]
            self.pm = previous_month
        except:
            self.pm = current_month
            previous_month = current_month
        try:
            prev_prev_month = available_months[-3]
        except:
            prev_prev_month = current_month

        current_month_dict = shitRegister["ByDateFormat"][current_month]
        date_keys = list(current_month_dict.keys())
        self.x_values = [x[0:5] for x in date_keys]

        for data in date_keys:
            day_prefix = data[0:2]
            
            cacate_cm = len(current_month_dict[data].get(shitter.getName(), []))
            
            def get_val_for_day(m_name, d_prefix):
                for d_key, users in shitRegister["ByDateFormat"][m_name].items():
                    if d_key.startswith(d_prefix):
                        return len(users.get(shitter.getName(), []))
                return None

            vals_for_avg = [cacate_cm]
            val_pm = get_val_for_day(previous_month, day_prefix)
            if val_pm is not None: vals_for_avg.append(val_pm)
            val_ppm = get_val_for_day(prev_prev_month, day_prefix)
            if val_ppm is not None: vals_for_avg.append(val_ppm)  

            average_shit = sum(vals_for_avg) / len(vals_for_avg)
            self.y_values.append(cacate_cm)
            self.average.append(average_shit)
        
        unique_dates = []
        for shit in shitter.getShits():
            if shit.getDate() not in unique_dates:
                unique_dates.append(shit.getDate())
                
        average_month = sum(self.y_values)/len(self.x_values)
        average_global = len(shitter.getShits())/len(unique_dates)
        value_most = max(self.y_values)
        day_most = self.x_values[self.y_values.index(value_most)]
        
        is_actual_month = (datetime.datetime.now().strftime("%B") == current_month)
        limit = datetime.datetime.now().day if is_actual_month else len(self.y_values)
        no_shit_days = self.y_values[0:limit].count(0)

        # calcolo cadenza
        intervalli = []
        shits_list = shitter.getShits()
        num_occorrenze = len(shits_list)

        if num_occorrenze > 1:
            for i in range(num_occorrenze - 1):
                # Distanza in ore tra l'occorrenza i e la i+1
                differenza = shits_list[i+1].getDateTime(string=False) - shits_list[i].getDateTime(string=False)
                distanza_ore = differenza.total_seconds() / 3600
                intervalli.append(distanza_ore)
            
            cadenza_media = sum(intervalli) / num_occorrenze
        else:
            cadenza_media = 0
        #• Cadenza di evacuazione media : {round(cadenza_media,2)} ore\n\
        self.stats = f"STATISTICHE INTESTINALI DI {shitter.getName().upper()}:\n\
        • Media Cacatoria mese corrente: {round(average_month,2)} cacate/giorno \n\
        • Media Cacatoria globale: {round(average_global,2)} cacate/giorno\n\
        • Il giorno più proficuo di {shitter.getName()} è stato il {day_most} con ben {value_most} cacate\n\
        • Questo mese {shitter.getName()} ha trascorso ben {no_shit_days} giorni senza cacare"

    def getAverage(self):
        return self.average
    
    def addGraph2Pdf(self, pdf):
            shitter_name = self.shitter.getName()
            fig, ax = plt.subplots()
            plt.plot(self.getXvalues(), self.getYvalues(), label=f"{self.cm}")
            plt.plot(self.getXvalues(), self.getAverage(), alpha=0.4, label="media trimestre", color="grey")
            plt.xticks(rotation=45, fontsize=7)
            plt.ylabel(f"Cacate di {shitter_name}")
            plt.title(f'Cacate di {shitter_name}')
            plt.legend()
            
            stats = self.stats
            text_height = 0.2
            ax.annotate(stats, xy=(0.5, -text_height), xycoords='axes fraction',
                        ha='center', va='top', linespacing=1.3, fontsize=11,
                        bbox=dict(boxstyle="round", facecolor='white', alpha=0.7))

            pdf.savefig(bbox_inches='tight', pad_inches=0.3)
            plt.close()
    
class ShitBarGraph(ShitGraph):
    
    def __init__(self, shitter: Shitter,data_inizio,data_fine, month="all"):
        self.shitter = shitter
        self.x_values = ["{:02d}".format(num) for num in range(1, 25)]
        self.y_values = [0] * 24
        
        mesi_inglesi = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]

        if month == "all":
            shits = shitter.getShits()
        else:
            #shits = [shit for shit in shitter.getShits() if getMonthFromDatetime(shit.getDateTime(string=False)) == month]
            shits = [shit for shit in shitter.getShits() if data_inizio <=shit.getDateTime(string=False)<= data_fine]
        
        for shit in shits:
            orario = shit.getHour(nozero=False)
            if orario == "00" or orario == "24":
                self.y_values[-1] += 1
            else:
                try:
                    idx = self.x_values.index(orario)
                    self.y_values[idx] += 1
                except:
                    continue

    def addGraph2Pdf(self, pdf):
        data = pd.DataFrame({"Orario": self.getXvalues(), "Cacate": self.getYvalues()})
        fig, ax = plt.subplots()
        sns.barplot(x="Orario", y="Cacate", data=data, hue="Orario", palette="Set3", legend=False)
        plt.title(f"Distribuzione per fascia oraria: {self.shitter.getName()}")
        plt.xlabel("Orario")
        plt.ylabel("Cacate")
        pdf.savefig(bbox_inches='tight', pad_inches=0.3)
        plt.close()

class PieChart(ShitGraph):

    def __init__(self, data_inizio, data_fine, bathroom: Bathroom):
        self.x_values = []
        self.y_values = []
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        
        labels = [x.getName() for x in bathroom.getShitters()] 
        
       
        values = []
        for shitter in bathroom.getShitters():
            # solo se nel range [data_inizio, data_fine]
            shits_nel_periodo = [
                s for s in shitter.getShits() 
                if self.data_inizio <= s.getDateTime(string=False) <= self.data_fine
            ]
            values.append(len(shits_nel_periodo))

        total = sum(values) if values else 1
        for idx, y in enumerate(values):
            
            if (y / total * 100) > 0.5:
                self.y_values.append(y)
                self.x_values.append(labels[idx])

    def addGraph2Pdf(self, pdf):
        if not self.y_values: return
        fig, ax = plt.subplots()  
        ax.pie(self.y_values, labels=self.x_values, autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Contributi cacatorici {self.data_inizio.strftime('%d/%m')} - {self.data_fine.strftime('%d/%m')}")
        pdf.savefig(bbox_inches='tight', pad_inches=0.3)
        plt.close()

def createPdf(bathroom,data_inizio,data_fine,upload = False):
    today = datetime.datetime.now()
    if upload:
        filename = r"shit_files\pdf_cacatorio.pdf"
    else:
        filename = f"shit_reports\Shit_Tracker_{today.day}_{today.month}.pdf"
    
    with PdfPages(filename) as pdf:
        fig, ax = plt.subplots()
        image = "img\background_cacatorio.png"
        if os.path.exists(image):
            img = plt.imread(image)
            ax.imshow(img, extent=[0, 1, 0, 1], alpha=0.2)
        
        ax.text(0.5, 0.5, bathroom.getClassifica(), ha='center', va='center', fontsize=12, bbox={"facecolor":"white", "alpha":0.5})
        ax.axis("off")
        pdf.savefig(fig)
        plt.close() 

        piechart = PieChart(bathroom=bathroom,data_inizio=data_inizio,data_fine=data_fine)
        piechart.addGraph2Pdf(pdf) 

        gaussian = GaussianChart(data_inizio = data_inizio,data_fine=data_fine,bathroom=bathroom)
        gaussian.addGraph2Pdf(pdf)

        for shitter in bathroom.getShitters():
            if len([shit for shit in shitter.getShits() if data_inizio <= shit.getDateTime(string=False) <= data_fine]) < SHITTER_THRESHOLD:
                continue
            tracker = ShitTracker(shitter=shitter)
            tracker.addGraph2Pdf(pdf)
            
            current_month_name = getMonthFromDatetime(bathroom.data_fine)
            bargraph = ShitBarGraph(shitter=shitter, data_inizio=data_inizio, data_fine = data_fine, month=current_month_name)
            bargraph.addGraph2Pdf(pdf)

        print(f"PDF Creato con Successo: {filename}")

   

    # if upload:
       
       
    #    repo_owner="Hrdo0"
    #    repo_name="cacatorio.github.io"
       
    #    with open(filename, "rb") as file:
    #         content = file.read()

 
    #         content_base64 = base64.b64encode(content).decode("utf-8")

    #         #creo url
    #         file_name_in_repo = "pdf_cacatorio.pdf"
    #         url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name_in_repo}"

    #         headers = {
    #             "Authorization": f"token {token}",
    #             "Accept": "application/vnd.github.v3+json"
    #         }

    #       # controllare se il file esiste già per ottenere il suo 'sha' 
    #         # (GitHub lo richiede per sovrascrivere file esistenti)
    #         response = requests.get(url, headers=headers)
    #         sha = ""
    #         if response.status_code == 200:
    #             sha = response.json().get("sha", "")

    #         # 5. Prepariamo i dati per l'invio
    #         data = {
    #             "message": "Update automatico via script",
    #             "content": content_base64,
    #             "branch": "main"
    #         }
    #         if sha:
    #             data["sha"] = sha # NPermette sovrascitt se il file esiste già

    #         # Send
    #         put_response = requests.put(url, headers=headers, data=json.dumps(data))

    #         if put_response.status_code in [200, 201]:
    #             print(f"File '{file_name_in_repo}' caricato con successo!")
    #         else:
    #             print(f"Errore: {put_response.json()}")


    