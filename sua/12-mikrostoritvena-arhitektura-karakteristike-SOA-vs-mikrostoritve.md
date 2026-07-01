# Predavanje 12 — Mikrostoritvena arhitektura: karakteristike, prednosti in izzivi, SOA vs mikrostoritve

> **O čem je predavanje:** zakaj monolit sčasoma postane problem, kaj so **mikrostoritve** in **9 karakteristik** mikrostoritvene arhitekture (po Fowler/Lewis), njene **prednosti in izzivi**, ter kako se **SOA razlikuje od mikrostoritev**.

---

## 1. Temelji uspešnega razvoja + kje je arhitektura

Tri noge uspešnega razvoja programske opreme:
- **Proces** — agilni razvoj, neprekinjena integracija/dostava/uvajanje ("Continuous Everything").
- **Organizacijska struktura** — majhne, avtonomne ekipe (6–8 razvijalcev).
- **Arhitektura** — na najvišjem nivoju izbiramo med **monolitno** in **mikrostoritveno**.

> Problem: monolitna arhitektura **ne podpira dobro** agilnega procesa in majhnih avtonomnih ekip → mikrostoritve zapolnijo to vrzel.

---

## 2. Monolitna arhitektura

**Monolit** = programska oprema, zasnovana kot **ena, samo-vsebovana enota**. Komponente so povezane med nivoji in **močno odvisne** → **tesna sklopljenost** kode.

**Lastnosti:**
- Poslovna logika je pogosto modularna (storitve, domenski objekti), a se **zgradi, zapakira in namesti kot ena celota** (v Javi WAR/EAR/JAR).
- Skaliranje: podvajanje instanc + load balancer (horizontalno).

**Prednosti monolita:**
- Enostaven razvoj (dobro poznana arhitektura), preprosto nameščanje (en artefakt), enostavno testiranje, enostavna ponovna uporaba kode, dobra podpora IDE.

> "Vse je super ... dokler ..." aplikacija ne zraste.

**Izzivi monolita (ko zraste na milijone vrstic):**
- Slabša preglednost, težje vzdrževanje, težji razvoj novih funkcionalnosti.
- **Pogosto nameščanje težavno** — vsaka sprememba zahteva namestitev **celotne** aplikacije; večje tveganje napak, daljši izpad → ekipe se izogibajo pogostemu deployu.
- **Težko skaliranje** — vire dodeljujemo le **celotni** aplikaciji, ne posameznim modulom (čeprav le en modul potrebuje več pomnilnika/CPU).
- Velika aplikacija **upočasni IDE** in zagon na strežniku → manjša produktivnost.
- **Dolgoročna vezava na sklad tehnologij** — menjava tehnologije je draga/tvegana/nemogoča → zastarele tehnologije.
- **Organizacijsko:** omejena avtonomija ekip (vsi delajo na isti aplikaciji, spremembe se prepletajo).
- Sčasoma "**monolitni pekel**" — prevelik in prekompleksen za vzdrževanje.

---

## 3. Kaj so mikrostoritve

- Izraz **microservice** skovan maja 2011 (delavnica arhitektov pri Benetkah), uradno sprejet 2012. Prakse so obstajale prej (Amazon, Netflix, Facebook — "finozrnati SOA").
- **Ideja:** namesto ene velike aplikacije sistem razdelimo na **več manjših, funkcionalno zaokroženih storitev**.

**Definicija:** *"Samostojna storitev z jasno opredeljeno, ozko usmerjeno funkcionalnostjo, ki jo prek API ponuja drugim delom sistema."*
- Predstavlja **poslovno zmožnost** znotraj domene (uporabniki, naročila, plačila ...).
- Pogosto **lastnik podatkov svoje domene** (CRUD nad eno/malo entitetami).
- Izvaja se kot **ločena instanca** v lastnem izvajalnem okolju (pogosto v oblaku, Docker).

**Definicija stila (Lewis & Fowler):** *pristop k razvoju ene aplikacije kot **niza majhnih storitev**, vsaka teče v svojem procesu in komunicira z **lahkimi mehanizmi** (pogosto HTTP resource API). Storitve so grajene okoli **poslovnih zmožnosti**, so **neodvisno namestljive** prek popolnoma avtomatizirane mašinerije, imajo **minimum centraliziranega upravljanja** in so lahko pisane v različnih jezikih z različnimi shrambami.*

**Primer:** mikrostoritev "prejem zalog" → prejme HTTP zahtevo (od druge storitve ali UI) → validira → zabeleži v **svojo** bazo → vrne potrditev.

**6 karakteristik mikrostoritve:** odgovorna za **eno zmogljivost**, **samostojno namestljiva**, sestavljena iz enega/več procesov, ima **lastno shrambo podatkov**, majhna ekipa vzdržuje nekaj mikrostoritev, je **zamenljiva**.

