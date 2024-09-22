# Search Engine for Static HTML Pages

## Descriere Proiect:
Acest proiect constă într-un motor de căutare personalizat pentru pagini HTML statice. Are două componente principale: un script Python pentru indexarea conținutului și o interfață web HTML/JavaScript pentru căutare.

### Componenta Python (indexer.py):
Scopul: Indexează conținutul paginilor HTML statice și creează fișiere de output pentru căutare.

### Funcționalități principale:
- Parcurge recursiv un director specificat pentru fișiere HTML.
- Extrage informații relevante din fiecare fișier HTML (titlu, URL canonical, dată, conținut).
- Normalizează textul (elimină diacritice, convertește la lowercase).
- Filtrează conținutul nedorit.
- Salvează informațiile extrase în fișiere de output (.txt).

### Pași de execuție:
1. Definește directoarele de input și output.
2. Parcurge toate fișierele HTML din directorul de input.
3. Pentru fiecare fișier HTML:
   - Extrage informațiile relevante:
   - Procesează și filtrează conținutul.
   - Salvează informațiile în fișiere de output.
4. Generează raport despre fișierele procesate și eventualele erori.

## Componenta HTML/JavaScript (search.html):
Scopul: Oferă o interfață pentru căutarea în conținutul indexat.

### Funcționalități principale:
- Interfață de căutare simplă cu un câmp de input și un buton.
- Încarcă conținutul indexat din fișierele de output.
- Efectuează căutări în conținutul încărcat.
- Afișează rezultatele căutării cu evidențierea termenilor căutați.

### Structura fișierului:
- HTML: Structura de bază a paginii și elementele de interfață.
- CSS (intern): Stilizarea elementelor de interfață și a rezultatelor.
- JavaScript: Logica de căutare și afișare a rezultatelor.

### Cum folosim search.html:
1. Utilizatorul introduce un termen de căutare.
2. Apasă butonul de căutare sau tasta Enter.
3. Scriptul caută termenul în conținutul încărcat.
4. Rezultatele sunt afișate, evidențiind termenii găsiți.
5. Link-urile către articolele originale sunt clickabile și se deschid în tab-uri noi.

## Configurare și Rulare:

### Instalare Python:
- Asigurați-vă că aveți Python instalat (versiunea recomandată: 3.12.6 sau mai recentă).
- Verificați instalarea în CMD cu: `python --version`
- Fisierul `GPT TEST.py` va face crawling in toate html si va extrage sub forma de fisiere txt toate informarmatiile din website. La final se vor crea automat fisierul `file_list.json` care contine numele tuturor fisierelor .txt nou create.

Fisierul `GPT TEST.py` va indexa continutul tagurilor urmatoare din fiecare fisier html:

<title>(.*?)</title>
<link rel="canonical" href="(.?)" />
<meta name="description" content="(.?)">
<h1>(.?)</h1>
<h1 class="custom-h1" itemprop="name">(.?)</h1>
<h2 class="text_obisnuit2">(.?)</h2>
<h3 class="text_obisnuit2">(.?)</h3>
<p class="text_obisnuit">(.?)</p>

### Instalare Node.js:
- Descărcați și instalați Node.js de la https://nodejs.org/
- Verificați instalarea în CMD cu:

  `node --version`
  
  `npm --version`

### Rularea serverului local:
- Deschideți CMD Administrator în folderul proiectului.
- Rulați comanda: `python -m http.server 8000`

### Accesarea interfeței de căutare:
- Deschideți un browser web și navigați la `http://localhost:8000/search.html`

## Cerințe de afișare pentru rezultatele căutării:
- Titlul și Autorul articolului (nu "Titlu necunoscut").
- Data extrasă din fișierul HTML (nu "Dată necunoscută").
- Linkul Canonical sub titlu.
- Descrierea sub link.
- Rezultatele afișate unul sub altul, nu pe o singură linie.
- Pentru fiecare rezultat, maxim 25 de cuvinte relevante din paragrafele care conțin cuvintele cheie.
- Selectarea celui mai reprezentativ paragraf (cel mai lung sau complex) dacă există mai multe paragrafe cu cuvinte cheie.

## Instrucțiuni de Utilizare:
1. Rulați scriptul Python pentru indexarea paginilor HTML.
2. Porniți serverul local folosind comanda Python menționată mai sus.
3. Accesați search.html prin browserul web la adresa locală.
4. Utilizați interfața pentru a căuta în conținutul indexat.

## Note importante:
- Asigurați-vă că toate dependențele necesare sunt instalate.
- Serverul local este necesar pentru a permite încărcarea fișierelor de indexare în browser.
- Pentru dezvoltare și testare, folosiți întotdeauna un server local, nu deschideți fișierele direct în browser.
