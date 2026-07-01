# Predavanje 13 — Izzivi in vzorci v mikrostoritvenih arhitekturah: dekompozicija, nameščanje, komunikacija, API Gateway, delne okvare, registracija in odkrivanje storitev, upravljanje podatkov

> **O čem je predavanje:** kako mikrostoritvena arhitektura rešuje svoje izzive z **vzorci**. Pokrije: **dekompozicijo** (kako razdeliti sistem), **nameščanje** (kako uvesti veliko storitev), **komunikacijo** (RPC vs sporočanje, API Gateway), **obravnavo delnih okvar** (Circuit Breaker), **registracijo/odkrivanje storitev**, in **upravljanje porazdeljenih podatkov** (database per service, EDA).

> Vir vzorcev: **microservices.io** (Chris Richardson).

---

## 1. Ključni izzivi in kako jih rešujemo

**Izzivi:** kako razdeliti sistem? kako uvajati (CI/CD)? kako komunicirati (odjemalec↔storitev, storitev↔storitev)? kako obvladati delne okvare? kako upravljati porazdeljene podatke in konsistentnost? kako testirati in koordinirati spremembe?

**Rešitve = vzorci + orodja:**
- **Vzorci/prakse:** API Gateway, Service Registry/Discovery, Circuit Breaker, Event Sourcing, CQRS, Saga.
- **Orodja/platforme:** knjižnice (komunikacija, odpornost, opazljivost), oblačne platforme, **zabojniki (Docker)** + **orkestracija (Kubernetes)**.

---

## 2. Dekompozicija: kako razdeliti sistem na mikrostoritve

**Osnovna načela:**
- stabilne meje med storitvami (jasne domene/odgovornosti),
- vsaka storitev = majhen nabor tesno povezanih funkcionalnosti (ena poslovna zmožnost),
- šibka sklopljenost (navzven API, notranjost svobodno spreminjamo),
- storitev naj vzdržuje majhna, **avtonomna** ekipa (~6–10 članov).
- **Cilj:** omogočiti **neodvisen in vzporeden razvoj + nameščanje**.

**Vzorci dekompozicije:**

| Vzorec | Kako |
|---|---|
| **Po poslovnih zmožnostih** (business capability) | storitev = dejavnost, ki ustvarja vrednost, pogosto vezana na entiteto (upravljanje naročil→naročila, strank→stranke). Primer trgovina: katalog, zaloge, naročila, dostava |
| **Po domenah/poddomenah** (DDD subdomain) | poslovanje razdelimo na domene → poddomene: **jedrna (core)** (konkurenčna prednost), **podporna (supporting)** (potrebna, ne ključna), **splošna (generic)** (standardna rešitev) |
| **Samozadostne storitve** (self-contained) | storitev odgovori na sinhroni klic z **minimalno odvisnostjo** od drugih (uporabi Saga za async sodelovanje, CQRS za lokalne kopije branja) |
| **Po odgovornostih ekip** (service per team) | storitev razmejimo tako, da jo obvlada ena avtonomna ekipa; obseg ne sme preseči **kognitivne zmožnosti** ekipe |

**Samozadostna storitev — zakaj:** če se ena zahteva razdeli na več sinhronih klicev, je razpoložljivost odvisna od **vseh** sodelujočih storitev (in latenca se sešteva). Rešitev: **Saga** (async poslovni proces prek lokalnih transakcij) + **CQRS** (lokalna kopija tujih podatkov za hitro branje).

**Koliko storitev? (granulacija):**
- **Premalo** → sistem se približa monolitu (isti problemi).
- **Preveč** → **Nano-service antivzorec** (preveč drobno, več omrežne komunikacije, večja latenca, večja operativna obremenitev, slabša preglednost).
- **Cilj:** dovolj majhne za neodvisno delo ekipe, a dovolj velike za smiselno poslovno odgovornost.

---

## 3. Nameščanje veliko storitev