**Skaliranje (Kocka skaliranja):**
- **Y-os: funkcijsko skaliranje** — sistem razdelimo po funkcijah/storitvah, skaliramo tiste z največjo obremenitvijo.
- **X-os: horizontalno skaliranje** — več enakih instanc iste storitve + load balancer.

---

## 4. 9 karakteristik mikrostoritvene arhitekture (Fowler/Lewis)

1. **Komponentizacija prek storitev** — komponenta = neodvisno zamenljiva/nadgradljiva enota. V tradiciji so to **knjižnice** (klic funkcij v istem procesu), pri mikrostoritvah so to **storitve** (svoj proces, komunikacija prek API). Glavna prednost: **neodvisno nameščanje**. Izziv: sprememba API-ja lahko zahteva prilagoditev odvisnih storitev → verzioniranje, združljivost nazaj.

2. **Organizacija kode okrog poslovnih zmožnosti** — ne po tehnoloških plasteh.
   - Monolit: koda po plasteh (UI/logika/podatki) → ekipe po tehnologiji (UI ekipa, back-end ekipa, DB ekipa).
   - Mikrostoritve: razdelitev po **domeni**; vsaka storitev vključuje vse sloje → **večfunkcijske (cross-functional) ekipe** (UX, podatki, razvoj, test, DevOps).
   > 💡 To sledi **Conwayjevemu zakonu**: struktura sistema posnema strukturo organizacije.

3. **"Produkti" namesto projektov** — projekt: razviješ, predaš v vzdrževanje, ekipo razpustiš. Produkt: storitev se **neprestano razvija**; ekipa je lastnik skozi cel življenjski cikel → **"you build it, you run it"**.

4. **Pametne končne točke & neumne cevi** (smart endpoints, dumb pipes) —
   - SOA gradi okoli **ESB** (pametno vodilo: usmerjanje, orkestracija, transformacije) → visoka kompleksnost.
   - Mikrostoritve: **pamet je v storitvah**, komunikacijski kanal je **preprost**. Storitev: prejme zahtevo → izvede logiko → vrne odgovor.
   - Dva načina komunikacije: **HTTP/REST** (zahtevek-odgovor) in **lahka sporočila** (asinhrono, preprost broker: RabbitMQ, ZeroMQ). Brez BPEL/WS-\*.

5. **Decentralizirano upravljanje** — namesto ene standardizirane platforme **polyglot programming** (za vsako storitev najprimernejši jezik: Node.js za spletne, C++ za realnočasovne) in **polyglot persistence** (različne baze). Pragmatičen odnos do standardov.

6. **Decentralizirano upravljanje podatkov** — **vsaka storitev je lastnik svojih podatkov** (database per service). Ni ene skupne baze. Lahko ločene instance istega SUPB ali različni SUPB. Izziv: **tehnične pogodbe** med storitvami → vzorci **Tolerant Reader** (odjemalec odporen na spremembe) in **Consumer-Driven Contracts** (pogodbe sooblikujejo odjemalci).

7. **Avtomatizacija infrastrukture** — nujna, ker ročno upravljanje mnogih storitev ni obvladljivo. **CI/CD cevovodi** za samodejno gradnjo, testiranje, uvajanje.

8. **Načrt za neuspeh** (design for failure) — okvare so **pričakovane**. Klic storitve lahko spodleti → odjemalec se odzove (timeouti, ponovni poskusi, nadomestni odziv). Poudarek na **monitoringu in opazljivosti** (tehnične metrike: zahteve/s, odzivni časi; poslovne metrike: nakupi/s).

9. **Evolucijsko načrtovanje** — hitre, pogoste, nadzorovane spremembe. Storitve so **neodvisno nadgradljive in zamenljive** → storitev lahko prepišemo z minimalnim vplivom; nekatere se sčasoma opustijo.

---

## 5. Prednosti mikrostoritev

| Prednost | Zakaj |
|---|---|
| **Manjše, enostavnejše aplikacije** | boljša razumljivost, manj težav z odvisnostmi, hitrejša izgradnja/zagon (sekunde vs minute), višja produktivnost |
| **Močne meje med moduli** | meje "prisiljene" z arhitekturo (komunikacija le prek API, ne direktno v bazo) |
| **Neodvisno nameščanje** | sprememba ene storitve = uvedba le te; manjše tveganje izpada; hitrejši time-to-market s CD |
| **Ni dolgoročne vezave na tehnologije** | poliglotski razvoj; lažje vključevanje kadrov z drugim skladom |
| **Tehnološka raznolikost, lažje preizkušanje** | zastarele tehnologije menjamo po korakih; preizkus nove tehnologije = omejeno tveganje |
| **Boljša izolacija napak** | napaka omejena na eno storitev, ostali sistem deluje naprej |

Dodatno: enostavnejše dodajanje funkcionalnosti, ločene neodvisne ekipe, neodvisno dodeljevanje virov.

---

## 6. Izzivi mikrostoritev

