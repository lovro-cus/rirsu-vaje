# Predavanje 10 — Strateški cilji SOA, SOA Manifesto, vzorci SOA, arhitekturni stil REST, vzorci/antivzorci REST, SOA vs REST

> **O čem je predavanje:** zakaj sploh gradimo SOA (7 strateških ciljev), kaj pravi **SOA Manifesto** (vrednote+načela), pregled **nabora načrtovalskih vzorcev SOA**, nato pa velik del o **REST** — kaj je, 5 arhitekturnih principov, RESTful storitve, vzorci in **antivzorci**, ter primerjava **SOAP/WS-\* vs REST** in vprašanje "ali lahko gradimo SOA z REST?".

---

## 1. Strateški cilji SOA

**7 strateških ciljev** (prvi 4 omogočajo zadnje 3):

**Prvi 4 (sredstva):**
1. **Prava/naravna interoperabilnost** — storitve so *vgrajeno* interoperabilne (ne glede na platformo/tehnologijo), zato **integracija postane odveč**. Ekipe A in B naredijo storitve, ekipa C jih le konfigurira in sestavi (brez integracijskih projektov).
   - *Interoperabilnost* = sposobnost izmenjave podatkov; *Integracija* = trud, potreben da to dosežemo (potrebna, ko sistemi niso kompatibilni).
2. **Poenotenje različnih okolij** — federirano ("zvezno") okolje prek standardiziranih storitev in enotnih pogodb.
3. **Več možnosti za raznolikost ponudnikov** — zmanjšamo **vendor lock-in**; arhitektura neodvisna od produktov.
4. **Večja usklajenost poslovanja in tehnologij** (business-IT alignment) — poslovne zmožnosti prevedemo v storitve; v SOA projektih poslovni analitik in arhitekt **skupaj** izdelata zasnovo (v klasičnih projektih analitik le preda dokumentacijo).

**Zadnje 3 (koristi/prednosti):**
5. **Večji ROI** (return on investment) — agnostične in ponovno uporabne storitve zmanjšajo integracijske projekte.
6. **Večja agilnost podjetja** — nove zahteve rešimo s **kompozicijo obstoječih storitev**. Primer: klasičen pristop = 100 % nove logike; SOA = 35 % nova + 65 % ponovna uporaba → strošek/3, čas/3.
7. **Manjše breme za IT** — manj "odpada" in podvajanja; IT preide iz "gasilske službe" v načrtnega skrbnika storitvene krajine.

> 💡 **Bistvo:** prve 4 (interoperabilnost, poenotenje, raznolikost, usklajenost) so **kako gradimo**; zadnje 3 (ROI, agilnost, manjše breme) so **kaj s tem pridobimo**.

---

## 2. SOA Manifesto

**SOA Manifesto** (2009, avtorji kot Thomas Erl, Grady Booch ...) = dokument s temeljnimi načeli, vrednotami in cilji SOA. Poudarja **organizacijske in poslovne koristi**, ne le tehnike.

### 6 vrednot (levo cenimo bolj od desnega)
1. **Poslovna vrednost** pred tehnološkimi strategijami.
2. **Strateški cilji** pred koristmi posameznega projekta.
3. **Notranja interoperabilnost** pred integracijami po meri.
4. **Storitve v skupni rabi** pred storitvami za posebne namene.
5. **Prilagodljivost** pred lokalno optimizacijo.
6. **Evolucijsko izpopolnjevanje** pred popolno začetno rešitvijo.

### Ključna načela (izbor)
- Spoštuj družbeno strukturo in strukturo moči organizacije (ne ruši, postopno prilagajaj).
- Sprejetje SOA naj bo **usmerjeno v poslovanje, ne v tehnologijo**.
- SOA zahteva spremembe na **mnogih ravneh** (vodenje projektov, življenjski cikel, ekipe).
- **Začni z majhnimi, izvedljivimi koraki** (pilotne rešitve gradijo zaupanje).
- **SOA ni produkt — ne moremo je kupiti**.
- Storitvena usmerjenost je **neodvisna od tehnologije in ponudnika**.
- "Prizadevaj si za **enotnost navzven, dopuščaj raznolikost navznoter**."
- Storitve identificiraj v sodelovanju z deležniki; razvijaj na podlagi dejanske uporabe (iterativno).

