# Master-Thesis-Repository
Contains Python code for Edvard August Eggen Sveum's Master's Thesis

The "SNA data preparations+" file contains the code to prepare the Patent for the social network analysis.
The Citation network data structuring and network construction file contains the Python code needed to prepare the patent data and construct patent citation networks used in the Main path analysis. 

Input for Gephi: IXA_FGepiE, IXI_FGephiE, Nodes_gephiE
Gephi output: GTISNPv2R1 and "SNA FC + FCV TIS R1" (also used as input for SNA data preperations+'s later sections).
"SNA FC + FCV TIS R1" also contains the calculated betweenness centrality values of the different actors.


Patent data retrieval and comments:
The data is available at Lens.org (2022) and can be retrieved in JSON format, but will require the files to be decompressed later afterwards.

Raw Patent data avalible at: https://www.lens.org/lens/search/patent/table?p=0&n=50&s=date_published&d=%2B&f=false&e=false&l=en&authorField=author&dateFilterField=publishedDate&orderBy=%2Bdate_published&presentation=false&preview=false&stemmed=true&useAuthorId=false&types.must=GRANTED_PATENT&classCpc.must=F17C2221%2F012&classCpc.must=F17C2223%2F0123&classCpc.must=Y02E60%2F32&classCpc.must=Y02E60%2F30&classCpc.must=Y02E60%2F50&classCpc.must=H01M2250%2F20&classCpc.must=H01M8%2F083&classCpc.must=H01M8%2F10&classCpc.must=H01M8%2F1004&classCpc.must=H01M2008%2F1095&classCpc.must=Y02T90%2F40&classCpc.must=B60L58%2F40&publishedDate.from=1900-01-01&publishedDate.to=2022-08-01 

The Original analysis was run on computer with 64 GB of RAM