| Izziv | Podrobnost |
|---|---|
| **Večja kompleksnost** | razvoj **porazdeljenih sistemov** (medprocesna komunikacija, obravnava delnih okvar) |
| **Poslovne transakcije čez več baz** | ni preprostih ACID/2PC transakcij → **saga, kompenzacije, eventual consistency** |
| **Testiranje** | storitev A odvisna od B, C ... prek omrežja → potrebni testi enot, komponent, **pogodb (contract testing)**, end-to-end |
| **Nameščanje in delovanje** | 10/50/100+ storitev, različne platforme/verzije → potrebna **orkestracija** (Kubernetes) in CI/CD |
| **Zmogljivost (latenca)** | omrežni klici počasnejši od in-process; veriga A→B→C poveča odzivni čas → manj klicev z več podatki, asinhroni/vzporedni klici |
| **Zanesljivost** | več storitev = večja verjetnost delnih izpadov → odpornost na napake |
| **Usklajevanje sprememb** | funkcionalnost čez več storitev zahteva nadzor verzij in pogodbe |

> ⚠️ **"Eventual consistency":** namesto takojšnje konsistentnosti (ACID) se podatki v več storitvah uskladijo **sčasoma** prek dogodkov — več v predavanju 14 (Saga, Event Sourcing, CQRS).

---

## 7. SOA vs mikrostoritvena arhitektura

**Skupno:** oba temeljita na **storitvah**, spodbujata **šibko sklopljenost**, modularnost, jasne vmesnike, neodvisnost od tehnologij. Mikrostoritve so se razvile **iz idej SOA**.

> Mikrostoritve pogosto razumemo kot **specializacijo / naslednji evolucijski korak SOA** z večjim poudarkom na sodobnih praksah razvoja in uvajanja.

**Ključne razlike:**

| Vidik | SOA | Mikrostoritve |
|---|---|---|
| **Deljenje komponent** | pogosto deljenje skupnih komponent/knjižnic → lahko tesna sklopljenost | **brez deljenja** — vsaka storitev ima svoje komponente/odvisnosti |
| **Podatkovna shramba** | lahko **skupna** baza/SUPB za več storitev | **database per service** — vsaka storitev lastnik svojih podatkov (dostop le prek API) |
| **Komunikacija** | osrednji **ESB** (pametno vodilo), pogosto SOAP | **lahki API-ji** (REST/HTTP), sporočila (JMS/AMQP), **brez pametnega vodila** |
| **Upravljanje** | pogosto **centralizirano** (standardi, skupne platforme, governance) | **minimalno centralizirano**, avtonomija ekip, pogodbe API |
| **Orkestracija** | **ključna** (kompozicija v poslovne procese; brez orkestracije "ni SOA") | izogibamo se ji (zahteva sklopljenost); **koreografija** prek pametnih končnih točk |
| **Nameščanje/skaliranje** | usklajeno/centralno; spremembe vplivajo širše; skaliranje oteženo | **neodvisno** uvajanje in skaliranje po storitvah |
| **Tehnologije** | tradicionalne podjetniške, močna standardizacija | sodobne prakse: **Docker, Kubernetes, DevOps, CI/CD** |
| **Kontekst** | velike integracije, heterogena okolja (interoperabilnost ključna) | okolja s pogostimi spremembami, hitro dostavo, prožnim skaliranjem (spletni sistemi) |

> 🔑 **Bistvo razlike:** SOA = **centralizacija + orkestracija + ESB + deljeni viri**; mikrostoritve = **decentralizacija + avtonomija + lahki API + database per service**. "Mikro" se ne nanaša na število vrstic kode, ampak na **omejen obseg odgovornosti** storitve.

---

## Ključni povzetek predavanja 12
- **Monolit**: preprost na začetku, a ob rasti = "monolitni pekel" (težko nameščanje/skaliranje/vzdrževanje, vezava na tehnologije, omejena avtonomija ekip).
- **Mikrostoritev**: samostojna, ozko usmerjena storitev okoli poslovne zmožnosti, z lastno shrambo, neodvisno namestljiva, zamenljiva.
- **9 karakteristik (Fowler/Lewis)**: komponentizacija prek storitev, organizacija okoli poslovnih zmožnosti, produkti namesto projektov, pametne končne točke & neumne cevi, decentralizirano upravljanje (podatkov), avtomatizacija infrastrukture, načrt za neuspeh, evolucijsko načrtovanje.
- **Prednosti**: manjše aplikacije, močne meje, neodvisno nameščanje, poliglotstvo, izolacija napak.
- **Izzivi**: kompleksnost porazdeljenih sistemov, transakcije čez baze (saga), testiranje, nameščanje, latenca, zanesljivost.
- **SOA vs mikrostoritve**: mikrostoritve = evolucija SOA; glavna razlika = **centralizacija/ESB/orkestracija (SOA)** vs **decentralizacija/lahki API/database-per-service (mikrostoritve)**.
