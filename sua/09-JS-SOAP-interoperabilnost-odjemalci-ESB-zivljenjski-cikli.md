# Predavanje 09 — JavaScript & Contract-First, interoperabilnost, sinhroni/asinhroni odjemalci, ESB, življenjski cikli SOA, tipi SOA

> **O čem je predavanje:** kako razviti SOAP storitev in odjemalce v treh svetovih (Java, .NET, JavaScript), kaj pomeni, da so storitve *interoperabilne*, kaj je *storitveno vodilo (ESB)*, in kako izgleda *življenjski cikel razvoja SOA rešitve* (bottom-up / top-down / agilno) ter kateri *tipi arhitektur* obstajajo.

---

## 1. Contract-First razvoj SOAP storitve v JavaScriptu

**Contract-First** = najprej napišemo pogodbo (WSDL + XML sheme), šele nato implementacijo.

- Za **Javo/.NET** obstajajo orodja, ki iz WSDL avtomatsko generirajo kodo (wsimport, dotnet-svcutil).
- Za **JavaScript** teh generatorjev **ni**, zato:
  - WSDL napišemo **ročno**,
  - storitev **ročno implementiramo** skladno z WSDL.

### Primer: TrafficService
Storitev za spremljanje prometa. Ima 2 operaciji:
- `TrafficSensorActivation(...)` — aktivacija senzorja (vhod: ime, tip, lat, long → izhod: SensorId, status, datum).
- `TrafficFlow(...)` — pošiljanje meritev pretoka (vhod: SensorId, datumi, pretok → izhod: Response).

**WSDL struktura (ponovitev):**
- `<wsdl:types>` — XML sheme za sporočila (request/response tipi).
- `<wsdl:message>` — sporočila, ki povezujejo elemente iz shem.
- `<wsdl:portType>` — nabor operacij (input/output).
- `<wsdl:binding>` — kako se operacije prenašajo (SOAP/HTTP).
- `<wsdl:service>` + `<wsdl:port>` — kje storitev živi (naslov URL).

**Implementacija v Node.js (modul `soap` + `express`):**
```javascript
const soap = require('soap');
const express = require('express');
const fs = require('fs');
const wsdl_file = fs.readFileSync("TrafficService.wsdl", "utf-8");

// implementacija operacij = navadne JS funkcije
const TrafficSensorActivationImpl = (params) => ({
  SensorID: uuid.v4(), ActivationStatus: 'Activated', ActivationDate: '2.12.2025'
});
const TrafficFlowImpl = (params) => ({ Response: 'OK' });

// serviceObject mora slediti strukturi WSDL: Service > Port > Operacija
const serviceObject = {
  TrafficService: { TrafficServiceSOAP: {
    TrafficSensorActivation: TrafficSensorActivationImpl,
    TrafficFlow: TrafficFlowImpl
  }}
};

const app = express();
app.listen(9090, () => {
  soap.listen(app, "/TrafficService", serviceObject, wsdl_file);
});
```

> 💡 **Bistvo:** v JS je storitev le objekt, katerega struktura (Service → Port → Operacija) natančno posnema WSDL. Modul `soap` poskrbi za XML/SOAP ovojnico.

---

## 2. Interoperabilnost spletnih storitev

**Interoperabilnost** = sposobnost sodelovanja ne glede na jezik/platformo.

Storitev je **interoperabilna**, ko:
- jo lahko uporabi odjemalec v **poljubnem jeziku na poljubni platformi**, in
- zna komunicirati s **katerokoli drugo storitvijo**.

> Interoperabilnost zahteva jasno razumevanje zahtev in **dosledno upoštevanje specifikacij**.

### WS-I (Web Services Interoperability Organization)
Organizacija, ustanovljena za zagotavljanje interoperabilnosti SOAP storitev. Naredila je:
- navodila in najboljše prakse,
- **profile** spletnih storitev + testna orodja.

### Profili
Nastali, ker se je uporabljalo veliko specifikacij različnih verzij, ki so si nasprotovale.
- **Profil** = seznam specifikacij (ime + verzija) + navodila, kako jih uporabljati skupaj.

**WS-I Basic Profile** — osnovni profil, vsebuje:
- **Sporočanje** = SOAP/HTTP
- **Opis** = WSDL
- **Odkrivanje** = UDDI
- **Struktura podatkov** = XML Schema
- **Serializacija** = XML 1.0

