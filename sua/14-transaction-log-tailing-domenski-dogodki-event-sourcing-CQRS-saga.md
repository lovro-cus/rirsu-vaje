# Predavanje 14 — Napredni vzorci v mikrostoritvah: Transactional Outbox, Transaction Log Tailing, domenski dogodki, Event Sourcing, CQRS, Saga

> **O čem je predavanje:** kako **zanesljivo posodobiti bazo IN objaviti dogodek** (problem "dual write"), kako shranjevati stanje kot **dogodke (Event Sourcing)**, kako ločiti branje od pisanja (**CQRS**) in kako izvesti **porazdeljeno transakcijo čez več storitev (Saga)** brez klasičnega 2PC.

---

## 1. Temeljni problem: kako atomarno posodobiti bazo + objaviti dogodek?

Ko se stanje spremeni, storitev pogosto naredi **dve stvari**:
1. zapiše spremembo v svojo bazo (INSERT/UPDATE),
2. objavi dogodek v sporočilni sistem (npr. "NaročiloUstvarjeno").

> ⚠️ **Problem "dual write":** lahko uspemo zapisati v bazo, a **ne uspemo objaviti dogodka** (ali obratno) → nekonsistentno stanje. Ni skupne transakcije med bazo in sporočilnim sistemom.

**Rešitve (vzorci za zanesljivo objavo dogodkov):** Transactional Outbox, Transaction Log Tailing, Event Sourcing (vsi sodijo pod "zagotavljanje konsistentnosti" ob EDA).

---

## 2. Vzorec: Transactional Outbox (Dogodki, ustvarjeni s strani aplikacije)

**Ideja:** storitev v **eni lokalni transakciji** zapiše **oboje** — poslovno spremembo IN dogodek v posebno **outbox tabelo** (npr. `Dogodki`).

```
LOKALNA TRANSAKCIJA (atomarno):
  INSERT v tabelo Narocila       (poslovni podatek)
  INSERT v tabelo Dogodki/Outbox (dogodek "NaročiloUstvarjeno")
```
- Ker sta oba zapisa v isti transakciji → **ni situacije "podatek shranjen, dogodek pa ne"**.
- **Objavljalec dogodkov** (posebna komponenta) periodično bere nove zapise iz outbox tabele, jih **objavi** v sporočilni sistem in **označi kot obdelane** (ali izbriše).

**Prednosti:**
- **domenski (visokonivojski) dogodki** — odražajo poslovni pomen ("OrderPlaced"), ne le sprememb vrstic.
- konsistentnost z lokalno transakcijo.

**Slabosti:**
- potrebna sprememba aplikacije (outbox tabela + logika),
- **možni duplikati (at-least-once)** — dogodek se lahko objavi večkrat → porabniki morajo biti **idempotentni** (dogodki naj imajo unikaten ID),
- najlažje v SQL; pri NoSQL le, če podpira ustrezne transakcije.

---

## 3. Vzorec: Transaction Log Tailing (CDC — Change Data Capture)

**Ideja:** storitev normalno zapiše v bazo. **Ločena komponenta na sistemski ravni spremlja dnevnik transakcij** (transaction log) baze, iz njega zazna spremembe in **objavi dogodke** v sporočilni sistem.

```
Storitev → INSERT v tabelo (navadna transakcija)
              ↓
        Dnevnik transakcij
              ↓ (rudarjenje dnevnika)
        CDC komponenta → objavi dogodek → Sporočilni sistem
```

**Prednosti:**
- **brez sprememb poslovne kode** (spremembe zajema ločena CDC komponenta),
- **točen zajem** (temelji na transakcijskem dnevniku, ne izpusti commit-anih sprememb),
- dobro za integracije/replikacije/analitiko.

**Slabosti:**
- dogodki so na **podatkovnem nivoju** ("row change events") → za poslovne dogodke potrebna dodatna interpretacija,
- **vezanost na SUPB** (vsaka baza ima svoj dnevnik),
- kompleksna semantika dostave (vrstni red, duplikati, at-least-once → idempotentnost pri porabnikih),
- operativna zahtevnost (konektorji, nadzor zaostanka/lag).

**Primeri:** **Debezium** (Kafka Connect: MySQL binlog, PostgreSQL logical replication), **MongoDB** (oplog + Change Streams), **AWS DynamoDB Streams**, LinkedIn Databus, Oracle GoldenGate, AWS DMS.

> 💡 **Outbox vs Log Tailing:** Outbox = aplikacija zapiše dogodek (domenski, a spremeni kodo). Log Tailing = infrastruktura bere dnevnik (brez kode, a dogodki so nizkonivojski).

