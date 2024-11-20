import json
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from typing import List
from pathlib import Path
from dataclasses import dataclass, asdict

# Download the stopwords
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

class Preprocessor:
   
    @staticmethod
    def preprocess(text: str, lang: str = "english") -> List[str]:
        
        if lang not in stopwords.fileids():
          raise ValueError(f"Language '{lang}' is not supported. The language should be one of the following: {stopwords.fileids()}")

        # Lowercase the text
        text = text.lower()
        
        # Replace ampersand with 'and'
        text = text.replace("&", " and ")
        
        # Normalize special characters (smart quotes, dashes, etc.)
        text = text.translate(str.maketrans("‘’´“”–-", "'''\"\"--"))
        
        # Remove unnecessary periods in acronyms
        text = re.sub(r"\.(?!(\S[^. ])|\d)", "", text)
        
        # Remove punctuation and replace with spaces
        text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
        
        # Tokenize using NLTK (language aware)
        tokens = word_tokenize(text, language=lang)
        
        # Remove stopwords for the given language
        stop_words = set(stopwords.words(lang))
        tokens = [word for word in tokens if word not in stop_words]

        # Stemming
        stemmer = SnowballStemmer(lang)

        # Stem the tokens
        tokens = [stemmer.stem(token) for token in tokens]

        return tokens


class InvertedIndexManager:

    @staticmethod
    def load_inverted_index(file_path: str):
        with open(file_path, 'r') as file:
            inverted_index = json.load(file)
        return inverted_index

    @staticmethod
    def save_index(output_folder_path: Path, lexicon: dict, inv_d: dict, inv_f: dict, doc_index: list, stats: dict):
        # Save each part to a separate JSONL file
        with open(f"{output_folder_path}/lexicon.jsonl", 'w', encoding='utf-8') as lex_file:
            for term, entry in lexicon.items():
                lex_file.write(json.dumps({"term": term, **asdict(entry)}, ensure_ascii=False) + '\n')

        with open(f"{output_folder_path}/inverted_file.jsonl", 'w', encoding='utf-8') as inv_file:
            for term_id, docids in inv_d.items():
                inv_file.write(json.dumps({"termid": term_id, "docids": docids, "freqs": inv_f[term_id]}, ensure_ascii=False) + '\n')

        with open(f"{output_folder_path}/doc_index.jsonl", 'w', encoding='utf-8') as doc_file:
            for doc_entry in doc_index:
                doc_file.write(json.dumps(doc_entry, ensure_ascii=False) + '\n')

        with open(f"{output_folder_path}/stats.json", 'w', encoding='utf-8') as stats_file:
            json.dump(stats, stats_file, ensure_ascii=False, indent=4)




