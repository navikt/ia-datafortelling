#!/bin/bash

export QUARTO_PRINT_STACK=true
export QUARTO_LOG_LEVEL=DEBUG

quarto render leverte_ia_tjenester/index.qmd

curl -X PUT -F index.html=@leverte_ia_tjenester/index.html \
     https://${NADA_ENV}/quarto/update/${LEVERTE_IA_TJENESTER_QUARTO_ID} \
     -H "Authorization: Bearer ${TEAM_TOKEN}"


quarto render key_metrics/index.qmd

curl -X PUT -F index.html=@key_metrics/index.html \
    https://${NADA_ENV}/quarto/update/${KEY_METRICS_QUARTO_ID} \
    -H "Authorization:Bearer ${TEAM_TOKEN}"