---

## 3. Načrtovalski vzorci SOA (pregled)

Vzorci so razvrščeni v skupine (Thomas Erl). Vsak vzorec opisujemo z: zahteva/izhodišče → problem → rešitev → aplikacija → vplivi → povezava s principi/cilji.

**5 glavnih kategorij:**
1. **Vzorci storitvenega inventarja** — temeljni (Canonical Protocol/Schema, Domain/Enterprise Inventory, Logic Centralization, Service Layers, Service Normalization), logičnih nivojev (abstrakcija entitete/procesa/podpornih/mikro-opravil), centralizacije, implementacije (State Repository, Stateful Services, Service Grid, Dual Protocols ...), upravljanja (Canonical Versioning, Metadata Centralization ...).
2. **Vzorci storitev** — temeljni (Agnostic/Non-agnostic Context, Service Encapsulation), implementacije (Service Facade, Redundant Implementation, **Microservice Deployment**, **Containerization** ...), varnosti (Exception Shielding, Message Screening ...), pogodb (Concurrent Contracts, Decoupled Contract ...), enkapsulacije legacy (Legacy Wrapper, File Gateway ...), upravljanja (Compatible Change, Service Decomposition/Refactoring, Version Identification ...).
3. **Vzorci kompozicij storitev** — kompozicija zmožnosti (Capability Composition/Recomposition), sporočanja (Asynchronous Queuing, **Event-Driven Messaging**, Reliable Messaging, Service Callback ...), implementacije (**Atomic Service Transaction**, **Compensating Service Transaction**, Composition Autonomy), varovanja komunikacije, transformacij (Data Format/Model Transformation, Protocol Bridging).
4. **Vzorci na osnovi REST** — Entity Linking, Lightweight Endpoint, Reusable Contract, Content Negotiation, Endpoint Redirection, Idempotent Capability.
5. **Sestavljeni vzorci** (grobozrnati, iz več drobnozrnatih) — Canonical Schema Bus, **Enterprise Service Bus**, Federated Endpoint Layer, Official Endpoint, **Orchestration**, Service Broker, Three-layer Inventory, Uniform Contract.

> 🔑 Ni treba znati vseh; pomembno je razumeti, da so vzorci **katalog preverjenih rešitev za ponavljajoče probleme** (kot recepti). Ključni pojmi zgoraj (poudarjeni) se pojavljajo tudi kasneje.

---

## 4. Arhitekturni stil REST

### Kaj je REST
- **REST = Representational State Transfer** ("prenos stanj kot predstavitev").
- Definiral **Roy Fielding, 2000** (doktorska disertacija; soavtor HTTP).
- **REST je arhitekturni STIL, ne standard!** Neodvisen od protokola (a najpogosteje HTTP).
- Ideja: kako izkoristiti HTTP in spletne standarde za enostavne, razširljive, **šibko sklopljene** porazdeljene sisteme (poudarek na **virih, reprezentacijah, standardnih HTTP metodah**).
- SOAP/WS-\* tudi uporabljajo HTTP, a **le kot prenos** — ne izkoristijo zmožnosti HTTP. REST je "ponovno rojstvo HTTP".

### 5 arhitekturnih principov REST
1. **Naslovljivi viri** (addressable resources)
2. **Enoten vmesnik za vire** (uniform interface)
3. **Predstavitvena usmerjenost** (representation-oriented)
4. **Komunikacija brez stanja** (stateless)
5. **HATEOAS** (Hypermedia As The Engine Of Application State)

---

### Princip 1: Naslovljivi viri
- **Vir (resource)** = ključna abstrakcija informacij (npr. knjiga, uporabnik, naročilo).
- Vsak vir ima **URI** (enolični identifikator).
- **Sintaksa URI:** `scheme://host:port/path?queryString#fragment`
  - primer: `http://epodjetje.com/kupci?priimek=Novak&postnastevilka=2000`
- **Zakaj URI pomemben:** enolična identifikacija, domačnost (uporabniki poznajo URL), interoperabilnost (na odjemalcu **le HTTP knjižnica**, brez stub/WSDL objektov).