**Problem:** monolit = 1 aplikacija, 1 deployment, 1 konfiguracija; mikrostoritve = N (10/100/1000) storitev, N deploymentov, N konfiguracij, N logov/metrik.

**Operativni izzivi:** CI/CD, konfiguracija (okolja, skrivnosti), opazljivost (monitoring/logi/tracing), zanesljivost, skaliranje. Heterogenost tehnologij, več instanc na storitev, izolacija instanc, omejevanje virov.

**Vzorec: Platforma za nameščanje** — abstrahira izvajalno okolje: razporejanje instanc, health checks, ponovni zagon ob napaki, load balancing, samodejno skaliranje.

**Strategije nameščanja (od težjega k lažjemu):**

| Strategija | Opis | Prednosti | Slabosti |
|---|---|---|---|
| **Več instanc na strežnik** | več storitev na en (V)strežnik | učinkovita raba virov, enostavno v majhnem obsegu | **slaba izolacija**, omejen nadzor virov, "dependency hell" |
| **Storitev na VM** | vsaka instanca = svoj VM | **visoka izolacija**, enkapsulacija (OS+runtime), dobra z oblakom | slaba izkoriščenost (vsak VM svoj OS), počasnejši zagon/gradnja |
| **Storitev na zabojnik** (Docker) | vsaka storitev = slika zabojnika | dobra izolacija, hitro uvajanje, učinkovita raba, enkapsulacija tehnologije | potrebna **orkestracija (Kubernetes)**, slabša izolacija kot VM (delijo jedro OS), zahtevnejša opazljivost |
| **Brezstrežniško** (serverless) | ponudnik skrije infrastrukturo | samodejno skaliranje, plačilo po uporabi | manj nadzora |

**Primeri platform:** orkestracija zabojnikov (**Kubernetes**, Docker Swarm, Nomad), upravljana v oblaku (ECS, EKS, AKS, GKE), serverless containers (Fargate, Cloud Run, Azure Container Apps), PaaS (Cloud Foundry, Heroku, App Service), **FaaS** (AWS Lambda, Azure Functions, Cloudflare Workers).

**Brezstrežniško (serverless):**
- **FaaS (Function as a Service):** izvajanje funkcij na zahtevo (dogodki/HTTP) — Lambda, Azure/Google Functions.
- **BaaS (Backend as a Service):** pripravljene zaledne storitve (avtentikacija, shramba) — Firebase, Supabase.

> 💡 **Docker Compose** poenostavi razvoj v ekipah: celotno okolje (koda + baza + sporočilni sistem) opišemo kot konfiguracijo → "en ukaz = enako okolje" na vsakem računalniku.

---

## 4. Komunikacija med storitvami

Mikrostoritve = **porazdeljen sistem** (ločeni procesi) → potrebna **medprocesna komunikacija** (ne lokalni klici kot v monolitu). Lahko je **več sto končnih točk**.

**Dva vprašanja:** (1) odjemalec↔storitve (usmerjanje, avtentikacija, enotna vstopna točka), (2) storitev↔storitev (sinhrono/asinhrono, odpornost, pogodbe).

### API-first pristop
API-je načrtujemo **pred implementacijo** (API = pogodba). Pri REST je API pogosto nastal kot "stranski produkt" → potreba po specifikaciji, neodvisni od implementacije → **OpenAPI/Swagger** (jasna definicija, usklajevanje ekip, generiranje dokumentacije/odjemalcev). Postopek: napiši IDL spec → uskladi z odjemalci → implementiraj.

**Formati sporočil:**
- **Besedilni** (JSON, XML) — berljivi, samoopisni; slabost: večji, počasnejši parsing.
- **Binarni** (Protocol Buffers, Avro) — kompaktni, hitri; slabost: potrebna stroga shema.

