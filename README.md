# Predicting Pension Funded Status

## Background and Motivation
The Pension Benefit Guarnty Corporation (PBGC) is a U.S. government agency tasked with insuring the pensions of roughly 40 million Americans across nearly 24,000 pension plans.  The PBGC provides government-mandated coverage for privately sponsored pension plans and charges premium amounts determined by Congress.  Plan sponsors are obligated to report plan funding information determined from an actuarial valuation of the plan annually to the PBGC.  However, the PBGC and plan participants may be interested in knowing (or estimating) the funded status of their plan between annual valuation points.
The PBGC requires plan sponors to provide advance and/or post-event notice for certain qualifying events deemed <a href = "https://www.pbgc.gov/prac/reporting-and-disclosure/reportable-events">Reportable Events</a>.  In addition the PBGC maintains an <a href = "https://www.pbgc.gov/prac/risk-mitigation">Early Warning Program </a> whereby it monitors a variety of corporate transactions and events that may pose an increased risk to the funding of a particular plan, or even to the system at large.  
Per its website on the  <a href = "https://www.pbgc.gov/prac/risk-mitigation">Early Warning Program </a>, the PBGC indicates it learns of such transactions through its own monitoring efforts, reports in the financial press, and notices provided by companies as reportable evnets.

## The Problem
I want to use publicly available data on pension plan sponsors to predict the funded status of their pension plan at a given point in time.  I will rely primarily on SEC filings.

## Data Sources
<ul>
<li><a href = "https://www.pbgc.gov/open/index">PGGC Open Data</a></li>
<li><a href = "https://www.pbgc.gov/about/budget-performance-and-planning/statebystate"> PBGC benefits paid across number of retirees by congressional district per state</a></li>
<li><a href = "https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets">US DOL Form 5500 Annual Return/Report of Employee Benefit Plan</a></li>
<li><a href = "https://www.sec.gov/dera/data/financial-statement-data-sets.html">SEC Filings</a></li>
</ul>

## Presentation
I plan to present the results of this study using slides and a Flask web app.