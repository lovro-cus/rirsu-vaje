# Predavanje 15 — Komunikacijski protokoli in tehnologije za razvoj storitev in API-jev

> **O čem je predavanje:** zgodovinski pregled in primerjava **tehnologij za oddaljeno komunikacijo/API-je** — od zgodnjih RPC (ONC RPC, CORBA, DCE RPC, DCOM), prek XML-RPC in EJB, do modernih (REST, SOAP, OData, GraphQL, gRPC, RSocket). Za vsako: **namen, filozofija, jezik za opis vmesnika (IDL), format sporočil, prenosni protokol, prva izdaja**. Vsi primeri uporabljajo isto storitev `TrafficService`.

---

## 1. Zakaj so pomembni

- **Povezovanje aplikacij** v heterogenih okoljih (brez njih ni interoperabilnosti).
- **Temelj porazdeljenih sistemov** (mikrostoritve, IoT, oblak).
- **API-ji** = način, kako aplikacije izmenjujejo podatke in ponujajo storitve.

Koncept API-jev obstaja od začetka porazdeljenega računalništva (prvi protokoli zahteva-odgovor že v 1960-ih; RPC tehnologije v zgodnjih 1980-ih).

---

## 2. Temeljni koncepti

### RPC (Remote Procedure Call)
- Oblika interakcije odjemalec-strežnik prek **zahteva-odgovor**.
- Program sproži proceduro **na drugem računalniku** enako, kot bi klical lokalno proceduro.
- Vmesna povezovalna oprema (proxy/stub) **skrije podrobnosti** komunikacije.
- **Prednosti:** abstrakcija kompleksnosti, transparentnost, ponovna uporaba.
- **Slabosti:** odvisnost od omrežja, potreba po **dosegljivosti** obeh strani, latenca, napake v omrežju.

### ORB (Object Request Broker)
- Middleware za komunikacijo med **porazdeljenimi objekti/komponentami** (objektno-orientiran, običajno **sinhron**).
- Neodvisnost od lokacije, jezika, protokola, OS.
- **Prednosti:** abstrakcija, interoperabilnost, skalabilnost.
- **Slabosti:** latenca (sinhrona narava), kompleksnost (CORBA), odvisnost od standardov.

---

## 3. Pregled tehnologij (kronološko)

| Tehnologija | Leto | IDL (opis vmesnika) | Payload | Prenos | Namen/filozofija |
|---|---|---|---|---|---|
| **ONC RPC** (Sun) | 1984 | RPC IDL | XDR (binarno) | UDP/TCP | RPC v heterogenih omrežjih (temelj NFS) |
| **CORBA** (OMG) | 1991 | IDL (→ jeziki) | IIOP (binarno) | TCP/IP | porazdeljeni **objekti**, večjezičnost |
| **DCE RPC** (OSF) | 1993 | IDL (C-sintaksa) | binarni tokovi | TCP/IP, UDP | RPC, temelj MS DCOM |
| **DCOM** (Microsoft) | 1996 | MIDL (+ACF) | serializ. DCOM objekti | TCP/IP, NetBIOS, HTTP | konkurenca CORBA na Windows |
| **XML-RPC** | 1998 | (ni; vse v XML) | XML | HTTP | RPC v XML prek HTTP |
| **EJB** (Java) | 1998 | Java IDL/Remote | Java objekti (DTO), pozneje XML/JSON | Java RMI, HTTP | poslovna logika, transakcije, varnost |
| **REST** (Fielding) | 2000 | ni (pozneje OpenAPI/RAML) | JSON (XML ...) | HTTP (+drugi) | arhitekturni stil, viri |
| **SOAP/WSDL** | 2003 | WSDL | XML (SOAP) | HTTP | W3C spletne storitve |
| **OData** (MS→OASIS) | 2007/2012 | CSDL (XML/JSON) | JSON (XML) | HTTP | standardiziran CRUD dostop do podatkov (REST) |
| **gRPC** (Google) | 2015 | Protocol Buffers | Protobuf (binarno, opc. JSON) | HTTP/2 | visoko zmogljiv RPC, streaming |
| **GraphQL** (Facebook) | 2012/2015 | GraphQL SDL | JSON | HTTP (+WebSocket) | poizvedbeni jezik, natančni podatki |
| **RSocket** (Netflix) | ~2015 | odvisno (npr. Protobuf) | ločeni metapodatki+podatki | TCP/WebSocket/Aeron/HTTP/2 | reaktivni binarni protokol, streaming |

---

## 4. Podrobnosti ključnih tehnologij

### ONC RPC IDL — elementi
- `program` (celoten vmesnik), `version` (verzije), `struct` (podatkovne strukture z omejitvami dolžine `string SensorName<128>`), funkcije z **unikatnim ID** (`= 1`).

### CORBA IDL — elementi
- `module` (logični sklop imen), `struct` (kompleksni tipi), `interface` (operacije z `in`/`out` parametri), podatkovni tipi (`string`, `short`, `long`, `sequence` ...).

### DCE RPC IDL — elementi
- `interface` + **UUID** (edinstvenost), `typedef struct` (C-sintaksa), `error_status_t` (povratne kode), atributi `[in]`/`[out]`/`[string]`, `version`.

### DCOM (MIDL) — elementi
- `library`, `import` (oaidl.idl, ocidl.idl), `interface : IUnknown` (osnovni COM vmesnik), `HRESULT` (povratna vrednost), `[in]`/`[out, retval]`, `coclass` (razred, ki implementira vmesnik), tip `BSTR` (OLE unicode string).

