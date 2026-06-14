# 📚 IT ARHITEKTURE – ZAPISKI ZA OBA KOLOKVIJA

> Pripravljeno za **ustni izpit**. Snov je razložena **čim bolj enostavno**, zahtevni pojmi imajo zraven **preprost primer**. 
> Predmet: IT arhitekture, IPT MAG 1 (UM FERI). Predavatelj: Luka Pavlič (K1), Matej Šprogar (K2-del).

## 🗺️ Kako uporabljati te zapiske
- **Kolokvij 1** = predavanja 1–10: kaj je arhitektura, vloga arhitekta, SOLID, arhitekturni stili, komunikacija, ADR, SPL, oblak/zabojniki/Kubernetes, serverless.
- **Kolokvij 2** = članki o testiranju, TDD, mockih in čisti arhitekturi (Uncle Bob, Fowler, Coplien).
- Vsak razdelek ima na koncu **📌 Za zapomniti** – to je idealno za zadnje ponavljanje pred ustnim.

---
---

# 🟦 KOLOKVIJ 1

## 🔑 Štiri ideje, ki povezujejo cel Kolokvij 1
1. **Arhitektura = zgodnje, težko spremenljive odločitve.** Loči **KAJ** (zahteve) od **KAKO** (načrt), a hkrati ju povezuje.
2. **Razklapljanje (loose coupling) je cilj.** Šibko sklopljeni, neodvisni gradniki → prožen, vzdržljiv sistem.
3. **Odloži nepomembne odločitve (baza, ogrodje, lokacija) na "zadnji odgovorni trenutek".**
4. **Vse je kompromis (trade-off).** Nefunkcionalne zahteve (varnost, hitrost, skalabilnost) si pogosto nasprotujejo → arhitekt jih uravnoteži.

---

## 1️⃣ UVOD: KAJ JE ARHITEKTURA IN ZAKAJ JE POMEMBNA

### 🎯 Glavna ideja
Sodobni svet teče na programski opremi (milijoni vrstic kode, tisoči razredov). Brez načrtne arhitekture nastane **kaos** – koda, ki "samo-da-dela", a je je nemogoče vzdrževati.

### 🏛️ Kaj je programska arhitektura? (3 definicije)
| Vir | Poudarek |
|---|---|
| Software Architecture in Practice | **Strukture** sistema: gradniki, **odvisnosti** med njimi in njihove **lastnosti** |
| CMU SEI | Množica **načrtovalskih odločitev** o strukturi in obnašanju; pomaga deležnikom razumeti, kako bo sistem dosegel kakovosti (spremenljivost, razpoložljivost, varnost) |
| Bass, Clements | **Najzgodnejše** odločitve – **najtežje jih je pravilno zadeti** in **najtežje spremeniti** kasneje; imajo najdaljnosežnejše posledice |

### 📐 Načrt vs. arhitektura (POMEMBNO razlikovanje)
- **Načrt (design)** = **podrobnosti**: razredi, operacije, vmesniki, protokoli, algoritmi. Vezan na konkretno platformo/jezik. Odgovarja na **KAKO**.
- **Arhitektura** = **čim bolj abstraktno**: le nakazani visoko-nivojski gradniki, način povezovanja in komunikacije. Je **osnova** za načrtovalske odločitve. Odgovarja na **KAJ na visoki ravni**.

> 💡 **Primer:** "Sistem ima ločen poslovni nivo in nivo za podatke, ki komunicirata preko REST API-ja" = arhitektura. "Razred `OrderService` ima metodo `createOrder(OrderDTO)` ki kliče `OrderRepository.save()`" = načrt.

### 🍝 Slaba vs. 🍲 dobra arhitektura
- **Slaba (špageti):** kompleksna, nekonsistentna, **toga, nestabilna**, težko testirati in vzdrževati.
- **Dobra (lazanja – plasti):** enostavna, razumljiva, **fleksibilna**, dopušča nadgradnje, lahko testirati/vzdrževati, **enostavno dodajanje funkcionalnosti**.

### 🧰 Arhitektura kot inženirstvo
Inženirji z uporabo znanstvenih spoznanj, **standardov**, ekonomije in socioloških/ekonomskih omejitev načrtujejo in gradijo sisteme. → Arhitektura je **obvladovanje tveganj(a)**.

### 📊 Kje arhitekturo definiramo? Nefunkcionalne zahteve (NFZ)
- **Funkcionalne zahteve (KAJ počne):** "Prenos osnovnega sredstva na drugega uporabnika."
- **Nefunkcionalne zahteve = omejitve (KAKO mora delovati, ni neposredno povezano s funkcijo):** hitro delovanje, prijava, reset gesla, varnost…

> NFZ (po Wikipediji) so kriteriji za **presojo delovanja** sistema, ne specifičnega obnašanja. **Načrt implementacije NFZ je v arhitekturi** (ker so NFZ "arhitekturno pomembne zahteve" – ASR).

**Standard ISO 25010 – kakovost izdelka (Software Product Quality):** funkcionalna ustreznost, **performance efficiency**, združljivost, uporabnost (interaction capability), **zanesljivost**, **varnost (security)**, **vzdržljivost (maintainability)**, fleksibilnost, varnost (safety).

> ⚠️ **Konflikt omejitev je normalen!** Npr. več varnosti → pogosto manj hitrosti. → Rešitev = **KOMPROMIS**.

### 🧱 Minimum specificiranja zahtev
- **Vizija** – kratek "plot" rešitve, meje (kaj vključimo / **česa NE**), ključne funkcionalnosti, deležniki.
- **Besednjak (glossary)** – ključni del za sporazumevanje o domeni; sestavi razvojna ekipa z domenskimi strokovnjaki. (Brez jasnih pojmov ne moremo modelirati zahtev.)
- **Popis vlog uporabnikov** + njihovih zahtev.
- **Funkcionalne** in **nefunkcionalne** zahteve.

### 📋 4+1 pogled na arhitekturo (Kruchten)
Eden bolj celovitih načinov dokumentiranja. **V središču: uporabniški scenariji**, okoli njih 4 pogledi:
1. **Logičen** pogled (funkcionalnost),
2. **Procesen** pogled (sočasnost, procesi),
3. **Razvojen** pogled (organizacija kode),
4. **Fizičen** pogled (namestitev na strojno opremo).

> Izhaja iz ogrodja RUP, predvideva UML, a se da prilagoditi. **Osnova so zahteve uporabnika.**

### 🌍 The World and the Machine (Michael Jackson, 1995)
Ali je res tako enostavno ločiti KAJ od KAKO? Ne.
- **Okolje (svet)** → senzorji (vhod) → **programska oprema (stroj)** → aktuatorji (izhod) → nazaj v okolje.
- Programska oprema lahko o realnem svetu **le sklepa** (preko senzorjev) in nanj vpliva **le preko aktuatorjev**.
- **Shared phenomena** = presek sveta in stroja (kar oboje "vidi").

> 💡 **Primer – Lufthansa 2904 (zakaj je to ključno!):** Letalo ni zaviralo, 2 mrtva. Varnostna zahteva: povratni potisk motorjev **le, ko je letalo na tleh**. Implementacija "na tleh" je bila vezana na **vrtenje koles >130 km/h**. Ob dežju (aquaplaning) so se kolesa zaradi vode vrtela prepočasi → sistem je sklepal **"nismo na tleh"** in blokiral zaviranje. 
> **Poanta:** Sistem je bil "pravilen" po specifikaciji, a model realnega sveta (predpostavka, da vrtenje koles = na tleh) je bil napačen. → Razumevanje **področja problema** je kritično.

### ⚠️ Nevarne predpostavke
"Medicinska sestra bo vedno vnesla pravilno količino", "GPS bo vedno dostopen", "voznik bo pozoren". → **Ne smemo se zanašati na idealne predpostavke** – ljudje delajo napake, naprave odpovedo.

### 💰 Zakaj/koliko investirati v arhitekturo? (Boehm, Turner)
Arhitektura je strošek dvojne narave:
- **Delo "v naprej"** (analiza tveganj, načrtovanje) = ker želimo dobro arhitekturo.
- **Podvojeno delo** (odprava defektov, preoblikovanja) = ker NIMAMO dobre arhitekture.

**Sweet spot** (najnižji skupni strošek) je odvisen od velikosti:
- **~10 KLOC (majhen projekt):** sweet spot pri **~20 % časa**; vnaprejšnje delo na arhitekturi je tu **skoraj izguba**.
- **~1.000 KLOC (1M vrstic):** sweet spot pri **~40 %**; brez arhitekture se takega projekta sploh ne da lotiti.
- Sweet spot drivers: **Rapid change → levo** (manj arhitekture), **High assurance → desno** (več arhitekture).

> 📈 **Cost to fix bugs (NIST):** napaka, najdena v fazi zahtev/arhitekture, je ~1x; v produkciji ~30x dražja. → Zgodaj najdene napake so poceni.

### 💬 Slavni citati (znati razložiti!)
- **R. C. Martin:** "The only way to go fast, is to **go well**." Cilj arhitekture je **minimizirati človeške vire** za gradnjo in vzdrževanje.
- **Foote & Yoder:** "Če misliš, da je dobra arhitektura draga, **probaj slabo**."
- **Fowler:** "High quality software is **cheaper** to produce." (Kakovosten softver je **cenejši** dolgoročno.)
- **Ralph Johnson:** arhitektura so odločitve, ki bi jih radi zgodaj zadeli prav.

### 📉 Fowler: Je dobra kakovost vredna stroška?
- Na prvi pogled **notranja kakovost** ni pomembna za stranko; stranki je važno, da funkcije pridejo hitro.
- Toda **"cruft" (slaba notranja kakovost)** povzroči, da nove funkcije trajajo dlje. 
- Krivulja: visoka notranja kakovost → kratek začetni upad, nato **dostavljaš hitreje (in ceneje)**. Točka preloma nastopi v **tednih, ne mesecih**.

### 📌 Za zapomniti (Uvod)
- Arhitektura = najzgodnejše, najtežje spremenljive odločitve; loči KAJ od KAKO.
- NFZ (omejitve) so arhitekturno pomembne; med seboj v konfliktu → kompromisi.
- 4+1 pogled = uporabniški scenariji + logičen/procesni/razvojni/fizični pogled.
- Lufthansa 2904 = napačen model realnega sveta ubije sistem (kolesa ≠ na tleh).
- Boehm sweet spot: malo arhitekture za majhne projekte, veliko za velike.
- Visoka kakovost je dolgoročno cenejša.

---

## 2️⃣ SNOVANJE ARHITEKTUR: VLOGA ARHITEKTA, POSTOPEK, SOLID

### 👷 Vloga "arhitekt" – več vlog glede na obseg (scope)
| Vloga | Kaj počne |
|---|---|
| **Enterprise Architect** | IT strategija celega podjetja, tehnološki standardi, platforme, integracije (across value streams) |
| **Domain Architect** | arhitektura znotraj **ene poslovne domene** |
| **Solution Architect** | celotna rešitev za projekt, integracije med sistemi, izbira tehnologij (**najboljši približek "IT arhitekta"**, across systems) |
| **Software/Application Architect** | software arhitektura, izbira ogrodij, konvencije kodiranja (single system) |
| **Infrastructure/Cloud, Data Architect** | infrastruktura, oblak, podatki |

> V manjših podjetjih so vloge **združene** (npr. Solution + Software). Arhitekt potrebuje **ŠIRINO** znanja, ne le globino.

### 🧑‍💼 Arhitekt je več kot "samo načrtovalec" (Bass, Clements, Kazman)
Potrebuje: **Leadership, Communication, Negotiation, Technical skills, Project skills, Analytical skills.**

**Tehnične naloge:** snovanje, analiza/ocena, dokumentiranje arhitektur, upravljanje zahtev, razvoj, testiranje, presoja in izbira tehnologij.
**Netehnične naloge:** upravljanje projekta/ljudi, podpora vodstvu in organizaciji, tehnično vodenje ekip.
**Lastnik "velike slike"** (ptičja perspektiva), skrbi za skladnost načrta.

### 🔁 Proces razvoja arhitekture
> Pomni: **(dobra) IT rešitev je preslikava realnega sveta.**

**GCE zanka (Generate-Communicate-Evaluate):** najnovejše zahteve → **Generate** (ustvari osnutek) → **Communicate** (komuniciraj) → **Evaluate** (ovrednoti) → trenutni dizajn → in spet od začetka. Iterativno.

**Klasičen pristop (iterativen):**
1. Analiza deležnikov,
2. Izvabljanje zahtev (pričakovano obnašanje),
3. Vrednotenje HW/SW možnosti,
4. Določanje obsega sistema,
5. Sprejem dolgoročnih odločitev.
→ Zajem zahtev → sprejem odločitev → dokumentiranje → ponovi.

**Proces Kazman & Cervantes:**
- **Architectural Analysis** (vhod: arhitekturni concerns + kontekst) → izloči **ASR (Architecturally Significant Requirements)**.
- **Architectural Synthesis** → kandidatne rešitve (iz **backlog-a**: architectural assets, ideje, stakeholderji/concerns, drivers).
- **Architectural Evaluation** → preverjena (validated) arhitektura.
- **Arhitekturne odločitve (tactics):** imajo dolgoročen vpliv, vplivajo na več komponent, jih je težko spremeniti, vplivajo na atribute kakovosti (performance, security, scalability). Temeljijo na **stilih in vzorcih**.

**ADD (Architecture-Driven Design):** ponavljajoči se koraki – pregled vhodov → cilj iteracije (izberi drivers) → izberi elemente za izpopolnitev → izberi design koncepte → instanciraj elemente in določi vmesnike → skiciraj poglede in zapiši odločitve → analiza in pregled.

