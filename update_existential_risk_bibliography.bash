#!/bin/bash
cp ExistentialRiskBibliography.csv ExistentialRiskBibliography.csv.old 2>/dev/null
cp existential-risk-bibliography.bib existential-risk-bibliography.bib.old 2>/dev/null
echo 'The biggest existential risk bibliography source: The Existential Risk Research Assessment (TERRA)'
echo 'Site: www.x-risk.net'
if (("$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)"=='ok'));then
    echo 'Downloading existential risk bibliography...'
    curl https://www.x-risk.net/application/download_csv/existential-risk/ 2>/dev/null 1>ExistentialRiskBibliography.csv
else
    echo 'Cannot connect to the Internet for update existential risk bibliography'
fi
echo 'Converting bibliography to BibTeX format...'
python3 csv2bibtex.py >ExistentialRiskBibliography.bib && echo 'Converting completed. You can use BibTeX bibliography in your research papers.'