**Smernice za URI:**
- Kratki; **samostalniki** (viri), ne glagoli; akcije v **HTTP metodah**, ne v URI.
- Hierarhijo izražamo s potjo: `knjiga/24/1998` namesto `?isbn=24&year=1998`.
- **Zbirke z množino:** `GET /knjige` (seznam), `POST /knjige` (nova); posamezni: `GET /knjige/123`.
- **NE** `GET /book?isbn=24&action=delete` (akcija v URI = napačno).
- **Verzioniranje:** v poti `/api/v1/books` (najpogosteje) ali v zaglavju `Accept: application/vnd.myapi.v1+json`.

---

### Princip 2: Enoten vmesnik (Uniform Interface)
- Za vse interakcije zadošča **končen, standardiziran nabor operacij** (HTTP metode).
- Odjemalec vedno uporablja iste operacije nad različnimi viri.

**HTTP metode:**
| Metoda | Varna | Idempotentna | Raba |
|---|---|---|---|
| GET | ✅ | ✅ | branje vira |
| HEAD | ✅ | ✅ | metapodatki brez vsebine |
| OPTIONS | ✅ | običajno ✅ | zmožnosti strežnika/vira |
| PUT | ❌ | ✅ | ustvarjanje / **polna** posodobitev |
| DELETE | ❌ | ✅ | brisanje |
| POST | ❌ | ❌ | kreiranje, akcije, podviri |
| PATCH | ❌ | ni nujno | **delna** posodobitev |

**Definiciji:**
- **Idempotentna** = poljubno klicev pusti sistem v enakem stanju kot en klic (GET, HEAD, PUT, DELETE, OPTIONS).
- **Varna** = ne spremeni stanja na strežniku (GET, HEAD, OPTIONS).

> 💡 **Idempotentnost je pomembna za robustnost:** če storitev vmes izpade, lahko odjemalec **varno večkrat pokliče** isto metodo (npr. DELETE) brez škode.

**CRUD ↔ HTTP:** CREATE=POST, READ=GET, UPDATE=PUT (cel vir!), DELETE=DELETE, PARTIAL UPDATE=PATCH.

---

### Princip 3: Predstavitvena usmerjenost
- Vir = abstrakten koncept; na zahtevo se pretvori v **predstavitev (representation)** — obliko, ki jo odjemalec razume.
- **En vir → več predstavitev:** brskalnik želi HTML, aplikacija JSON, drugi CSV/XML/binarno.
- Ločitev vira od predstavitve = šibka sklopljenost.

**Dva načina izbire formata:**
1. **"Vsiljen" format** (URI postfix): `GET /vir.json`, `GET /vir.xml` — **pogosta praksa, NE standard**.
2. **Pogajanje o vsebini** (content negotiation, priporočeno): odjemalec pošlje `Accept: application/json, application/xml`, strežnik izbere in vrne `Content-Type: application/json` (ali `406 Not Acceptable`).

**MIME tip** (`type/subtype`): `text/html`, `application/json`, `application/xml`, `image/jpeg`, `application/octet-stream` ... — pove, kaj je v vsebini sporočila.

---

### Princip 4: Komunikacija brez stanja (stateless)
- **Vsaka zahteva je samozadostna** — vsebuje vse potrebno; strežnik **ne hrani sej** in ne upošteva prejšnjih zahtev.
- Loči:
  - **STANJE APLIKACIJE** — skrbi zanj **odjemalec** (kje v procesu je).
  - **STANJE VIRA** — vzdržuje ga **strežnik** (trajno shranjevanje).
- **Prednosti:** lažje horizontalno skaliranje, boljši cache, večja odpornost, preprostejši strežnik.
- **Kompromis:** daljše zahteve (pošiljanje identifikatorja/žetonov), potreba po JWT/tokenih, del odgovornosti za stanje na odjemalcu.

> 💡 **Primer nakupovanja brez stanja:** namesto "seje" so **košarica, naročilo, račun VIRI** na strežniku (npr. `/uporabniki/Janez/kosarica`). Vsaka zahteva pošlje identiteto ("jaz sem Janez + žeton"). URI košarice lahko uporabijo tudi druge storitve.