### EJB — gradniki
- **Oddaljeni vmesnik** (`extends Remote`, metode mečejo `RemoteException`), **implementacija** (`@Stateless` bean s poslovno logiko), **JNDI** (iskanje komponent), **EJB container** (transakcije, varnost, viri).

### OData (CSDL) — elementi
- `<edmx:Edmx>` (koren), `<Schema>` (Namespace), `<EntityType>` (entiteta z `<Key>` in `<Property>` tipi `Edm.String` ...), `<EntityContainer>`/`<EntitySet>` (zbirke). Standardiziran CRUD nad podatki v REST slogu.

### GraphQL (SDL) — elementi
- `schema` (query/mutation), `type` (entitete s polji), `Query` (poizvedbe), `Mutation` (spreminjanje), **non-nullable** tipi (`String!` = obvezno). En endpoint, klient zahteva **točno določene podatke**.
```graphql
type Query {
  getTrafficSensors: [TrafficSensor]
  getTrafficFlow(trafficId: String!, dateFrom: String!, dateTo: String!): TrafficFlow
}
type Mutation {
  activateTrafficSensor(sensorName: String!, ...): TrafficSensorActivationResponse
}
```

### gRPC (Protocol Buffers) — elementi
- `syntax = "proto3"`, `package`, `service` (z `rpc` metodami), `message` (strukture s **oštevilčenimi polji** `= 1` za učinkovito serializacijo). Generira kodo za odjemalca/strežnik v več jezikih; teče na **HTTP/2** (dvosmerno, streaming, nizka latenca).
```proto
service TrafficService {
  rpc TrafficSensorActivation (TrafficSensorActivationRequest) returns (TrafficSensorActivationResponse);
}
message TrafficSensorActivationRequest {
  string sensor_name = 1;
  string sensor_type = 2;
}
```

### RSocket — ključne funkcionalnosti
- **Reaktivni model** (async, streams), nizka latenca, **komunikacijski vzorci**: Request/Response, Fire-and-Forget, Streaming (eno/dvosmerni). Deluje na več prenosih (TCP, WebSocket, Aeron, HTTP/2). Cilj: zamenjati neučinkovit HTTP pri visoki prepustnosti/dvosmerni komunikaciji. Loči metapodatke od vsebine.

---

## 5. Filozofije (opis iz tabele)

- **CORBA** = "Porazdeljeni objekti" (objektni).
- **SOAP** = "RPC" (stroga standardizacija, visoka interoperabilnost, platformna neodvisnost).
- **EJB** = "Komponentno orientiran".
- **XML-RPC** = "RPC na XML" (enostaven, predhodnik SOAP).
- **REST** = "RESTful API" (enostavnost, nizka sklopljenost, razširljivost).
- **OData** = "REST na steroidih" (podpora poizvedbam, bogati metapodatki).
- **gRPC** = "RPC na HTTP/2" (hitrost, dvosmerno pretakanje, večjezičnost).
- **RSocket** = "Dvosmerni protokol" (optimiziran za streaming, minimalna poraba virov).
- **GraphQL** = "Poizvedbe nad podatki" (natančne poizvedbe, introspekcija, **en endpoint**).

---

## 6. Kako se tehnologije ujemajo s principi SOA?

Predavanje postavi vprašanje (brez fiksnih odgovorov): katere tehnologije podpirajo principe SOA — **standardizacija pogodb, šibka sklopljenost, abstrakcija, ponovna uporaba, avtonomnost, brez stanja, odkrivanje, kompozicija**?

> 💡 Grobo: **SOAP/WSDL** ima najbolj formalne pogodbe in standardizirano odkrivanje (UDDI); **REST** je šibko sklopljen, brez stanja; **gRPC** ima stroge pogodbe (Protobuf), a je bolj sklopljen; **GraphQL** daje odjemalcu prilagodljivost poizvedb (en endpoint). Nobena tehnologija ni "najboljša" — izbira je odvisna od zahtev (kot pri SOAP vs REST, pred. 10).

---

## Ključni povzetek predavanja 15
- **Evolucija:** RPC (ONC/DCE) → objekti (CORBA/DCOM) → XML (XML-RPC, SOAP) → EJB → REST → moderni (OData, GraphQL, gRPC, RSocket).
- **Vsaka tehnologija ima:** IDL (opis vmesnika), payload format, prenosni protokol.
- **Zgodnje (CORBA/DCOM/DCE)**: binarni, sinhroni, objektni, kompleksni, platformno vezani (DCOM=Windows).
- **XML doba (XML-RPC/SOAP)**: berljiv XML prek HTTP, stroga standardizacija.
- **REST**: arhitekturni stil (ne protokol), JSON, brez enotnega IDL (→ OpenAPI).
- **Moderni:**
  - **OData** = standardiziran CRUD/poizvedbe nad podatki v REST slogu (CSDL).
  - **GraphQL** = odjemalec zahteva točno določene podatke, en endpoint (SDL, query/mutation/subscription).
  - **gRPC** = zmogljiv RPC prek HTTP/2 + Protobuf, streaming, večjezičnost.
  - **RSocket** = reaktivni binarni protokol, več prenosov, streaming.
- **Ni univerzalne izbire** — odvisno od zahtev (zmogljivost, interoperabilnost, prilagodljivost, streaming).
