# Predavanje 16 — Razvoj storitev na osnovi gRPC

> **O čem je predavanje:** kaj je **gRPC**, kako deluje (contract-first z **Protocol Buffers**), **4 modeli komunikacije** (unary + 3 streaming), ter praktičen razvoj gRPC storitve, strežnika in **sinhronega/asinhronega odjemalca** v Javi.

---

## 1. Kaj je gRPC

- **Izvor:** odprtokodna evolucija Googlove interne RPC infrastrukture **Stubby**; javno objavljen **2015**.
- **Namen:** učinkovit RPC za povezovanje **mikrostoritev** v različnih jezikih.
- **Osnovne lastnosti:**
  - visoko zmogljivo RPC ogrodje (vtičniki: load balancing, tracing, health check, avtentikacija),
  - uradne knjižnice v **11 jezikih** (C/C++, C#, Java, Go, Kotlin, Node.js, Python, PHP, Ruby, Dart, Objective-C),
  - temelji na **HTTP/2**, podpira **4 tipe klicev**,
  - privzeto **Protocol Buffers** kot IDL, **contract-first** pristop (`.proto` → generiranje kode).

**Primeren za:** nizko zakasnitev + zanesljivost + streaming; **service-to-service** komunikacijo; poliglotska okolja; podatkovne centre; mobilne odjemalce; **IoT/edge**; spletne odjemalce prek **gRPC-Web**.

**Osnovni principi (grpc.io):** storitve namesto objektov, sporočila namesto referenc, agnostična vsebina, pretakanje, preklic/timeout, nadzor toka, standardizirane statusne kode, interoperabilnost, odprtost.

---

## 2. Kako deluje

- Deluje kot klasičen RPC: odjemalec sproži metodo strežniške aplikacije **enako, kot da bi bila lokalna**.
- Definiramo **vmesnik storitve** s seznamom metod; vsaka metoda = **vhodno sporočilo (zahteva)** + **izhodno sporočilo (odgovor)**.
- Strežnik implementira vmesnik; odjemalec dobi **namestniški objekt (stub)** z enakimi metodami.
- **Interoperabilnost:** iz iste `.proto` specifikacije se generira **native koda** za strežnike in odjemalce v različnih jezikih (npr. Java strežnik + Go/Python/JS odjemalci).

```
Odjemalec                                Strežnik
  poslovna logika                          poslovna logika
       ↓                                        ↑
  stub odjemalca                           stub strežnika
  (zapakiraj/serializiraj)   ──HTTP/2──→   (odpakiraj/deserializiraj)
```

---

## 3. Protocol Buffers (Protobuf)

- Privzeti format sporočil + jezik za opis podatkov (`.proto`) v gRPC.
- Odprtokodna tehnologija Google za serializacijo strukturiranih podatkov.
- Podobno kot XML/JSON, a: **kompaktna binarna oblika** (manjša sporočila), **hitrejša (de)serializacija**, jasna shema, lažje generiranje kode, neodvisen od jezika.

**Ključne značilnosti:** kompaktno kodiranje (binarno), tipizirana shema (manj napak), hitrost.

**Osnovni koncepti:**
- podatke definiramo v `.proto`,
- podatki so organizirani kot **message** (sporočilo) — logični zapis iz **polj** (ime, tip, vrednost),
- polja imajo **oštevilčene oznake** (`= 1`, `= 2`) za identifikacijo pri serializaciji.

```proto
syntax = "proto3";
package aips;
option java_package = "si.feri.aips";
message Student {
  string ime = 1;
  string priimek = 2;
  string studijskiProgram = 3;
}
```

**Generiranje kode:** prevajalnik **`protoc`** ustvari razrede/strukture za ciljni jezik (getterji/builder + (de)serializacija):
```
protoc --java_out=. student.proto
```

**Tipi:** osnovni (`int32/64`, `uint32/64`, `float`, `double`, `string`, `bool`, `bytes`), sestavljeni (`enum`, gnezdena sporočila, **`repeated`** = seznami). Skalarni `.proto` tipi se preslikajo v tipe ciljnega jezika (npr. `.proto double` → Java `double`, Python `float`).

---

## 4. Definicija gRPC storitve v .proto

- `service` = ime storitve + seznam metod,
- vsaka `rpc` metoda: ime + **vhodno sporočilo** + **izhodno sporočilo**,
- odjemalec mora poznati strukturo zahteve/odgovora → **pogodba v `.proto`**.

```proto
syntax = "proto3";
package aips;
service Referat {
  rpc VpisStudenta (NovStudent) returns (VpisanStudent) {}
}
message NovStudent { string ime = 1; string priimek = 2; string studijskiProgram = 3; }
message VpisanStudent { string vpisnaStevilka = 1; string ime = 2; ... }
```

---

## 5. Štirje modeli komunikacije

| Model | `.proto` | Opis |
|---|---|---|
| **Unary** (zahteva/odgovor) | `rpc M (Req) returns (Resp)` | 1 zahtevek → 1 odgovor (klasičen sinhroni RPC) |
| **Server streaming** (pretakanje s strani strežnika) | `returns (stream Resp)` | 1 zahtevek → **tok** odgovorov; povezava aktivna do signala konca |
| **Client streaming** (pretakanje s strani odjemalca) | `(stream Req) returns (Resp)` | **tok** zahtev → 1 odgovor (ob koncu toka) |
| **Bidirectional streaming** (dvosmerno) | `(stream Req) returns (stream Resp)` | oba **hkrati** izmenjujeta tokova; vrstni red se v vsakem toku ohrani |

```proto
// unary:                  rpc Obvesti (ObvestiloZahteva) returns (ObvestiloOdgovor)
// server streaming:       rpc Obvesti (ObvestiloZahteva) returns (stream ObvestiloOdgovor)
// client streaming:       rpc Obvesti (stream ObvestiloZahteva) returns (ObvestiloOdgovor)
// bidirectional:          rpc Obvesti (stream ObvestiloZahteva) returns (stream ObvestiloOdgovor)
```

> 💡 Streaming je **glavna prednost gRPC** pred klasičnim REST — omogoča ga HTTP/2. Uporabno za obveščanje, prenos velikih količin podatkov, realnočasovne tokove.

---

## 6. Praktičen primer (Java) — TrafficService

Storitev z 2 operacijama: `TrafficSensorActivation` (aktivacija senzorja) in `TrafficFlow` (poročanje o prometu).

### Koraki
1. **`.proto` datoteka** (v `main/proto/trafficservice.proto`) — definira `service TrafficService` z metodama + sporočila (`TrafficSensor`, `TrafficSensorActivationResponse`, `TrafficFlowData`, `TrafficFlowResponse`).
2. **Knjižnice (pom.xml):** `grpc-netty-shaded` (runtime), `grpc-protobuf`, `grpc-stub`, `protobuf-java`, `javax.annotation-api`.
3. **Plugin za generiranje kode:** `protobuf-maven-plugin` + `os-maven-plugin` → `mvn compile` generira Java kodo (razredi sporočil + `TrafficServiceGrpc`).

### Implementacija storitve
Razred **razširi** generirani `TrafficServiceImplBase`, prepiše metode. Vsaka metoda dobi `request` in **`StreamObserver<Response> responseObserver`**:
```java
public class TrafficSensorServiceImpl extends TrafficServiceImplBase {
    @Override
    public void trafficSensorActivation(TrafficSensorData request,
            StreamObserver<TrafficSensorActivationResponse> responseObserver) {
        String sensorId = UUID.randomUUID().toString();
        TrafficSensorActivationResponse response = TrafficSensorActivationResponse.newBuilder()
                .setSensorId(sensorId)
                .setActivationStatus("OK")
                .setActivationDate(OffsetDateTime.now().toString())
                .build();
        responseObserver.onNext(response);      // pošlji odgovor
        responseObserver.onCompleted();         // zaključi
    }
}
```
> `StreamObserver`: `onNext()` = pošlji sporočilo, `onCompleted()` = konec, `onError()` = napaka. Pri streaming metodah `onNext()` kličemo večkrat.

### Implementacija strežnika
```java
Server server = ServerBuilder.forPort(50051)
        .addService(new TrafficSensorServiceImpl())
        .build().start();
server.awaitTermination();
```

### Sinhroni odjemalec (Blocking Stub)
Klic RPC: odjemalec ustvari kanal, stub zakodira sporočilo v binarno, ga pošlje kot **HTTP POST** prek HTTP/2 kanala, strežnik deserializira in izvede metodo (odgovor v obratni smeri).
```java
ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50051)
        .usePlaintext().build();
var stub = TrafficServiceGrpc.newBlockingStub(channel);   // BLOCKING = sinhrono
TrafficSensorData sensor = TrafficSensorData.newBuilder()
        .setSensorName("Senzor-1").setLattitude(46.5547).setLongitude(15.6459).build();
var activation = stub.trafficSensorActivation(sensor);    // blokira do odgovora
```

### Asinhrono prožanje
Sinhroni klic **blokira glavno nit** do odgovora. Async ne blokira — callback se pokliče v ločeni niti, ko prispe odgovor. Dva načina:

**A) Async Stub — `StreamObserver<T>`** (`newStub`):
```java
public class TrafficSensorActivationCallback implements StreamObserver<...Response> {
    public void onNext(...Response r) { /* obdelaj odgovor */ }
    public void onCompleted() { /* konec */ }
    public void onError(Throwable t) { /* napaka */ }
}
// klic:
var client = TrafficSensorServiceGrpc.newStub(kanal);
client.trafficSensorActivation(data, new TrafficSensorActivationCallback());
```

