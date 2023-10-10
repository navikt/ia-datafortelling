#!/bin/bash

quarto render leverte_ia_tjenester.qmd

curl -X PUT leverte_ia_tjenester.html \
    https://${NADA_ENV}/quarto/update/${QUARTO_ID} \
    -H "Authorization:Bearer ${QUARTO_TOKEN}"