Verzije: Basic Profile 1.0, 1.2, 2.0.

**Za razvijalce pomembno:** profil prepoveduje SOAP kodiranje vsebine (povzročalo je težave) in zahteva `use="literal"` binding — dovoljena sta **rpc/literal** ali **document/literal**.

**Orodja za validacijo vmesnikov:** razvojna orodja, **SoapUI**.

> 🔑 **Enostavna analogija:** profil je kot "seznam kompatibilnih delov" — če vsi uporabijo iste standarde iste verzije, se sistemi ujamejo kot lego kocke.

---

## 3. Odjemalci SOAP storitev

**Kaj pomeni "prožiti" storitev SOAP?** Generirani razredi/vmesniki (iz WSDL) skrivajo (abstrahirajo) 3 korake:
1. **Oblikovanje zahteve SOAP** — serializacija objektov v XML in v SOAP ovojnico.
2. **Pošiljanje zahteve** — prek HTTP/HTTPS.
3. **Procesiranje odgovora** — deserializacija XML nazaj v objekte.

### 3a. Java odjemalec (JAX-WS, `wsimport` prek `jaxws-maven-plugin`)
- Plugin dobi URL do WSDL in generira odjemalski proxy.
- `mvn clean generate-sources` → generira vmesnik (npr. `DavcnaBlagajna`) z operacijami.

**Sinhroni odjemalec** (nit se blokira do odgovora):
```java
DavcnaBlagajnaServiceService service = new DavcnaBlagajnaServiceService(); // proxy
DavcnaBlagajna port = service.getDavcnaBlagajnaServicePort();               // vmesnik
Racun racun = new Racun(); racun.setZnesek(100.0); ...
Racun rezultat = port.novRacun(racun);  // BLOKIRA dokler ni odgovora
```

**Asinhroni odjemalec:** v `src/jaxws/async-bindings.xml` vklopimo `<enableAsyncMapping>true`. Za vsako operacijo dobimo **3 načine**:
- **sinhrono** — `Racun novRacun(racun)`
- **async polling** — `Response<T> novRacunAsync(racun)` → sami preverjamo `isDone()`
- **async callback** — `Future<?> novRacunAsync(racun, AsyncHandler<T>)` → ogrodje pokliče `handleResponse()`

```java
// POLLING: sami sprašujemo, ali je gotovo
Response<NovRacunResponse> odg = port.novRacunAsync(racun);
while(!odg.isDone()) { Thread.sleep(100); }   // periodično preverjanje
odg.get().getReturn().getId();

// CALLBACK: ogrodje nas obvesti
AsyncHandler<NovRacunResponse> handler = response -> {
    Racun r = response.get().getReturn();  // se pokliče ko rezultat prispe
};
Future<?> f = port.novRacunAsync(racun, handler);
```

> 💡 **Polling vs Callback:** Polling = ti vsakih 5 min pogledaš v nabiralnik, ali je prišel paket. Callback = poštar pozvoni, ko ga prinese. Callback je učinkovitejši.

### 3b. .NET odjemalec (`dotnet-svcutil`)
- `dotnet-svcutil <wsdl-url>` generira `Reference.cs` (proxy razred + tipi).
- Moderni .NET (8+) **privzeto generira async API** z `Task<T>` + `async/await` (Task-based Asynchronous Pattern, TAP).
```csharp
var client = new DavcnaBlagajnaClient();
NovRacunResponse response = await client.NovRacunAsync(racun);  // await
Racun rezultat = response.@return;
```

### 3c. JavaScript odjemalec
SOAP = XML prek HTTP. V JS **ni generatorjev**, zato dve možnosti:

**Nizkonivojsko (fetch)** — ročno sestavimo SOAP envelope in ga pošljemo:
```javascript
const response = await fetch(url, {
  method: "POST",
  headers: { "Content-Type": "text/xml;charset=utf-8" },
  body: soapEnvelope  // ročno napisan XML
});
```

**Z modulom `soap`** (`npm install soap`) — prebere WSDL in ponudi JS metode:
```javascript
// callback stil
soap.createClient(wsdl, (err, client) => {
  client.NovRacun(args, (err, odg) => console.log(odg.return.id));
});
// await stil
const client = await soap.createClientAsync(wsdl);
const [result] = await client.NovRacunAsync(args);
```
Modul `soap` podpira: RPC/dokumentno sporočanje, sync/async, WS-Security.

