class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.espositore = None
        self.disponibile = True

    @property
    def prezzo_finale(self):
        #per lo stand standard il prezzo corrisponde a quello base
        return self.prezzo_base

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        #per ordinare gli stand in base al prezzo finale
        return self.prezzo_finale < other.prezzo_finale

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Occupato da {self.espositore.codice}"
        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_finale:.2f}€ - {stato}"

class StandPrese(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese_extra):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese_extra = int(prese_extra)

    @property
    def prezzo_finale(self):
        #7% in più
        return self.prezzo_base * (1* 0.97 * self.prese_extra)

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Occupato da {self.espositore.codice}"
        return f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_finale:.2f}€ - Prese aggiuntive: {self.prese_extra} - {stato}"

class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    @property
    def prezzo_finale(self):
        #30% in più
        return self.prezzo_base *1.30

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Occupato da {self.espositore.codice}"
        return f"{self.codice}: Premium ({self.posizione}) | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo_finale:.2f}€ - {stato}"

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        stand_str = f"Stand: {self.stand.codice}" if self.stand else "Nessuno stand assegnato"
        return f"{self.codice} - {self.nome} {self.cognome} | {stand_str}"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.stand_list = [] #Lista che conterrà gli oggetti Stand
        self.espositore_list = [] #Lista che conterrà gli oggetti Espositore


    """Aggiungere setter e getter se necessari"""

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    #utilizzp @property e @setter per consentire di leggere e modificare in modo sicuro il nome del centro
    #come richiesto dall'opzione 1

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        with open(file_path, "r", encoding='utf-8') as f:
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue
                campi = riga.split(",")
                codice = campi[0]

                if codice.startswith('ST'):
                    if len(campi) > 4:
                        s = Stand(campi[0], campi[1], campi[2], campi[3])
                    elif len(campi) == 5:
                        try:
                            prese = int(campi[4])
                            s = StandPrese(campi[0], campi[1], campi[2], campi[3], prese)
                        except ValueError:
                            s = StandPrese(campi[0], campi[1], campi[2], campi[3], campi[4])
                    self.stand_list.append(s)

                elif codice.startswith('ES'):
                    e = Espositore(campi[0], campi[1], campi[2])
                    self.espositore_list.append(e)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand_trovato = None
        for s in self.stand_list:
            if s.codice == codice_stand:
                stand_trovato = s
                break

        espositore_trovato = None
        for e in self.espositore_list:
            if e.codice == codice_espositore:
                espositore_trovato = e
                break

        # Controlli di validazione ed eccezioni
        if not stand_trovato:
            raise ValueError(f"Lo stand {codice_stand} non esiste.")
        if not espositore_trovato:
            raise ValueError(f"L'espositore {codice_espositore} non esiste.")
        if not stand_trovato.disponibile:
            raise ValueError("Lo stand selezionato non è disponibile.")
        if espositore_trovato.stand is not None:
            raise ValueError("L'espositore ha già uno stand assegnato.")

        # Effettua l'associazione bidirezionale
        stand_trovato.disponibile = False
        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand = stand_trovato


    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        if not self.espositore_list:
            print('Nessun espositore registrato')
            return

        for e in self.espositore_list:
            print(e)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand_list)

