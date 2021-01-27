# DOPPThreatenedSpecies

## Information

The whole data analysis and modeling can be found in the DOPPThreatenedSpecies.ipynb notebook.

Web scraping is seperatated in the IUCN_web_scraping.py module.
For this the geckodriver is also needed. 

The countries.yml provides a list of selected countries by region needed for web scraping.
This file can be loaded using the accompanying countries module.


## Conda Environment
To run assignment notebook, follow the steps provided below:

1. Import the environment in conda, run: `conda env create -f environment.yml`
2. Activate environment with `conda activate dopp`
3. Run `jupyter notebook` in conda environment shell.
3. Run notebook `DOPPThreatenedSpecies`.
Check [conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for futher details.