# ia-datafortelling
Datafortelling for leverte IA-tjenester.

NB: Endringer i koden vil (per nå) ikke innvirke på cronjoben som allerede er kjører. Du må først
fjerne jobben med `kubectl delete cronjob ia-datafortelling -n teamia` _før_ Github Actions deployer
koden.

For å debugge lokalt må du først kjøre `gcloud auth login`, og brukeren din må ha leserettigheter
til BigQuery-datasettet som heter `ia-tjenester-metrikker`. 