---

## 4. Vzorec: Event Sourcing (dogodkovno shranjevanje)

**Ideja:** stanje NE shranjujemo kot "trenutno stanje", ampak kot **zaporedje dogodkov (append-only)**.

- **Klasično:** tabela `Narocila` s stolpcem `STATUS = 'NovoNarocilo'` (hranimo **kako je zdaj**).
- **Event Sourcing:** hranimo zaporedje dogodkov (hranimo **kaj se je zgodilo**):
  - `NarociloUstvarjeno` → `PlaciloPotrjeno` → `NarociloOdposlano` ...
- **Trenutno stanje** dobimo tako, da dogodke **ponovno predvajamo (replay)** v pravilnem vrstnem redu.
- Dogodki so **neizbrisljivi** — ne popravljamo zgodovine, dodamo nov dogodek.

**Tabela Events (namesto tabele stanja):**
| Aggregate ID | Aggregate Type | Event ID | Event Type | Event Data |
|---|---|---|---|---|
| 101 | Naročilo | 901 | NarociloUstvarjeno | ... |
| 101 | Naročilo | 902 | PlaciloPotrjeno | ... |
| 101 | Naročilo | 903 | NarociloOdposlano | ... |

Za vsako poslovno entiteto identificiramo **domenske dogodke** (npr. Košarica: IzdelekDodan, IzdelekOdstranjen; Naročilo: NovoNaročilo, NaročiloPreklicano ...).

**Shramba dogodkov (Event Store)** mora hkrati: trajno hraniti dogodke (kot baza) IN distribuirati dogodke porabnikom (kot pub/sub).
- rešitve: **EventStoreDB**, Axon Server (event-native); **Eventuate** (SQL + Kafka, hibrid); lastne implementacije.

**Prednosti:** sledljivost/revizijska sled (kdo, kaj, kdaj), ponovljivost ("time travel" — stanje za poljuben trenutek), lažje povezovanje (objaviš dogodke), dobro se ujema s **CQRS**.

**Izzivi:** aplikacijo pišemo od začetka, manj znan stil (učna krivulja), rekonstrukcija stanja iz mnogih dogodkov je lahko počasna, **verzioniranje sheme dogodkov**, napak ne "popravljamo" (dodajamo dogodke), pazi na **duplikate** (idempotentni handlerji).

---

## 5. Vzorec: CQRS (Command Query Responsibility Segregation)

**Problem:** Event Sourcing reši posodabljanje, a **oteži poizvedbe**. Če shramba dogodkov omogoča branje samo po **primarnem ključu**, ni mogoče izvesti poizvedbe kot "najdi stranke z naročili > 1000 v zadnjem tednu" (potreben join čez podatke dveh storitev).

**CQRS = ločitev odgovornosti za:**
- **Command** — operacije, ki **spreminjajo** stanje (zapis: POST/PUT/DELETE).
- **Query** — operacije, ki **berejo** stanje (branje: GET).

**Sistem se razdeli na 2 komponenti:**
```
        Command API (POST/PUT/DELETE)          Query API (GET)
              ↓ (ukazna stran)                      ↑ (povpraševalna stran)
        zapiše dogodke                        bere iz READ MODELA (hitro)
              ↓                                      ↑
        Shramba dogodkov  ──── posodablja ───→  Read model (MongoDB/Redis/SQL/
                          (pogosto asinhrono)   ElasticSearch — po meri UI)
```

- **Write model** zapisuje (dogodke/podatke), **Read model** = optimizirana **projekcija** za branje (manj joinov, hitre poizvedbe).
- Read model se posodablja iz zapisa **pogosto asinhrono** → **možna sčasoma konsistentnost** (UI mora tolerirati zamik).

**Zakaj CQRS:** različne zahteve branja/pisanja (veliko branja, malo pisanja), optimizacija branja (read modeli po meri), **neodvisno skaliranje** branja in pisanja.

**CQRS + Event Sourcing** se dopolnjujeta: ES napaja CQRS (write zapisuje dogodke, read modeli = projekcije iz dogodkov). Toda CQRS gre tudi **brez** ES (klasična SQL baza za write + projekcije za read).

**Izzivi CQRS:** več komponent = večja kompleksnost, disciplina pri usklajevanju write↔read, sčasoma konsistentni podatki, več integracijskega testiranja.

---

## 6. Vzorec: Saga (porazdeljena transakcija)

**Problem:** v mikrostoritvah ima vsaka storitev svoje podatke → **klasična ACID transakcija čez več baz ni praktična** (2PC neprimeren). A poslovni proces pogosto zahteva posodobitev več storitev (naročilo + plačilo + zaloga).

