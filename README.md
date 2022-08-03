# ia-datafortelling

Datafortelling 
over leverte digitale (selvbetjente) IA-tjenester. Du finner den [her](https://data.intern.nav.no/story/3f485566-49fc-4867-937e-618293158ef8).

## Utvikling

Secrets for dette prosjektet ligger
i [Google Secret Manager](https://console.cloud.google.com/security/secret-manager?project=teamia-prod-df3d)
.

Endringer i koden vil (per nå) ikke innvirke på eventuelle cronjober som allerede er satt opp. Du må
fjerne jobben med `kubectl delete cronjob ia-datafortelling -n teamia` _før_ du pusher kode
til `main`-branchen.

### Lokal kjøring og debugging

For å debugge lokalt må du først autentisere deg med `gcloud auth login`. Brukeren din må ha
leserettigheter
til [BigQuery-datasettet](https://console.cloud.google.com/bigquery?project=teamia-prod-df3d&ws=!1m4!1m3!3m2!1steamia-prod-df3d!2sia_tjenester_metrikker)
som heter `ia-tjenester-metrikker` i prosjektet `teamia-prod-df3d`.

For å oppdatere datafortellingen via lokal kjøring, må du legge inn
miljøvariabel `DATASTORY_TOKEN=x`, for eksempel under "Edit Configurations" i Intellij. Verdien `x`
refererer her til et token som peker på den datafortellingen som du ønsker å oppdatere.
Se [NADA-docs](https://docs.knada.io/dele-innsikt/datafortelling/#oppdatere-eksisterende-datafortelling)
for mer info.

### Formatering med Black

I listen over avhengigheter (`requirements.txt`) finner du en referanse til _black_, som er et
formateringsbibliotek ala _prettier_ for Javascript. Det er anbefalt
å [integrere dette verktøyet i IDE-en](https://black.readthedocs.io/en/stable/integrations/editors.html)
.
