# Predavanje 11 — Razvoj storitev REST (Java: JAX-RS & Spring Boot, .NET: ASP.NET Core, JavaScript: Express+Mongoose) + tehnologije za opis vmesnikov

> **O čem je predavanje:** praktičen razvoj **iste REST storitve** (`racuni`, CRUD) v treh svetovih — **Java** (JAX-RS/Jersey in Spring Boot), **.NET** (ASP.NET Core klasičen Web API in Minimal API) ter **JavaScript** (Node.js + Express + Mongoose). Nato pregled **tehnologij/standardov za opis vmesnikov** (WADL, RSDL, JSDL, SSDL, USDL, WSDL 2.0).

> Vse implementacije izpostavljajo **isti vmesnik**:
> | API | Opis |
> |---|---|
> | `GET /api/racuni` | seznam vseh računov |
> | `GET /api/racuni/{id}` | en račun |
> | `POST /api/racuni` | ustvari nov račun (→ 201 + Location) |
> | `PUT /api/racuni/{id}` | posodobi cel obstoječi račun |
> | `DELETE /api/racuni/{id}` | zbriše račun |

---

## 1. Java — JAX-RS (Jakarta RESTful Web Services)

**JAX-RS** = standardni API za REST storitve v Javi (prej Java EE, danes **Jakarta EE**). Temelji na **anotacijah** v izvorni kodi (opišejo vire, URI-je, HTTP metode, formate).

**Kaj JAX-RS zagotavlja:**
- anotacije za vire (`@Path`, `@GET` ...),
- vezavo URI↔metoda (`/racuni/{id}` → metoda),
- vezavo parametrov (`@PathParam`, `@QueryParam`, `@HeaderParam`, `@FormParam`),
- delo s telesom (MessageBodyReader/Writer — brez ročne (de)serializacije),
- samodejno pretvorbo v JSON/XML (JAXB, Jackson),
- preslikavo izjem v HTTP odzive (`ExceptionMapper`),
- pogajanje o vsebini (`Accept`, `Content-Type`),
- Client API za klicanje.

**Pogoste anotacije:** `@ApplicationPath` (koren), `@Path`, `@GET/@POST/@PUT/@DELETE/@PATCH`, `@Produces` (format odgovora), `@Consumes` (format zahteve), `@PathParam`, `@QueryParam`, `@Context` (dostop do UriInfo).

**Implementacije JAX-RS:** **Jersey** (referenčna, Oracle/Eclipse), **RESTEasy** (JBoss/Red Hat, privzeta v WildFly), Apache CXF, RESTlet. Pogosto že vključen v aplikacijski strežnik (WildFly, Payara, TomEE).

### Primer (Jersey + Grizzly, vgrajen strežnik)
```java
@Path("/api/racuni")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class RacuniResource {
    private static final Map<String, Racun> DATA = new ConcurrentHashMap<>();

    @GET                                          // GET /api/racuni
    public Collection<Racun> getVsiRacuni() { return DATA.values(); }

    @GET @Path("{id}")                            // GET /api/racuni/{id}
    public Response getRacun(@PathParam("id") String id) {
        Racun r = DATA.get(id);
        return (r == null) ? Response.status(NOT_FOUND).build() : Response.ok(r).build();
    }

    @POST                                         // POST /api/racuni
    public Response ustvariRacun(Racun racun, @Context UriInfo uriInfo) {
        String id = UUID.randomUUID().toString();
        racun.setId(id); DATA.put(id, racun);
        URI location = uriInfo.getAbsolutePathBuilder().path(id).build();
        return Response.created(location).entity(racun).build();  // 201 + Location
    }

    @PUT @Path("/{id}")                           // PUT — zamenja cel vir
    public Response updateRacun(@PathParam("id") String id, Racun racun) {
        if (!id.equals(racun.getId())) return Response.status(BAD_REQUEST).build();
        if (DATA.get(id) == null)      return Response.status(NOT_FOUND).build();
        DATA.put(id, racun); return Response.noContent().build();  // 204
    }

    @DELETE @Path("{id}")
    public Response izbrisiRacun(@PathParam("id") String id) {
        return (DATA.remove(id) == null) ? Response.status(NOT_FOUND).build()
                                         : Response.noContent().build();
    }
}
```
Zagon (`Main.java`): `ResourceConfig` registrira vire iz paketa, `GrizzlyHttpServerFactory` požene HTTP strežnik.

