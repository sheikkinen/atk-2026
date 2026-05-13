# Asiakaspalvelun agenttialusta

> **ATK-2026** | Tekoälypuhelinhaastattelu

## Mikä tämä on?

Tekoälypohjainen puhelinhaastattelijabotti, joka käy luonnollisen
vuoropuhelun soittajan kanssa ja kerää rakenteista tietoa — ilman lomakkeita.

Botti esittäytyy, kysyy tarvittavat tiedot, toistaa ne ääneen ja tallentaa
vasta vahvistuksen jälkeen. Tässä demossa botti on nimeltään **Hieronta Maatti**
ja kerää ATK-2026-tapahtuman osallistujien muistoja ja yhteystietoja.

---

## Puhelun rakenne — neljä vaihetta

Sama rakenne toimii kaikissa kyselyissä. Ainoastaan skeema vaihtuu.

```
📞  AVAUS
    Botti toivottaa ja esittää ensimmäisen kysymyksen
    ("Hei, olen Hieronta Maatti. Millä nimellä kutsumme teidät?")

🔄  LUOTAUS  (toistuu kunnes kaikki pakolliset tiedot on kerätty)
    ├─ Poimi tiedot soittajan puheesta
    ├─ Tunnista puuttuvat kentät
    └─ Kysy seuraava puuttuva tieto luontevasti, teitittellen

📋  YHTEENVETO
    Botti lukee kerätyt tiedot ääneen ja pyytää vahvistuksen
    ├─ "Kyllä" → tallennus
    ├─ "Ei, korjataan..." → korjaa kentät → uusi yhteenveto
    └─ "Voisitteko toistaa?" → selventää → uusi yhteenveto

✅  TOIMENPIDE
    Tiedot tallennetaan, botti sanoo hyvästit
```

---

## Kolme osaa — vain yksi muuttuu

### 1. Graafi — pysyy samana (`graph.yaml`)

Graafi toteuttaa yllä olevan neljän vaiheen rakenteen. Se on kirjoitettu
kerran ja toimii sellaisenaan kaikissa kyselyissä.

```
START → init → load_schema → avaus → [luotaussilmukka] → yhteenveto → tallennus → END
```

Graafi ei sisällä mitään kyselykohtaista — kentät, tekstit ja kysymykset
tulevat skeemasta.

### 2. Promptit — lähes samat kaikissa kyselyissä (`prompts/`)

Neljä promptia hoitaa koko vuoropuhelun logiikan. Ne lukevat kenttäkuvaukset
skeemasta, joten ne toimivat uudessa kyselyssä ilman muutoksia tai pienellä
säätämisellä.

| Prompti | Tehtävä |
|---------|---------|
| `extract_fields` | Poimii soittajan puheesta rakenteisen JSON:n kentistä |
| `generate_probe` | Muotoilee seuraavan tarkentavan kysymyksen puuttuvasta tiedosta |
| `recap` | Tiivistää kerätyt tiedot ääneen luettavaksi yhteenvedoksi |
| `classify_recap` | Luokittelee soittajan vastauksen: vahvistus / korjaus / tarkennus |

Kaikki promptit käyttävät luontevaa suomen kieltä ja välttävät lomakemaista kysymistä.

### 3. Skeema — vaihtuu kyselystä toiseen (`schema.yaml`)

Skeema on ainoa tiedosto, joka muuttuu kampanjasta toiseen. Se määrittää
mitä kerätään, miten botti esittäytyy ja miten puhelu päättyy.

```yaml
# schema.yaml — ATK-2026-esimerkki
name: Marketing-kampanjan suosittelukysely
opening: "Hei, olen Hieronta Maatti. Millä nimellä kutsumme teidät?"
farewell: "Kiitoksia. Kutsumme teidät mahdollisimman pian."

fields:
  - id: name
    label: Nimi
    description: Vastaajan koko nimi
    required: true

  - id: organization
    label: Organisaatio
    description: Vastaajan organisaatio tai yritys
    required: true

  - id: memento_atk_days
    label: Muisto ATK-päiviltä
    description: Mukava muisto näiltä tai aiemmilta ATK-päiviltä
    required: true

  - id: miscellaneous
    label: Muuta tietoa
    description: Muita tietoja, joita vastaaja haluaa jakaa
    required: false
```

Uusi kampanja = uusi `schema.yaml`. Graafia tai prompteja ei tarvitse koskea.

---

## Tekninen rakenne

```
Soittaja ←→ PSTN ←→ Agenttialusta (FSM) ←→ Integraatiot
                            │
                  ┌─────────┴──────────┐
                  │   graph.yaml       │  ← YAMLGraph
                  │   schema.yaml      │  ← vaihtuu per kampanja
                  │   prompts/         │  ← yhteiskäyttöiset
                  └────────────────────┘
                
```

---

*Asiakaspalvelun agenttialusta · YAMLGraph-pohjainen puhelintekoäly*

---

## Haluatko kuulla lisää?

Ota yhteyttä — rakennetaan yhdessä seuraava voicebot ja kyselyagenttisi.

**[linkedin.com/in/samijpheikkinen](https://www.linkedin.com/in/samijpheikkinen/)**

---

## Puheluiden hallinta (FSM) *video*

[![Puheluiden hallinta (FSM)](https://img.youtube.com/vi/pP8YEVTldic/hqdefault.jpg)](https://youtu.be/pP8YEVTldic)

---

## Lisätietoja

| Projekti | Kuvaus |
|---------|--------|
| [sheikkinen/yamlgraph](https://github.com/sheikkinen/yamlgraph) | YAMLGraph-kehys — graafi, promptit, skeema |
| [sheikkinen/statemachine-engine](https://github.com/sheikkinen/statemachine-engine) | Moottori puheluiden hallintaan |
| [sheikkinen/synthetic-finnish-journal](https://github.com/sheikkinen/synthetic-finnish-journal) | Muita käyttökohteita YAMLGraphille |
 [sheikkinen/scripture-dev](https://github.com/sheikkinen/scripture-dev) | Vaatimusten jäljitettävyyden takaava AI-kehitysprosessi | 
