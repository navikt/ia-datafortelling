# ia-datafortelling

Datafortelling over leverte digitale (selvbetjente) IA-tjenester. Du finner
den [her](https://data.intern.nav.no/story/3f485566-49fc-4867-937e-618293158ef8).

## Utvikling

Dette prosjektet bruker Python 3.11. 

Secrets for dette prosjektet ligger
i [Google Secret Manager](https://console.cloud.google.com/security/secret-manager?project=teamia-prod-df3d)

I listen over avhengigheter (`requirements.txt`) finner du en referanse til _black_, som er et
formateringsbibliotek (ala _prettier_ for Javascript). Det er anbefalt
å [integrere dette verktøyet i IDE-en](https://black.readthedocs.io/en/stable/integrations/editors.html)

### Lokal kjøring og debugging

For å debugge lokalt må du først autentisere deg med `gcloud auth login`. Brukeren din må ha
leserettigheter
til [BigQuery-datasettet](https://console.cloud.google.com/bigquery?project=teamia-prod-df3d&ws=!1m4!1m3!3m2!1steamia-prod-df3d!2sia_tjenester_metrikker)
som heter `ia-tjenester-metrikker` i prosjektet `teamia-prod-df3d`.

For å oppdatere datafortellingen via lokal kjøring, må du legge inn
miljøvariabel `DATASTORY_TOKEN=x`, for eksempel under "Edit Configurations" i Intellij. Verdien `x`
refererer her til et token som peker på den datafortellingen som du ønsker å oppdatere.
Se [NADA-docs](https://docs.knada.io/dele-innsikt/datafortelling/#oppdatere-eksisterende-datafortelling) for mer info.

### Kontakt
for henvendelser, opprett [issue her på GitHub](https://github.com/navikt/ia-datafortelling/issues).  
Ansatte i NAV-IT kan også kontake oss i Slack-kanalen #teamia

### Troubleshooting
> [NOTE]
> Feil: `google.auth.exceptions.DefaultCredentialsError`  
> Løsning: Kjør `gcloud auth application-default login`

> [NOTE]
> Feil: `You are authorizing client libraries without access to a web browser.`  
> Løsning: `Legg til flagg --no-launch-browser` til `gcloud auth login` 