**Primerjava treh svetov:**
| | Java | .NET | JavaScript |
|---|---|---|---|
| Generator | wsimport (jaxws-maven-plugin) | dotnet-svcutil | **ni ga** |
| Odjemalec | močno tipiziran, sync+async | močno tipiziran, privzeto async (`Task`) | ročno (fetch) ali modul `soap` |

---

## 4. Storitveno vodilo — ESB (Enterprise Service Bus)

**ESB** = vmesni sloj (middleware) med poslovnimi aplikacijami, ki zagotavlja interoperabilnost med aplikacijami z **različnimi protokoli**.

- Je **arhitektura** (množica pravil/principov integracije prek "vodila").
- **Osnovni namen:** integracija različnih aplikacij prek **skupnega komunikacijskega vodila**.
- Zagotavlja **šibko sklopljenost** — aplikacije komunicirajo prek vodila, brez neposrednih odvisnosti in brez vedenja druga o drugi.
- Omogoča: usmerjanje, preoblikovanje in obogatitev sporočil, pretvorbo protokolov (npr. HTTP↔JMS).

### Zakaj ESB? Problem point-to-point
- **Point-to-point:** vsaka integracija = ločena povezava med dvema sistemoma.
- Sčasoma nastanejo **"špageti" rešitve** — visoka medsebojna odvisnost, zamenjava sistema je skoraj nemogoča, skaliranje je drago in počasno.

```
POINT-TO-POINT (kaos):        SKUPNO VODILO (red):
 A---B                          A   B   C
 |\ /|                          |   |   |
 | X |                        ==+===+===+==  (ESB vodilo)
 |/ \|                          |   |   |
 C---D                          D   E   F
 (N² povezav)                   (vsak se poveže le na vodilo)
```

### Prednosti ESB
- Večja **agilnost** organizacije — ponovna uporaba obstoječih sistemov.
- Zmanjša verjetnost **SOA anti-vzorcev** (tesno sklopljene storitve, ad-hoc integracije, podvajanje logike).
- **Kanonični format sporočil**: en standardiziran format (XML/JSON) po vodilu → vsaka aplikacija govori z vsako. ESB po potrebi transformira iz/na kanonični format.

### ESB in SOA — pomembno!
- ESB **sam po sebi NE implementira SOA**! Le zagotavlja lastnosti, ki SOA omogočajo.
- ESB ni nujno vezan na spletne storitve (lahko REST, JMS ...).
- Mora: temeljiti na odprtih standardih, biti prilagodljiv/razširljiv, omogočati vzorce SOA.

### Zmogljivosti ESB (v kontekstu SOA)
- **Povezljivost/adapterji** — HTTP(SOAP/REST), FTP, SFTP, JMS ...
- **Transformacija** — XSLT, XPath/XQuery, skriptni jeziki (JS, Groovy).
- **Inteligentno usmerjanje** — content-based & rule-based routing.
- **API po meri** — lastni adapterji/komponente.
- **Koreografija/orkestracija** delovnih tokov (BPM).
- **Upravljanje** (deployment, verzije, logging, monitoring), **prožilci** (event-driven), **varnost** (avtentikacija, avtorizacija, šifriranje).

### Produkti ESB
Apache Synapse, ServiceMix, **Mule ESB**, JBoss ESB, **WSO2 ESB**, Oracle Service Bus, TIBCO, MS BizTalk, Red Hat Fuse, Dell Boomi, Talend ESB ...

**WSO2 ESB** — vse mehanizme ESB (usmerjanje, load-balancing, fail-over, throttling, preklapljanje protokolov, transformacije), podpira EDA, deklarativni razvoj s konfiguracijo (namesto kodiranja).
- **Primer eBay:** WSO2 ESB procesira **>1 milijardo transakcij/dan**; izbrali 100 % odprtokodno rešitev po 6-mesečnem vrednotenju.

---

## 5. Življenjski cikli razvoja SOA rešitev

### Metodologija razvoja IS
"Strukturiran sklop načel, metod, postopkov, standardov in smernic za načrtovanje, razvoj, uvedbo in vzdrževanje IS." Cilj: razvoj naj bo **učinkovit, ponovljiv, v okviru časa/stroškov, izpolni pričakovanja uporabnikov**.