**Architectural Drivers (vhod v dizajn):** Design Purpose, Primary Functionality, **Quality Attributes**, Constraints, Architectural Concerns.

### 👁️ Viewpoints and Perspectives (Rozanski, Woods) – 3 stebri
1. **Deležniki (stakeholders)** – osebe, na katere arhitektura vpliva; imajo različna pričakovanja.
2. **Pogledi (Viewpoints)** – vzorci/predloge/konvencije za **strukturiranje** definicije arhitekture; vsak se osredotoča na **en vidik** sistema.
3. **Perspektive (Perspectives)** – aktivnosti/taktike/smernice, ki gledajo **kako posamezna lastnost (varnost, zmogljivost) vpliva na vsak pogled**.

**Pogledi (viewpoints):**
- **Funkcijski** – funkcionalni elementi, odgovornosti, interakcije.
- **Informacijski** – kako sistem hrani/obdeluje/distribuira podatke; statična struktura + tok informacij.
- **Sočasnosti (Concurrency)** – usklajevanje sočasnih procesov.
- **Razvojni (Development)** – organizacija kode, orodja, procesi za gradnjo/test/vzdrževanje.
- **Namestitveni (Deployment)** – odvisnosti med izvajanjem (SW, HW, omrežje); razporeditev v produkciji.
- **Operativni (Operational)** – uporaba v produkciji, administracija, monitoring, nadgradnje, obvladovanje napak.

**Perspektive (npr. Security, Performance, Availability, Evolution)** se "položijo" čez poglede. Npr. **Information Security** (access control), **Concurrency Performance** (shared resources, blocking, queuing), **Functional Evolution** (extension points, flexible interfaces). 
**Naloga arhitekta:** določiti **prioritete** med atributi kakovosti, doseči minimalne pragove in **uravnotežiti kompromise** (npr. varnost vs zmogljivost).

### ✅ (Splošni) principi dobrega snovanja arhitektur
- Gonilo so **zahteve uporabnikov**.
- Spodbujanje **komunikacije** o odločitvah in njihovem vplivu.
- Zagotavljanje **upoštevanja arhitekturnih odločitev** skozi cel razvoj.
- Postopno, jasni cilji/vhodi/izhodi; upoštevaj **časovni in finančni okvir**.
- **Fleksibilnost** (odločitve glede na kontekst), **neodvisnost od ene tehnologije**.
- Mora biti **integralni del SDLC**, vklopljen v obstoječe inženirske prakse.

### 🧩 SOLID principi (R. C. Martin) — KLJUČNO za ustni!
> Cilj: strukture, ki jih je **enostavno spreminjati**, **enostavno razumeti** in so **osnova za ponovno uporabo**.

#### S — Single-Responsibility Principle (SRP)
"Gradnik naj ima **le en razlog za spremembo**." Razlog za spremembo = zahteva **enega uporabnika/naročnika**.
- ⚠️ **NI** isto kot "naredi eno stvar dobro"!
- ❌ NE: "Gradnik naj skrbi za trajnost podatkov." 
- ✅ DA: "Gradnik naj generira plačilne listine **administrativnemu osebju** Podjetja d.o.o." (en deležnik = en razlog za spremembo).
- Na nivoju komponent isto = **Common Closure Principle**: razredi, ki se spreminjajo skupaj, naj bodo v isti komponenti.
> 💡 **Primer:** Če bi en razred generiral poročilo ZA računovodstvo IN format ZA HR, ima dva razloga za spremembo → krši SRP. Loči ju.

#### O — Open-Closed Principle (OCP) [Bertrand Meyer, 1980]
"Gradnik naj bo **odprt za razširitve, a zaprt za spremembe**." Ob novi zahtevi raje **dodajamo** kodo kot **spreminjamo** obstoječo (spreminjanje = večje tveganje).
- Izvedba: identificiraj **variabilnosti** ("Point of Variation") in jih opremi s **stabilnimi vmesniki** → uporaba vmesnikov namesto implementacije.
> 💡 **Primer:** Namesto `if (placilo == "kartica") {...} else if (placilo == "paypal") {...}` (spreminjaš ob vsakem novem načinu) → vmesnik `NacinPlacila` z metodo `placaj()`, vsak nov način = nov razred (samo dodaš). Polimorfizem > dedovanje.

#### L — Liskov-Substitution Principle (LSP) [Barbara Liskov, 1988]
"Sistem gradimo iz **enostavno zamenljivih gradnikov**." Podtip mora biti uporaben **povsod**, kjer pričakujemo nadtip, ne da bi se obnašanje pokvarilo.
> 💡 **Primer (klasičen):** `Kvadrat extends Pravokotnik` zveni logično, a če `setSirina()` pri kvadratu spremeni tudi višino, se obnašanje pokvari tam, kjer koda pričakuje pravokotnik → krši LSP. Pazljiva uporaba generalizacije!

#### I — Interface-Segregation Principle (ISP)
"Izogibajmo se **nepotrebnim odvisnostim**." Več **majhnih, specializiranih** vmesnikov je bolje kot en velik vseobsegajoč.
- Kako si lahko odvisen od nečesa, česar ne uporabljaš? Odvisen si lahko od **dela** gradnika → loči (segregiraj) vmesnike.
> 💡 **Primer:** Namesto velikega vmesnika `Delavec { delaj(), jej(), spi() }` (robot ne je/spi!) → ločeni vmesniki `Delavni`, `Hranljivi`, `Spalni`. Razred implementira le, kar potrebuje.

#### D — Dependency-Inversion Principle (DIP)
"Visoko-nivojski moduli (poslovna logika) naj **NE bodo odvisni** od nizko-nivojskih (detajli). Oboji naj bodo odvisni od **abstrakcij**."
- Tradicionalna smer: UI → poslovne komponente → integracija → trajni podatki (visoka sklopljenost).
- **Obrat odvisnosti** preko vmesnikov: detajli (baza) so odvisni od poslovnih pravil, ne obratno.
- Orodja: vmesniki, izogibanje konkretnim implementacijam, izogibanje dedovanju od konkretnih razredov in preoblaganju (override) konkretnih metod.
> 💡 **Primer:** `OrderService` (poslovna logika) ne kliče neposredno `MySQLDatabase`, ampak vmesnik `OrderRepository`. `MySQLOrderRepository` ta vmesnik implementira. Bazo lahko zamenjaš brez dotika poslovne logike. (To je tudi srce Čiste arhitekture iz K2!)

### 📌 Za zapomniti (Snovanje + SOLID)
- Solution Architect ≈ "IT arhitekt"; arhitekt rabi širino + komunikacijo + leadership.
- Proces: analiza → sinteza (iz backloga) → evalvacija; vhod = architectural drivers (vključno z atributi kakovosti).
- Viewpoints (struktura) + Perspectives (kakovosti čez poglede); arhitekt uravnoteži kompromise.
- **SOLID:** **S**=en razlog za spremembo, **O**=odprto za razširitve/zaprto za spremembe, **L**=zamenljivi podtipi, **I**=majhni vmesniki, **D**=obrni odvisnosti preko abstrakcij.

---

## 3️⃣ UVELJAVLJENI ARHITEKTURNI STILI

> Stil = preverjena dobra praksa za **organizacijo gradnikov sistema**.

### 🏗️ Pregled stilov
(1-/2-/3-/večnivojska) **nivojska arhitektura**, **cevovod (pipeline)**, **komponentna**, **storitvena (SOA)**, **dogodkovno gnana (EDA)**, **mikrostoritvena (MSA)**, **brezstrežniška (serverless)**.

### 🥞 Večnivojska (layered) arhitektura
**Ideja:** uporabniško zahtevo razrešujemo **postopno po nivojih**; vsak nivo obdela en aspekt. Komponente so združene **horizontalno** (šibko sklopljene znotraj, močno vezljive).
- Tipični nivoji: **Presentation (UI) → Business Logic → Persistence/Data Access → Database**.
- **Izolacija nivojev:** odvisnosti kažejo navzdol; sprememba komponente vpliva le na sosednja nivoja. Nivoji so "CLOSED" (zahteva mora skozi vse), izjemoma dovolimo preskok.

**✅ Prednosti:** vsak nivo = abstrakcija; ločevanje kode; omejena odgovornost (lažja implementacija/test); dobro definirani vmesniki; **odlična privzeta izbira, ko nisi prepričan**; de-facto standard (RUP); preslika organiziranost IT oddelkov.

**❌ Slabosti:** tendenca k **monolitu** (sprememba → namestitev celote); težave z zanesljivostjo/robustnostjo; **težavno skaliranje**; obdelava ni najučinkovitejša.
> ⚠️ **Antivzorec "Architecture Sinkhole":** zahtevki samo "potujejo" skozi nivoje brez procesiranja. **Pravilo 80-20:** sprejemljivo, če ~20 % zahtevkov le potuje, 80 % pa se dejansko obdeluje.

### 🧩 Storitveno usmerjena arhitektura (SOA)
Storitve (Account, Book, Order, Shipping) komunicirajo preko **ESB (Enterprise Service Bus)** – centralnega vodila. Consumers ↔ ESB ↔ Providers. Pogosto deljene baze.

### 📨 Dogodkovno gnana arhitektura (EDA)
Temelji na **objavi, naročanju in odzivanju na (asinhrone) dogodke**. Avtonomne komponente: **generatorji** in **odjemalci** dogodkov. Ob objavi dogodka vsi zainteresirani: preberejo → procesirajo → prožijo nadaljnje → generirajo nove dogodke.
- **Visoko skalabilno**, šibko sklopljeni gradniki.
- Dve topologiji:
  - **Mediator** – centralna orkestracija: sporočilo → mediacija → kanal → procesor.
  - **Broker (posrednik)** – brez centralne orkestracije; brezpogojno posredovanje/naročniški model; za enostavne dogodke.
- **Slabosti:** dodatni členi → možna slabša učinkovitost; večja kompleksnost infrastrukture; posrednik = enotna točka odpovedi; varnost; transakcije; težave pri sinhronih procesih; **verzioniranje sporočil**.

### 🔬 Mikrostoritvena arhitektura (MSA)
> **Mikrostoritve** = kontekstno omejeni gradniki, ki jih je možno **neodvisno nameščati** in komunicirajo s **sporočili** (sinhrono ALI asinhrono).
> **MSA** = stil gradnje rešitev iz skladno sestavljenih mikrostoritev + **avtomatizacija**.

**Kdaj je storitev res MIKROstoritev?** Neodvisna, majhna, komunicira s sporočili, **kontekstno omejena**, neodvisno razvita, **decentralizirana**, zgrajena/nameščena z avtomatizacijo (+ majhna ekipa, enostaven API).

**Odgovor na monolit:** monolit = vsa funkcionalnost v enem procesu, skalira z repliciranjem celote. MSA = vsak element funkcionalnosti = ločena storitev, skalira z distribucijo. **Vsaka MS ima svojo bazo!**

**Določanje meja MS:** ni "prav/narobe", temveč "bolje/slabše". Vprašanje je **poslovno**, ne tehnično (dobra arhitektura preslika realno poslovanje). Pristop: **Domain-Driven Design (DDD)** – fokus na domeni, iterativno sodelovanje IT in domenskih strokovnjakov. **PAZLJIVO!** (lahko se zaplete).

**✅ Prednosti:** stroga modularnost (kode, ekip), neodvisnost pri nameščanju, **tehnološka svoboda**.
**❌ Slabosti:** je **distribuiran sistem** (z vsemi izzivi), pogosto **eventual consistency** (prihodnja konsistentnost), visoka kompleksnost vzdrževanja.

**⚠️ Predpogoji za MSA (Fowler):** **rapid provisioning** (nov strežnik v urah), **basic monitoring** (zaznava tehničnih in poslovnih težav), **rapid deployment** (hitra avtomatizirana dostava). Brez tega → ne lotevaj se MSA.

> 📊 **Trend (Jakarta EE 2025):** Hibrid 43 %, mikrostoritve 33 % (rastejo), monoliti 14 % (padajo). Popularnost MSA morda upada.

### 📊 Primerjava stilov (Mark Richards)
| Atribut | Layered | Event-driven | Microkernel | Microservices | Space-based |
|---|---|---|---|---|---|
| Overall Agility | ⬇️ | ⬆️ | ⬆️ | ⬆️ | ⬆️ |
| Deployment | ⬇️ | ⬆️ | ⬆️ | ⬆️ | ⬆️ |
| Testability | ⬆️ | ⬇️ | ⬆️ | ⬆️ | ⬇️ |
| Performance | ⬇️ | ⬆️ | ⬆️ | ⬇️ | ⬆️ |
| Scalability | ⬇️ | ⬆️ | ⬇️ | ⬆️ | ⬆️ |
| Development | ⬆️ | ⬇️ | ⬇️ | ⬆️ | ⬇️ |

> Tudi večslojne arhitekture danes pogosto dojemamo kot **"monolitne"**. Spekter kompleksnosti: Monolit → Microservices → Serverless.

### 📌 Za zapomniti (Stili)
- Layered = varna privzeta izbira; pazi na Sinkhole antivzorec.
- SOA = storitve preko ESB; MSA = neodvisne MS, vsaka svoja baza, sporočila.
- EDA = asinhroni dogodki, mediator vs broker topologija.
- MSA prednosti (modularnost, neodvisno nameščanje, tehnološka svoboda) vs slabosti (distribuiranost, eventual consistency, kompleksnost).
- Meje MS so poslovno vprašanje (DDD). MSA rabi provisioning + monitoring + deployment.

---

## 4️⃣ KOMUNIKACIJSKI STILI IN SOČASNOST V PORAZDELJENIH ARHITEKTURAH