---

## 2. Java — Spring Boot

**Spring Boot** = najbolj razširjeno Java ogrodje za REST/spletne aplikacije/**mikrostoritve** (zgrajeno na Spring).

**Glavne značilnosti:**
- **minimalna konfiguracija** ("convention over configuration"),
- **vgrajeni strežnik** (Tomcat/Jetty/Undertow) → `java -jar`, brez zunanjega strežnika,
- **samodejna konfiguracija** + **starter** odvisnosti (JPA, Security ...),
- podpora testiranju (MockMvc, TestRestTemplate),
- zelo primerno za **mikrostoritve** (+ Spring Cloud).

### Primer (Spring Web + Spring Data JPA + H2 + Lombok)
**Entiteta** (Lombok `@Data` generira getterje/setterje):
```java
@Entity @Data @NoArgsConstructor @AllArgsConstructor
public class Racun {
    @Id private String id;
    private String datum, kraj, ppId, davcnaSt;
    private double znesek;
}
```
**Repozitorij** — samo vmesnik, Spring implementira CRUD:
```java
public interface RacunRepository extends JpaRepository<Racun, String> {}
// dobiš: findAll(), findById(id), save(racun), deleteById(id) ...
```
**Kontroler:**
```java
@RestController
@RequestMapping("/api/racuni")
public class RacunController {
    private final RacunRepository repo;   // vstavljen prek konstruktorja (DI)

    @GetMapping                            // GET vsi
    public ResponseEntity<List<Racun>> getAll() {
        var vsi = repo.findAll();
        return vsi.isEmpty() ? ResponseEntity.noContent().build() : ResponseEntity.ok(vsi);
    }
    @GetMapping("/{id}")
    public ResponseEntity<Racun> enRacun(@PathVariable String id) {
        var r = repo.findById(id).orElse(null);
        return (r == null) ? ResponseEntity.notFound().build() : ResponseEntity.ok(r);
    }
    @PostMapping                           // POST → 201 + Location
    public ResponseEntity<Racun> novRacun(@RequestBody Racun racun) {
        if (racun.getId() == null || racun.getId().isBlank())
            racun.setId(UUID.randomUUID().toString());
        var shranjen = repo.save(racun);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest()
                        .path("/{id}").buildAndExpand(shranjen.getId()).toUri();
        return ResponseEntity.created(location).body(shranjen);
    }
    @PutMapping("/{id}")
    public ResponseEntity<Void> posodobi(@PathVariable String id, @RequestBody Racun racun) {
        if (!repo.existsById(id)) return ResponseEntity.notFound().build();
        racun.setId(id); repo.save(racun);
        return ResponseEntity.noContent().build();
    }
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> izbrisi(@PathVariable String id) {
        if (!repo.existsById(id)) return ResponseEntity.notFound().build();
        repo.deleteById(id); return ResponseEntity.noContent().build();
    }
}
```

> 💡 **JAX-RS vs Spring Boot:** anotacije so podobne (`@GET`→`@GetMapping`, `@PathParam`→`@PathVariable`, telo→`@RequestBody`). Spring Boot doda JPA repozitorije in vgrajen strežnik.

---

## 3. .NET — ASP.NET Core

**ASP.NET Core** = odprtokodno, **večplatformsko** (Windows/macOS/Linux) ogrodje za spletne aplikacije in API-je. Optimizirano za **cloud-native, mikrostoritve**.

**Zakaj nastal:** klasični ASP.NET (.NET Framework, `System.Web`) je bil obsežen, težko razširljiv in ni sledil SPA/oblak/mikrostoritvam. ASP.NET Core je **napisan na novo**, združuje MVC + Razor Pages + Web API na skupnem temelju.
- Ne uporablja `System.Web.dll` → modularen (**NuGet** paketi), manjši, hitrejši.
- Zahteve teče skozi **middleware cevovod** (verigo komponent).
- Vgrajen **Dependency Injection (DI)**, logging, konfiguracija; podpora Docker/Kubernetes/Azure.

**Glavni koncepti Web API:** REST arhitektura, MVC (v API brez View), brez stanja, odjemalec-strežnik, HTTP (+HTTP/2), async/await.

### 3a. Klasičen Web API (Controller)
```csharp
[ApiController]
[Route("api/[controller]")]     // → /api/racuni
public class RacuniController : ControllerBase
{
    private static readonly ConcurrentDictionary<string, Racun> _data = new();

    [HttpGet]                    // GET vsi
    public ActionResult<IEnumerable<Racun>> GetVsi() => Ok(_data.Values);

    [HttpGet("{id}")]
    public ActionResult<Racun> GetEn(string id) =>
        _data.TryGetValue(id, out var r) ? Ok(r) : NotFound();

    [HttpPost]                   // POST → 201 + Location (CreatedAtAction)
    public ActionResult<Racun> Post([FromBody] Racun racun) {
        if (string.IsNullOrEmpty(racun.Id)) racun.Id = Guid.NewGuid().ToString();
        _data[racun.Id] = racun;
        return CreatedAtAction(nameof(GetEn), new { id = racun.Id }, racun);
    }

    [HttpPut("{id}")]
    public IActionResult Put(string id, [FromBody] Racun racun) {
        if (!_data.ContainsKey(id)) return NotFound();
        racun.Id = id; _data[id] = racun; return NoContent();
    }

    [HttpDelete("{id}")]
    public IActionResult Delete(string id) {
        if (!_data.ContainsKey(id)) return NotFound();
        _data.TryRemove(id, out _); return NoContent();
    }
}
```
**Pomožne metode kontrolerja:** `Ok()`→200, `CreatedAtAction()`→201, `BadRequest()`→400, `NotFound()`→404, `NoContent()`→204. Priporočen povratni tip: `ActionResult<T>` / `IActionResult` (fleksibilnost + statusne kode).

**DI in življenjski cikel storitev:**
- registracija: `builder.Services.AddScoped<IRacunService, RacunService>();`
- kontroler dobi storitev prek konstruktorja.

| Tip | Opis | Primer |
|---|---|---|
| **Singleton** | 1 instanca za celotno aplikacijo | logger, cache, konfiguracija |
| **Scoped** | nova instanca za vsako HTTP zahtevo | DbContext |
| **Transient** | nova instanca ob vsaki uporabi | lahke, kratkožive brez stanja |

**Swagger/OpenAPI:** `AddSwaggerGen()` + `UseSwagger()`/`UseSwaggerUI()` → samodejna dokumentacija + interaktivno testiranje.

### 3b. Minimal API (od .NET 6)
Poenostavljena alternativa Controller/Action — vse z `MapGet/MapPost/...`, handlerji **inline**. Za majhne API-je, **mikrostoritve**, prototipe.
```csharp
var app = WebApplication.CreateBuilder(args).Build();
IRacunRepository repo = new RacunRepository();

app.MapGet("/api/racuni", () => Results.Ok(repo.GetAll()));
app.MapGet("/api/racuni/{id}", (string id) => {
    var r = repo.Get(id);
    return r == null ? Results.NotFound() : Results.Ok(r);
});
app.MapPost("/api/racuni", (Racun racun, HttpContext ctx) => {
    // ROČNA validacija (ni samodejne ModelState kot v klasičnem API)
    if (string.IsNullOrWhiteSpace(racun.Datum) || racun.Znesek <= 0)
        return Results.BadRequest("Podatki niso veljavni.");
    var nov = repo.Add(racun);
    return Results.Created($".../api/racuni/{nov.Id}", nov);
});
app.MapPut("/api/racuni/{id}", (string id, Racun racun) => {
    if (repo.Get(id) is null) return Results.NotFound();
    repo.Update(id, racun); return Results.NoContent();
});
app.MapDelete("/api/racuni/{id}", (string id) => {
    if (repo.Get(id) is null) return Results.NotFound();
    repo.Delete(id); return Results.NoContent();
});
app.Run();
```

**Klasičen API vs Minimal API:**
| Vidik | Klasičen | Minimal |
|---|---|---|
| Routing | `[HttpGet]` atributi | `app.MapGet(...)` |
| Arhitektura | Controller + atributi | funkcionalna |
| Testljivost | visoka (ločeni razredi) | nižja |
| DI | konstruktor | parametri lambda |
| Validacija | `ModelState.IsValid` + `[Required]` | **ročna** (ali FluentValidation) |

> 💡 Minimal API je **koncept enak Express (Node.js)**: ni razredov, le handler funkcije (`app.MapGet` ↔ `app.get`), inline.

---

## 4. JavaScript — Node.js + Express + Mongoose

**Osnova:** **Express** (spletno ogrodje), **Mongoose** (ODM za MongoDB), (**body-parser**/`express.json()`), cors.