if __name__ == "__main__":
    text = """
    Digital humanities \u2013 Matricolandosi\nSkip to content\nSearch\nSearch\nIT\nEN\nCHOOSE YOUR DEGREE PROGRAM\nFEES AND SCHOLARSHIPS\nSTUDENT CARD\nINTERNATIONAL STUDENTS\nSERVICES\nDigital humanities\nThe Degree Program in Digital Humanities has an open access.\nIn order to attend the course, students must take a\nnon-selective evaluation test\nto verify the initial preparation level.\nThis test can be taken even after the enrolment completion.\nHere\nyou can find the evaluation test information.\nHow to enrol\nEnrolment for the a.y. 2023/2024 will start at the end of July 2023. The official dates are being defined.\n1) Sign up to Alice portal\nEnter your personal data on\nAlice portal\n.\nYou will need to access using your\nSPID\nor\nTax code\n.\n2) Choose your course\nAfter signing up, you can choose:\nStandard enrolment;\nDegree program shortening (in the event of a university degree already obtained);\nRelocation from another University.\nThe procedure will request:\nID scanned copy\npassport-sized photo (\nplease check size\n)\nHigh school diploma details (Secondary School Name, year, final mark).\nStudents with a\nforeign qualification\nare required to upload:\nDeclaration of Value (DV) issued by the Italian Diplomatic Authorities in their home country, along with the official translation into Italian of the diploma, legalised (or with an \u201capostille\u201d) and validated,\nOR\n, the\nENIC-NARIC\ncertificate is accepted in Italian Language. These documents should attest at least 12 years of schooling and the relevant qualification should allow the access to higher education.\nFor Degree Program shortening the obtained University degree will be required. For relocation from another University previous university career will be required from the other university.\nAt the end of procedure please print and sign the FORIM to complete enrolment and upload it on the Alice portal in the Career section annexes.\nStudents with special needs\nStudents with handicap under art. 3 Italian Law no. 104/1992 or with a certified disability equal or above 66% are required to upload a medical certificate attesting their health condition for university tuition fees exemption (duty stamp is required anyway).\nSome special categories under art. 1.1.2 lett. d) e) and art.1.1.3 lett. c) of the Regulations on Tuition fees (such as Italian government scholarship holders, competition winners, detained subjects ) shall email to\nmatricolandosi@unipi.it\nfor a specific calculation of tuition fees.\n3) First installment of university tuition fees\nIf you are not applying for the DSU scholarship\nIf you are not applying for the DSU scholarship, which will be acquired automatically, after choosing your programme, you are required to pay the first installment of tuition fees.\nInformation and deadlines regarding fees and scholarships for the a.y. 2023/2024 are still being defined\n.\nInternational students\nwith a foreign qualification\napplying for a visa\napplicants can pay the first installment of fees and\nsubmit the necessary documentation\nby 29 February 2024 without delay.\nIf you are applying for the DSU scholarship\nIf you are applying for the scholarship, which is\nautomatically acquired\nand results in\nimmediate enrolment after the \u2018choice of course\u2019\n, the payment of the first installment is deferred\nto the deadline of the second tuition fee installment\n: those who successfully gain the scholarship will not be required to pay any university fees. They will only\nhave to pay \u20ac16.00 for duty stamp\n.\nWithin 3 working days from the payment (or from the \u2018choice of course\u2019 in case of submission of the scholarship application), you will receive a welcome email and on you home page of the Alice portal, in the \u2018NOTES\u2019 section, the message \u2018ENROLLED 2023/24\u2019, will be displayed until the documents presented online\nare validated\n.\n4) Enrolment validation and Student Card\nAfter tuition fee payment (or alternatively after scholarship application) you are required to upload the FORIM signed on both 2 pages in the Career section annexes of Alice portal. This document will be checked by the Matricolandosi Centre along with your ID card.\nAs confirmation of your enrolment registration, you will receive a\nwelcome email\nto your personal email address and at the same time the wording \u2018REGISTERED 2023/24\u2019 will be displayed on the Alice portal home page, in the \u2018NOTES\u2019 field, which will remain visible until your documents (FORIM, ID document) have passed all the administrative checks.\nOnly after FORIM has been validated will you be able to book the withdrawal of your Student Card..\nThe procedures for issuing the Student card can be seen\nhere\n.\nStudents with\nforeign qualification\n, regardless of their citizenship, must upload the necessary documents that must be validated by the International Office (\nwis@unipi.it\n); after enrolment, they will have to upload the enrolment form (FORIM) and follow the procedure described on the page for issuing the student card.\n5) Degree program shortening and Relocation from another University\nFor Degree Program shortening the previous university career will be recognized after submitting to the Students Office the \u201c\nqualifications recognition\n\u201d form with the annexed self certification of all exams.\nFor relocation from another University the Students Office will confirm you the acceptance of the discharge papers from the university of origin.\nPlease find more details about study programs and career opportunities at\nDegree Program web page\n.\n\u00a9 2024\nMatricolandosi\nContacts\nContacts for Holders of qualifications awarded abroad\nWis! Tel. +39 3384706070 (Monday-Wednesday-Friday 10 a.m. -1 p.m.)\nwis@unipi.it\n|\nWIS! Office\nBack to top
    """

    text_it = """
        Viticoltura ed enologia \u2013 Matricolandosi\nVai al contenuto\nCerca\nCerca\nIT\nEN\nSCEGLI IL CORSO\nBORSE DI STUDIO E TASSE\nCARTA DELLO STUDENTE\nSTUDENTI INTERNAZIONALI\nSERVIZI\nViticoltura ed enologia\nIl corso di laurea in Viticoltura ed enologia \u00e8 ad\naccesso libero\n.\n\u00c8 necessario per\u00f2 sostenere un\ntest non selettivo\ndi verifica della preparazione iniziale.\nIl test pu\u00f2 essere sostenuto anche dopo l\u2019immatricolazione.\nVai alle informazioni sul test di valutazione.\nPer informazioni sul piano di studi e sbocchi professionali\nvai alla presentazione del corso.\nCome immatricolarsi\nLe immatricolazioni per l\u2019a.a. 2024/25 inizieranno il 24 luglio 2024.\n1) Registrazione sul portale Alice\nIl primo dato richiesto \u00e8 l\u2019accesso con il\ncodice fiscale.\nInserisci nel\nportale Alice\ni tuoi dati anagrafici e personali: al termine della procedura ricordati di annotare l\u2019username e password che compariranno nella pagina di riepilogo.\n2) Scelta del corso sul portale Alice\nDopo la registrazione puoi scegliere tra:\nimmatricolazione standard;\nabbreviazione di carriera (se hai gi\u00e0 conseguito un titolo);\ntrasferimento in ingresso (per chi proviene da altro ateneo italiano).\nIl sistema richieder\u00e0:\nla scansione di un documento identit\u00e0\nuna fototessera\u00a0in formato elettronico (\ncontrolla il formato\n)\ni dati del diploma di maturit\u00e0 (anno conseguimento, istituto scolastico e votazione conseguita).\nGli studenti con\ntitolo estero\ndovranno inoltre caricare:\nDichiarazione di valore (DV)\n, rilasciata dalla Rappresentanza diplomatica italiana competente per territorio, corredata da traduzione ufficiale del diploma in lingua italiana, autenticato o munito di Apostille,\nOPPURE\n, Attestato di comparabilit\u00e0 rilasciato dai\ncentri ENIC-NARIC\n, in lingua italiana.\nDa entrambi i documenti devono risultare almeno 12 anni di scolarit\u00e0 complessiva e il titolo conseguito deve consentire in loco l\u2019accesso all\u2019istruzione superiore.\nPer le \u2018abbreviazioni di carriera\u2019 sar\u00e0 richiesto anche il titolo di studio universitario gi\u00e0 conseguito e per i \u2018trasferimenti in ingresso\u2019 la carriera pregressa svolta in altro ateneo italiano.\nCompletata la procedura devi stampare e firmare il Formulario per l\u2019Immatricolazione (FORIM), necessario per il perfezionamento dell\u2019immatricolazione, e fare l\u2019upload dello stesso nella sezione dedicata (Allegati carriera) del portale Alice.\nStudenti con invalidit\u00e0 o appartenenti a categorie particolari\nLo studente con disabilit\u00e0, con riconoscimento di handicap ai sensi dell\u2019art. 3 co. 1 della L. 104/1992, o con invalidit\u00e0 riconosciuta pari o superiore al 66% dovr\u00e0 fare l\u2019upload del certificato medico attestante le proprie condizioni per ottenere l\u2019esonero dal pagamento delle tasse universitarie (lo studente \u00e8 comunque tenuto al pagamento dell\u2019imposta di bollo).\nAltre categorie particolari previste dal Regolamento sulla contribuzione degli studenti 2024/25 (ad es. borsisti del governo italiano, vincitori di gare, detenuti, portatori di handicap riconosciuti compresi tra il 45 e il 65%) devono contattare\nmatricolandosi@unipi.it\nper chiedere il calcolo della tassa personalizzata.\n3) Pagamento della prima rata delle tasse\nSe non presenti domanda di borsa di studio DSU\nSe non presenti domanda di borsa di studio DSU, che sar\u00e0 acquisita automaticamente, dopo la \u201cScelta del corso\u201d, devi pagare la prima rata delle tasse.\nDal 1 ottobre \u00e8 applicata un\u2019indennit\u00e0 di mora cos\u00ec definita:\n\u20ac 50,00, dal 1 ottobre 2024 al 31 ottobre 2024\n\u20ac 100,00 dal 1 novembre 2024 al 30 novembre 2024\n\u20ac 150,00, dal 1 dicembre 2024 (fino al 31 dicembre 2024 per gli immatricolati)\nGli studenti internazionali con\ntitolo estero\ne\nrichiedenti visto\npossono pagare la prima rata delle tasse\ne presentare la documentazione necessaria\nentro il\n28 febbraio 2025 senza mora.\nSe presenti la domanda di borsa di studio DSU\nSe presenti la domanda di borsa di studio, che sar\u00e0 acquisita\nautomaticamente e comporter\u00e0 l\u2019immediata immatricolazione dopo la \u2018scelta del corso\u2019\n, il pagamento della prima rata \u00e8 posticipato alla\ndata di scadenza della seconda rata della contribuzione\n: coloro che risulteranno vincitori della borsa non saranno tenuti ad alcun pagamento di tasse universitarie, dovranno solamente pagare il\nbollo virtuale di \u20ac 16,00\n.\nEntro 3 giorni lavorativi dal pagamento (o dalla \u2018scelta del corso\u2019 in caso di presentazione della domanda di borsa di studio) ti arriver\u00e0 una mail di benvenuto e sulla tua home page del portale Alice, nel campo \u2018NOTE, sar\u00e0 visualizzato il messaggio \u2018IMMATRICOLATO 2024/25\u2019, visibile fino alla compiuta\nvalidazione\ndei documenti presentati on line.\n4) Controllo documenti e rilascio Carta dello Studente\nDopo il pagamento (o in alternativa dopo la presentazione della borsa di studio), che saranno acquisite automaticamente, se non hai ancora provveduto dovrai fare\nobbligatoriamente l\u2019upload del Formulario di immatricolazione (FORIM)\n, firmato nella prima e nella seconda pagina, tramite la sezione dedicata \u201cAllegati carriera\u201d del portale Alice. Tale documento sar\u00e0 controllato dal personale del Centro Immatricolazioni \u201cMatricolandosi\u201d insieme al documento d\u2019identit\u00e0.\nA conferma dell\u2019avvenuta registrazione dell\u2019immatricolazione riceverai una \u201cmail di benvenuto\u201d al tuo indirizzo di posta elettronica personale e contemporaneamente sar\u00e0 visualizzata sulla Home page del portale Alice, nel campo \u2018NOTE\u2019, la dicitura \u2018IMMATRICOLATO 2024/25\u2019 che rester\u00e0 visibile finch\u00e9 i tuoi documenti (FORIM, documento d\u2019identit\u00e0, permesso di soggiorno) non avranno superato tutti i controlli amministrativi.\nSoltanto dopo la validazione del FORIM potrai prenotare il ritiro della Carta dello studente.\nLe informazioni relative alla Carta dello studente e al suo ritiro sono consultabili\nqui.\nGli studenti con\ntitolo estero\n, a prescindere dalla loro cittadinanza, devono fare l\u2019upload dei\ndocumenti necessari\nche dovranno essere validati da parte dell\u2019Ufficio Internazionale (\nwis@unipi.it\n); successivamente all\u2019immatricolazione, dovranno fare l\u2019\nupload del Formulario di immatricolazione (FORIM)\ne seguire l\u2019iter di cui alla\npagina\nper il rilascio della carta dello studente.\nAbbreviazioni e trasferimenti\nSe hai seguito la procedura per l\u2019abbreviazione di carriera: ricordati che per il riconoscimento della tua precedente carriera devi presentare in Segreteria studenti il modulo di \u201c\nriconoscimento titoli\n\u201d allegando l\u2019autocertificazione degli esami sostenuti. Scadenza 31 dicembre 2024.\nSe hai seguito la procedura per il trasferimento da un altro ateneo, per il perfezionamento devi attendere la comunicazione della Segreteria studenti dell\u2019arrivo del foglio di congedo dell\u2019universit\u00e0 di provenienza. Termine per il trasferimento al 28 febbraio 2025.\n\u00a9 2024\nMatricolandosi\nContatti\nNumero verde Studenti 800018600\nMatricolandosi:\nTel: 0502213616-619 dal luned\u00ec al venerd\u00ec dalle 9 alle 12\nmatricolandosi@unipi.it\nConcorsi: Tel: 0502213429 dal luned\u00ec al venerd\u00ec dalle 9 alle 13\nconcorsinumerochiuso@unipi.it\nSegreterie decentrate\nWIS!(Welcome International Students!) Office\nper studenti con titolo estero\nTel. +39 3384706070 luned\u00ec \u2013 mercoled\u00ec \u2013 venerd\u00ec dalle 10 alle 13\nwis@unipi.it\nTorna in cima
    """
    print(Preprocessor.preprocess(text_it, lang="italian"))