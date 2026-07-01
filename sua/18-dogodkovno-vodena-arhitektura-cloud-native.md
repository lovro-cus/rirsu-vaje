# Predavanje 18 — Dogodkovno vodena arhitektura (EDA) in Cloud-native storitvena arhitektura

> **O čem je predavanje:** dva zadnja sklopa — **EDA (Event-Driven Architecture)**: kako sistemi komunicirajo prek dogodkov (komponente, življenjski cikel, vrste, povezava s SOA); ter **Cloud-native**: računalništvo v oblaku (NIST karakteristike, storitveni/uvajalni modeli) in **načela arhitekture za oblak**.

---

# DEL 1: Dogodkovno vodena arhitektura (EDA)

## 1. Kaj je EDA
- **Event-Driven Architecture** = pristop, kjer sistemi "slišijo" dogodke in se nanje **inteligentno odzovejo**.
- Aplikacije komunicirajo prek **dogodkov** (event messages).
- **Producer** objavi dogodek (npr. `OrderCreated`), **consumerji** ga **asinhrono** obdelajo.
- Dogodki potujejo prek **event bus / message broker** (Kafka, RabbitMQ, NATS).
- **Prednosti:** ohlapna sklopljenost, skalabilnost, odzivnost, boljša integracija mikrostoritev.

## 2. Dogodek — temeljni gradnik
- **Dogodek** = "relevantna sprememba stanja v sistemu ali njegovem okolju." Opisuje, da se je **nekaj zgodilo** (pretekli čas), in lahko sproži obdelavo pri **več porabnikih**.
- Sestavljen iz:
  - **Glava (metadata):** ID dogodka, tip/ime, časovni žig, zaporedna številka/retry, izvor/iniciator.
  - **Telo (payload):** dejanska vsebina, ki jo porabniki obdelajo.

## 3. Ključne ideje EDA
- Sistemi se **ne kličejo neposredno**, ampak reagirajo na objavljene dogodke.
- Osnovni vzorec: **producer → broker/event bus → consumer(ji)** (asinhrono).
- Ključni odločitvi: **kateri dogodki obstajajo** in **kako jih poimenujemo/strukturiramo** (event schema, verzioniranje).
- Tipični izzivi: **eventual consistency, podvajanje dogodkov (idempotentnost), urejanje zaporedja (ordering)**.

## 4. EDA vs EDP (Event-Driven Programming)
- **EDP** = koncept, kjer izvajanje sprožijo dogodki in obravnavalniki. Vključuje:
  - **event dispatcher** (vzdržuje seznam registriranih poslušalcev za tipe dogodkov),
  - **event listener/handler** (koda, ki se sproži ob dogodku; se registrira pri dispatcherju).
- Razlika od tradicionalnega (zaporednega) programiranja: potek **ni vnaprej določen**, sprožajo ga dogodki; ni osrednjega dela, ki vodi potek.

| | EDP | EDA |
|---|---|---|
| Nivo dogodkov | **nizkonivojski** (klik miške, tipka) | **visokonivojski** (oddano naročilo, potrjeno plačilo) |
| Skupno | dinamično povezovanje, sporočila, šibka sklopljenost, asinhronost, prijava na vrste dogodkov | |

## 5. Osnovne komponente EDA
1. **Generatorji dogodkov** — avtonomne komponente (senzorji, bralniki, algoritmi), ki ob spremembi ustvarijo dogodek. Nahajajo se kjerkoli (znotraj/zunaj organizacije); v podatke dogodka običajno vključijo vse potrebno za obdelavo.
2. **Poslušalci (odjemalci) dogodkov** — povezani na skupno vodilo, čakajo na dogodek določene vrste; ko ga prejmejo, sprožijo izvajanje (lahko nastanejo novi dogodki). Morajo **prepoznati dogodke** in vedeti, na katere so **prijavljeni**.
3. **Procesne enote dogodkov** — obdelajo dogodke (preverijo, dopolnijo, preoblikujejo, združijo, posredujejo); na podlagi pravil določijo pomen in naslednja dejanja.

