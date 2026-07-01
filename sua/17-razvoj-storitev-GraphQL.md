# Predavanje 17 — Razvoj storitev na osnovi GraphQL

> **O čem je predavanje:** kaj je **GraphQL**, zakaj rešuje težave REST-a (**over-fetching / under-fetching**, več klicev), kaj je **shema** (Query/Mutation/Subscription), kako izgledajo poizvedbe in mutacije, ter praktičen razvoj GraphQL API-ja v **Javi + Spring for GraphQL + JPA**.

---

## 1. Kaj je GraphQL

- Razvil **Facebook** (interno 2012, javno 2015 na React.js Conf), odprtokoden.
- **Osnovna ideja:** pridobivanje podatkov na osnovi **deklarativne poizvedbe** v času izvajanja.
  - **Odjemalec določi, katere podatke potrebuje**; strežnik je odgovoren, da jih zagotovi točno skladno s poizvedbo.
- **GraphQL API = ena končna točka** (en URL), ki odjemalcem zagotovi točno tiste podatke, ki jih zahtevajo.
  - V REST/SOAP: **več končnih točk** z vnaprej določenimi (fiksnimi) strukturami → tesna sklopljenost storitve z odjemalci.

> ⚠️ **Pomembno:** GraphQL je **povpraševalni jezik za API-je, NE za podatkovne baze/podatke!** Je **PB-agnostičen** — deluje s katerimkoli mehanizmom za upravljanje podatkov.

---

## 2. Problem REST-a, ki ga GraphQL rešuje

**Primer:** podatki o študentu, njegovih predmetih in ocenah.

**REST — 3 ločene zahteve:**
```
GET /student/{id}            → osnovni podatki
GET /student/{id}/predmeti   → seznam predmetov
GET /student/{id}/ocene      → ocene
```
Težave REST-a:
- **več klicev** (N+1 problem),
- **over-fetching** (dobiš več polj, kot rabiš),
- **under-fetching** (moraš narediti dodatne klice).

**GraphQL — ena poizvedba dobi vse:**
```graphql
query {
  student(id: "re233...") {
    vpisnaStevilka
    ime
    priimek
    predmeti { naziv semester ECTS }   # gnezdeno
    ocene    { naziv datum ocena }     # gnezdeno
  }
}
```
Odgovor (JSON) je **skladen s strukturo poizvedbe** — samo zahtevana polja, v enem klicu (HTTP POST).

---

## 3. GraphQL shema (Schema)

- **Definira zmožnosti API-ja** — kako lahko odjemalec bere/spreminja podatke.
- Je **pogodba** med odjemalcem in strežnikom (kot **WSDL** za SOAP, **.proto** za gRPC).
- Je zbirka **GraphQL tipov**, definiranih s posebnimi **korenskimi tipi**:
  - **`type Query { ... }`** — bralne operacije (vstopna točka za branje),
  - **`type Mutation { ... }`** — pisalne operacije (ustvarjanje/posodabljanje/brisanje),
  - **`type Subscription { ... }`** — naročnine (realnočasovna obvestila prek WebSocket).

**Primer sheme:**
```graphql
type Query {
  getStudent(id: ID!): Student
  vsiPredmeti(id: ID!): [Predmet!]!
  vseOcene(id: ID!): [Ocena!]!
}
type Mutation {
  createStudent(ime: String!, priimek: String!, smer: String!): Student!
  updateStudent(id: ID!, ime: String!, ...): Student!
  deleteStudent(id: ID!): Student!
}
type Student {
  id: ID!
  vpisnaStevilka: String!
  ime: String!
  predmeti: [Predmet!]!
  ocene: [Ocena]
}
type Predmet { id: ID! naziv: String! semester: String! ects: Int! }
type Ocena  { id: ID! naziv: String! ocena: Float! datum: String! student: Student! }
```
> **`!`** = obvezno (non-nullable). **`[Predmet!]!`** = obvezen seznam obveznih Predmetov.

---

## 4. Operacije

### Query (branje)
Odjemalec izbere polja; dodajanje polj = več podatkov v odgovoru:
```graphql
query { vsiStudenti { ime priimek } }           # samo ime+priimek
query { vsiStudenti { ime priimek email smer } } # + email+smer
```

**Gnezdenje poizvedb** (glavna izrazna moč) — sledi strukturi tipov:
```graphql
query {
  vsiStudenti {
    ime priimek
    ocene { naziv datum ocena }   # strežnik razčleni in doda ocene vsakemu študentu
  }
}
```

### Mutation (pisanje)
Tri oblike: **ustvarjanje, posodobitev, brisanje**. Sintaksa enaka kot pri branju; mutacija vrne izbrana polja rezultata:
```graphql
mutation {
  createStudent(ime: "Janko", priimek: "Slak", smer: "ITK") {
    id ime priimek smer   # katere podatke želimo nazaj
  }
}
```

---

## 5. Praktičen primer: Java + Spring for GraphQL + JPA