---

### Princip 5: HATEOAS
- **Hypermedia As The Engine Of Application State** — kar najbolj loči REST od drugih arhitektur.
- Ideja: interakcija se v celoti upravlja skozi **hipermedijske dokumente**, ki jih strežnik dinamično vrača — predstavitev vira **vsebuje povezave (linke), kaj lahko narediš naprej**.
- V praksi se veliko "REST API-jev" (GitHub, Stripe) **ne drži** HATEOAS strogo → je **idealiziran** princip.

**Primer (bančni račun):**
```xml
<racun>
  <st_racuna>12345</st_racuna>
  <stanje currency="eur">100,00</stanje>
  <link rel="polog" href="/racun/12345/polog" />
  <link rel="dvig"  href="/racun/12345/dvig" />
  <link rel="prenos" href="/racun/12345/prenos" />
  <link rel="zapri" href="/racun/12345/zapri" />
</racun>
```
Po dvigu, ko je stanje negativno (`-25,00`), strežnik vrne **samo `polog`** (drugih akcij ni več) → **hipermedija vodi stanje aplikacije**. Uporablja se lahko format **Atom** (`<link rel href type>`).

---

## 5. RESTful spletne storitve

- Storitve, ki sledijo REST principom. **HTTP je naravna izbira** (enoten nabor metod, stateless, URI naslavljanje).

**Low REST vs High REST** (le praktičen opis, ne standard):
| Low REST | High REST |
|---|---|
| GET za branje, **POST za vse ostalo** | semantični URI (viri, ne akcije) |
| URI-ji niso "lepi" (glagoli, action param.) | konsistentne metode GET/POST/PUT/DELETE(/PATCH) |
| poljubni MIME tipi | strukturirani odgovori (JSON/XML) |
| | HATEOAS kjer smiselno |

**Izzivi REST:**
- koliko dosledno slediti principom (high vs low),
- ali so 4 metode dovolj (kasneje PATCH),
- preslikava sinhronih REST operacij na **asinhrone/dogodkovne** zaledne sisteme (potreba po vrstah, webhookih),
- **ni strogega standarda za opis** REST API-jev → de-facto: **OpenAPI/Swagger**, RAML, API Blueprint.

### Metodologija razvoja REST storitev (7 korakov)
1. Identifikacija virov, ki jih izpostavimo.
2. Modeliranje povezav (prehodi stanj) med viri.
3. Definicija "lepih" URI.
4. Razumevanje pomena GET/POST/PUT/DELETE za vsak vir.
5. Načrtovanje in dokumentacija predstavitev.
6. Implementacija in namestitev.
7. Testiranje (brskalnik, odjemalec, Fiddler ...).

### Ustvarjanje virov: PUT vs POST
- **PUT `/vir/{id}`** → `201 Created` — **odjemalec določi ID** (npr. GUID). Idempotenten.
- **POST `/vir`** → `201 Created` + `Location: /vir/{id}` — **strežnik določi ID**. Ni idempotenten (več klicev = več virov).

### Sočasni dostop (lost update)
Problem: dva odjemalca hkrati spreminjata isti vir → **izguba novejših podatkov (lost update)**.
Rešitev: strežnik zavrne posodobitev, če se je vir vmes spremenil → **`409 Conflict`** (tipično s pomočjo ETag/If-Match).

---

## 6. Načrtovalski vzorci in ANTIVZORCI REST

### Vzorci (dobre prakse)
- **Enoten vmesnik** — problem: vsak ponudnik svoje metode → tesna sklopljenost. Rešitev: standardiziran enoten API prek ponudnikov (isti path/shema, razlika le v `host`). Zamenjava ponudnika = zamenjaš le host.
- **Preusmeritev končne točke** — URI se spremeni; strežnik vrne `301 Moved Permanently` / `307 Temporary Redirect` + `Location: /novURI`. Odjemalci uporabljajo stare naslove in sledijo preusmeritvam.
- **Končna točka entitete** — vsako poslovno entiteto izpostavimo na **lastnem stabilnem URI-ju** (`/zaposleni/123`) → lažje predpomnjenje in povezovanje.
- **Povezovanje entitet** — povezave do povezanih virov vključimo v predstavitev (`/oseba/janez/racun`) → odjemalec **sledi povezavam, ne ugiba** (= HATEOAS). Povezave v zaglavju (`Location`, `Link`) ali v telesu (`_links`).
- **Pogajanje o predstavitvi** — odjemalec pošlje `Accept`, strežnik izbere format ali vrne `406`. Večdimenzionalno: `Accept` (format), `Accept-Language` (jezik), `Accept-Charset` (znaki), `Accept-Encoding` (gzip). Prednost: manj podvajanja URI-jev, šibkejša sklopljenost.
- **Porazdeljeno medpomnjenje (caching)** — cilj: enako predstavitev tvorimo čim manjkrat. Mehanizmi HTTP:

