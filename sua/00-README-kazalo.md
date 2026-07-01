# Zapiski — Storitveno usmerjene arhitekture (SUA)

Podrobni zapiski predavanj **09–18**, izdelani iz PDF gradiva. Vsaka datoteka vsebuje povzetke, tabele in razlage težjih konceptov z enostavnimi primeri (označeni z 💡).

## Kazalo

| # | Datoteka | Vsebina na kratko |
|---|---|---|
| 09 | [JS/SOAP, interoperabilnost, odjemalci, ESB, življenjski cikli](09-JS-SOAP-interoperabilnost-odjemalci-ESB-zivljenjski-cikli.md) | Contract-First v JS; WS-I profili; sinhroni/asinhroni odjemalci (Java/.NET/JS); ESB; pristopi razvoja SOA (bottom-up/top-down/agilno); modeli storitev; 4 tipi arhitektur |
| 10 | [Strateški cilji SOA, Manifesto, vzorci, REST](10-strateski-cilji-SOA-manifesto-vzorci-REST.md) | 7 strateških ciljev; SOA Manifesto (vrednote/načela); katalog vzorcev SOA; **REST** (5 principov, HTTP metode, caching, antivzorci); SOAP vs REST; SOA z REST |
| 11 | [Razvoj REST (Java/.NET/JS) + opis vmesnikov](11-razvoj-REST-Java-NET-JavaScript-opis-vmesnikov.md) | Ista CRUD storitev v JAX-RS, Spring Boot, ASP.NET Core (+Minimal API), Express+Mongoose; WADL/RSDL/JSDL/SSDL/USDL/WSDL 2.0 |
| 12 | [Mikrostoritvena arhitektura + SOA vs mikrostoritve](12-mikrostoritvena-arhitektura-karakteristike-SOA-vs-mikrostoritve.md) | Monolit vs mikrostoritve; 9 karakteristik (Fowler/Lewis); prednosti/izzivi; SOA vs mikrostoritve |
| 13 | [Izzivi in vzorci: dekompozicija, nameščanje, komunikacija, API Gateway, odkrivanje](13-izzivi-vzorci-mikrostoritve-dekompozicija-namescanje-komunikacija-APIgateway-odkrivanje.md) | Dekompozicija; strategije nameščanja (zabojniki/serverless); RPC vs sporočanje; API Gateway; Circuit Breaker; service discovery/registry; database per service; EDA za konsistentnost |
| 14 | [Napredni vzorci: Outbox, Log Tailing, Event Sourcing, CQRS, Saga](14-transaction-log-tailing-domenski-dogodki-event-sourcing-CQRS-saga.md) | Problem dual write; Transactional Outbox; CDC/Log Tailing; Event Sourcing; CQRS; Saga (orkestracija/koreografija) |
| 15 | [Komunikacijski protokoli in tehnologije API](15-komunikacijski-protokoli-tehnologije-API.md) | Evolucija: RPC/ORB, ONC RPC, CORBA, DCE RPC, DCOM, XML-RPC, EJB, REST, SOAP, OData, GraphQL, gRPC, RSocket (primerjava) |
| 16 | [Razvoj storitev na osnovi gRPC](16-razvoj-storitev-gRPC.md) | gRPC + Protocol Buffers; contract-first; 4 modeli komunikacije; razvoj strežnika/odjemalca (sinhroni/asinhroni) v Javi |
| 17 | [Razvoj storitev na osnovi GraphQL](17-razvoj-storitev-GraphQL.md) | GraphQL vs REST (over/under-fetching); shema (Query/Mutation/Subscription); razvoj v Spring for GraphQL + JPA |
| 18 | [Dogodkovno vodena arhitektura + Cloud-native](18-dogodkovno-vodena-arhitektura-cloud-native.md) | EDA (dogodki, komponente, Pub/Sub, vrste); EDA vs EDP; oblak (NIST, SaaS/PaaS/IaaS); cloud-native načela |

## Rdeča nit predmeta

```
SOA temelji (SOAP, WSDL, Contract-First)  ── pred. 9
      │
      ├─ Strateški cilji + Manifesto + vzorci ── pred. 10
      │
      ├─ REST kot alternativa SOAP ──────────── pred. 10–11
      │
      ▼
Mikrostoritve (evolucija SOA) ─────────────── pred. 12
      │
      ├─ Vzorci: dekompozicija, nameščanje,
      │  komunikacija, API Gateway, odkrivanje ─ pred. 13
      │
      ├─ Podatki: Outbox, Event Sourcing,
      │  CQRS, Saga (eventual consistency) ───── pred. 14
      │
      ▼
Komunikacijske tehnologije ────────────────── pred. 15
      ├─ gRPC ─────────────────────────────── pred. 16
      └─ GraphQL ──────────────────────────── pred. 17
      │
      ▼
EDA + Cloud-native (celovita slika) ────────── pred. 18
```

## Ključni pojmi skozi predmet
- **Šibka sklopljenost** — rdeča nit vseh arhitektur (SOA, REST, mikrostoritve, EDA).
- **Interoperabilnost** — cilj SOA; WS-I profili, standardni vmesniki.
- **Contract-first** — pogodba pred implementacijo (WSDL, .proto, GraphQL shema, OpenAPI).
- **Idempotentnost** — ključna za robustnost porazdeljenih sistemov (retry, Saga, dogodki).
- **Eventual consistency** — konsistentnost brez 2PC (database per service → EDA, Saga, CQRS).
- **Orkestracija vs koreografija** — centralni dirigent vs samostojne storitve na dogodke.