### Knjižnice
- **GraphQL Java** (graphql-java.com) = jedro (GraphQL Java Engine za izvajanje poizvedb), a **ne** procesira HTTP/JSON.
- **Spring for GraphQL** = izpostavi API prek HTTP (integracija s Spring). Odvisnosti: web, **graphql**, websocket, data-jpa, h2, devtools.

### Nastavitve (application.properties)
```properties
spring.graphql.graphiql.enabled=true          # GraphiQL UI na /graphiql
spring.graphql.schema.printer.enabled=true     # shema na /graphql/schema
spring.graphql.websocket.path=/graphql         # WebSocket za subscriptions
spring.datasource.url=jdbc:h2:mem:studb        # H2 in-memory baza
```

### Shema
V **`src/main/resources/graphql/schema.graphqls`** (Spring privzeto išče v `classpath:graphql/**`).

### Entitete + repozitoriji (JPA)
- `StudentEntity`, `PredmetEntity`, `OcenaEntity` (JPA `@Entity`; `OcenaEntity` ima `@ManyToOne` na Student).
- Repozitoriji razširijo `JpaRepository`; `OcenaRepository` doda `findByStudent_Id(Long)`.

### GraphQL kontroler (anotacije)
Razred z **`@Controller`** prestreza GraphQL zahteve. Anotacije:
- **`@QueryMapping`** — metoda postane operacija v `Query`,
- **`@MutationMapping`** — metoda postane operacija v `Mutation`,
- **`@SubscriptionMapping`** — operacija v `Subscription`,
- **`@SchemaMapping`** — poveže metodo s poljem v shemi,
- **`@Argument`** — veže argument iz poizvedbe na parameter metode.

```java
@Controller
public class StudentGraphqlController {
    private final StudentRepository studentRepo;
    // ... konstruktor (DI) ...

    @QueryMapping
    public StudentEntity getStudent(@Argument String id) {
        return studentRepo.findById(Long.parseLong(id)).orElse(null);
    }
    @QueryMapping
    public List<OcenaEntity> vseOcene(@Argument String id) {
        return ocenaRepo.findByStudent_Id(Long.parseLong(id));
    }

    @MutationMapping
    public StudentEntity createStudent(@Argument String ime, @Argument String priimek, @Argument String smer) {
        String vpisna = "V" + System.currentTimeMillis();
        String email = (ime + "." + priimek).toLowerCase() + "@example.com";
        return studentRepo.save(new StudentEntity(vpisna, ime, priimek, email, smer));
    }
    @MutationMapping
    public StudentEntity deleteStudent(@Argument String id) {
        StudentEntity s = studentRepo.findById(Long.parseLong(id)).orElseThrow();
        studentRepo.delete(s);
        return s;
    }
}
```

### Zagon in testiranje
- `./mvnw spring-boot:run`
- **GraphiQL** (interaktivno testiranje): `http://localhost:8080/graphiql`
- H2 konzola: `http://localhost:8080/h2-console`

Primeri:
```graphql
mutation { createStudent(ime:"Ana", priimek:"Novak", smer:"IPT") { id ime email } }
mutation { createOcena(naziv:"SUA", ocena:9.0, datum:"2026-01-12", studentId:"1") { id student { ime } } }
query    { getStudent(id:"1") { ime predmeti { naziv } ocene { naziv ocena } } }
```

---

## 6. Primerjava GraphQL z REST (povzetek)

| | REST | GraphQL |
|---|---|---|
| Končne točke | **več** (fiksne) | **ena** |
| Kaj dobiš | vnaprej določeno (over/under-fetching) | **točno kar zahtevaš** |
| Več virov | več klicev | **en klic** (gnezdenje) |
| Pogodba | OpenAPI (neobvezno) | **shema** (obvezna) |
| Sklopljenost | tesnejša (fiksne strukture) | šibkejša (odjemalec izbira) |
| Operacije | GET/POST/PUT/DELETE | Query / Mutation / Subscription |

> 💡 **Kdaj GraphQL:** ko imajo odjemalci raznolike potrebe po podatkih (npr. mobilna vs spletna aplikacija) in želimo zmanjšati število klicev. Slabosti (niso poudarjene v predavanju): kompleksnejše predpomnjenje (en URL/POST), tveganje predragih poizvedb, N+1 na strežniku.

---

## Ključni povzetek predavanja 17
- **GraphQL** (Facebook, 2015) = povpraševalni jezik za API-je; **odjemalec določi, katere podatke rabi**, strežnik jih vrne točno tako.
- **Ena končna točka** vs več REST točk; rešuje **over/under-fetching** in več klicev prek **gnezdenja**.
- **Shema** = pogodba (kot WSDL/proto); korenski tipi **Query** (branje), **Mutation** (pisanje), **Subscription** (realnočasovno). `!` = obvezno.
- **PB-agnostičen** — ni tehnologija za podatke, ampak za API.
- **Razvoj (Java):** Spring for GraphQL + `schema.graphqls` + JPA entitete/repozitoriji + `@Controller` z `@QueryMapping`/`@MutationMapping`/`@Argument`; testiranje z **GraphiQL**.
