# NCR Air Quality and EV Fleet Growth: Measuring EVIDA's Impact (2014–Present)

## Problem Statement

I want to answer: "Does early data after the Electric Vehicle Industry Development Act (EVIDA) in 2022 show any measurable change in NCR PM2.5 air quality and fleet composition trends, and is that change significant relative to the continued growth of the overall vehicle fleet?"

My hypothesis is that EVIDA has had a positive but limited effect on air quality in the NCR. Any gains from cleaner vehicles are likely being offset by the simultaneous growth in total vehicle registrations, which means the net improvement in PM2.5 may not yet be statistically significant. If the data confirms this, the findings point to specific next actions: mandating Euro 5 emission standards for new vehicle registrations, setting binding EV fleet share targets per LGU, expanding EVIDA's charging infrastructure mandate, and introducing end-of-life vehicle policies to phase out the oldest and most polluting vehicles from the NCR fleet. If the data instead shows a meaningful improvement in PM2.5 alongside growing EV adoption, the findings would support accelerating EVIDA's implementation timeline, scaling up EV incentives, and using the NCR as a model for replication in other high-density regions in the country.

## Audience

This project is for national government agencies — specifically DOTr, DENR-EMB, and DOE — who need data-grounded evidence to evaluate whether EVIDA's current implementation pace is sufficient, and whether complementary policies are needed to achieve meaningful air quality improvements in the NCR. It is also relevant to the automotive industry for aligning product roadmaps with regulatory direction, and to businesses and LGUs planning supportive infrastructure for accelerated EV adoption.

## KPI or Key Metric

The main metric I want to track is NCR annual average PM2.5 concentration (µg/m³), measured against the share of electric and hybrid vehicles as a percentage of total registered vehicles in the NCR per year.

## Likely Data Source

I will explore the following sources. Note that data coverage varies per source — vehicle fleet data currently runs to 2023 while air quality data extends to present via OpenAQ API:

- DENR-EMB National Air Quality Status Reports (https://air.emb.gov.ph) — annual NCR PM2.5 averages, 2016–2021
- DENR official press releases (https://denr.gov.ph) — NCR PM2.5 averages, 2022–2023
- PSA Compendium of Philippine Environment Statistics, Table 5.8.1 (https://psa.gov.ph) — registered vehicles by fuel type, 2014–2023
- DOE / EVAP Annual EV Industry Reports — EV and hybrid registration counts, 2022–2024
- OpenAQ API (https://api.openaq.org/v3) — station-level PM2.5 readings from NCR EMB stations, 2023–present

## Possible Final Dashboard

The dashboard should help the audience quickly see whether NCR PM2.5 levels declined after EVIDA took effect in 2022, and whether the growth in EV and hybrid vehicle share is large enough to explain any observed change — or whether total fleet growth is canceling out the gains from cleaner vehicles.
