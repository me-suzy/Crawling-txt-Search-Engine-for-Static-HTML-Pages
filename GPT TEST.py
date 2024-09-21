import os
import re
from bs4 import BeautifulSoup
import unicodedata

# Funcția care normalizează textul: elimină diacriticele și convertește la litere mici
def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

# Funcția care evidențiază termenii căutați în textul returnat (cu bold)
def highlight_search_term(text, search_term):
    # Normalizează termenul căutat și textul pentru comparație
    normalized_text = normalize_text(text)
    normalized_search_term = normalize_text(search_term)

    # Căutăm toate aparițiile termenului căutat în textul normalizat
    matches = [(m.start(), m.end()) for m in re.finditer(re.escape(normalized_search_term), normalized_text)]

    # Evidențiere în textul original pentru a păstra diacriticele și forma corectă
    highlighted_text = ""
    last_index = 0
    for start, end in matches:
        highlighted_text += text[last_index:start] + f"<b>{text[start:end]}</b>"
        last_index = end
    highlighted_text += text[last_index:]

    return highlighted_text

# Funcția care extrage informații dintr-un fișier HTML și le formatează
def extract_info(html_content, search_terms):
    info = []

    # Extrage titlul
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        info.append(f"<b style='color: blue;'>{title_match.group(1).strip()}</b>")

    # Extrage link-ul canonical
    canonical_match = re.search(r'<link rel="canonical" href="(.*?)"', html_content, re.IGNORECASE)
    if canonical_match:
        info.append(f"<b style='color: green;'>Canonical: {canonical_match.group(1)}</b>")

    # Extrage data
    date_match = re.search(r'On (.*?), in', html_content)
    if date_match:
        info.append(f"<b style='color: red;'>In data de: {date_match.group(1)}</b>")

    # Extrage paragrafele specifice și elimină tagurile HTML
    content = []

    # Pentru <p class="text_obisnuit2"><em>...</em></p>
    for match in re.finditer(r'<p class="text_obisnuit2"><em>(.*?)</em></p>', html_content, re.IGNORECASE | re.DOTALL):
        content.append(match.group(1).strip())

    # Pentru <p class="text_obisnuit">...</p>
    for match in re.finditer(r'<p class="text_obisnuit">(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL):
        content.append(match.group(1).strip())

    # Pentru <p class="text_obisnuit2">...</p> (fără <em>)
    for match in re.finditer(r'<p class="text_obisnuit2">(?!<em>)(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL):
        content.append(match.group(1).strip())

    # Filtrăm conținutul nedorit
    filtered_content = [item for item in content if not item.startswith("Ultimele articole accesate de cititori:")
                        and not item.startswith("DONAȚIE RECURENTĂ")
                        and not "Ochii mei vad lucruri pe care tu nu le vezi" in item]

    # Adaugă conținutul filtrat fără taguri HTML
    info.extend(filtered_content)

    return "\n".join(info)

# Funcția care realizează crawling-ul fișierelor și salvează output-ul
def crawl_and_save(folder_path, output_folder, search_terms):
    file_counter = 1
    current_file = open(os.path.join(output_folder, f'output_{file_counter}.txt'), 'w', encoding='utf-8')
    current_size = 0
    indexed_files = []
    error_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Indexare: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as html_file:
                        html_content = html_file.read()

                    extracted_info = extract_info(html_content, search_terms)
                    info_size = len(extracted_info.encode('utf-8'))

                    if current_size + info_size > 1000000:  # 1MB
                        current_file.close()
                        indexed_files.append(f'output_{file_counter}.txt')
                        file_counter += 1
                        current_file = open(os.path.join(output_folder, f'output_{file_counter}.txt'), 'w', encoding='utf-8')
                        current_size = 0

                    current_file.write(extracted_info + '\n--------\n')
                    current_size += info_size
                except Exception as e:
                    print(f"Eroare la indexarea fișierului {file_path}: {str(e)}")
                    error_files.append(file_path)

    current_file.close()
    indexed_files.append(f'output_{file_counter}.txt')

    print("\nFișiere .txt create:")
    for file in indexed_files:
        print(file)

    if error_files:
        print("\nFișiere cu erori la indexare:")
        for file in error_files:
            print(file)
    else:
        print("\nNu au fost erori la indexare.")

    return file_counter

# Funcția de căutare care utilizează normalizarea textului și evidențiază termenii
def search_in_files(search_term, output_folder):
    search_term = normalize_text(search_term)
    results_found = False
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = normalize_text(f.read())
                    if re.search(re.escape(search_term), content):
                        print(f"Rezultatul căutării găsit în: {file_path}")
                        results_found = True
    if not results_found:
        print("Nu s-au găsit rezultate.")

# Setează folderele de input și output
html_folder = r'd:\100'
output_folder = r'd:\100\Output'
search_terms = ['iesiţi la aer', 'iesiti la aer']

# Crează folderul de output dacă nu există
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Termenul de căutare pentru evidențiere
search_term = "iesiti la aer"

# Efectuează crawling și salvare cu evidențierea termenului
num_files = crawl_and_save(html_folder, output_folder, search_terms)
print(f"\nProcesul de crawling și salvare a fost finalizat. {num_files} fișiere create.")

# Caută textul dorit în fișierele de output
search_in_files(search_term, output_folder)