**Vrste obdelave dogodkov:**
- **Preprosta** — vsak dogodek posamično.
- **Tokovna** — dogodki kot tok (zaporedje + časovna bližina).
- **Kompleksna (CEP)** — daljše serije dogodkov; prepoznavanje **vzorcev** po pravilih.

## 6. Odziv na dogodke + življenjski cikel
**Oblike odziva:** samodejni odziv, samodejno obveščanje sistemov/ljudi, odziv s posredovanjem človeka.

**Življenjski cikel dogodka:**
1. **Generiranje** (iniciator/generator),
2. **Prenos** (prek kanala do procesne enote),
3. **Procesiranje** (ovrednotenje telesa, združevanje/filtriranje po pravilih, neodvisno od generatorja),
4. **Odziv** (ko je dogodek zanimiv za odjemalca).

## 7. Vrste EDA (Manas Deb, Oracle)
- **Eksplicitna EDA** — generatorji **vedo, kdo so poslušalci** in komu pošiljajo → **tesna sklopljenost**.
- **Implicitna EDA** — ni definiranih povezav; **poslušalci sami določijo**, kateri dogodki jih zanimajo → **šibka sklopljenost**, bolj dinamične/agilne rešitve.

## 8. SOA + EDA
- Povezavo najlažje razumemo prek **upravljanja poslovnih procesov**.
- **BPEL** je bližje **SOA** (postopkovno vodenje storitev v zaporedje korakov), a podpira tudi sodelovanje več udeležencev (bližje EDA). BPEL je večinoma **postopkoven**, ne opisen; razvoj gre v smer **deklarativnega** pristopa.
- Jack van Hoof: *"Če želiš podpreti neodvisnost med koraki poslovnega procesa, je EDA prava pot — primerna za federirana in avtonomna okolja."*

## 9. Povzetek EDA
- Osnovna enota = **dogodek**; vsebuje **generatorje** in **odjemalce** dogodkov.
- **Šibko sklopljena**, uporablja **asinhrono komunikacijo** (vzorec **Objavi/Naroči — Publish/Subscribe**).
- Uporablja splošne komunikacijske sisteme (**ESB**, adapterji, mediatorji).
- **Ne temelji na centralnem kontrolerju!**
- Prednosti za posel: agilnost pri spremembah stanj, napredno povezovanje podatkov (analitika), dinamična poslovna pravila, inteligentne rešitve.

---

# DEL 2: Cloud-native arhitektura

## 1. Kontekst
- **Gartner:** do 2025 >85 % podjetij razvija po **cloud-first** principu; >95 % digitalnih rešitev na cloud-native platformah (skok s 30 % v 2021). "Vse necloud bo veljalo za legacy."

## 2. Računalništvo v oblaku (NIST 2011)
Model za **vseprisoten, priročen omrežni dostop na zahtevo** do skupnega nabora nastavljivih virov (omrežja, strežniki, pomnilnik, aplikacije, storitve), ki jih je mogoče **hitro zagotoviti in sprostiti** z minimalnim naporom.

**5 bistvenih karakteristik:**
1. **Samopostrežba na zahtevo** (on-demand self-service) — potrošnik si sam avtomatsko zagotovi vire, brez človeka na strani ponudnika.
2. **Širokopasovni omrežni dostop** — prek standardnih mehanizmov, tanki in debeli odjemalci (mobilne, tablice, računalniki).
3. **Združevanje virov** (resource pooling) — dinamično dodeljevanje fizičnih/virtualnih virov; potrošnik ne pozna točne lokacije (le abstraktno: kontinent/država/DC).
4. **Hitra prožnost** (rapid elasticity) — vire prožno zagotovimo/sprostimo (avtomatsko skaliranje); občutek "neomejenih" zmogljivosti.
5. **Merjena storitev** (measured service) — samodejno merjenje, nadzor, optimizacija, poročanje uporabe (plačilo po uporabi).