**ETag** (Entity Tag) — oznaka (hash/verzija) predstavitve vira:
```
# 1. strežnik vrne z ETag
HTTP/1.1 200 OK
ETag: "88d979a0..."
# 2. odjemalec pošlje pogojno zahtevo
GET /vir
If-None-Match: "88d979a0..."
# 3a. če ni spremembe → 304 Not Modified (brez telesa, uporabi cache)
# 3b. če je sprememba → 200 OK z novim telesom in novim ETag
```
**Last-Modified** — enaka logika, a temelji na **času** zadnje spremembe: strežnik pošlje `Last-Modified`, odjemalec `If-Modified-Since`. Slabost: ločljivost ~1 sekunda (več sprememb v isti sekundi se "skrije") → ETag natančnejši.

- **Idempotentne zmožnosti** — v porazdeljenih sistemih pride do timeoutov/ponovnih pošiljanj. Če operacije **niso idempotentne**, ponovitev povzroči podvojena naročila/dvojna knjiženja. Rešitev: zasnuj operacije idempotentno (GET varen, PUT/DELETE idempotentna). ESB lahko pomaga (zanesljivo posredovanje, vrste, retry), a **sam ne zagotovi idempotentnosti**.

### Antivzorci (napake) — "RPC prek HTTP, ne REST"
- **Tuneliranje GET** — `GET /api?method=brisiStranko&id=4102` — GET spreminja stanje (krši semantiko), podatki v dnevnikih/zaznamkih, omejena dolžina URI.
- **Tuneliranje POST** — POST kot "tunel" za lasten protokol (npr. SOAP ovojnica) → HTTP le prenos, semantika metod neizkoriščena, otežen cache.
- **Tuneliranje napak skozi telo** — vedno `200 OK`, napaka le v telesu → infrastruktura ne more uporabiti statusnih kod. **Boljše:** prave HTTP kode (`404 Not Found`) + podrobnosti v telesu.

**Standardne HTTP kode:** 2xx uspeh (200 OK, 201 Created, 204 No Content), 3xx preusmeritve (301, 304 Not Modified), **4xx napaka odjemalca** (400 Bad Request, 401, 403, 404, 405 Method Not Allowed, 406, 409 Conflict, 415 Unsupported Media Type), **5xx napaka strežnika** (500, 501, 503 Service Unavailable, 504 Gateway Timeout).

> ⚠️ **Roy Fielding o "Microsoft REST Guidelines":** "REST != HTTP." Če API ne upošteva **vseh** omejitev REST (posebej HATEOAS), to ni REST — pošteno je govoriti o **HTTP API / spletnem API**. Smernice so koristne za HTTP API-je, a niso RESTful.

---

## 7. SOAP / WS-\* vs REST

**Osnovna razlika:**
| WS-\* (SOAP/RPC) | REST |
|---|---|
| **middleware / povezovalna oprema** | **arhitekturni stil** za spletne vire |
| usmerjenost v **operacije/storitve** | usmerjenost v **vire** |
| za integracijo poslovnih sistemov | odprti API-ji, sodelovanje, mobilne apl. |
| močno tipizirani vmesniki (WSDL, XSD) | prožni lahki formati (JSON, XML) |
| 1 endpoint URI, `POST /soap/endpoint` za vse | N URI-jev, GET/POST/PUT/DELETE nad viri |
| skrivanje zaledja (princip) | odprti viri, hiperlinki, HATEOAS |