### 🌐 Zakaj porazdeljeni sistemi
Sistem razdelimo po več računalnikih (zaradi zahtevnosti, poslovnih potreb, integracije IS). **Izzivi:** znane rešitve v novi luči + nove težave; učinkovitost, zanesljivost, varnost.

### ⚠️ "Zmote" porazdeljenega računalništva (fallacies) — KLJUČNO
Napačno predpostavljamo, da je omrežje:
1. **zanesljivo** – NI! (odpovedi HW/SW, varnostne grožnje → rabimo redundanco, ponovno pošiljanje, potrditve, ignoriranje duplikatov, pazi na **vrstni red**).
2. **brez zamika (latence)** – NI! (latenca > pasovna širina kot problem; **NE tretiraj oddaljenih klicev kot lokalnih**; MANJ klicev, VEČ podatkov hkrati).
3. **z neskončno pasovno širino** – NI! (paketi se izgubljajo; pošiljaj le potrebne podatke).
4. **varno** – NI! (vedno kriptiraj; varnost na nivoju omrežja, HW IN SW).
5. **s fiksno topologijo** – NI! (operaterji jo spreminjajo; uporabi imeniške storitve, ne statičnih končnih točk).
6. **z enim administratorjem** – NI! (več operaterjev, sodelujoča podjetja; nimaš nadzora, druge domene morda ne zaupajo).
+ tudi: nadgradnje delov sistema, na katere nimaš vpliva.

> 🔑 **Dva splošna napotka:** (1) naj komunikacijo počne **nekdo drug** namesto tebe (ogrodje, platforma, vmesni sloj); (2) **čim manjkrat, čim večja količina podatkov**.

### 📡 Komunikacijski stili (vzorci)

#### Vzorec: Deljeni podatki (Shared Data)
Več komponent si deli in obdeluje podatke, ki ne pripadajo nobeni. Izmenjava preko **branja/pisanja v deljeno bazo**; iniciira lahko katera koli komponenta.
- **MSA varianta: deljena podatkovna baza** – ena baza za več storitev, ACID transakcije, prost dostop do tujih podatkov.
- **❌ Slabosti:** baza = **ozko grlo**, **ena točka odpovedi**, **močna sklopljenost** pošiljatelja in prejemnika. (Raje NE v kombinaciji s sočasnimi dostopi.)

#### Vzorec: Komunikacija 1-1 (P2P – Peer-to-Peer)
Enakovredne komponente, vsaka lahko iniciira komunikacijo; tipično **sinhrono (zahteva-odgovor)**, redkeje asinhrono. Komponente izpostavijo funkcionalnost preko API; dinamično lociranje (imeniške storitve).
- **❌ Slabosti:** **močna sklopljenost** (komponente vedo druga za drugo v kodi), odvisnost od topologije; težko vodenje varnosti/konsistence/razpoložljivosti; težko zagotoviti **kombinacijo** NFZ.
- Predstavnik: **Gnutella** (P2P file sharing).

#### Vzorec: Namestnik (Proxy)
Komunikacija z objektom **izključno preko vmesnika**. Vmesnik definira dostopno funkcionalnost; implementacija + skrita pomožna funkcionalnost. → **Uporabnik je neodvisen od implementacije.** (Client → Subject interface → Proxy → RealSubject.)

#### Vzorec: Poziv na daljavo (RPC / RPI)
Oddaljeni klic metode/funkcije, kot da bi bila lokalna. **MSA vzorec POZIV NA DALJAVO:** storitve komunicirajo z RPI, protokol zahteva/odgovor (npr. **REST**).
- **gRPC:** odprtokodno RPC ogrodje; podpira mnogo jezikov; IDL = **ProtoBuffers** (binarna serializacija); transport **HTTP/2**; varnost SSL/TLS; +streaming. (Analogija: REST = vrtna cev, gRPC = gasilska cev 🔴.)
- **REST (Representational State Transfer)** – arhitekturni stil **spleta**:
  1. **Identifikacija virov z URI**.
  2. **Enotni vmesnik:** GET (poizvedba, idempotentna, cache), POST (kreiranje), PUT (posodobitev), DELETE (brisanje).
  3. **Samo-opisnost** sporočil (metapodatki, predstavitve).
  4. **Hiperpovezave** za prehode med stanji.

#### Vzorec: Posrednik (Broker)
Komunikacija poteka **posredno** preko posrednika. Odjemalec ne ve za lokacijo/vmesnik/zasedenost strežnika.
- Broker loči odjemalce od strežnikov; locira in posreduje (morda preoblikuje) klic. Eno-/obojesmerno, sinhrono/asinhrono.
- Gradniki: Client-Side Proxy, Server-Side Proxy, Bridge, Broker (locateServer, registerServer…).
- Odjemalec in strežnik se povežeta **ločeno** (lokacijsko/časovno).
- **❌ Slabosti:** dodatna latenca, ozko grlo, **ena točka odpovedi**, kompleksnost, težje testiranje, varnostna ranljivost.
- Primeri: **CORBA** (ORB, IIOP), **ESB**.

#### MOM (Message-Oriented Middleware) — pošiljanje sporočil
**Pošiljatelj → Posrednik → Prejemnik.** Posrednik sprejme sporočilo in ga posreduje registriranim prejemnikom (lahko več). Pošiljatelj lahko po oddaji **"pozabi" (fire-and-forget)**.
- Naloge posrednika: ne blokira pošiljatelja, prevzame odgovornost za dostavo, sprejema od več pošiljateljev za več prejemnikov.
- **Zagotovljena dostava:** 1. pošiljanje → 2. trajno hranjenje → 3. sprejem → 4. potrditev → 5a. umik / 5b. potrditev.
- Predstavniki: JMS, **RabbitMQ**, **Apache Kafka**.

#### Vzorec: Objavi-Naroči (Publish-Subscribe)
Mnogo neodvisnih komponent, ki **niso znane vnaprej**. Odjemalci se **naročijo**, strežnik **generira**, sporočilo se reproducira vsem naročnikom (tipično **enosmerno**, preko posrednika).
- **❌ Težave:** povečana latenca, slabša predvidljivost (vrstni red naročnikov), zagotovljeno naročanje.
- **GoF vzorec Opazovalec (Observer / Dependent / Publish-Subscribe):** odvisnost ena-proti-mnogo; ob spremembi celote (Subject) se obvestijo opazovalci (registerObserver, unregisterObserver, notifyObservers → update()).
- ⚠️ **MOM Topic – pozor pri naročnikih:** navaden **neaktiven naročnik nikoli ne dobi sporočila**; **trajen (durable) naročnik** ga dobi, ko postane aktiven (sporočilo se trajno hrani, izbriše ko so vsi trajni naročniki obveščeni).
- **Streaming (Kafka):** Producer → Broker (Topic → Partitions) → Consumer; Zookeeper, offset.

#### MSA vzorci za zunanji API
- **MSA vzorec PREHOD (API Gateway):** enotna vstopna točka za vse odjemalce; preusmerja/agregira zahteve; lahko preverja pooblastila; lahko en gateway na storitev ali skupen.
- **MSA vzorec ZALEDJA ZA UPORABNIŠKE VMESNIKE (Backend for Frontend, BFF):** ločen gateway/vmesnik **za vsako vrsto odjemalca** (mobilni, spletni, tretje aplikacije).
- **MSA vzorec DOMENSKI DOGODEK (Domain Event):** poslovno logiko organiziraš kot DDD agregate, ki **oddajajo dogodke** ob spremembi; druge storitve te dogodke uporabljajo.
- **MSA vzorec SPOROČANJE:** asinhrono sporočanje preko kanalov. Načini: zahteva/odgovor, obvestila (brez odgovora), zahteva/asinhron odgovor, objava/naročnina, objava/asinhron odgovor.

### 🔄 Sinhrono vs. asinhrono (sporočilni sistem vs. RPC/ORB)
**Sporočilne sisteme (asinhrono) uporabi ko želiš:** hitre odzive (skrbi te procesni čas), porazdeljevanje bremena, prioritetno procesiranje, **šibko sklopljenost/integrabilnost**, lokacijsko porazdelitev, paralelno procesiranje, visoko zanesljivost, M-N komunikacijo.
**NE uporabi sporočil ko:** **TAKOJ** potrebuješ rezultat za nadaljevanje, velika verjetnost neuspeha, operacija je del **večje transakcije**, slaba učinkovitost prenosa, varnostno domeno prenašaš na strežnik.

### ⚙️ Sočasnost (concurrency) — dilema
| Pojem | Pomen |
|---|---|
| **Hkratno (concurrent)** | program omogoča **istočasno** izvajanje akcij (lahko na enem jedru, prepleteno) |
| **Paralelno (parallel)** | **hkratno** izvajanje na paralelni strojni opremi (več jeder) |
| **Porazdeljeno (distributed)** | paralelno v omrežju z neodvisnimi procesorji **brez skupnega pomnilnika** |

> 💡 **Analogija:** 2 vrsti + 1 avtomat = concurrent. 2 vrsti + 2 avtomata = parallel.

**Klasična delitev razporejanja opravil:**
- **Cooperative (sodelujoč):** nit ima nadzor, dokler ga sama ne preda; po prioritetah; hiter, brez težav s sinhronizacijo; težje programiranje; niti tečejo **hkratno**.
- **Pre-emptive:** OS z uro menja kontekste (time slice); počasnejši (jedro upravlja); lažje programiranje; bolj zanesljiv (manj stradanja); niti lahko tečejo **paralelno**.

**V čem je problem? (race condition)**
> 💡 **Primer:** 3 niti hkrati kličejo `povecajZaEna()` (`rez=st; rez=rez+1; st=rez;`). Rezultat ni 900, ampak npr. 871, ker se operacije **prepletejo** (ena nit prebere staro vrednost, preden druga zapiše).
> **Rešitev:** rezervirana beseda **`synchronized`** (zaklepanje na nivoju objekta) ali **`volatile`**.

**Sinhronizacija z monitorji:** rešujejo problem **kritične sekcije**; monitor = **pasivni** element (M), nit = **aktivni** element (N); poskrbi za vzajemno izključevanje in sinhronizacijo.
**`wait()`/`notify()`/`notifyAll()`:** `wait()` ustavi nit, dokler druga ne pokliče `notify`; `notifyAll()` zbudi vse čakajoče. (Klasičen primer: proizvajalec-potrošnik z omejeno vrečko/buffer.)

**Stateless vs Stateful:**
- **Stateless (brez stanja):** visoka učinkovitost, enostavno porazdeljevanje bremena, izpadi vozlišč niso problem. (Instance pool – kateri koli stateless gradnik obravnava klic.)
- **Stateful (s stanjem):** slabša učinkovitost, obnašanje v skladu z OO, težavno porazdeljevanje bremena.

> 🔮 **Zakaj funkcijsko programiranje?** Mooreov zakon dosegamo s **horizontalno** skalabilnostjo (več jeder/vozlišč). Težava paralelizma je pogosto v **podatkih (deljeno spremenljivo stanje)**. → **Stateless** + **nespremenljivo (immutable) stanje** + **funkcija kot parameter** to rešijo.
> 💡 `for (int i...) {...}` (imperativno/strukturno) vs `list.forEach(s -> {...})` (deklarativno/funkcijsko).

### 🔒 Mehanizmi deljenja virov + izzivi
Kontrolirano (tipično **zaklepanje**), pazljivo z deljenimi viri, definiraj **na nivoju arhitekture**.
**Izzivi:**
- **Smrtni objem (deadlock):** komponenta ne more do vira, ker ga je druga zaklenila. → zaklepaj v **fiksnem vrstnem redu**; bolje: čim krajše zaklepanje; najbolje: **odpovej se zaklepanju**.
- **Vzajemno čakanje (contention):** dve komponenti hkrati hočeta isti vir; ni hudo, a upočasnjuje → ustrezno dimenzioniraj bazene virov.
- **Tekmovanje za vire (race):** več komponent hkrati izvaja operacijo → lahko izguba/okvara podatkov → vedno varuj deljene vire, uporabljaj nespremenljivo stanje, čim manj komunikacije.

> 🎯 **Fokus arhitekta:** nizko-nivojska sinhronizacija (niti) je **implementacijski detajl**! Arhitekt skrbi za sočasnost in odvisnosti na nivoju **večjih komponent** in določi pravila/vzorce. Aplikacijski strežniki, bazeni virov, **stateless** komponente v vsebnikih in orodja za analizo nam pomagajo ("ne izumljaj tople vode").

### 📌 Za zapomniti (Komunikacija + sočasnost)
- Zmote distribuiranih sistemov: omrežje NI zanesljivo/brez latence/neskončno/varno/fiksno/z enim adminom.
- Stili: deljeni podatki (ozko grlo), P2P (močna sklopljenost), proxy, RPC/REST/gRPC, broker (ena točka odpovedi), MOM/pub-sub (šibka sklopljenost).
- MSA vzorci: API Gateway, BFF, Domain Event, Messaging.
- Sinhrono (takoj rezultat, transakcije) vs asinhrono (skalabilnost, šibka sklopljenost).
- concurrent ≠ parallel ≠ distributed; race condition → synchronized; deadlock/contention/race.
- Stateless > stateful za skaliranje; immutable stanje rešuje paralelizem.

---

## 5️⃣ ADR – ARCHITECTURAL DECISION RECORDS (arhitektura v agilnem svetu)

### 🏃 Kontekst: agilni razvoj
Agilno = **odlašanje z odločitvami** ("Make decisions at the **last responsible moment**"), maksimiranje neopravljenega dela, fokus na funkcionalnostih.
- **Cost of deciding** pada s časom, **cost of deferring** raste → presečišče = zadnji (ekonomsko) odgovorni trenutek.
- Parcialni pristopi: vmesni čas za načrtovanje (ni prava arhitektura), Technical Owner, **architectural epics/stories**, **Architectural Runway** (vnaprejšnje omogočanje prihodnjih funkcij z "enablerji").