**3 osnovni storitveni modeli:**
| Model | Kaj dobiš | Kaj nadzoruješ | Kaj NE |
|---|---|---|---|
| **SaaS** (Software) | ponudnikove **aplikacije** (npr. spletni odjemalec) | le nastavitve aplikacije | infrastrukturo, OS, aplikacijo |
| **PaaS** (Platform) | okolje za **lastne aplikacije** (podprti jeziki/orodja) | svoje aplikacije + konfiguracijo izvajalnega okolja | osnovno infrastrukturo |
| **IaaS** (Infrastructure) | **računski/shranjevalni/omrežni viri** (namestiš OS+apl.) | OS, shrambo, aplikacije, (omejeno) omrežje | podporno infrastrukturo |

**Drugi modeli (\*aaS):** BaaS (Backend), **FaaS** (Function), AaaS (Application), CaaS (Computing), STaaS (Storage), BPaaS (Business Process).

**Vrste oblakov (uvajalni modeli):** **zasebni** (private), **skupnostni** (community), **javni** (public), **hibridni** (hybrid). Novejši: **multi-cloud**, HPC cloud, region cloud.

## 3. Cloud-native arhitektura
- Nastala zaradi izzivov sodobnega razvoja: **hitrejši razvoj/dostava, tehnološke novosti, stalne spremembe** v organizacijah.
- **Celovita arhitektura/filozofija**, ki v polni meri izkorišča oblak. **Poudarek ni na strežnikih, ampak na storitvah!**
- Cilj večine organizacij v digitalni transformaciji.

**Načela arhitekture za oblak (Reznik et al.):**
- **Kontejnerizacija** — aplikacija + odvisnosti v paketu (namesti/poženi/testiraj kjerkoli).
- **Dinamično upravljanje** — javne oblačne storitve, plačilo po porabi.
- **Mikrostoritve** — manjše, šibko sklopljene, zamenljive storitve.
- **Avtomatizacija** — ročna opravila zamenjamo z avtomatiziranimi.
- **Orkestracija** — celovito upravljanje zabojnikov (**Kubernetes**).

**5 načel (Google):** načrtuj za **avtomatizacijo**; premišljeno ravnaj s **stanjem** (komponente brez stanja, stanje v namenskih storitvah); prednost **upravljanim storitvam**; **večplastna zaščita**; **arhitekturo nenehno izpopolnjuj**.

**7 načel (Alibaba):**
1. **Storitveno usmerjeno načrtovanje** (jasne meje, dogovorjeni vmesniki),
2. **Prožnost** (samodejno prilagajanje obremenitvi),
3. **Zmožnost opazovanja** (logi, meritve, sledenje),
4. **Odpornost na napake** (napake pričakovane, sistem se omeji/popravi),
5. **Avtomatizacija vseh postopkov**,
6. **Ničelno zaupanje** (zero trust — vsak dostop se preveri, minimalne pravice),
7. **Nenehni razvoj arhitekture**.

> 💡 **Povezava celotnega predmeta:** cloud-native združi vse obravnavano — **mikrostoritve** (pred. 12–14), **komunikacijo** (REST/gRPC/GraphQL, pred. 11/16/17), **EDA** (ta pred.), **kontejnerje/orkestracijo** (pred. 13) in **odpornost na napake** (pred. 13) v celovito filozofijo gradnje sodobnih storitvenih rešitev.

---

## Ključni povzetek predavanja 18
- **EDA:** komunikacija prek **dogodkov** (producer → broker → consumer, asinhrono, **Pub/Sub**); dogodek = glava + telo; komponente = generatorji/poslušalci/procesne enote; vrste **eksplicitna** (tesno) vs **implicitna** (šibko); **brez centralnega kontrolerja**; izzivi eventual consistency/idempotentnost/ordering.
- **EDA vs EDP:** EDP = nizkonivojski dogodki (GUI), EDA = visokonivojski poslovni dogodki.
- **Oblak (NIST):** 5 karakteristik (samopostrežba, omrežni dostop, združevanje virov, prožnost, merjenje); modeli **SaaS/PaaS/IaaS**; vrste zasebni/javni/hibridni.
- **Cloud-native:** poudarek na **storitvah, ne strežnikih**; načela = kontejnerizacija, mikrostoritve, avtomatizacija, orkestracija (Kubernetes), dinamično upravljanje, brez stanja, opazljivost, odpornost, zero trust, nenehni razvoj.
