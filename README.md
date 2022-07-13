# ia-datafortelling

Datafortelling for leverte IA-tjenester.

Secrets for dette prosjektet ligger i Google Secret Manager.

NB: Endringer i koden vil (per nå) ikke innvirke på eventuelle cronjober som allerede er satt opp.
Du må fjerne jobben med `kubectl delete cronjob ia-datafortelling -n teamia` _før_ Github
Actions deployer koden.

For å debugge lokalt må du først kjøre `gcloud auth login`, og brukeren din må ha leserettigheter
til BigQuery-datasettet som heter `ia-tjenester-metrikker` i prosjektet `teamia-prod-df3d`.