**Spremembe API-ja:**
- **Manjše (združljive nazaj):** dodamo opcijska polja → odjemalci jih ignorirajo.
- **Večje (nezdružljive):** sprememba/odstranitev polj → **verzioniranje** (v URL ali glavi).

### Vzorec: Komunikacijski stili
- **RPC (sinhrono)** — neposreden klic + čakanje na odgovor (REST/HTTP, gRPC).
- **Sporočanje (asinhrono)** — izmenjava sporočil/dogodkov prek posrednika; pošiljatelj ne čaka.
- **Domensko specifično** — EDA, pub/sub, Saga.

**Topologije interakcije:**
| | Sinhrono | Asinhrono |
|---|---|---|
| **1:1** | zahteva-odgovor (HTTP/gRPC) | ukaz-odgovor prek sporočil (korelacijski ID) |
| **1:N** | fan-out (problematično: cascading failures) | **pub/sub** (dogodek → več naročnikov, npr. "OrderCreated") |

> **Dogodek** = enosmerno obvestilo, da se je nekaj zgodilo (fire-and-forget). **Ukaz** = zahteva, da nekdo nekaj naredi.

**RPC:**
- prednosti: enostaven, znan, naravni request-response, brez posrednika.
- slabosti: omejen na sinhrono; storitev **mora biti dosegljiva** (sicer timeout); odjemalec mora poznati naslavljanje.

**Sporočanje (message broker):** pošiljatelj odda sporočilo v sistem, prejemnik(i) ga prevzame(jo) ko lahko.
- **Vrste (queues):** en prejemnik.
- **Teme (topics):** publish/subscribe, več naročnikov.
- prednosti: **šibka sklopljenost** (neodvisnost v času in prostoru), obstojnost/zanesljiva dostava, različni vzorci.
- slabosti: dodatna infrastruktura/kompleksnost, request-response težje (potrebna korelacija).
- primeri: **RabbitMQ, Apache Kafka**, ActiveMQ, NSQ, ZeroMQ, IBM MQ, Amazon SQS, Google Pub/Sub.

---

## 5. Vzorec: API Gateway (API prehod)

**Problem direktnega povezovanja** front-end ↔ storitve: veliko omrežnih klicev/latenca, različni protokoli, upravljanje naslovov/vrat, odvisnost od notranje strukture.

**Rešitev:** **enotna vstopna točka**, ki sprejme zahtevo in jo usmeri do storitev, po potrebi združi odgovore in **skrije notranjo kompleksnost**.

**API Gateway lahko:**
- posreduje/preusmeri zahtevo do storitve,
- **orkestrira** klic čez več storitev (sestavi en odgovor),
- izpostavi **API prilagojen odjemalcu** (drug za splet, drug za mobilno),
- **prevaja protokole** (notranji gRPC ↔ zunanji REST),
- doda skupne (**precne**) funkcije: **avtentikacija/avtorizacija, omejevanje prometa (rate limiting), beleženje (logging)**.

**Prednosti:** odjemalcu ni treba odkrivati storitev; API prilagojen odjemalcu; manj zahtevkov/prenosa (združevanje); manjša latenca; poenostavljena koda odjemalca.
**Izzivi:** dodatna kompleksnost (nova komponenta), **kritična vstopna točka** (mora biti visoko razpoložljiva), potencialno daljši odziv (dodaten skok).

> **Primer Netflix API:** optimizirali število klicev odjemalca (manj klicev → manjša zakasnitev). Arhitektura: dinamično dodajanje končnih točk, izvajanje storitev v različnih jezikih, asinhroni/reaktivni model, nivo za upravljanje napak, abstrakcija dostopa do zaledja. (Sorodni vzorec: **BFF — Backend For Frontend**.)

---

## 6. Obravnava delnih okvar

**Problem:** ena storitev preneha delovati / postane počasna → kaj se zgodi s klici?

**Problem omejenega števila niti:** sinhroni klic blokira nit, dokler ni odgovora. Če storitev ne odgovori, **niti se kopičijo** → sčasoma so **vse niti blokirane** → pade celotna aplikacija (cascading failure).

