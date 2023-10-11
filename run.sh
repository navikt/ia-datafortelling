#!/bin/bash

quarto render index.qmd

curl -X PUT \
     -F index.html=@index.html \
     https://${NADA_ENV}/quarto/update/${LEVERTE_IA_TJENESTER_QUARTO_ID} \
     -H "Authorization: Bearer ${TEAM_TOKEN}"
