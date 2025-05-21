<h1 align="center">Dragonfly Analyzer</h1>
<img src="ui/assets/img/preview.jpg" alt="Dragonfly Analyzer" width="1280"/>

### 📹 Demonstrācija
--- 

[Saite uz video demonstrāciju](https://www.youtube.com/watch?v=q-MgwmnXWBw&ab_channel=BogdansKologrivovs)

### 📌 Projekta uzdevums
---

**Dragonfly Analyzer** ir rīks, kas automatizēti apkopo un sagatavo statistikas pārskatus, pamatojoties uz lauka novērojumiem par spārēm.
Tas paredzēts biologu un ekologu atbalstam, kuri strādā ar indikatoru sugām — sugām, kuru skaits ir īpaši jutīgs pret vides pārmaiņām.

Programma apstrādā Excel failus ([datu faila piemērs](_datafiles/1_Calopteryx%20splendens.xlsx)) ar datiem par sugām un veido kopsavilkuma pārskatu.

📊 Rezultāta pārskatā ietvertā informācija:
* Kopējais īpatņu skaits 
* Skaits pa gadiem 
* Skaits pa kvadrātiem 
* Skaita dinamika pa gadiem 
* Vidējā temperatūra, mākoņu daudzums un vēja stiprums:
    * pa gadiem 
    * pa kvadrātiem 
    * dinamika pa gadiem 
* Pārsvarā novērotie ūdens apstākļi
* Ūdens apstākļu dinamika 
* Pārsvarā novērotā noēnojuma pakāpe 
* Noēnojuma dinamika

Programma automatizē rutīnas aprēķinus un pārskatu struktūras izveidi, ļaujot speciālistiem koncentrēties uz datu interpretāciju, kā arī izmantot rezultātus nākamajos, sarežģītākos analīzes posmos, piemēram, TWINSPAN klasifikācijā.

Rezultāta pārskatu iespējams saglabāt trīs dažādos formātos: **JSON**, **XML** vai **Excel** atkarībā no lietotāja izvēles ([rezultātu piemērs](_datafiles/results)).

Projekts radās kā risinājums reālai problēmai — palīdzēt pazīstamam pētniekam paātrināt datu sagatavošanu viņa bakalaura darbam bioloģijā.

### 🐍 Python bibliotēkas izmantotas projekta izstrādes laikā
---

  #### 📦 Trešo pušu bibliotēkas:
  * `pandas` — datu tabulu analīzei; izmantota datu ielādei un apstrādei no Excel failiem.
  * `openpyxl` — Excel failu lasīšanai un rakstīšanai ar formatējumu.
  * `Pillow` - izmantots darbam ar attēliem grafiskā interfeisā.

  #### 🧰 Standarta Python moduļi:
  * `pathlib` - ceļu un failu struktūras apstrādei.
  * `numbers`- abstraktu skaitlisko tipu pārbaudei un validācijai.
  * `re` - regulāro izteiksmju izmantošanai (piemēram, failu nosaukumu apstrādei).
  * `multiprocessing` - izmantots lai paralēlizēt grafiska interfeisa atjaunošanu un failu operāciju izpildi.
  * `tkinter` - izmantots grafiska interfeisa izstrādei.
  * `dataclasses` - lai būtu iespējams izmantot `@dataclass` dekoratoru `Node` klasēs.
  * `os` - izmantots darbam ar failiem failu sistēmā.
  * `typing` - izmantots tipu anotāciju norādīšanā.
  * `time` - izmantots programmas izpildes laika mērīšanai.
  * `xml` - izmantots datu izvadīšanai `XML` formātā.
  * `json` - izmantots datu serializācijai un ievadei/izvadei `JSON` formātā.
    
### 🧱 Projekta izstrādes laikā izmantotas pašdefinētas datu struktūras 
---

* `HashTable` — pielāgota datu struktūra, kas atkārto `dict` uzvedību. Tās izmērs tiek dinamiski palielināts (kad piepildījums sasniedz 70%), nodrošinot efektīvu darbību ar lieliem datu apjomiem.
* `ProcessSafeQueue` - pielāgota datu struktūra, kas atkārto `multiprocessing.Queue` uzvedību. Tika izmantots datu apmaiņai starp grafiska interfeisa procesu un procesu, kur izpildās operācijas ar failiem. Pamatā izmantota `LinkedList` struktūra, lai datu izņēmšanas sarežģitība būtu `O(1)`, un kad uzkrājas 1000 izlietotu elementu un rindā nav noderīgas informācijas, izpildās rindas tīrīšana (visi elementi sarakstā tiek dzēsti). Papildus, ir izveidots pašdefinēts izņēmums `EmptyProcessSafeQueueError`, kas tiek izsaukts pēc datu izņēmšanas mēģinājuma, ja rinda ir tukšā.
---

#### 🧩 Pārējās svarīgākās programmas daļas (kas nav datu struktūras)
_Lai gan zemāk minētie komponenti nav klasificējami kā datu struktūras, tie ir būtiski programmas darbībai un loģikai. Šis nav pilns saraksts, bet tajā iekļautas galvenās       programmas daļas:_
* `DragonflyAnalyzer` — galvenā klase, kas atbild par datu apkopošanu, rezultātu aprēķināšanu un kopsavilkuma izveidi.
* `Dragonfly` — klase, kas reprezentē vienu spāres sugu un saglabā ar to saistīto statistiku.
* `ErrorCollector` — kļūdu kolektors, kas apkopo visas izpildes laikā radušās kļūdas un palīdz ērti veikt atkļūdošanu.
* `UICommandHandler` — klase, kas ietver sevī grafiska interfeisa notikumu apstrādi, kā arī izpildā ievades datu validāciju un procesa, kur izpildās operācijas ar failiem, palaišanu.
* `WidgetManager` — klase, kas palīdz strukturēt darbu ar `tkinter` logrīkiem, nodrošinot to pārvaldību, izvietošanu un organizāciju lietotāja saskarnē.
* `Tooltip` — klase, kas ir pašdefinēts tkinter logrīks, kas atkārto `HTML title` atribūta uzvedību.
* `StyleManager` - klase, kas apkopo stilus no `JSON` faila un pārvērš tos `ttk.Style` objektā.
* `FileWriter`, `JsonWriter`, `XmlWriter` - klases, kas nodrošinā datu izvadi failā `JSON` un `XML` formātā.

### 🖥️ Programmatūras izmantošanas metodes
---
1. Atkarību instalācija
   ```bash
   pip install -r requirements.txt
   
2. Lietotājs palaiž programmu, izmantojot komandrindu:
   ```bash
   python app/main.py
3. Tiek atvērta grafiskā saskarne, kas izveidota ar `tkinter`

4. Saskarnē pieejamas šādas funkcijas:
   * rezultātu faila formāta izvēle (Excel, XML, JSON)
   * Excel failu pievienošana
   * analīzes palaišanas poga
   * programmas norises un kļūdu žurnāls

5. Pēc palaišanas programma apstrādā failus un saglabā rezultātus lietotāja izvēlētajā vietā datorā.

---


#### 🔮 Alternatīva pieeja (tikai Windows)

1. Noklikšķināt uz `windows_run.bat`

2. Batch skripts pārbaudīs Python instalāciju un versiju

3. Pēc tam Batch skripts pārbaudīs nepieciešamas atkarības, un uzinstālē tos

4. Ja viss iepriekš minēts izpildās veiksmīgi, grafiskā saskarne atvērsies automātiski!
---

<p align="center"><strong>Kopīga izstrāde ar <a href="https://github.com/lbrezgin/">@lbrezgin</a>.</strong> Sinhronizēta kopija <a href="https://github.com/lbrezgin/dragonfly_analyzer">šeit</a>.</p>