### ❗ Problem
Arhitekturne odločitve se sprejemajo na sestankih, v Slack/Teams, **v glavah posameznikov**. Čez čas se izgubi: **kontekst, razlogi, zavrnjene alternative** → ponavljanje istih debat, napačne spremembe, "Zakaj smo to sploh naredili?".

### 💡 Rešitev: ADR (Michael Nygard, 2011; Tech Radar 2017)
**ADR = kratek dokument, ki zajame eno pomembno arhitekturno odločitev skupaj s kontekstom in posledicami.**
- Ne dokumentiramo (cele) **arhitekture**, ampak **arhitekturne odločitve**.
- Majhen (1-pager), **verzioniran**, sledljiv. De-facto: **GIT + Markdown**, najpogosteje preko **PR (pull request) → review → merge**.

### 📖 Terminologija (AKM – Architecture Knowledge Management)
| Kratica | Pomen |
|---|---|
| **ASR** | Architecturally-Significant Requirement – zahteva z merljivim vplivom na arhitekturo |
| **AD** | Architecture Decision – izbira pri načrtovanju, ki reši ASR |
| **ADR** | Architecture Decision Record – dokument, ki zajame ASR s kontekstom in posledicami |
| **ADL** | Architecture Decision Log – zbirka vseh ADR za projekt/organizacijo |

> Definicija: "An Architectural Decision (AD) is a **justified design choice** that addresses a functional or non-functional requirement that is **architecturally significant**."

### 📄 Struktura ADR (minimalna predloga)
```
# ADR-123: [Naslov odločitve]
## Context: [Zakaj? Kaj nas sili v odločitev?]
## Decision: [Kaj smo se odločili?]
## Consequences:
- Good: [koristi]
- Bad: [kompromisi]
```
**Tipičen primer (ADR 001 – izbira baze):** Kontekst → Odločitev (PostgreSQL) → Razlogi → **Alternative (MySQL, MongoDB)** → Posledice. + Status, Datum, Avtor.

**Statusi:** `Proposed → Accepted` / `Rejected` / `Deprecated` / `Superseded`.

### 🔄 Postopek sprejema
1. Identifikacija potrebe → 2. priprava osnutka → 3. pregled/diskusija (iteracija) → 4. sprejem (konsenz) → 5. implementacija/spremljanje → 6. arhiviranje.
- **Sprememba:** stari ADR gre v **Superseded**, nastane nov. Pri zavrnitvi → **Rejected** z razlogom.

### ⭐ Značilnosti dobrega ADR
1. **Jasna utemeljitev** (kontekst, alternative, stroški/koristi). Primer: "Primerjali Kafka in RabbitMQ; izbrali Kafka zaradi večje prepustnosti."
2. **Enoznačna in specifična** – en ADR = ena odločitev; časovni žig.
3. **Nespremenljiv** – ne urejaš obstoječega; dodaš nov ali nadomestiš ("ADR-05 → nadomeščen z ADR-12").

### 📝 Predloge in primeri
- **MADR**, **Nygard ADR**, **Y-Statement** (IBM), drugi.
- **Y-Statement:** *"In the context of `<use case>`, facing `<concern>`, we decided for `<option>` and neglected `<other options>`, to achieve `<quality>`, accepting `<downside>`, because `<rationale>`."*
- **Google ADR:** Authors, Context/problem, Functional & non-functional requirements, Critical User Journey (CUJ), Overview of key options, Decision + reasons.
- Standard **IEEE/ISO/IEC 42010:2022**.
- **Orodja:** GIT+MD+PR (`/docs/adr`), VS Code ADR Manager, **Log4brains**, ADR Log CLI, Confluence/Notion.

### ✅ Dobre prakse / ⚠️ napake
- **Prakse:** definiraj predlogo, dogovori se kaj je arhitekturna odločitev, vključi ADR v **PR proces**, določi odgovornosti, redno pregleduj zastarele ADR.
- **Napake:** preveč detajlov/predolg dokument, dokumentiranje za nazaj, brez jasnega "decision" dela, ADR ni del razvojnega procesa.
- **Uporabljajo:** agilne ekipe, startupi, cloud-native ekipe, **Microsoft (Azure), Amazon (AWS), Google, Spotify, GOV.UK**.

### 📌 Za zapomniti (ADR)
- ADR dokumentira **odločitve**, ne cele arhitekture; majhen, verzioniran v Git, preko PR.
- ASR → AD → ADR → ADL.
- Struktura: Context / Decision / Consequences (+ alternative, status).
- Nespremenljiv: stari → Superseded, nov nastane.
- Reši izgubo konteksta in "zakaj smo to naredili".

---

## 6️⃣ SPL – PROGRAMSKE PRODUKTNE LINIJE (Software Product Lines)

### 🎯 Glavna ideja
**SPL = množica programskih izdelkov, ki si delijo skupen, obvladljiv nabor funkcionalnosti določenega segmenta/namena in so razviti na predpisan način iz množice skupnih gradnikov (core assets).**
> Več "različic" istega izdelka za več strank (npr. Free / PRO / Demo / Test / Razvoj). 
> "Most work is about **integration** instead of **creation**."

### 🧩 Funkcionalnosti
- **Skupne (temeljne)** – v vseh linijah, enake → realiziraj v skupnem osnovnem gradniku.
- **Opcijske** – le v nekaterih linijah.
- **Alternativne** – ista funkcionalnost, drugačna izvedba.

### 🆚 Posamezni izdelki vs. SPL
> 💡 **Primer:** Imaš izdelke `ABCD`, `ABCEF`, `GCEF`. Pri SPL so vsi gradniki (A,B,C,D,E,F,G) del **ene produktne linije**. Spremeniš "C" → sprememba se odslika **na vseh izdelkih hkrati**. Pri ločenih izdelkih bi moral spremeniti vsakega posebej.

### 🔁 Zakaj? (ponovna uporaba)
"Tradicionalna" ponovna uporaba (subroutines → modules → objects → components → services) je bila **drobnozrnata, priložnostna, tehnično gnana** → ni dosegla poslovnih ciljev. SPL = **sistematična** ponovna uporaba **večjih zaključenih enot** na **poslovnem** nivoju.

### 🔄 Procesi (omogočena ponovna uporaba celotnega procesa razvoja)
**Razvoj osnovnih gradnikov** + **Razvoj izdelkov** + **Upravljanje** (3 sklopi).
**Produkti pertain to** poslovnim ciljem/domeni, **share an** arhitekturo, **are built from** komponent/storitev (core assets). Product lines: take economic advantage of commonality, bound variation.

### 🏭 Kje se uporabljajo
Mobilne aplikacije, nadzorni sistemi (ladje, sateliti), letalska industrija, avtomobili, medicinske naprave, tiskalniki, finančni/davčni sistemi…

### 💎 Doprinosi (Northrop, SEI)
- do **10x** boljša produktivnost,
- do **10x** boljša kakovost,
- skupni stroški razvoja znižani do **60 %**,
- time-to-market krajši do **98 %**,
- prehod na nova tržišča v mesecih (ne letih).

### 🔑 Kdaj uporabiti SPL
- enaka funkcionalnost za različne izdelke/stranke,
- enaka sprememba mora v več izdelkov,
- enaka funkcionalnost se mora **različno obnašati** glede na izdelek,
- ne moreš več vzdrževati starih različic (stranka mora preiti na novo),
- ne znaš oceniti stroška prenosa funkcionalnosti,
- spremembe infrastrukturnih gradnikov vodijo v nepredvidljivo obnašanje,
- večino truda porabiš za **vzdrževanje**, ne za nove funkcije.

### 🚫 Kaj NI SPL
Splošna ponovna uporaba (knjižnic), razvoj enotnega sistema, klasičen komponentni/storitveni razvoj, arhitektura z možnostjo konfiguriranja, samo različice ene programske opreme.

### 🌳 Modeliranje variabilnosti — Feature Model
> **Variabilnost** = sposobnost PO ali gradnika, da jo lahko učinkovito **razširimo, spremenimo ali prilagodimo** za uporabo v določenem kontekstu.

**Feature model (diagram lastnosti):** drevo z notacijo:
- **Mandatory (obvezna)** – polna pika ●,
- **Optional (opcijska)** – prazna pika ○,
- **Alternative (točno ena izmed)** – prazen lok,
- **Or (ena ali več)** – poln lok,
- relaciji **requires** in **excludes** (npr. "CreditCard **implies** High security").

> 💡 **Primer (E-Shop):** Catalogue (obvezno), Payment {Bank transfer / Credit card – or}, Security {High / Standard – alternative}, Search (opcijsko).

**Variabilnost na nivoju funkcionalnosti:** prisotnost / odsotnost / drugačna realizacija.
**Na tehničnem nivoju:** podatki, tok izvajanja, tehnologija (SW/HW), kriteriji kakovosti, ciljno okolje.

### 🔧 Realizacija variabilnosti
Vključitev gradnika/komponente/storitve, **načrtovalski vzorci** (tovarna, abstraktna tovarna, most), dedovanje, razširjanje (vključki), **parametriziranje**, konfiguracijski deskriptorji (metapodatki ob izvajanju), direktive ob prevajanju, **generiranje izvorne kode**.

### 💰 Ekonomski + skriti vidik
- **Skriti stroški:** arhitektura (podpora variabilnostim), gradniki (točke variabilnosti), testiranje (različno obnašanje), poslovni načrt (družina, ne posameznik), projektni plan, dodatna tehnična znanja.
- **Ekonomska krivulja (Weiss & Lai):** SPL ima **višji začetni strošek**, a po **payoff point** (cca. 2-3 izdelki) je skupni strošek nižji od ločenega razvoja.

> 📊 **Empirična študija (24alife, Pavlič et al.):** SPL dal **126 % višji functionality-based velocity**, +100 % novih funkcionalnosti z istim trudom, notranja kakovost nespremenjena, **zunanja kakovost izboljšana**, večja samozavest razvijalcev. Danes podpora na nivoju platforme (**Android Flavors / build variants**).

### 📌 Za zapomniti (SPL)
- SPL = sistematična ponovna uporaba za **družino** izdelkov s skupno arhitekturo + core assets.
- Funkcionalnosti: skupne / opcijske / alternativne → **feature model** (mandatory/optional/or/alternative + requires/excludes).
- Smiselno pri **>80 % skupnih funkcionalnosti**; višja začetna investicija, payoff po nekaj izdelkih.
- Realizacija variabilnosti: vzorci, parametriziranje, konfiguracija, generiranje kode.
- Uspeh = dobra arhitektura + jasno upravljanje variabilnosti.

---

## 7️⃣ OBLAČNO DOMORODNE ARHITEKTURE: OBLAK, ZABOJNIKI, CNCF, KUBERNETES

### ☁️ Kaj je računalništvo v oblaku
> NIST: "Model za **ubikvitaren, priročen, on-demand** omrežni dostop do **deljenega bazena** nastavljivih virov (omrežja, strežniki, shramba, aplikacije), ki se **hitro zagotovijo in sprostijo** z minimalnim upravljanjem."

**Konvencionalno vs. oblak:**
| Konvencionalno | Oblak |
|---|---|
| Namenska strojna oprema, fiksne kapacitete | Deljena strojna oprema, **dinamične** kapacitete |
| Plačilo po kapaciteti | **Plačilo po uporabi (pay-as-you-go)** |
| Upravljanje preko adminov | Upravljanje preko **API-jev** |

> Temelj = **VIRTUALIZACIJA**.

### 📈 Optimizacija virov + skalabilnost
- Klasične kapacitete = stopnice (preveč ali premalo virov); oblak sledi dejanskim potrebam.
- **Vertikalna skalabilnost (scale-up):** nadgrajevanje obstoječega vozlišča.
- **Horizontalna skalabilnost (scale-out):** dodajanje vozlišč. (Cloud favorizira horizontalno.)

### 🔑 5 lastnosti oblaka
1. **Deljeni viri** (skupni bazen, ekonomija obsega),
2. **Omrežni dostop** (odprti standardi, IP/HTTP/REST),
3. **Samopostrežnost po potrebi** (avtomatizirano, realnočasovno),
4. **Skalabilnost in elastičnost** (dinamično dodajanje/sproščanje),
5. **Merjenje uporabe / QoS** (pay-as-you-go, prekinljivo).

**Poslovni vidik:** znižanje stroškov, pay-as-you-go, time-to-market, ROI, **CAPEX → OPEX**, Green IT, **multi-tenant** (ena namestitev za več strank). 
**Tehnični vidik:** virtualizacija, večnajemniški model, samopostrežba, avtomatizacija, API-ji, merjenje, orodja.

### 🏢 Namestitveni modeli
- **Javni oblak** – širši javnosti, pay-as-you-go (AWS, Azure, Rackspace). Prednosti: samopostrežba, navidezno neskončni viri, zanesljivost, brez začetnih stroškov. Pasti: **vendor lock-in**, zasebnost, izpadi, SLA, zakonodaja (lokacija podatkov).
- **Privatni oblak** – le ena organizacija; večji nadzor/varnost; on-premise ali zunanji (OpenStack, Hyper-V). Izberi ko: ekonomičnejša lastna infra, predvidljiva poraba, občutljivi podatki, skladnost z zakoni.
- **Hibridni oblak** – kombinacija; občutljivo v privatnem, računski viri iz javnega; ob konicah **cloudbursting**.

### 🍰 XaaS modeli
| Model | Kaj kot storitev |
|---|---|
| **IaaS** | Infrastructure (ti upravljaš OS+ navzgor) |
| **PaaS** | Platform (ti upravljaš aplikacije+podatke) |
| **SaaS** | Software (vse upravlja ponudnik) |
| **FaaS** | Function |
| **CaaS** | Containers |
| **BaaS/MBaaS** | (Mobile) Backend |
| DaaS, SSOaaS, AIaaS… | |

