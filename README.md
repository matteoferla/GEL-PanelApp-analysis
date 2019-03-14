# Genomics England PanelApp analysis
An analysis of the genes in Genomics England (GEL) PanelApp.

## Details
Written for python3.

## PanelWrapper
Two classes within wrap the GEL PanelApp Rest API. Panel and Gene.                 

Both contain a class method called `.get_list(verbose=false)`, which retrieves all the entrries and returns a list of instances of Panel or Gene.
Do note that the classes inherit a base class that has the fetching power.

The attributes of Gene() instance are:
* gene_data
* type
* name
* confidence_level
* penetrance
* mode_of_pathogenicity
* publications
* evidence
* phenotypes
* mode_of_inheritance
* tags
* panel

Those of Panel are:
* name
* id
* disease_group
* disease_sub_group
* status
* relevant_disorders
* n_genes
* types


## Licence
The licence is the same as the GEL PanelApp. To figure what that is, look for that.

