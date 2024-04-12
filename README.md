ia-datafortelling
================

Datafortelling over leverte digitale (selvbetjente) IA-tjenester. Du finner
den [her](https://data.intern.nav.no/story/3f485566-49fc-4867-937e-618293158ef8).

# Utvikling

Prosjektet bygges med github [workflow](.github/workflows/deploy-naisjob.yml) og deployes til nais som en [Naisjob](https://docs.nais.io/naisjob).

Jobben kjører i intervaller som er definert i cron-utrykket `spec.schedule` i [prod.yaml](.nais/prod.yaml).

Secrets for dette prosjektet ligger
i [Google Secret Manager](https://console.cloud.google.com/security/secret-manager?project=teamia-prod-df3d)

## Kom i gang

Installer [python3.11](https://www.python.org/downloads/).

Installer quarto ved å følge guiden på [på quarto sine nettsider](https://quarto.org/docs/get-started/).

Som en god praksis, opprett et virtuelt pythonmiljø i root til prosjektet:

```
python3.11 -m venv env && source env/bin/activate
```

Installer avhengigheter med

```
pip3 install -r requirements.txt
```

Det er anbefalt at du itegrerer formateringsverktøyet
_black_ [i IDE-en du bruker](https://black.readthedocs.io/en/stable/integrations/editors.html).

## Lokal kjøring og debugging

For å debugge lokalt må du først autentisere deg med

```
gcloud auth login --update-adc
``` 

Brukeren din må ha
leserettigheter
til [BigQuery-datasettet](https://console.cloud.google.com/bigquery?project=teamia-prod-df3d&ws=!1m4!1m3!3m2!1steamia-prod-df3d!2sia_tjenester_metrikker)
som heter `ia-tjenester-metrikker` i prosjektet `teamia-prod-df3d`.

Generer datafortellingen lokalt ved å kjøre 
```
quarto render leverte_ia_tjenester/index.qmd
```

# Oppdater avhengigheter

- Oppdater python:
  - Sjekk versjon i Dockerfile opp mot Python sin siste versjon [her](https://www.python.org/downloads/).
  - Dersom kom ny versjon, lag et lokalt virtual miljø på nytt.
- Oppdater python pakker:
  - `pip3 install --upgrade pip`
  - `pip3 install --upgrade <pakke>`
  - Oppdater `requirements.txt` manuelt (eller bruk `pip3 freeze > requirements.txt`)
  - Kjør datafortellingene lokalt på nytt og sammenlign med prod

# Henvendelser

Spørsmål knyttet til koden eller prosjektet kan stilles som et [issue her på GitHub](https://github.com/navikt/ia-datafortelling/issues).

## For NAV-ansatte

Interne henvendelser kan sendes via Slack i kanalen #team-pia.

# Feilsøking

> [!WARNING]
> Feil: `google.auth.exceptions.DefaultCredentialsError`  
> Løsning: Kjør `gcloud auth application-default login`

> [!WARNING]
> Feil: `You are authorizing client libraries without access to a web browser.`  
> Løsning: Legg flagg `--no-launch-browser` etter `gcloud auth login` 