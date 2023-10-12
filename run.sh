#!/bin/bash

export QUARTO_PRINT_STACK=true
export QUARTO_LOG_LEVEL=DEBUG

quarto render leverte_ia_tjenester/index.qmd

curl -X PUT -F index.html=@index.html \
     https://${NADA_ENV}/quarto/update/${LEVERTE_IA_TJENESTER_QUARTO_ID} \
     -H "Authorization: Bearer ${TEAM_TOKEN}"