Klasično: IaaS (sam: podatki, aplikacije, vmesni sloj, OS) → PaaS (sam: podatki, aplikacije) → SaaS (vse ponudnik). Spodaj vedno: virtualizacija, HW, shramba, omrežje.

### ☁️ Iz vidika razvijalca/arhitekta
Oblak = naslednja stopnja distribuiranih arhitektur (predvsem **MSA in serverless**); razvoj z interoperabilnimi tretjimi gradniki; **horizontalno razširjanje**; lastništvo ni v eni domeni; uporaba standardov (pogosto na račun učinkovitosti).

### 🌐 Domorodne vs ne-domorodne aplikacije
- **Cloud-enabled** – premaknjena v oblak, a razvita za klasičen podatkovni center; nekaj prilagoditev.
- **Cloud-native (cloud-ready/cloud-centric)** – razvita z oblačnimi principi **v zasnovi**: multi-tenancy, elastično skaliranje, lahka integracija/administracija.

**CNA (Cloud Native Application):** načrtovana za delovanje (zgolj) v oblaku; distribuiranost, zunanji ponudniki, storitvena orientiranost, lokalne instance (redundanca); zgrajena na zabojnikih/mikrostoritvah/API; ločitev storitev od omrežnega naslova.

### 🔧 Širši kontekst virtualizacije
**Virtualizacija** (tehnologija: izolacija, učinkovitost) → **Avtomatizacija** (proces: IaC, CI/CD, ponovljivost) → **Standardizacija** (arhitektura/distribucija: neodvisnost od platforme, prenosljivost).

### 🖥️ Virtualizacija (VM)
- Virtualni stroj = izolirano računalniško okolje; **hipervizor (VMM)** deli fizične vire na logične.
- Neodvisnost od strojne opreme, konsolidacija (več VM na manj strežnikov), nižji stroški.
- Predstavniki: VMware, VirtualBox, Hyper-V, KVM, Xen, QEMU, Proxmox.
- **Migracija VM:** dobro v LAN; v WAN pazi na latenco.
- Platforme za delitev VM: **Vagrant Boxes**, OVA/OVF, Bitnami.

### 🤖 Avtomatizacija razvojno/namestitvene arhitekture
- **CI/CD** → večja hitrost, kakovost, pogosta integracija/nameščanje, standardizirano grajenje ("nič več 'pri meni dela'").
- **Vagrant** – orodje za upravljanje VM, avtomatizacija razvojnega okolja; **Vagrantfile** (box, omrežje, CPU/RAM, provision skripta); ukazi `vagrant up | ssh | halt`.
- **Terraform** – **Infrastructure as Code (IaC)**: infrastrukturo (VM, omrežja, diski) opišeš **deklarativno** s kodo (`.tf`); ukazi `terraform init | plan | apply | destroy`. Cloud ali on-premise. VM = "resource".
- Tudi: Ansible, Puppet, Chef.

### 📦 ZABOJNIKI (containers)
**Zabojnik = aplikacija + (standardizirano) okolje.** Bolj učinkovita "virtualizacija", standardizacija namestitvenih slik.
> 💡 **Primer:** Včasih PostgreSQL = prenesi, prevedi, konfiguriraj. Danes: `docker run -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:17.2`.

**Virtualni stroj vs. zabojnik (POMEMBNO):**
| Virtualni stroj | Zabojnik |
|---|---|
| Vsak VM ima **svoj OS** | Uporablja **jedro gostiteljevega OS** |
| Poljuben OS | PO mora biti skladna z gostiteljevim OS |
| Zagon **minute** | Zagon **sekunde** |
| Velikost **GB** | Velikost **MB** |
| Manjše število lokalno | Večje število lokalno |
| Trajno spremenljivi diski | **Niso trajno spremenljivi** (immutable) |

**Zgodovina (Kratzke):** Dedicated Server → Virtualization → **Containerization/Microservices** → **Serverless/FaaS** (time-sharing).

### 🐳 Platforma Docker
De-facto standard za zabojnike, odprtokoden, naslavlja distribucijo PO celostno.
**Trije koncepti:**
- **Zabojnik = izoliran proces** (NI VM, le proces).
- **Slika (image) = standardno pakiranje** (vse binarne datoteke, odvisnosti, konfiguracija).
- **Register = repozitorij slik** (Docker Hub – javen/zaseben).

**Kako deluje:** nadgrajuje jedro OS (chroot, imenski prostori); **Docker Engine** (dockerd + CLI) → **containerd** → **runc** (OCI runtime). 

**Docker slika (image):** posnetek datotečnega sistema + ukaz za zagon; **verzionirana, brez stanja, nespremenljiva**; vsaka sprememba = nova verzija; lahko temelji na drugi sliki.
**Docker zabojnik:** delujoč primerek slike; iz ene slike več zabojnikov.

**Kaj je v zabojniku:** sistemska orodja, izvajalno okolje (JRE/CLR), strežnik (Tomcat/IIS), knjižnice, konfiguracija, aplikacija.

**Življenjski cikel:** `created → running ↔ paused ↔ restarting → exited`. Ukazi: `docker run | start | stop | kill | pause | unpause | rm`.

**Docker CLI:** slike (`images, build, commit, export`), zabojniki (`ps, create, run, start, stop, rm, pause`), hub (`login, pull, push, search`).
**Ekosistem:** Docker Engine, Hub, **Swarm** (orkestracija), **Compose** (več zabojnikov), Desktop, Scout (varnost), Build Cloud, Testcontainers.
**Alternativa CLI:** Portainer.io (GUI).

**Omrežje:** `bridge` (privzeto lokalno), `host` (neposredno omrežje gostitelja), `overlay` (porazdeljeno, več vozlišč). **Port mapping** `-p 8080:80`. Zabojniki v istem omrežju se vidijo po **imenu**.

**Trajnost podatkov – Volume:** zabojniki so kratkotrajni → ob brisanju se podatki izgubijo. **Volume** = trajen datotečni sistem ločen od cikla zabojnika; lahko deljen med zabojniki (`docker run -v mysql_data:/var/lib/mysql ...`).

**Dockerfile** (gradnja lastne slike): `FROM` (osnovna slika), `COPY/ADD`, `RUN`, `CMD/ENTRYPOINT`, `ENV`, `EXPOSE`, `WORKDIR`, `VOLUME`, `USER`.
- **Sloji (layers):** vsak ukaz = nov sloj; sloji se delijo/predpomnijo → hitrejša gradnja; nespremenljivi. **Pogoste spremembe naj bodo v zadnjih slojih.**
- **Večstopenjska gradnja (multi-stage):** loči build okolje od run okolja → manjša končna slika.
- **Multi-platform:** `docker buildx --platform linux/amd64,linux/arm64` (slika za eno arhitekturo ne dela na drugi).
- **Deljenje:** Docker Hub (`tag`, `push`, `pull`).

**Docker Compose** – orkestracija več zabojnikov v eno celoto; format **YAML**: `services` (zabojniki), `volumes`, `networks`, `depends_on`. Ukazi `docker compose build | up -d | ps | down`.

### 🎼 Orkestracija in razširjanje zabojnikov
Ob rasti: koordinacija, vrstni red zagonov, nameščanje/nadgradnje, monitoring, kaj ko zabojnik "pade".
> ⚠️ **Niti Docker Swarm niti Kubernetes sama NE poganjata zabojnikov** – uporabljata spodaj ležeč runtime (Swarm → Docker Engine, K8s → ContainerD).

**Orkestracija omogoča:** razporejanje/razvrščanje, **skaliranje (horizontalno)**, spremljanje stanja + ukrepanje, visoko razpoložljivost, varnost, odkrivanje storitev, CD, nadgradnje.

#### Docker Swarm vs. Kubernetes
| | Docker Swarm | Kubernetes |
|---|---|---|
| Skaliranje | ročno | **avtomatsko (autoscaling)** |
| Namestitev | **enostavna, hitra** | kompleksna, časovno potratna |
| Load balancing | **avtomatsko** | ročna konfiguracija |
| GUI | ni dashboarda | **vgrajen dashboard** |
| Monitoring | 3rd-party (ELK) | **vgrajeno** |
| Optimiziran za | 1 velika gruča | več manjših gruč |
| Za koga | manjše org., PoC, dev | velike org., kompleksne potrebe, produkcija |

> **Kubernetes je de-facto standard** na vseh oblakih. Swarm = enostavnejši, za manjše/PoC.

#### Dilema: Kubernetes — skriti detajl ali lingua franca?
- **#1 Hide it:** razvijalce ne zanima koliko replik/Roles/StatefulSets – le da imajo HTTP endpoint → skrij K8s v CI/CD, dev samo pusha kodo.
- **#2 Expose it:** razvijalci niso več le koderji; pri MSA naj sami sprejemajo infrastrukturne odločitve. ("Krasni novi svet" – s katerim se ni nujno strinjati.)

#### Kubernetes (K8s) — koncepti (KLJUČNO za ustni!)
> "Resna" orkestracija, odprtokodna (Google, CNCF). Sama nima CLI (standard = **kubectl**). Distribucije za razvoj: **Minikube, MicroK8s, Docker Desktop**.

| Koncept | Pomen |
|---|---|
| **Pod** | osnovna enota; 1+ zabojnikov; skupaj nameščeni, **minljivi (ephemeral)**; delijo **IP** in **Volume**; komunikacija preko localhost |
| **Node (vozlišče)** | fizični/virtualni stroj, poganja pode; vsebuje **kubelet** (nadzira vozlišče) + **container runtime (CRE)** + kube-proxy |
| **Cluster (gruča)** | zbirka vozlišč (compute, memory, storage, network) |
| **Control plane** | API server, scheduler, controller manager, (cloud controller manager), **etcd** (persistence store); globalno stanje gruče |
| **Service** | izpostavi funkcionalnost; združuje pode na **logični** ravni (preko **label**); load balancing; tip LoadBalancer/NodePort/ClusterIP |
| **Label** | ključ-vrednost za grupiranje objektov; **selektorji** izbirajo po labelah (`role=webserver`) |
| **ReplicaSet** | skrbi, da vedno teče želeno število podov; self-healing |
| **Deployment** | "blueprint" za pode; updates & rollback nad ReplicaSet |
| **StatefulSet** | za porazdeljene shrambe (Cassandra); stabilen hostname, ordinal index, stabilna shramba, urejen zagon |
| **Volume** | trajna shramba (preko CSI), mountana v zabojnik |
| **Secret** | občutljivi podatki (gesla, tokeni); v etcd; mount kot datoteke ali env; tmpfs/memory |
| **Namespace** | izolacija/grupiranje virov; obseg imen; **šibka oblika izolacije** |
| **Annotation** | poljubni metapodatki |

> **YAML deployment:** `kind: Deployment` (želeno stanje, replicas, image, containerPort) + `kind: Service` (LoadBalancer, selector, port). Podobno Docker Compose.
> **kubectl ukazi:** `kubectl get nodes|pods`, `create deployment`, `expose deployment`, `apply -f file.yaml`, `logs`, `describe pod`, `port-forward`.

#### K8s povezani vzorci (sidecar/ambassador/adapter)
- **Sidecar:** dodatni zabojnik v podu poleg glavnega; glavni ga ne pozna. *Primer: centralni zbiralec logov – glavni piše v stdout, sidecar pošlje v centralno storitev.*
- **Ambassador:** predstavi oddaljeno storitev kot lokalno + uveljavlja politiko. *Primer: Redis – glavni se poveže na `localhost:6379`, ambassador filtrira/usmeri write na master, read na replike.*
- **Adapter:** standardizira **izhod** glavnega zabojnika. *Primer: nova verzija dela poročila v novem formatu; adapter ga prilagodi na star format, dokler vsi porabniki ne nadgradijo.*

### 🔐 Varnost zabojnikov
- Skeniranje slik: **Trivy, Clair, Grype/Syft, Docker Scout, Snyk, Aqua, Prisma Cloud**.
- **CVE** = globalni identifikator ranljivosti (MITRE/NIST). **SBOM** = seznam knjižnic/odvisnosti/licenc.
- **Docker Hardened Images:** minimalne slike (distroless/alpine/scratch), manj paketov → manj CVE; read-only FS, omejene Linux zmožnosti, SELinux/AppArmor, CIS Benchmarks; plačljivo FIPS/STIG.

### ✅ Dobre prakse + kontrolni seznam (horizontalno razširljiva aplikacija)
- **Hladni zagon (cold start):** prevajanje vnaprej, smiselna izbira jezika, ogrevanje.
- **HPA (Horizontal Pod Autoscaler):** samodejno (de)skaliranje podov glede na CPU/RAM.
- **Kakovost slik:** en namen, generična zasnova, majhna velikost, stanje od zunaj.
- **Lokacija nameščanja:** geografsko bliže uporabnikom (latenca, zakonodaja).
- **Napake pri kodi:** N+1 poizvedbe, zaklepanje vrstic, manjkajoči indeksi, neuporaba asinhronih funkcij, neuporaba HTTP/2/predpomnjenja.
- **Kontrolni seznam:** normaliziraj bazo (a le toliko kot treba), indeksi, ločene read/write instance, cache (Redis); konfiguracija ločena od kode, skrivnosti v namenskem sistemu; 1 strok = 1 slika = 1 storitev, HPA, stateless (brez stanja v lokalnem FS), večregijska arhitektura; metrike, centralno logiranje, monitoring (Grafana), threshold alerting.