- **NE mešamo** SOAP in REST storitev.
- **Varnost:** WS-\* → WS-Security, XML Signature/Encryption (od-točke-do-točke, ni nujen HTTPS). REST → HTTPS (SSL/TLS), Basic Auth, OAuth/OAuth2, OpenID, JWT.
- **Zanesljivost/async:** WS-\* → WS-Addressing, WS-ReliableMessaging, JMS/MSMQ. REST → vrste, webhooki.
- **Sklada:** WS-\* ima obsežen sklad (SOAP, WSDL, UDDI, WS-Security, WS-BPEL ...); REST ima lahek sklad (URI, HTTP, MIME, JSON/XML, Atom/AtomPub, SSL/TLS).

> **Ni univerzalno boljšega!** Izbira je odvisna od problema, zahtev in omejitev (način integracije, pogodbe, varnost, transakcije, kompozicija ...).

---

## 8. Ali lahko gradimo SOA z REST?

- **Na višjem nivoju DA, a ne popolnoma.**
- SOA temelji na **funkcijski dekompoziciji** (komponente, poslovne storitve, poslovni procesi/orkestracija BPEL). REST temelji na **dekompoziciji na vire** → **ROA (Resource-Oriented Architecture)**.
- Prava vprašanje: *ali ROA zgrajena na REST zadovolji vse cilje/principe SOA?*
- **Aforizem:** *"If WS-\* is the RPC of the Internet, REST is the DBMS of the Internet."* — REST viri se navzven obnašajo kot tabele (INSERT/SELECT/UPDATE/DELETE ↔ POST/GET/PUT/DELETE).

**Storitev vs Vir:**
| Storitev | Vir |
|---|---|
| samo-vsebovana komponenta za **poslovno funkcionalnost** | direktno dosegljiva komponenta, ki ponuja **podatke** (+ povezave na druge vire) |
| funkcionalnost v javnem vmesniku (WSDL) | definiran z URL + vhodi/izhodi; **akcije v predstavitvi** (HATEOAS) |

- SOA principi (standardizacija pogodb, šibka sklopljenost, abstrakcija, ponovna uporaba, avtonomnost, brez stanja, odkrivanje, kompozicija) — z REST **jih je mogoče** doseči, a **ni samoumevno**: zahteva disciplinirano modeliranje, governance/verzioniranje in **formalni opis vmesnikov** (WADL, WSDL 2.0, **OpenAPI**). Za REST ni enega univerzalnega standarda kot WSDL.
- **Orkestracija** je glavna prednost SOA (kompozicija storitev v poslovne procese). WS-\* ima **WS-BPEL**. REST osnovno **nima koncepta kompozicije** (nastali so MashUps). WSDL 2.0 HTTP Binding lahko ovije RESTful storitve, a WS-BPEL 2.0 ob nastanku ni podpiral WSDL 2.0.

---

## Ključni povzetek predavanja 10
- **7 strateških ciljev SOA**: 4 sredstva (interoperabilnost, poenotenje, raznolikost, usklajenost) → 3 koristi (ROI, agilnost, manjše breme IT).
- **SOA Manifesto**: 6 vrednot (poslovna vrednost, strateški cilji, notranja interop., skupna raba, prilagodljivost, evolucija) + načela ("SOA ni produkt", "začni majhno", "enotnost navzven, raznolikost navznoter").
- **Vzorci SOA**: 5 kategorij (inventar, storitve, kompozicije, REST, sestavljeni) = katalog rešitev.
- **REST**: arhitekturni stil (Fielding 2000), **5 principov**: naslovljivi viri, enoten vmesnik, predstavitvena usmerjenost, brez stanja, HATEOAS.
- **HTTP**: idempotentne (GET/PUT/DELETE) in varne (GET/HEAD) metode; CRUD↔HTTP; caching z ETag/Last-Modified; kode 2xx/3xx/4xx/5xx.
- **Antivzorci**: tuneliranje GET/POST/napak = RPC prek HTTP ≠ REST.
- **SOAP vs REST**: operacije vs viri; ni univerzalno boljšega.
- **SOA z REST**: možno na višjem nivoju, a zahteva disciplino; šibka točka = opis vmesnikov in orkestracija.
