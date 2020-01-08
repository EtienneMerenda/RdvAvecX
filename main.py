# -*- encoding: utf-8 -*-

from scraper import Scraper
import os
import requests
import threading
import time
import pickle


class DownLoad(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.RLock()

    def run(self):

        dl_bool = False

        # Récupération des noms des fichiers déja téléchargés
        with self.lock:
            with open("name_list_already_dl", "rb") as file:
                name_list = pickle.load(file)

            # Tant qu'on ne trouve un un fichier qui n'est pas présent
            # dans le dossier ou la liste de nom, on remove les liens de la liste.
            while dl_bool is False:
                self.name = epi_info_list[0]["name"]
                self.link = epi_info_list[0]["link"]
                if f"{self.name}.mp3" in present_file or f"{self.name}.mp3" in name_list:
                    del epi_info_list[0]

                # Quand on trouve, on le suppirme de la liste pour les autres threads
                # Et en passe à la suite.
                else:
                    del epi_info_list[0]
                    dl_bool = True

        responseMP3 = requests.get(self.link, stream=True)
        self.weight = responseMP3.headers["Content-Length"]
        with open(f"./Data/{self.name}.mp3", 'wb') as mp3:
            for chunk in responseMP3.iter_content(chunk_size=256):
                mp3.write(chunk)

        with self.lock:
            with open("name_list_already_dl", "wb") as file:
                name_list.append(f"{self.name}.mp3")
                file.write(pickle.dumps(name_list))


class ThreadManager():

    def __init__(self):
        pass

    def set_thread_object(self, nb=1):
        self.thread_list = []
        for i in range(0, nb):
            self.thread = DownLoad()
            self.thread_list.append(self.thread)
            time.sleep(0.5)

    def set_start(self):
        for thread_object in self.thread_list:
            thread_object.start()

    def statut(self):
        statut_list = []
        for thread_object in self.thread_list:
            statut_list.append(thread_object.is_alive())
        return statut_list

    def weight(self):
        weight_list = []
        for thread_object in self.thread_list:
            weight_list.append(thread_object.weight)
        return weight_list

    def get_name(self):
        name_list = []
        for thread_object in self.thread_list:
            name_list.append(thread_object.name)
        return


if not os.path.isdir("./Data"):
    os.mkdir("./Data")
    print("Le dossier introuvable. Création effetuée.")
if not os.path.isfile("name_list_already_dl"):
    with open("name_list_already_dl", "wb") as file:
        name_list = []
        tmp = pickle.dumps(name_list)
        file.write(tmp)
    print("Création du fichier contenant les noms des épisodes déjà téléchargés.")
present_file = os.listdir("./Data")

# Attribution du lien de la page principale du lien.
url = "http://rendezvousavecmrx.free.fr/"

# Passage dans l'objet Scraper() qui requests et soup le bordel.
admin = Scraper()
admin.set_url("http://rendezvousavecmrx.free.fr/page/liste.php")
admin.get_url()
admin.decode()
admin.soup()
soup = admin.get_soup()
focus_table = soup.find("tbody")
episode_info = focus_table.find_all("tr")

epi_info_list = []

for item in episode_info:
    # récupération de chaque lien d'épisodes.
    link = url + item.find("td", attrs={"class": "icone"}).a["href"][3:]
    # récupération du nom en remplaçant les espaces pas des "_"
    name = item.find("td", attrs={"class": "titre_emission"}).text.replace(" ", "_").replace("\n", "").replace("_:_", "_").replace("/", "_in_").replace("?", "")

    epi_info_list.append({"name": name, "link": link})

nb = int(input("Combien de téléchargements simultanés ?"))

while len(epi_info_list) > 0:
    thread_manager = ThreadManager()
    thread_manager.set_thread_object(nb)
    thread_manager.set_start()

    # Boucle d'attente de la fin des téléchargements actifs avec affichage de téléchargements.
    while True in thread_manager.statut():
        time.sleep(0.5)
        os.system('cls')
        print(f"fichiers restants: {len(epi_info_list)}")
        i = 1
        for thread in thread_manager.statut():
            if thread is True:
                txt = "en cours."
            else:
                txt = "terminé."
            print(f"Téléchargement {i}: {txt}")
            i += 1
