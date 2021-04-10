# UCLA_CS_245_Project5

This is the introductory page for the CS-245 team Big Data Fall 2020 at UCLA.

## Project Goals
Our objective is to design a dynamic graph neural network which fore-casts the Covid-19 pandemic spread inside the United States. We willapproach this problem by building a graphG= (V,E) where the setVcontains nodes representing places (e.g. cities, counties, states) while thesetEcontains edges representing relationships between the nodes. Theserelationships static or dynamic. Static edges could be defined an edgebetween city and county that the city is part of or two counties that shareboarders. Dynamic edges could be defined by time dependent data likehuman mobility between two states. The space and time dependent natureof a pandemic requires us to capture the temporal and spatial featuresthat contributes to the spread. We need to come up with a model thancan reconcile these spatial and temporal features to forecast the countof infections at each granularity levels(cities, counties, states). Dynamicgraph neural networks are explored as a possible approach to make theseforecasts.

## Data Preparation Plan
So far, we have identified the following data sources which will be groupedtogether to create the final data set used for training the model.
CDC State wise daily infection data
- COVID-19 Case Surveillance Public Use Data | Data | Centers for Disease Control and Prevention (cdc.gov)
    - Submission_date,state,tot_cases,conf_cases,prob_cases,new_case,pnew_case,tot_death,conf_death,prob_death,new_death,pnew_death,created_at,consent_cases,consent_deaths
    - 17,641 rows of data.
- Nytimes county level Covid infection data
    - nytimes/covid-19-data: An ongoing repository of data on coronavirus cases and deaths in the U.S. (github.com)
    - date,county,state,fips,cases,deaths
    - 803,684 rows of data.
- Safegraph State visitor monthly data
    - Places Schema (safegraph.com)
    - Year,month,state,num_visits,num_unique_visitors
    - 602 rows of data.
- Safegraph state population weekly data
    - Places Schema (safegraph.com)
    - Date_range_start,date_range_end,state,census_block_group,number_devices_residing
    - 5,062,411 rows of data.

## Runing the project 
Please use Python3 for  data cleaning scripts in Cleaner_scripts. The raw data file is expected to be in the same folder as the scripts. 
For the jupyter noteboks we can use the notebooks from jupyter aong with the packages. you can also use the google collab for running the code.

### ARIMA & LSTM
You can find the ARIMA and LSTM model under ``jupyter/``. Simply run them and and it should generate the ARIMA and LSTM analysis/forecasts.

### GNN
You can find the graph neural network under ``GNN/``. 

|File name|Content|
|---------|-------|
|network.py| Contains class defining the MPNN+LSTM network.|
|model.py| Run this file to train/forecast with the model.|
|hparams.json| File contains hyperparameters to modify the model.|

Other files in under GNN/ include some of our other work.

#### Using model.py

The file ``model.py`` can train or make forecasts using an existing model. You can find an prebuilt model under ``example/model/``. Note that ``hparams.json`` requiers parameter changes based on where the existing model is located. Make sure to change the following params in ``hparam.json`` if required.

|Parameter|Description|
|---------|-----------|
|lossfile|Destination of output for loss file if training the model.|
|forecastfile|Destination for forecast data.|
|checkpoint|Destination of existing model to load.|

There are 1 params that model.py accepts given below. If you modified the params in ``hparams.json`` correctly, you can simply run ``model.py``.
|Parameter|Description|
|---------|-----------|
|--Run|(Train\|Forecast)|

Example:

``python model.py --Run Forecast``
# UCLA_CS_245_Project5
