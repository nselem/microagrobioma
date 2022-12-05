# Descarga del SRA

## Script `sra_downloader.py`

El script `sra_downloader.py` permite descargar archivos comprimidos de muestras almacenadas en el [Sequence Read Archive (SRA)](https://www.ncbi.nlm.nih.gov/sra) en formatos `fasta` o `fastq`. Para su ejecución, sólo se requiere un archivo `csv` con el siguiente formato: la primer fila debe contener los títulos de las columnas, el resto de las filas corresponden a cada muestra, con los números de acceso en la primera columna y el nombre (o descripción) de la muestra en la segunda; por ejemplo:

```text
acc,name
SRR5240887,amplicon_rhizosphere_dioon_merolae_72hrs
SRR11092501,shotgun_rhizosphere_poaceae_dgo1
```

Para correr el script sobre un archivo `accessions.csv`, se incluye el nombre del archivo `csv` y luego el formato de los archivos destino (que puede ser `fasta` o `fastq`); por ejemplo:

```text
./sra_downloader.py accessions.csv fastq
```

Todos los archivos se descargarán en el directorio actual. El script notificará sobre la muestra que esté descargando en un momento dado, así como si falla en la descarga de alguna muestra, en cuyo caso el script volverá a intentar hasta haber descargado completamente el archivo. El script no descargará archivos que ya fueron descargados anteriormente. Es recomendable correr el script en un `screen` aparte ya que el proceso puede durar mucho tiempo.

Después de descargar los archivos, se pueden descomprimir usando el siguiente comando de bash:

```text
gunzip -k -v *.gz
```

## Descripción de los archivos descargados

Los archivos se descargaron en el directorio `/datos/metamex` y se resumen en la siguiente tabla. Los estudios a los que corresponden los números se describen después de la tabla.

|Accesión|Tipo de secuenciación|Parte de planta|Descripción|Estudio|
|:-:|:-:|:-:|:-:|:-:|
SRR10591228|amplicon|rhizosphere|echinocactus_platyacanthus_wild3_1|1
SRR10591226|amplicon|rhizosphere|neobuxbaumia_polylopha_cultivated1_1|1
SRR10591227|amplicon|rhizosphere|echinocactus_platyacanthus_wild3_2|1
SRR10591224|amplicon|rhizosphere|neobuxbaumia_polylopha_cultivated1_2|1
SRR10591225|amplicon|rhizosphere|neobuxbaumia_polylopha_cultivated2|1
SRR10591233|amplicon|rhizosphere|echinocactus_platyacanthus_cultivated2|1
SRR10591234|amplicon|rhizosphere|echinocactus_platyacanthus_cultivated1|1
SRR10591223|amplicon|rhizosphere|neobuxbaumia_polylopha_wild1|1
SRR10591231|amplicon|rhizosphere|neobuxbaumia_polylopha_wild3|1
SRR10591232|amplicon|rhizosphere|neobuxbaumia_polylopha_wild2|1
SRR10591229|amplicon|rhizosphere|echinocactus_platyacanthus_wild3_3|1
SRR10591230|amplicon|rhizosphere|echinocactus_platyacanthus_cultivated3|1
SRR11092501|shotgun|rhizosphere|poaceae_dgo1|2
SRR11092499|shotgun|rhizosphere|solanum_lycopersicum_jal5|2
SRR11092511|shotgun|rhizosphere|poaceae_ags1|2
SRR11092508|shotgun|rhizosphere|poaceae_sin2|2
SRR11092498|shotgun|rhizosphere|asteraceae_jal5|2
SRR11092509|shotgun|rhizosphere|solanum_lycopersicum_sin2|2
SRR11092506|shotgun|rhizosphere|solanum_lycopersicum_slp1|2
SRR11092496|shotgun|rhizosphere|fagales_nay2|2
SRR11092505|shotgun|rhizosphere|poaceae_slp1|2
SRR11092502|shotgun|rhizosphere|solanum_lycopersicum_dgo1|2
SRR11092512|shotgun|rhizosphere|solanum_lycopersicum_ags1|2
SRR4142430|shotgun|phylosphere|agave_salmiana_magueyal|3
SRR4142433|shotgun|phylosphere|agave_tequilana_penjamo|3
SRR4140276|shotgun|rhizosphere|agave_salmiana_sanfelipe|3
SRR4140275|shotgun|rhizosphere|agave_salmiana_magueyal|3
SRR4140278|shotgun|rhizosphere|agave_tequilana_amatitan|3
SRR4140277|shotgun|rhizosphere|agave_tequilana_penjamo|3
SRR4141180|shotgun|rhizosphere|myrtillocactus_geometrizans_magueyal|3
SRR4142459|shotgun|phylosphere|opuntia_robusta_sanfelipe|3
SRR4142283|shotgun|rhizosphere|opuntia_robusta_sanfelipe|3
SRR4142282|shotgun|phylosphere|agave_salmiana_sanfelipe|3
SRR4142418|shotgun|rhizosphere|myrtillocactus_geometrizans_sanfelipe|3
SRR4142417|shotgun|rhizosphere|opuntia_robusta_magueyal|3
SRR4142460|shotgun|phylosphere|myrtillocactus_geometrizans_magueyal|3
SRR10127271|shotgun|phylosphere|myrtillocactus_geometrizans_sanfelipe|3
SRR10127267|shotgun|phylosphere|agave_tequilana_amatitan|3
SRR5166355|shotgun|phylosphere|opuntia_robusta_magueyal|3
SRR5240887|amplicon|rhizosphere|dioon_merolae_72hrs|4
SRR5240836|amplicon|rhizosphere|dioon_merolae_1month_1|4
SRR5240884|amplicon|rhizosphere|dioon_merolae_1month_2|4
SRR5240886|amplicon|rhizosphere|dioon_merolae_1month_3|4
SRR5240833|amplicon|rhizosphere|dioon_merolae_1month_4|4
SRR5240888|amplicon|rhizosphere|dioon_merolae_1month_5|4
SRR5240837|amplicon|rhizosphere|dioon_merolae_1year_1|4
SRR5240885|amplicon|rhizosphere|dioon_merolae_1year_2|4
SRR5829603|unknown|rhizosphere|phaseolus_vulgaris_white_nodule|5
SRR5829600|unknown|rhizosphere|macroptilium_atropurpureum_mix_nodule|5
SRR5829609|unknown|rhizosphere|phaseolus_vulgaris_pink_nodule|5

Los estudios se encuentran numerados de la siguiente manera:

1. Corresponde a [Gs0150452](https://gold.jgi.doe.gov/study?id=Gs0150452): *Rhizosphere microbial communities from cultivated and wild cactus plants in Queretaro, Mexico*.
2. Corresponde a [Gs0156837](https://gold.jgi.doe.gov/study?id=Gs0156837): *Rhizosphere and soil microbial communities from various locations in Mexico*.
3. Corresponde a [Gs0053055](https://gold.jgi.doe.gov/study?id=Gs0053055): *Agave microbial communities from California, USA, and Mexico*.
4. Corresponde a [Gs0132935](https://gold.jgi.doe.gov/study?id=Gs0132935): *Coralloid root microbial communities from various locations in Chiapas, Mexico*.
5. Corresponde a [Gs0114676](https://gold.jgi.doe.gov/study?id=Gs0114676): *Root nodule microbial communities of legume samples collected from USA, Mexico and Botswana*.

## Anexo: contenidos del script `sra_downloader.py`

```python
#!/usr/bin/env python3

import csv
import os
import sys
import time
from datetime import datetime
from urllib.request import urlretrieve

file_format = sys.argv[2]
link = f"https://trace.ncbi.nlm.nih.gov/Traces/sra-reads-be/{file_format}?acc="

# Open CSV file
with open(sys.argv[1], "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)

    for acc, name in reader:
        filename = f"{acc}_{name}.{file_format}.gz"

        # Check if file exists, skip if true
        if os.path.exists(filename):
            print(f"{datetime.now()}: Skipping {acc} as it already exists.")
            continue

        print(f"{datetime.now()}: Downloading {acc}.")

        # Fetch file, if download fails, retry until successful
        while True:
            try:
                urlretrieve(link + acc, filename)
                break
            except Exception:
                print(f"{datetime.now()}: Failed to download {acc}, retrying...")
                time.sleep(5)

        print(f"{datetime.now()}: Finished downloading {acc}.")

print(f"{datetime.now}: Finished!")
```