**Saga = porazdeljena transakcija kot zaporedje lokalnih transakcij.** Vsak korak:
- izvede **lokalno transakcijo** v eni storitvi,
- sproži naslednji korak (dogodek ali ukaz).

Če korak **ne uspe**, Saga sproži **kompenzacijske transakcije**, ki **logično razveljavijo** že izvedene korake.

> 🔑 **Kompenzacija ni rollback na nivoju baze**, ampak **poslovno razveljavljanje** — npr. "rezervacijo zaloge" razveljavimo s "sprostitev rezervacije". Konsistentnost = **eventual consistency**.

### Dva načina izvedbe Sage

**A) Orkestracija (orchestrated saga):**
- Obstaja **orkestrator** (osrednja storitev), ki pošilja ukaze storitvam, spremlja odgovore/dogodke, odloča o naslednjih korakih in kompenzacijah.
- Če pride do napake, je orkestrator odgovoren za **klice, ki razveljavijo** stanje.
- ✅ jasen nadzor poteka, lažje razumevanje.
- ❌ dodatna komponenta, tveganje "preveč centralne logike".

```
Orkestrator (Naročilo):
  1. → Plačilo: "Potrdi plačilo?" ← "Plačilo potrjeno"
  2. → Zaloga: "Zmanjšaj zalogo"  ← "Zaloga zmanjšana"
  3. → Dostava: "Dostavi izdelek" ← "Dostava potrjena"
  (ob napaki v koraku 3 → orkestrator kliče kompenzacije za 1,2)
```

**B) Koreografija (choreographed saga):**
- **Ni centralnega vodje** — storitve se odzivajo na dogodke in sprožajo naslednje dogodke. Ne čaka se na odgovor.
- ✅ manj centralizacije, bolj šibko povezano.
- ❌ potek težje sledljiv, večja potreba po opazovanju.

```
Naročilo → objavi "Izdelek naročen"
Plačilo  → (naročeno na dogodek) → objavi "Izdelek plačan" ali "Plačilo ni uspelo"
Zaloga   → (naročeno) → ...
Dostava  → (naročeno) → ...
```

**Praktični izzivi Sage:** **idempotentnost** (podvojena sporočila varno obdelati), **zanesljivost sporočil** (robusten broker), **sledenje** (correlation ID, tracing), kompenzacije niso vedno popolne (le poslovna razveljavitev), timeouti in ročno posredovanje pri dolgih procesih.

> 💡 **Orkestracija vs koreografija:** orkestracija = dirigent vodi orkester (ena storitev ukazuje). Koreografija = plesalci znajo svoj del in se odzivajo drug na drugega (brez dirigenta).

---

## 7. Programska ogrodja za razvoj mikrostoritev

Ker je infrastrukture veliko (konfiguracija, logging, odkrivanje storitev, Circuit Breaker, health checks, metrike), uporabimo **ogrodja z out-of-the-box podporo**:

- **Java:** Spring Boot, **Spring Cloud** (config, discovery, routing, load balancing, circuit breakers), Dropwizard, **Quarkus** (Kubernetes-native), Micronaut, Helidon, Eclipse MicroProfile.
- **.NET:** ASP.NET Core (HTTP API, gRPC).
- **Node.js/TypeScript:** NestJS.
- **Python:** FastAPI.
- **Go:** Go kit.

---

## Ključni povzetek predavanja 14
- **Problem dual write:** baza + dogodek nista v skupni transakciji → rešitve:
  - **Transactional Outbox** — dogodek v isto lokalno transakcijo (outbox tabela), objavljalec ga bere; domenski dogodki, a sprememba kode.
  - **Transaction Log Tailing (CDC)** — CDC bere dnevnik baze (Debezium); brez kode, a nizkonivojski dogodki.
- **Event Sourcing:** stanje = zaporedje dogodkov (append-only), stanje dobimo z replay; sledljivost + time travel, a učna krivulja in počasna rekonstrukcija.
- **CQRS:** ločimo **Command** (zapis) od **Query** (branje, optimiziran read model/projekcija); rešuje poizvedbe pri ES; sčasoma konsistentno.
- **Saga:** porazdeljena transakcija = zaporedje lokalnih transakcij + **kompenzacije** (poslovno razveljavljanje, ne DB rollback); **orkestracija** (dirigent) vs **koreografija** (dogodki); eventual consistency.
- Vse temelji na **idempotentnosti** in **zanesljivem sporočanju**.
- Za razvoj: ogrodja (Spring Cloud, Quarkus, ASP.NET Core ...).