**body-parser** = razpozna podatke iz telesa HTTP zahteve *preden* pridejo do kontrolnikov. Ponuja: JSON, Raw (Buffer), Text (string), URL-encoded parser. **Ne** razpozna multi-part → za to `multer`, `busboy`, `formidable`.

### Primer
**Model (Mongoose shema):**
```javascript
const racunSchema = new mongoose.Schema({
  id:       { type: String, required: true },
  datum:    { type: String, required: true },
  kraj:     { type: String, required: true },
  znesek:   { type: Number, required: true },
  ppId:     { type: String, required: true },
  davcnaSt: { type: String, required: true }
});
module.exports = mongoose.model('Racun', racunSchema);
```
**Inicializacija (`index.js`):** poveže se na (in-memory) MongoDB, `app.use(express.json())`, `app.use('/api/racuni', racuniRoutes)`, `app.listen(PORT)`.

**Poti (`routes/racuni.js`):**
```javascript
const router = express.Router();

router.get('/', async (req, res) => {                    // GET vsi
    try { res.json(await Racun.find({})); }
    catch { res.status(500).json({ msg: "Napaka na strežniku" }); }
});
router.get('/:id', async (req, res) => {                 // GET en
    const racun = await Racun.findById(req.params.id);
    if (!racun) res.status(404).json({ msg: `Račun ${req.params.id} ni najden` });
    res.json(racun);
});
router.post('/', async (req, res) => {                   // POST → Location
    const racun = new Racun(req.body);
    await racun.save();
    res.setHeader('Location', `${req.protocol}://${req.headers.host}${req.originalUrl}/${racun._id}`);
    res.json(racun);
});
router.route('/:id').put(async (req, res) => {           // PUT
    if (req.params.id !== req.body._id) return res.status(400).json('IDja nista enaka!');
    const racun = await Racun.findByIdAndUpdate(req.params.id, req.body);
    res.json({ msg: 'Račun je bil posodobljen' });
});
router.delete('/:id', async (req, res) => {              // DELETE
    const brisi = await Racun.findByIdAndDelete(req.params.id);
    if (!brisi) res.status(404).json({ msg: `Račun ${req.params.id} ne obstaja` });
    else res.status(200).json({ msg: 'Račun je bil zbrisan' });
});
```

> 💡 **Primerjava treh svetov (isti CRUD):** Java (JAX-RS anotacije / Spring `@GetMapping`), .NET (`[HttpGet]` atributi / Minimal `MapGet`), JS (`router.get`). Vzorec je povsod enak: metoda → pot → operacija nad shrambo → HTTP status.

---

## 5. Tehnologije in standardi za opis vmesnikov storitev

Zakaj? Da je vmesnik **strojno berljiv** (generiranje odjemalcev, dokumentacija, odkrivanje). Za SOAP obstaja WSDL; za REST ni enotnega standarda.

| Tehnologija | Predstavitev | Za kaj |
|---|---|---|
| WS-\*, UDDI | XML | SOA (računalniki) |
| SoaML, UPMS | UML | modeliranje storitev |
| **WADL** | XML | opis RESTful storitev |
| **WSDL 2.0** | XML | SOAP + REST |
| OWL-S, WSMO, SAWSDL ... | OWL/RDFS/XML | **semantične** spletne storitve (avtomatizacija) |

### WADL (Web Application Description Language)
- "**WSDL za RESTful storitve**" — strojno berljiv opis HTTP storitev (XML, 2005, Sun/Marc Hadley).
- Struktura: `<application>` → `<grammars>` (sheme) → `<resources base>` → `<resource path>` → `<method>` (z `<request>`/`<response>`, `<param>`, `<representation>`, `<fault>`).
- Orodja: `wadl2java` (generira odjemalca, uporablja JAXB), **WADL-first** razvoj.

### RSDL (RESTful Service Description Language)
- XML besednjak za opis REST na osnovi **hipermedije** (ena vstopna točka, viri, povezave, medijski tipi).
- **RSDL vs WADL:** WADL kritizirajo, ker spodbuja **tesno sklopljenost** (direktno izpostavi URI-je in fiksne poti, definira lastne napake namesto HTTP kod) → statični metapodatki namesto **HATEOAS**. RSDL to popravlja.

### JSDL (JSON Service Description Language)
- Opis vmesnika v **JSON** (JSON Schema + dodatne strukture). Opiše operacije (transport, target, inputType, parametri, returns) in tipe.

### SSDL (SOAP Service Description Language)
- Opis SOAP storitev, poudarek na **sporočilno orientiranem** pristopu (ne RPC). Formalizira modele izmenjave sporočil (MEP/CSP/Rules/SC frameworks). Ostal **akademski**, ni prešel v industrijo.

### USDL (Universal Service Description Language)
- Platformsko neodvisen jezik za opis **različnih vrst storitev** (ne le IT!). **Holistčen** — 3 vidiki: **tehnični, poslovni** (lastništvo, ceniki, pravni), **operativni**.
- WSDL/WS-\* = ustvarjeno za **računalnike (SOA)**; USDL = za **ljudi (Internet of Services)** — vključuje cenike, nivoje storitev, razpoložljivost, splošne pogoje.
- Moduli: Foundation, Service, Service level, Technical, Functional, Interaction, Participants, Pricing, Legal. Strojno berljiv, W3C, razširljiv. Podpiral SAP, a ni zaživel.

### WSDL 2.0 (2007, priporočilo W3C)
- Izboljšava WSDL 1.1 (ta nikoli ni bil formalni standard, a industrijsko sprejet).
- **Novosti:** preprostejša struktura, **polna podpora SOAP + REST**, **odstranjen `<message>`** (sporočila prek XML shem), QoS lastnosti, več MEP-ov.
- **Preimenovanja:** `<definitions>`→`<description>`, `<portType>`→`<interface>`, `<port>`→`<endpoint>`.
  - `<interface>` = abstraktna definicija (KAJ) — operacije + `<fault>`.
  - `<service>`/`<endpoint>` = konkretna definicija (KAKO+KJE) — kje je storitev dostopna (binding + URL).
- **8 MEP-ov** (Message Exchange Pattern = pogodba o izmenjavi): In-Only, Robust In-Only, In-Out, In-Optional-Out, Out-Only, Robust Out-Only, Out-In, Out-Optional-In.
- **Slaba podpora v orodjih** (izjema Axis2/wsdl2Java).

---

## Ključni povzetek predavanja 11
- **Ista REST CRUD storitev** v 5 tehnologijah — vzorec povsod enak: metoda → pot → operacija → HTTP status (200/201/204/404).
- **Java**: JAX-RS (anotacije `@Path/@GET`, impl. Jersey/RESTEasy) in Spring Boot (`@RestController`, JPA repozitorij, vgrajen strežnik).
- **.NET**: ASP.NET Core (middleware, DI, NuGet) — klasičen Web API (`[HttpGet]`, `ActionResult`) in Minimal API (`MapGet`, kot Express).
- **JS**: Express + Mongoose (`router.get`, sheme, `findById/save/findByIdAndDelete`).
- **Opis vmesnikov**: za REST ni enotnega standarda — **WADL** (WSDL za REST, a tesno sklopljen), **RSDL** (hipermedijski, HATEOAS), **JSDL** (JSON), **SSDL** (SOAP, akademski), **USDL** (holistčen, tudi poslovno/pravno), **WSDL 2.0** (SOAP+REST, `<interface>`/`<endpoint>`, 8 MEP).
