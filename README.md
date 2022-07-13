# ia-datafortelling

Datafortelling
over [leverte IA-tjenester](https://data.intern.nav.no/story/3f485566-49fc-4867-937e-618293158ef8) .

Secrets for dette prosjektet ligger
i [Google Secret Manager](https://console.cloud.google.com/security/secret-manager?project=teamia-prod-df3d)
.

NB: Endringer i koden vil (per nå) ikke innvirke på eventuelle cronjober som allerede er satt opp.
Du må fjerne jobben med `kubectl delete cronjob ia-datafortelling -n teamia` _før_ Github Actions
deployer koden.

For å debugge lokalt må du først kjøre `gcloud auth login`, og brukeren din må ha leserettigheter
til [BigQuery-datasettet](https://console.cloud.google.com/bigquery?project=teamia-prod-df3d&ws=!1m4!1m3!3m2!1steamia-prod-df3d!2sia_tjenester_metrikker)
som heter `ia-tjenester-metrikker` i prosjektet `teamia-prod-df3d`.