### 🏪 Docker/CaaS v oblaku
**Zakaj:** upravljanje gruč prepustiš ponudniku, ni lastne HW, avtomatizacija, razpršitev čez več oblakov.
**Primeri uporabe (CaaS):** mikrostoritve, DevOps, hibridni/multi-cloud, modernizacija (lift-and-shift).
**Ponudniki:** Amazon ECS/EKS, Azure (AKS, Container Instances, Container Registry), Google (GKE, **Cloud Run**), OpenShift, IBM Cloud, Oracle Cloud, DigitalOcean.
- **GKE** = gruča Compute Engine instanc + povezava z Google storitvami.
- **Google Cloud Run** = podaš sliko zabojnika, platforma ustvari instanco; **stateless**, samodejno skaliranje, plačilo na desetinko sekunde.

### 📌 Za zapomniti (Oblak/Zabojniki/K8s)
- Oblak: deljeni viri, omrežni dostop, samopostrežba, elastičnost, merjenje; pay-as-you-go; CAPEX→OPEX.
- IaaS/PaaS/SaaS/FaaS/CaaS; javni/privatni/hibridni oblak.
- VM (svoj OS, GB, minute) vs zabojnik (jedro gostitelja, MB, sekunde, immutable).
- Docker: slika (nespremenljiva predloga) → zabojnik (instanca); Dockerfile + sloji; Compose + Volume + omrežja.
- Orkestracija: Swarm (enostaven) vs Kubernetes (zmogljiv, de-facto standard).
- K8s: **Pod** (osnovna enota, deli IP/Volume) → Node → Cluster; Deployment/ReplicaSet, Service+Label, Secret, Namespace, Volume.
- Vzorci: sidecar / ambassador / adapter.

---

## 8️⃣ BREZSTREŽNIŠKE ARHITEKTURE: BaaS, FaaS, Serverless

### 🔁 Event-first arhitekture (uvod)
Vsaka neodvisna storitev naj ima vire za delovanje **tudi če ostale ne delujejo**; storitve združujemo v neodvisne podsisteme **brez neposredne komunikacije** (preko posrednika sporočil). Cilj: enostavnost, nizka kompleksnost, gradnja iz ponovljivih gradnikov.
- Vzorci storitev (Gilbert): **Backend for Frontend**, **External Service Gateway**, **Control Service**.
- **CPCQ (Command, Publish, Consume, Query):** loči zapis sprememb / objavo dogodkov / porabo dogodkov / branje → asinhrona, odzivna arhitektura. (Service X: command→db→publish → event hub → Service Y: consume→db→query.)

### ❓ Kaj je brezstrežniška arhitektura?
> ⚠️ **Serverless ≠ Functions!** Funkcije, ki se izvedejo na zahtevo, so **le del** brezstrežniškega zaledja. Strežniki **še vedno obstajajo**, le ne skrbiš zanje.

**Lastnosti serverless računalništva:**
1. Ne skrbiš za **upravljanje strežnikov/procesov**.
2. **Samodejno** prilagajanje obsega in zagotavljanje.
3. **Stroški glede na uporabo** (ne po kapaciteti).
4. Zmogljivosti niso definirane po velikosti/številu.
5. **Implicitno visoka razpoložljivost**.

**Definicije:** "providing backend services on an **as-used** basis" (Cloudflare); "build and run apps **without managing infrastructure**" (AWS); **"costs you nothing if nobody is using it"** (Paul Johnston).

**Dva sestavna dela:**
- **FaaS (Functions as a Service)** – storitev računalništva.
- **BaaS (Backend as a Service)** – model storitev (+ shramba, sporočanje, varnost/SSO).

> ⚠️ **Zmota CaaS:** BaaS/FaaS ≠ CaaS! CaaS doda dodaten sloj v obliki **zabojnikov**.

### 🆚 MSA vs. brezstrežniška arhitektura
| | Mikrostoritvena | Brezstrežniška |
|---|---|---|
| Avtonomnost | na nivoju **storitve**, svoj cikel | na nivoju **funkcije**, eno delo na dogodek |
| Skalabilnost | možno, a če sam → težavno | **popolnoma samodejno** |
| Odpornost | svoje okolje | odvisna od ponudnika |
| Fleksibilnost | poljuben jezik/ogrodje | odvisna od ponudnika |
| Podatki | vsaka MS svoja baza | ponudnik zagotovi shrambo |
| Poslovni razcep | vezano na storitev | vezano na **funkcijo** |
| Stanje | deljenje stanja med klici | **popolnoma brez stanja** |
| Nivo abstrakcije | razvojni model | računalniška platforma |

> Razvojni spekter: Večslojna → SOA → MSA → Brezstrežniška. Serverless je **prej alternativa kot zamenjava**.

### 🗄️ BaaS (Backend as a Service)
**Zakaj:** za aplikacijo rabiš frontend + backend; od backenda pogosto le osnovne **CRUD** operacije → uporabi storitev ponudnika namesto lastnega zaledja.
**Značilnosti:** vnaprej pripravljene storitve (avtentikacija, upravljanje uporabnikov, shramba), enostavna vzpostavitev (le projekt + API), modularnost, samodejno skaliranje, pay-as-you-go (**primeren za majhen promet**).
**= PaaS++**; osredotočiš se na **uporabniški vmesnik/odjemalca**, infrastrukturo prepustiš tretji osebi.

**Tipična BaaS arhitektura (3 sloji):** 1. baze (NoSQL/SQL, podvajanje, backup), 2. aplikacijski strežniki (autoscale), 3. izravnalnik obremenitve + **CDN**.

**Gradniki BaaS:** shramba podatkov (NoSQL/SQL), shramba datotek (ločena), avtentikacija/upravljanje uporabnikov, **FaaS**. Komunikacija preko **API**.

**✅ Prednosti:** krajši time-to-market, nižji stroški (ni ekipe za zaledje), širok nabor funkcionalnosti.
**❌ Slabosti:** manj nadzora (nad implementacijo/infrastrukturo), **vendor lock-in** (težka migracija podatkov), manj prilagodljivosti.

**Ponudniki BaaS:** **Google Firebase** (Firestore NoSQL, Realtime DB, Auth, Cloud Storage), **AWS Amplify**, **Appwrite** (open-source), **Supabase** (open-source, PostgreSQL), Parse, Back4App, Azure, Kinvey.

### ⚡ FaaS (Functions as a Service)
> **FaaS = oblačna storitev, ki omogoča zaganjanje kode kot odziv na dogodke, brez vzpostavljanja infrastrukture ali razvoja zaledja.**
> "Nekoč" skrbi: nastavitev računalnika, odziv na obremenitve, plačilo tudi v mirovanju, konfiguracija. → FaaS: ni konfiguracije, plačaš le izvajanje, scale-up na zahtevo, ko ni zahtev → funkcije se ustavijo.

**Značilnosti:** **brez stanja (stateless)**, **dogodkovno gnana**, izvajalna okolja se vzpostavljajo/uničujejo po potrebi, **fino granulirano razširjanje**. Arhitektura vsebuje vsaj: **Trigger (sprožilec) → Controller (krmilnik) → Executor (izvajalno okolje)**.

**Spekter:** Monolitno zaledje → Mikrostoritve → **Funkcije** (najbolj drobnozrnato).

**✅ Uporabno za:** izvedbo ob spremembi podatkov, pošiljanje e-pošte, poslušanje čakalne vrste, časovna opravila, odziv na API klic.
**❌ NE za:** dolgotrajna dela (omejitve), ohranjanje stanja, ko želiš nadzor nad scale-up.

**Skalabilnost:** avtomatsko – npr. 1000 hkratnih zahtev → platforma sama požene več funkcij.
**Poraba (pay-as-you-go):** v mirovanju nič stroškov; **slabost:** pri pogostem proženju se stroški hitro naberejo.
**Dogodkovna orientiranost:** funkcije se izvedejo le ob dogodkih; prednost = aktivne le ko treba; slabost = kompleksnost upravljanja stanja (vse stateless).

#### Prožilci (triggers)
- **HTTP** – ob HTTP(S) zahtevi (gradnja API brez stalnega strežnika; AWS API Gateway → Lambda, GCP HTTP functions).
- **Spremembe v bazi** – vstavi/posodobi/briši (Firebase Realtime DB Triggers, AWS DynamoDB Streams).
- **Shramba datotek (Storage)** – nalaganje/posodobitev/brisanje (AWS S3 Triggers, GCP Storage Triggers; npr. generiranje thumbnaila).
- **Časovni (Cron / Scheduled)** – v intervalu (AWS CloudWatch Events, Google Cloud Scheduler; npr. čiščenje podatkov).
- **Message Queue** – ob sporočilu (AWS SQS, Google Pub/Sub; npr. obdelava naročil).
- **Dogodki v BaaS** – registracija uporabnika, sprememba gesla, spremembe dovoljenj.
- **Specifični:** AWS Kinesis (data streams), Azure Event Grid, IBM Cloud Functions (Kafka, CouchDB).

#### FaaS – ponudniki in ogrodja
- Ponudniki: **AWS Lambda**, **Google Cloud Functions**, **Azure Functions**, Cloudflare Workers, Twilio Functions.
- Open-source: **OpenFaaS, Apache OpenWhisk, Knative, Fission** (na Docker/Kubernetes).
- Ogrodja: **Serverless Framework** (multi-cloud, YAML), AWS SAM, Firebase Functions, Azure Functions Core Tools.
- Jeziki: Node.js, Python, Java, C#, Go, PHP, Ruby…

### 🤔 Funkcije — DA ali NE? (presoja na primerih)
| Scenarij | Razmislek | Odločitev |
|---|---|---|
| E-mail ob registraciji | trigger=event, stateless | ✅ tipičen primer za funkcijo |
| Prikaz podatkov profila | request-response, rabi podatke | ❌ raje BaaS |
| Preračun plače (neto iz bruto) | čisti izračun stateless / kompleksno | funkcija ali mikrostoritev |
| Thumbnail ob nalaganju slike | storage trigger, CPU a kratko | ✅ verjetno funkcija |
| Rezervacija terminov | kompleksna domena, transakcije | ❌ raje mikrostoritev |
| Pošiljanje SMS | brez stanja, klic zunanjega API, trigger | ✅ zelo primerno |
| Generiranje PDF | velika količina, pogostost, zahtevno | **odvisno od pogostosti** |

> 💡 **Strošek je odločilen!** PDF z Puppeteer: ~0.014 USD/1000 PDF. Pri 1.000.000 PDF/mesec = ~14 USD (cena stalnega zabojnika DigitalOcean ~15 USD). Pri 5M PDF = ~70 USD → **predrago**, raje zabojnik. → **Funkcije so poceni pri redkem proženju, drage pri pogostem.**

### ✅ Dobre prakse razvoja FaaS
- **Ena funkcija, ena naloga** (SRP za funkcije). Npr. `sendWelcomeEmail()` ne sme hkrati pisati v bazo.
- **Kratkožive funkcije, več izvedb** – ceneje več hitrih kot ena kompleksna.
- **Upravljanje odvisnosti** – eksplicitne, čim manjše (npr. `checkUserStatus(dbConnection)` – povezava kot parameter → lažje testiranje/mocking).
- **Izogibanje klicem drugih funkcij** – ohranja izoliranost, nižje stroške; raje vrni rezultat klicatelju (`generateReport()` ne kliče `sendEmail()`).
- **Dogodki in stanje:** ob enem dogodku ena funkcija; funkcije **stateless** (podatke iz baze).
- **Granularna dovoljenja** – vsaka funkcija dostop le do virov, ki jih rabi (varnost; a kompleksnejše upravljanje).
- **Testiranje + ravnanje z napakami** – urejeno, uporabniku prijazno, ponovni poskus.

### 🧪 Testiranje FaaS
- **Testiraj tudi v oblaku** (najbolj zanesljivo); izolirana okolja/računi, nadzor stroškov (alerti, limiti).
- **Mock testi** le kot **prva faza** (hitre iteracije, izolirana poslovna logika); koda mora biti testirana tudi v oblaku.
- **Emulatorji** uporabni, a se lahko razlikujejo od dejanske platforme → kombiniraj z oblakom. (Npr. **Firebase Emulator Suite:** `firebase init functions`, `firebase emulators:start`.)

### 🏢 Večnajemne (multi-tenant) SaaS rešitve
Ena aplikacija, ista infrastruktura za več strank (tenant); **(logično) ločeni podatki**; nižji stroški vzdrževanja (nadgradnja enkrat za vse); **varna izolacija med najemniki**.
- **Dobre prakse:** "tenant-aware" avtentikacija/avtorizacija, vsak zahtevek mora imeti kontekst tenanta, logična/fizična ločitev po varnosti, logi/šifriranje/nadzor dostopa.

**Izolacija podatkov:** skupna baza skupne tabele (`tenant_id`) → skupna baza ločene sheme → ločena baza za tenanta → hibridno.
**Izolacija konfiguracije:** config po tenantu v bazi, feature flags po tenantu, ločeni profili, politike dostopa po tenantu.

### 📋 12-Factor App (metodologija za SaaS/cloud-native)
Standardizira pot od kode do produkcije; loči kodo od konfiguracije; eksplicitne odvisnosti; zamenljive podporne storitve; **stateless procesi**; hiter zagon; minimalne razlike dev/prod.

| # | Faktor | Pomen |
|---|---|---|
| 1 | **Enotna koda (Codebase)** | en repozitorij, več namestitev |
| 2 | **Odvisnosti** | eksplicitno deklarirane in izolirane |
| 3 | **Konfiguracija** | v **okoljskih spremenljivkah**, ne v kodi |
| 4 | **Podporne storitve** | baza/cache/queue = priključni viri |
| 5 | **Build / release / run** | ločimo gradnjo, izdajo, zagon |
| 6 | **Procesi** | **stateless**, share-nothing |
| 7 | **Izpostavljanje portov** | aplikacija sama posluša na portu |
| 8 | **Sočasnost** | skaliranje z dodajanjem procesov |
| 9 | **Disposability** | hiter zagon, predvidljiva ustavitev |
| 10 | **Dev/prod parity** | okolja čim bolj podobna |
| 11 | **Dnevniki (Logs)** | tok dogodkov (stdout/stderr), zbira platforma |
| 12 | **Admin procesi** | enkratne naloge kot ločeni procesi |