**B) Future Stub — `FutureCallback<T>`** (`newFutureStub`):
```java
public class TrafficSensorFutureCallback implements FutureCallback<...Response> {
    public void onSuccess(...Response r) { /* uspeh */ }
    public void onFailure(Throwable t) { /* napaka */ }
}
// klic:
var client = TrafficServiceGrpc.newFutureStub(kanal);
ListenableFuture<...Response> odg = client.trafficSensorActivation(sensor);
Futures.addCallback(odg, new TrafficSensorFutureCallback(), executorService);
```

**Tri vrste stub-ov:**
- `newBlockingStub` → **sinhrono** (blokira),
- `newStub` → **asinhrono** s `StreamObserver`,
- `newFutureStub` → **asinhrono** s `Future`/`ListenableFuture`.

**Testiranje:** orodje **Postman** (podpira gRPC) ali grpcurl.

---

## Ključni povzetek predavanja 16
- **gRPC** = zmogljiv, večjezičen RPC (Google, 2015), **HTTP/2** + **Protocol Buffers** (binarno), **contract-first** (`.proto`).
- **Protobuf**: sporočila (`message`) s **oštevilčenimi polji**, generiranje kode s `protoc`, kompaktno+hitro.
- **Storitev**: `service` + `rpc` metode (vhod/izhod sporočilo).
- **4 modeli:** unary, server streaming, client streaming, bidirectional (streaming omogoča HTTP/2).
- **Razvoj v Javi:** `.proto` → generiranje → impl. razširi `...ImplBase` z `StreamObserver` (`onNext/onCompleted/onError`) → strežnik `ServerBuilder` → odjemalec stub.
- **Odjemalci:** BlockingStub (sinhrono), Stub+StreamObserver / FutureStub+FutureCallback (asinhrono).
