#!/bin/bash
compat50 2> /dev/null
echo 'The biggest existential risk bibliography source: The Existential Risk Research Assessment (TERRA)'
echo 'Site: www.x-risk.net'
pingresult="$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo 'yes' || echo 'no')"
if [[ $pingresult = 'yes' ]];then
    echo 'Downloading existential risk bibliography...'
    curl https://www.x-risk.net/application/download_csv/existential-risk/ 2>/dev/null 1>ExistentialRiskBibliography.csv
else
    echo 'Cannot connect to the Internet for update existential risk bibliography'
fi