**Rešitve:**
- **Časovne omejitve (timeout)** — največji čas čakanja, da niti niso predolgo blokirane.
- **Omejevanje sočasnih klicev** — omejen bazen niti (če je poln, je odvisna storitev počasna/nedosegljiva).
- **Vzorec Circuit Breaker (prekinjevalec tokokroga / "varovalka"):**
  - spremljamo stopnjo napak (več zaporednih neuspehov),
  - ob pragu **"odpremo varovalko"** → začasno blokiramo nove klice,
  - po določenem času poskusimo znova → uspeh = normalno stanje, sicer varovalka spet odprta.

> 💡 **Analogija Circuit Breaker:** kot električna varovalka. Ko zazna, da je "vezje" (storitev) v okvari, jo **odklopi**, da preprečimo poškodbo celotnega sistema. Po času preveri, ali je težava odpravljena.

**Ravnanje ob napaki:**
- **fallback** (nadomestni odziv),
- podatki iz **cache** (če je sprejemljiva zastarelost),
- **informacija o napaki** (koda + sporočilo).

**Orodja za odpornost:** Hystrix (Netflix, zgodovinsko), **Resilience4J** (moderni naslednik), Failsafe, Spring Cloud Circuit Breaker.

---

## 7. Registracija in odkrivanje storitev

**Osnovni izziv:** odjemalec mora poznati **lokacijo** storitve (naslov+vrata/URL). V mikrostoritvah so lokacije **dinamične** (oblak/zabojniki, samodejno skaliranje, nove instance na različnih gostiteljih) → statična konfiguracija ni obvladljiva → **dinamično odkrivanje (Service Discovery)**.

### Vzorci odkrivanja
- **Client-side discovery** — odjemalec vpraša **register storitev** za seznam instanc in **sam izbere** (+ load balancing).
  - prednosti: prilagodljiv load balancing (npr. najbližja instanca).
  - slabosti: tesnejša sklopljenost z registrom, logika v vsakem jeziku, register = kritična komponenta.
  - primeri: **Netflix Eureka**, Ribbon, Zuul.
- **Server-side discovery** — odjemalec pošlje zahtevo **posredniku** (load balancer/API prehod), ta izbere instanco iz registra in preusmeri.
  - prednosti: preprostejša koda odjemalca, pogosto vgrajeno v platforme.
  - slabosti: omejeni algoritmi LB, dodatne komponente.
  - primeri: **AWS ELB**, NGINX Plus, **Kubernetes**.

### Register storitev (Service Registry)
Komponenta, ki hrani informacije o instancah (naslov, vrata). Podpira registracijo/odregistracijo in poizvedovanje.
- primeri: **Eureka, ZooKeeper, Consul, etcd**; Kubernetes/Marathon imajo vgrajen (prek DNS/imen).
- zahteve: instanca se ob zagonu registrira, ob ustavitvi odjavi; **okvarjene instance samodejno odstranimo** → potreben **health check / heartbeat**.

### Vzorci registracije
- **Samo-registracija (self-registration)** — instanca se **sama** registrira/odjavi.
  - prednosti: preprosto, brez dodatnih komponent.
  - slabosti: vezanost na register, podvajanje logike v jezikih, **nezanesljiva odjava ob nenadnem izpadu** (nujen heartbeat/health check).
  - primeri: Eureka, ZooKeeper (začasni znaki).
- **Komponenta za registracijo (third-party registrar)** — zunanji **registrator** zazna instanco in jo registrira (storitev ne ve za register).
  - prednosti: storitve preproste, samodejno spremljanje stanja, včasih "iz škatle".
  - slabosti: registrator = dodatna kritična komponenta.
  - primeri: Gliderlabs Registrator (Docker), Eureka Prana, **Kubernetes/Marathon**.

---