**Zakaj potrebujemo metodologijo?** — raziskave **CHAOS (Standish Group)**:
- CHAOS 2009 (~50.000 projektov): 32 % uspešnih, 44 % "challenged" (zamude/prekoračitve), 24 % neuspešnih.
- CHAOS 2020: 31 % uspešnih, 50 % challenged, 19 % neuspešnih.
- **Agilni projekti so ~3× bolj verjetno uspešni** kot Waterfall; Waterfall ima ~2× večjo verjetnost neuspeha.
- Uspešnost že desetletja ~30 % — **ključni dejavniki so ljudje, proces, organizacija** (ne le tehnologija).

**Modeli razvoja IS:** vodopadni, iterativni, inkrementalni, spiralni, agilni (Scrum, Kanban). V praksi se kombinirajo.

### Pristopi k razvoju SOA
Tri splošne strategije:

| Pristop | Kako | Prednosti | Slabosti |
|---|---|---|---|
| **BOTTOM-UP** | obstoječe aplikacije "ovijemo" (wrapping) v storitve | ponovna uporaba, hiter začetek, nižji začetni stroški | arhitektura ostane nespremenjena, ni prave storitvene naravnanosti, ni centraliziranega načrtovanja → višji stroški vzdrževanja |
| **TOP-DOWN** | iz poslovnih ciljev/procesov izpeljemo storitve, nato tehnična realizacija | konsistentnost, standardizacija, strateška usklajenost, kakovostna SOA | visoki začetni stroški, dolga pot do rezultatov, manj takojšnjih koristi |
| **AGILNI (middle-out)** | kombinacija; iterativno, sproti upošteva povratne informacije | prilagodljivost, hitra vidnost rezultatov, boljša komunikacija | nevarnost izgube širše slike, kompleksnost, tveganje "nikoli končanega" projekta |

> 💡 **Analogija:** Bottom-up = obstoječe sobe hitro povežeš z vrati (hitro, a nered). Top-down = najprej narišeš celoten načrt hiše (počasno, a lepo). Agilno = gradiš sobo za sobo po načrtu, ki ga sproti popravljaš.

### Osnovne faze življenjskega cikla SOA
`Storitveno-naravnana analiza → Modeliranje storitev → Storitveno-naravnano načrtovanje → Razvoj storitev → Testiranje storitev → Nameščanje storitev` → nato **Upravljanje storitev**.

### Storitveno-naravnana analiza
Začetna faza — določi cilje (vizijo), nivoje storitev, inventar. **Ključni vprašanji:**
- **KATERE storitve** moramo zgraditi?
- **KATERI del logike** mora biti v posamezni storitvi?

Cilji: definicija kandidatnih operacij, grupiranje v kandidatne storitve, identifikacija ponovno uporabnih storitev, modeli kompozicij.

**Kandidatne storitve** = abstraktne definicije storitev (na logičnem nivoju). Analiza pripravi predlog (vhod v načrtovanje), **še ne gradi**.

### Pojmi: zmožnost : operacija : metoda
- **Zmožnost (capability)** = abstraktna funkcija storitve (dokler ne vemo, kako bo zgrajena).
- **Operacija** = zmožnost implementirana kot spletna storitev.
- **Metoda** = zmožnost implementirana kot komponenta.
> Izraz "zmožnost" loči **abstraktni pojem** storitve od njene **implementacije**.

### Modeli (tipi) storitev
Storitve delimo po tipu logike, ponovni uporabi in vezanosti na domeno:

| Model | Kaj | Ponovna uporaba | Primer |
|---|---|---|---|
| **Entitetne** (entity) | vezane na poslovne objekte (stranka, izdelek, naročilo); CRUD | **visoka** | `Zaposleni`: GetProfil, UpdateProfil, GetZgodovina ... |
| **Poslovne / opravilne** (task) | izvajajo konkreten poslovni proces/nalogo | **najnižja** | `Naročilo`: Pošlji (sproži poslovni proces); pogosto kontrolnik kompozicije |
| **Podporne** (utility) | splošne funkcionalnosti, neodvisne od poslovanja | **visoka** | `Transformacija`: APImport, APExport |

Znotraj inventarja se organizirajo v **nivoje**: nivo poslovnih/opravilnih → nivo entitetnih → nivo podpornih storitev.