### 🚀 Cloud Native 2.0
Ne le zabojniki, ampak tudi: platforme, avtomatizacija, opazljivost, varnost, **poslovni izidi**, organizacija/ekipe. CNCF poudarja **ljudi, procese, politike in tehnologijo** (Cloud Native Maturity Model). 
Izzivi CN 1.0 → rešitve CN 2.0: centralizirani viri → distribuirani oblak; infra-agnostic → application-driven infra; ekskluzivni clustri → hibridno nameščanje; kompleksen O&M → **serverless**; podatki → storage-compute decoupling; ročno upravljanje → avtomatizacija; varnost → comprehensive cloud security; AI integracija.

### 📌 Za zapomniti (Serverless)
- **Serverless ≠ funkcije**; lastnosti: ni upravljanja strežnikov, samodejno skaliranje, plačilo po uporabi, implicitna razpoložljivost.
- **BaaS** = gotovo zaledje (Firebase: Auth, Firestore, Storage); osredotočiš se na frontend; slabost = vendor lock-in.
- **FaaS** = stateless, event-driven funkcije; Trigger → Controller → Executor; prožilci: HTTP, DB, Storage, Cron, Queue.
- Funkcije DA: event-driven, stateless, kratko. NE: dolgo, stateful, pogosto (drago).
- 12-factor app + multi-tenant + Cloud Native 2.0.

---
---

# 🟩 KOLOKVIJ 2 – TESTIRANJE, TDD IN ČISTA ARHITEKTURA

> Večino člankov je napisal **Robert C. Martin (Uncle Bob)**, dva **Martin Fowler** in **James O. Coplien**.

## 🔑 Tri ideje, ki povezujejo vse članke
1. **Razklapljanje (decoupling) je cilj.** Dober dizajn loči poslovna pravila od podrobnosti (baza, splet, ogrodje).
2. **Odvisnosti naj kažejo navznoter / navzgor.** Podrobnosti so odvisne od poslovne logike, ne obratno (Dependency Inversion).
3. **Testi so del sistema.** Z njimi ravnaj enako skrbno kot s produkcijsko kodo; ne sklapljaj jih z notranjostjo kode.

> 💡 **Rdeča nit:** *Več ko posplošiš produkcijsko kodo in bolj specifični ko so testi, bolj je sistem razklopljen, prožen in lahek za vzdrževanje.*

---
---

# 🧪 SKLOP A – TESTIRANJE, TDD IN »MOCKI«

---

## 01 – Test Contra-variance (Testna kontravarianca)

> Avtor: Robert C. Martin (Uncle Bob)

### 🎯 Glavna ideja v enem stavku
**Struktura testov NE sme biti zrcalna slika strukture produkcijske kode.** Če imaš za vsak razred natanko en testni razred, si si ustvaril past.

### 🧩 Problem: »krhki testi« (Fragile Test Problem)
Krhki testi = ko majhna sprememba v kodi zahteva ogromno popravkov v testih.
Tipičen vzrok je **kovariantna past**: za vsak produkcijski razred narediš en testni razred (`User`→`UserTest`…). To ustvari **strukturno sklopljenost** med testi in kodo.

**Zakaj je to slabo?** Ko refaktoriraš (razbiješ razred na manjše), se podre kup testov, čeprav se obnašanje navzven ni spremenilo. Prava refaktorizacija postane nemogoča.

### ✅ Rešitev: kontravarianca (namerno razhajanje struktur)
> *»The structure of your tests should not be a mirror of the structure of your code.«*

**Razvojni proces:** razred `X` + test `XTest` skozi **javni API** → ko se nakopičijo privatne metode, jih izločiš v ločene razrede → te se testirajo **posredno** skozi javni API `X` → API postane ožji/abstraktnejši. → Manj testov, vezanih le na **stabilen javni vmesnik**.

### 🔄 Ključni princip: testi in koda gresta v nasprotni smeri
- **Testi** → vse bolj **specifični/konkretni**.
- **Produkcijska koda** → vse bolj **generična/splošna**.
> *»We decouple by generalizing!«* (Razklapljamo s posploševanjem.)

### 📌 Za zapomniti
- ❌ NE: en testni razred za vsak produkcijski razred (kovariantna past).
- ✅ DA: testi merijo na javni API; notranje razrede testiraj posredno.
- 🔁 Testi → specifični; koda → generična. Posploševanje = razklapljanje = varno refaktoriranje.

---

## 02 – First-Class Tests (Testi kot prvorazredni državljani)

> Avtor: Robert C. Martin (Uncle Bob)

### 🎯 Glavna ideja
Programerji, ki opustijo unit-teste, jih najpogosteje niso obravnavali kot **»prvorazredne državljane«**. Težava ni v testih, ampak v tem, kako z njimi ravnamo. → Teste obravnavaj **enako kot produkcijsko kodo**.

### 📖 Kontekst
Uncle Bob odgovarja avtorju, ki je opustil unit-teste (postali krhki zaradi **prevelikega mockanja**) in prešel na počasne **sistemske teste (~15 min)**. To ni rešitev – le slabe mikro-teste je zamenjal s slabimi funkcionalnimi testi; 15-min zanka krši TDD.

### 📚 Definicije vrst testov
| Vrsta | Kdo / za koga | Kaj preverja |
|---|---|---|
| **Unit test** | programerji | obnašanje po pričakovanjih programerja |
| **Acceptance test** | poslovna stran | poslovne zahteve |
| **Integration test** | arhitekti/tehnika | pravilna spojitev podsklopov (napeljava) |
| **System test** | tehnika | integracijski test za **cel sistem** (napeljava) |
| **Micro-test** | programerji | zelo majhen, ena funkcija |
| **Functional test** | programerji | širši, s primernimi mocki za počasne komponente |

> Integracijski/sistemski testi preverjajo **napeljavo (plumbing)**, ne poslovne logike.

### 🛠️ Od kod krhki testi
Iz **slabega dizajna**: pretirano mockanje, sklopljenost na detajle implementacije, testi kot »junk code«, prevelika odvisnost od mocking ogrodij.

### ✅ Rešitev
1. Razklopi teste skozi dizajn (OO, **DIP**), 2. vzorci (**Facade, Strategy**), 3. **ročno** pisanje dvojnikov (sili k zmernemu mockanju), 4. postopno nižaj granulnost, 5. ohranjaj standarde kode.

> ⚠️ **Paradoks:** Kakovostno ≠ sklopljeno. Teste obravnavaj resno, a jih ohrani neodvisne.

### 📌 Za zapomniti
- Opustitev unit-testov = znak vzdrževalnega neuspeha, ne neuspeha metode.
- Krhkost iz slabega dizajna + pretiranega mockanja. Reši z DIP, Facade, Strategy, ročnimi dvojniki.

---

## 03 – Ali TDD škodi arhitekturi?

> Avtor: Robert C. Martin (Uncle Bob)

### 🎯 Glavna ideja
TDD sam po sebi **NE škodi** dizajnu. Kakovost je odvisna od tega, **KAKO** ga uporabljaš.
> *»It is not TDD that creates bad designs. It's you.«*

### 🧩 Problem sklopljenosti
Diagram: slab pristop (uporabniki direktno sklopljeni na storitve) vs dober (razklopljeni preko API-ja, polimorfni vmesniki).
**🔑 Trik:** zamenjaj besedo **»USER« z »TEST«** → testi potrebujejo **iste dizajnerske principe** kot produkcijska koda (test je le še en uporabnik kode).

### ⚠️ Past: korespondenca ena-na-ena
En testni razred na produkcijski razred, ena testna metoda na produkcijsko metodo → *»a one-to-one correspondence implies extremely tight coupling«*. (Primer: FitNesse 2001–2008.)

### 🌱 Emergence
**Zmota:** da bi cela arhitektura »zrasla« iz TDD (absurdno). **Resnica:** iz cikla **red–green–refactor** se postopoma pojavi **dizajn nižje ravni**.
> *»As the tests get more specific, the production code gets more generic.«* — dvosmerna napetost naravno ustvari API-je in ločitev odgovornosti.

### ⚙️ Zakaj deluje
Med refaktoriranjem zavestno uporabljaš **OCP** in **DIP** + ohranjaš teste specifične → razklopljena arhitektura.

### 📌 Za zapomniti
- TDD je nevtralno orodje; za dizajn si odgovoren ti.
- »USER« → »TEST«; izogibaj se korespondenci ena-na-ena.
- Testi specifični, koda generična; uporabljaj OCP in DIP.

---

## 04 – Zakaj je večina unit-testiranja zapravljanje

> Avtor: James O. Coplien · ⚖️ **nasproten pogled** (protiargument Uncle Bobu!)

### 🎯 Glavna ideja
Unit-testiranje (zlasti v OOP + agilno) pogosto **zapravlja vire** namesto izboljšuje kakovost.

### 🕰️ Zgodovinski kontekst
FORTRAN: funkcije = zaključene računske enote, testabilne. OOP: objekti združijo podatke+metode → obnašanje nepredvidljivo brez izvedbe → agresivno mockanje za umeten kontekst.

### 🧨 Glavni argumenti
1. **Teorija informacij:** temeljito testiranje bi zahtevalo testno kodo za rede večjo od produkcijske (Turing). Pokritost ~1:10¹².
2. **Nizka informacijska vrednost:** test, ki vedno uspe = nič informacije; **tavtološki testi** (nastaviš X=5, preveriš X=5) = zapravljanje. Teste, ki leto niso padli, zavrzi.
3. **Brez poslovne vrednosti:** »programerske fantazije«; če ne znaš reči katera poslovna zahteva bi padla → test ima morda **negativno neto vrednost**.
4. **Degradacija arhitekture:** drobljenje funkcij le za pokritost (coverage) uniči razumljivost.
5. **Breme vzdrževanja:** testi = moduli; TDD uvede sklopljenost koda↔testi.

### ✂️ Katere zavreči / ✅ obdržati
- **Zavrzi:** ki leto niso padli, brez korelacije, tavtološke, brez poslovne vrednosti, podvojitve sistemskih.
- **Obdrži:** ključne algoritme z neodvisnim »oraklom«, regresijske (sistemska raven), tiste s poslovno zahtevo.

### 🔧 Boljše prakse
Assertion-i v produkcijski kodi, težišče na **sistemsko/integracijsko** raven, **CI**, eksploratorno testiranje, analiza najslabšega primera.

### 🧠 Psihološka past
Lov na »zeleno vrstico« (green bar) → ugibanje (guess-and-check) namesto analize (pavlovski refleks).

### 📌 Za zapomniti (in za debato)
- »Testiranje ne izboljša kakovosti; **razvoj** jo izboljša.«
- Vsak test naj ima **izsledljivo poslovno vrednost**; vrednost prinese test, ki **lahko pade**.
- 🔁 **Nasprotje:** Uncle Bob bi rekel, da krhkost in nizka vrednost izhajata iz **slabega dizajna in mockanja**, ne iz unit-testov.

---

## 05 – Mocks Aren't Stubs (Mocki niso stubi)

> Avtor: Martin Fowler

### 🎯 Glavna ideja
»Mock« je le ena od **petih vrst** lažnih objektov. Članek razloži razlike + dva sloga TDD: **classical** in **mockist**.

### 🔤 Osnovni pojmi
- **SUT (System Under Test)** = objekt, ki ga testiraš.
- **Collaborators** = objekti, od katerih je SUT odvisen.
- **Test Double** = splošen izraz za lažen objekt (po »stunt double«).

### 🎭 Pet vrst testnih dvojnikov (Meszaros)
| Vrsta | Kaj počne |
|---|---|
| **Dummy** | posreduje se, a **nikoli ne uporabi** (zapolni parameter) |
| **Fake** | **delujoča** implementacija z bližnjicami (npr. in-memory baza) |
| **Stub** | vrača **vnaprej določene odgovore** |
| **Spy** | stub, ki **beleži** kako je bil klican |
| **Mock** | napolnjen s **pričakovanji**, preveri pravilne klice |

> Samo **mock** zahteva **preverjanje obnašanja**; ostali običajno preverjanje stanja.

### 🔍 Dva načina preverjanja
- **State verification:** po izvedbi pogledaš **stanje** (npr. zaloge v skladišču).
- **Behavior verification:** preveriš, da je SUT izvedel **prave klice** (npr. najprej `hasInventory()`, nato `remove()`).

### ⚔️ Classical vs Mockist TDD
| | Classical | Mockist |
|---|---|---|
| Objekti | **pravi**, dvojniki le pri »težavnih« | **mocki** za vsak sodelavec |
| Smer | **middle-out** | **outside-in** |
| Preverjanje | **stanje** | **obnašanje** |
| Povezava | – | BDD |

### ⚖️ Trade-offs
- **Izolacija:** napaka v deljenem objektu zruši veliko classical testov; mockist zruši le teste SUT-a. A classical ujamejo napake interakcij.
- **Sklopljenost:** mockist testi se **tesno sklopijo z implementacijo** → padejo ob refaktoriranju, čeprav je obnašanje enako. Classical gledajo stanje → stabilnejši.
- **Slog dizajna (mockist spodbuja):** Role Interfaces, Collecting Parameter, **Tell-Don't-Ask**, izogibanje »train wrecks« (`a.b().c().d()` – Demetrин zakon).