## 8. Upravljanje porazdeljenih podatkov

**Podatkovne zahteve/izzivi:** poizvedbe pogosto združujejo podatke več storitev; posodobitve zahtevajo usklajevanje čez več storitev (porazdeljene transakcije); različne potrebe po shrambi; replikacija; **podatkovna avtonomija** storitev.

### Vzorec A: Deljena (skupna) baza
Klasika iz monolita — več storitev dostopa do istih tabel.
- prednosti: enostavna implementacija, **ACID transakcije**, centraliziran nadzor.
- slabosti: **ni enkapsulacije**, tesna sklopljenost storitev in ekip, spremembe modela zahtevajo usklajevanje → izguba avtonomije, "zamrznjen" model.

### Vzorec B: Database per Service (baza na storitev) ✅ (priporočeno)
**Vsaka storitev je lastnik svojih podatkov**; dostop le prek API.
- realizacije: privatne tabele / privatna shema / privatni podatkovni strežnik.
- prednosti: **ohlapna sklopljenost**, **polyglot persistence** (vsaka storitev izbere najboljši SUPB: relacijski, ključ-vrednost, dokumentni ...).
- slabosti: **težje povezovanje podatkov** (porazdeljene poizvedbe), težja **konsistentnost** (eventual consistency), **ne moremo 2PC** → potrebni vzorci (Saga, kompenzacije).

### Konsistentnost brez 2PC
- **Problem:** poslovni proces zahteva posodobitev več virov v eni transakciji, a v mikrostoritvah ni skupne ACID baze; zaradi async klicev nastanejo začasno **nekonsistentna stanja**.
- **Primer:** Stranka ima limit; ob potrditvi naročila mora vsota vseh odprtih naročil ≤ limit. Naročilo in Stranka sta v **ločenih storitvah/bazah** → kako preveriti?

### Vzorec: Dogodkovno-usmerjena arhitektura (EDA)
- **EDA (Event-driven Architecture):** sistemi "slišijo" dogodke in se odzovejo. **Dogodek** = nekaj pomembnega, kar se zgodi.
- **Za konsistentnost:** storitve **objavijo dogodke** ob spremembi stanja; druge storitve so **naročene** in posodobijo svoje stanje → **sčasoma konsistentno (eventual consistency)** stanje + sinhronizacija podvojenih podatkov.
- **Primer (async, eventual consistency):** Novo naročilo → storitev Naročilo objavi "Naročilo ustvarjeno" → storitev Stranka rezervira sredstva → objavi "Sredstva rezervirana" ali "Premalo sredstev" → storitev Naročilo posodobi stanje.

> ⚠️ To je **uvod v predavanje 14** (Event Sourcing, CQRS, Saga — mehanizmi, kako to naredimo pravilno in zanesljivo).

---

## Ključni povzetek predavanja 13
- **Dekompozicija:** po poslovnih zmožnostih / domenah / samozadostnosti / ekipah; pazi na granulacijo (ne monolit, ne nano-service).
- **Nameščanje:** strategije (več na strežnik / VM / **zabojnik** / serverless); potrebna **orkestracija (Kubernetes)** + CI/CD.
- **Komunikacija:** **RPC (sinhrono)** vs **sporočanje (asinhrono, broker)**; API-first + OpenAPI; verzioniranje API.
- **API Gateway:** enotna vstopna točka — usmerjanje, agregacija, prevajanje protokolov, precne funkcije (varnost, rate limiting, logging).
- **Delne okvare:** timeout + omejevanje niti + **Circuit Breaker** (Resilience4J); fallback/cache.
- **Odkrivanje:** client-side vs server-side; **register storitev** (Eureka/Consul/Kubernetes); samo-registracija vs registrator; health check.
- **Podatki:** **Database per Service** (avtonomija, polyglot persistence) → konsistentnost brez 2PC prek **EDA / eventual consistency** (uvod v Saga/CQRS/Event Sourcing).