### Agnostične vs ne-agnostične storitve
- **Agnostičen** (grško "brez znanja") = logika **ni vezana** na določeno nalogo → **večnamenska, ponovno uporabna** v več procesih.
- **Ne-agnostičen** = logika vezana na specifično nalogo (ima znanje o njej).
- Cilj storitvene naravnanosti: večina storitev naj bo **funkcijsko agnostičnih** (univerzalnih).

### Inventar storitev
- **Neodvisno standardizirana in upravljana množica komplementarnih storitev** znotraj meje podjetja.
- Najboljša praksa: vse storitve dostopne prek istega inventarja (v velikih okoljih → domenski inventarji).
- **Normaliziran inventar** = storitve se ne prekrivajo (vsaka v svojih mejah). Prekrivanje = **ne-normaliziran** → cilj je **normalizacija** (izogibanje podvajanju).

**Upravljanje inventarja glede na pristop:**
- **Top-down** → višji začetni stroški, a **nižji stroški upravljanja** kasneje.
- **Bottom-up** → nižji začetek, a **višji stroški upravljanja** (manj upoštevane storitvene naravnanosti).

### Storitveno-naravnano načrtovanje
Nadaljuje se, kjer se je analiza zaključila. Vhod = kandidatne storitve. Za vsak model storitve poseben proces: načrtovanje entitetnih → podpornih (utility) → poslovnih → storitev orkestracije.

---

## 6. Tipi storitveno usmerjenih arhitektur

Štirje nivoji (vsak ima svoj doseg), od najožjega k najširšemu:

1. **Arhitektura storitve** — notranja zgradba **ene** storitve (kako je implementirana).
   - Primerljiva s komponento; storitev ima jasen vmesnik + notranjo zgradbo (lahko več komponent/virov).
   - Zahteve (posebej za agnostične): **neodvisne, samo-zadostne, samo-vsebujoče**, z jasnimi vmesniki in dogovorjenimi formati. Vsebuje: osnovno logiko + procesiranje glave, avtentikacijo, (de)šifriranje, validacijo, pretvorbo ...

2. **Arhitektura kompozicije storitev** — kako **več storitev** povežemo v večje rešitve (orkestracije, delovni tokovi, kompozitne storitve). Primerljiva z integracijsko arhitekturo (npr. ovijanje legacy sistemov).

3. **Arhitektura inventarja storitev** — celovit nabor **vseh** storitev v okolju/podjetju: kategorije, domene, pravila poimenovanja/verzioniranja/ponovne uporabe. Cilj: urejen inventar, ne ad-hoc rešitve.

4. **Storitveno-naravnana poslovna arhitektura** — **najvišji** nivo; poslovne zmožnosti, procesi in organizacijske enote opisani kot storitve. Določa okvirje/pravila, ki se prenašajo navzdol na vse ostale arhitekture.

```
┌─ Storitveno-naravnana POSLOVNA arhitektura ─────────┐  najširše
│  ┌─ Arhitektura INVENTARJA storitev ─────────────┐  │
│  │  ┌─ Arhitektura KOMPOZICIJE storitev ──────┐  │  │
│  │  │  ┌─ Arhitektura STORITVE ────────────┐  │  │  │  najožje
│  │  │  │  (ena storitev)                   │  │  │  │
│  │  │  └───────────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

---

## Ključni povzetek predavanja 9
- **Contract-First v JS**: WSDL + implementacija ročno; modul `soap` naredi objekt strukture Service→Port→Operacija.
- **Interoperabilnost**: dosežemo z upoštevanjem specifikacij; **WS-I Basic Profile** predpisuje kombinacijo standardov (document/literal ali rpc/literal).
- **Odjemalci**: Java/.NET imata generatorje (sync + async: polling/callback/Task), JS nima → fetch ali modul `soap`.
- **ESB**: skupno vodilo namesto point-to-point špagetov; šibka sklopljenost, kanonični format; **ne implementira SOA, ampak jo omogoča**.
- **Življenjski cikel**: pristopi bottom-up / top-down / agilno; faze analiza→...→upravljanje.
- **Pojmi**: zmožnost/operacija/metoda; entitetne/poslovne/podporne storitve; agnostičnost; normaliziran inventar.
- **4 tipi arhitektur**: storitev → kompozicija → inventar → poslovna (od ozkega k širokemu).