### ✅ Sklep
Fowler je **classical** TDD-er. Oba sloga morata biti dopolnjena z grobozrnatimi **acceptance testi**. Ni le tehnična, je **filozofska** izbira.

### 📌 Za zapomniti
- 5 dvojnikov: Dummy, Fake, Stub, Spy, Mock.
- Stanje (classical) vs obnašanje (mockist). Mocki = boljša izolacija, a tesnejša sklopljenost.

---

## 06 – When to Mock (Kdaj uporabiti mock)

> Avtor: Robert C. Martin (Uncle Bob)

### 🎯 Glavna ideja
Mocki so močni, a strateški. Ravnovesje med **nič mockov** in **vse mockano**.

### ❌ Nič mockov
1. **Počasnost** (baza/omrežje 1000x počasnejše), 2. **nizka pokritost** (težko testirati napake/izjeme), 3. **krhkost** (nepovezane komponente).

### ❌ Preveč mockov
1. **Paradoks zmogljivosti** (refleksija počasnejša od prave kode), 2. **eksplozija kompleksnosti** (mocki vračajo mocke), 3. **škoda dizajnu** (preveč vmesnikov le za mockanje → over-engineering).

### ✅ »Goldilocks« mocki (ravno prav)
> **Hevristika:** *»Mock across architecturally significant boundaries, but not within those boundaries.«* (Mockaj čez arhitekturno pomembne meje, ne znotraj njih.)

Mockanje na robovih (baze, strežniki, zunanje storitve) → hitrejši testi, izolacija od napak, lahko testiranje error scenarijev, polna pokritost poti FSM, čistejša koda, **arhitekturna disciplina**.

### ✍️ Piši mocke ročno
Enostavnost (brez DSL), ponovna uporaba, razmišljanje o dizajnu, zmogljivost, IDE generira. Ogrodja le »z zelo rahlim dotikom«.

### 📌 Za zapomniti
- Iščeš ravnovesje. 🔑 **Mockaj čez arhitekturne meje, ne znotraj njih.** Piši ročno. Testabilna koda = dobra arhitektura.

---

## 07 – The Little Mocker (Mali mocker)

> Avtor: Robert C. Martin (Uncle Bob) · 📝 sokratski dialog

### 🎯 Glavna ideja
»Mock« neformalno = cela družina. Formalno **hierarhija petih vrst**.

### 🪜 Hierarhija
```
Dummy  ──►  Stub  ──►  Spy  ──►  Mock        (Fake je popolnoma ločen!)
```
> *»A Mock is a kind of spy, a spy is a kind of stub, and a stub is a kind of dummy. But a fake isn't a kind of any of them.«*

| Vrsta | Bistvo | Primer |
|---|---|---|
| 🟦 **Dummy** | neuporabljen (vrača null) | `return null;` |
| 🟩 **Stub** | vrača vrednosti | `return true;` |
| 🟨 **Spy** | beleži klice ⚠️ tesna sklopljenost | `authorizeWasCalled = true;` |
| 🟥 **Mock** | preverja pričakovanja (`verify()`); »Mocks know what they are testing« | jMock, EasyMock, Mockito; **mock je vedno tudi spy** |
| 🟪 **Fake** | prava (poenostavljena) **logika** | `return user.equals("Bob");` |

### 🧰 Praktičen nasvet
Stube/spye piše ročno (IDE pomaga); izogiba se mocking ogrodjem (čudna sintaksa); **fakes** piše redko (sam jih ni že 30 let).

### 📌 Za zapomniti
Dummy=neuporabljen, Stub=vrača, Spy=beleži, Mock=preverja (`verify`), Fake=prava logika. Hierarhija: Dummy→Stub→Spy→Mock; **Fake ločen**.

---
---

# 🏛️ SKLOP B – ARHITEKTURA

---

## 08 – A Little Architecture (Malo o arhitekturi)

> Avtor: Robert C. Martin (Uncle Bob) · 📝 sokratski dialog

### 🎯 Glavna ideja
Pravi arhitekt **NE** odloča prvenstveno o bazi/ogrodju/strežniku — to so **detajli**. Arhitektura = kako **odložiti** te odločitve in ohraniti poslovna pravila neodvisna.

### ❓ O čem arhitekti zares odločajo?
> *»You didn't list the important decisions. You listed the irrelevant ones.«* — baza je le **»IO naprava«**.

### 🔄 Dependency Inversion Principle
| | Smer |
|---|---|
| Klici ob izvajanju (runtime) | **navzdol**: poslovna pravila → baza |
| Odvisnosti v izvorni kodi | **navzgor**: baza → poslovna pravila |
➡️ Implementacija baze je odvisna od poslovnih pravil (OO-vmesniki, ki jih baza implementira).

### 🧩 Interface Segregation
❌ en velik »gateway« vmesnik → ✅ vsako poslovno pravilo svoj **ozek vmesnik**.

### 🏆 Pravi dosežek = ODLOG (deferral)
Dobra arhitektura dopušča odlog izbire baze/strežnika/ogrodja → loose coupling, hitrejši testi, prilagodljivost.

### 📌 Za zapomniti
- Baza/splet/ogrodje = **detajli**. 🔑 Odvisnosti v izvorni kodi kažejo navznoter/navzgor (DIP); klici navzdol. Vsako pravilo svoj ozek vmesnik (ISP). Arhitekt **odloži** nepomembne odločitve.

---

## 09 – The Clean Architecture (Čista arhitektura)

> Avtor: Robert C. Martin (Uncle Bob)

### 🎯 Glavna ideja
Združuje vzorce (Hexagonal, Onion, DCI, BCE). Isti cilj: **ločitev odgovornosti** s plastenjem → neodvisno od ogrodja, testabilno, prožno glede UI/baze.

### ⭕ Koncentrični krogi (od zunaj navznoter)
```
Frameworks & Drivers (baza, splet, orodja) ← detajli
  Interface Adapters (MVC, presenters, controllers, SQL)
    Use Cases (aplikacijska poslovna pravila)
      Entities (poslovna pravila podjetja)
         odvisnosti kažejo ──► NAVZNOTER
```
1. **Frameworks & Drivers** – detajli, »lepilo«. »The Web is a detail. The database is a detail.«
2. **Interface Adapters** – pretvorba podatkov med formati; MVC, SQL.
3. **Use Cases** – aplikacijsko-specifična pravila; izolirani od baze/UI/ogrodja.
4. **Entities** – pravila celotnega podjetja; najmanj verjetno se spremenijo.

### 📏 Pravilo odvisnosti (The Dependency Rule)
> *»Source code dependencies can only point inwards.«* Notranji krog **ne sme** poznati ničesar iz zunanjega → jedro ostane stabilno.

### ✨ Lastnosti
Neodvisnost od ogrodij, visoka testabilnost (brez UI/baze), zamenljiv UI, zamenljiva baza (Oracle→MongoDB), izolacija poslovnih pravil.

### 🚪 Prečkanje meja
**DIP:** notranja plast kliče **vmesnik (output port)**, zunanja ga implementira → odvisnosti še vedno navznoter (control flow teče navzven). Čez meje potujejo **preproste podatkovne strukture / DTO**, nikoli entitete/vrstice baze.

### 📌 Za zapomniti
- 4 krogi: Entities → Use Cases → Interface Adapters → Frameworks & Drivers.
- 🔑 Pravilo odvisnosti: izvorne odvisnosti kažejo **samo navznoter**. Čez meje: DIP (output port) + DTO. Baza/splet = detajla.

---

## 10 – Clean Microservice Architecture (Čista mikrostoritvena arhitektura)

> Avtor: Robert C. Martin (Uncle Bob)

### 🎯 Glavna ideja (provokacija)
> **Mikrostoritve so možnost POSTAVITVE (deployment), NE arhitektura.**

Sistem po čisti arhitekturi se postavi na različnih merilih (od enega procesa do mnogo strežnikov), ne da bi koda vedela kako.

### 📊 Spekter postavitev (od najbolj do najmanj skalabilnega)
1. Mikrostoritve na več strežnikih → 2. več MS na en strežnik → 3. več MS kot en izvršljivec → 4. niti v enem VM (čakalne vrste) → 5. dinamično povezane komponente (navadni klici funkcij).
➡️ Čista arhitektura deluje **identično** na vseh nivojih.

### 💡 Osrednji argument
Če koda **ne ve** za mehanizem postavitve, je ta **arhitekturni detajl** → odloži ga do zadnjega odgovornega trenutka. (»forced ignorance«)

### 🚫 Kritika BDUF + »monolit«
Ni treba sistema vnaprej zasnovati kot mikrostoritvenega (»BDUF Baloney«). Dobro modularen sistem (JAR/DLL) **ni monolit**.

### ⚖️ Kompromisi
- **Proti MS – prednosti:** svoboda jezikov/ogrodij/baz, ekstremno razklapljanje.
- **Proti MS – cena:** startup/shutdown vrstni red, konfiguracija, podvajanje kode, **verzioniranje sporočil**, operativna kompleksnost.

### ✅ Priporočila
Ne predpiši in ne prepovej MS; oblikuj **neodvisno od postavitve**; **začni preprosto**, skaliraj po potrebi.

### 📌 Za zapomniti
- Mikrostoritve = **način postavitve**, ne arhitektura. Čista arhitektura določa **KAJ**, ne **KAKO**. Postavitev = detajl. Začni preprosto (ne BDUF).

---

## 11 – Screaming Architecture (Kričeča arhitektura)

> Avtor: Robert C. Martin (Uncle Bob)

### 🎯 Glavna ideja
Arhitektura naj **»kriči« NAMEN sistema** (kaj počne), ne ogrodja.
> *»What does the architecture of your application scream?«*

### 🏠 Metafora gradbenih načrtov
Ob načrtih hiše vidiš »hiša«; ob načrtih knjižnice vidiš »knjižnica«. Enako naj koda razkrije: **zdravstveni sistem? računovodski?** … ali pa vidiš le Rails/Spring/Hibernate?

### 🧱 Poudari uporabniške primere (Jacobson)
> *»Architectures are not (or should not be) about frameworks.«* Najprej strukturiraj okoli **poslovnih funkcij**, izbiro tehnologije **odloži**.

### 🌐 Splet je detajl
> *»The Web is a delivery mechanism.«* Sistem se da postaviti kot konzolno/spletno/thick-client aplikacijo brez preurejanja. Poslovni objekti = »plain old objects« → testabilni brez infrastrukture.

### ✅ Praktičen zaključek
Nov član ekipe ob pogledu v repozitorij naj **takoj razume domeno**. »Kje so pogledi/kontrolerji?« → »To so detajli, ki te zaenkrat ne bi smeli skrbeti.«

### 📌 Za zapomniti
- Arhitektura naj **kriči namen** (domeno), ne ogrodja. Splet = detajl/mehanizem dostave. Poslovni objekti = navadni objekti → testabilni.

---
---

# 🎓 SKUPNI POVZETEK ZA HITRO PONAVLJANJE PRED USTNIM

### 🟦 Kolokvij 1 — bistvo
- **Arhitektura** = najzgodnejše, najtežje spremenljive odločitve; KAJ vs KAKO; NFZ so arhitekturno pomembne (kompromisi).
- **SOLID:** S=en razlog za spremembo, O=odprto/zaprto, L=zamenljivi podtipi, I=majhni vmesniki, D=obrni odvisnosti.
- **Stili:** layered (privzeto), SOA (ESB), EDA (dogodki), MSA (neodvisne MS), serverless.
- **Komunikacija:** zmote distribuiranih sistemov; sinhrono vs asinhrono; broker/MOM/pub-sub; concurrency (race → synchronized, deadlock); **stateless** za skaliranje.
- **ADR:** dokumentiraj odločitve (Context/Decision/Consequences) v Git; ASR→AD→ADR→ADL.
- **SPL:** družina izdelkov, feature model (mandatory/optional/or/alternative), variabilnost.
- **Oblak:** 5 lastnosti, IaaS/PaaS/SaaS/FaaS, VM vs zabojnik, Docker (slika→zabojnik, Dockerfile, Compose, Volume), **Kubernetes** (Pod/Node/Cluster/Service/Deployment), sidecar/ambassador/adapter.
- **Serverless:** ≠funkcije; BaaS (gotovo zaledje) + FaaS (stateless, event-driven, Trigger→Controller→Executor); 12-factor; multi-tenant.

### 🟩 Kolokvij 2 — bistvo
- **Testni dvojniki:** Dummy → Stub → Spy → Mock; **Fake** = prava poenostavljena logika (ločen).
- **State vs behavior verification** = **Classical vs Mockist** TDD.
- **Mockaj čez arhitekturne meje, ne znotraj njih** (When to Mock).
- Struktura testov ≠ struktura kode (Contra-variance); testi specifični, koda generična.
- Teste obravnavaj kot prvorazredno kodo. TDD je nevtralen — za dizajn si odgovoren ti.
- ⚖️ Coplien (nasproten pogled): vsak test naj ima izsledljivo poslovno vrednost.
- **Arhitektura:** baza/splet/ogrodje = detajli → odloži (A Little Architecture); **Pravilo odvisnosti: navznoter** (Clean Architecture); mikrostoritve = način postavitve (Clean Microservice); arhitektura naj **kriči namen** (Screaming Architecture).

> 🧲 **Skupna nit obeh kolokvijev:** *Loči poslovno logiko od podrobnosti, obrni odvisnosti (DIP), in tako dobiš sistem, ki je testabilen, prožen in lahek za vzdrževanje.*

---

> 💪 **Srečno na ustnem izpitu!** Najprej preglej "Za zapomniti" razdelke in "Skupni povzetek" — to so najverjetnejša izpitna vprašanja. Pri zahtevnih pojmih si zapomni en preprost primer (Lufthansa za "World & Machine", plačilo z vmesnikom za OCP, stunt double za test doubles).
