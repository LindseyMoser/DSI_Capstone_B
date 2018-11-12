# Predicting Pension Funded Status

## Background and Motivation
<p>The Pension Benefit Guarnty Corporation (PBGC) is a U.S. government agency tasked with insuring the pensions of roughly 40 million Americans across nearly 24,000 pension plans.  The PBGC provides government-mandated coverage for privately sponsored pension plans and charges premium amounts determined by Congress.  Plan sponsors are obligated to report plan funding information determined from an actuarial valuation of the plan annually to the PBGC.  However, the PBGC and plan participants may be interested in knowing (or estimating) the funded status of their plan between annual valuation points.</p>
<p>The PBGC requires plan sponors to provide advance and/or post-event notice for certain qualifying events deemed <a href = "https://www.pbgc.gov/prac/reporting-and-disclosure/reportable-events">Reportable Events</a>.  In addition, the PBGC maintains an <a href = "https://www.pbgc.gov/prac/risk-mitigation">Early Warning Program </a> whereby it monitors a variety of corporate transactions and events that may pose an increased risk to the funding of a particular plan, or even to the system at large. </p> 
<p>Per its website on the  <a href = "https://www.pbgc.gov/prac/risk-mitigation">Early Warning Program </a>, the PBGC indicates it learns of such transactions through its own monitoring efforts, reports in the financial press, and notices provided by companies as reportable evnets.</p>

## The Problem
I want to use publicly available data on pension plan sponsors to predict the funded status of a pension plan at a given point in time.  I will rely primarily on historical Form 5500 information and current SEC filings.  There are non-trivial costs associated with gathering information for plans which are or may become underfunded; therefore I would like to create a model that allows interested parties to make predictions using free, publicly available data.

## Data Sources and Storage
<ul>
<li><a href = "https://www.pbgc.gov/open/index">PGGC Open Data</a></li>
<li><a href = "https://www.pbgc.gov/about/budget-performance-and-planning/statebystate"> PBGC benefits paid across number of retirees by congressional district per state</a></li>
<li><a href = "https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets">US DOL Form 5500 Annual Return/Report of Employee Benefit Plan</a></li>
<li><a href = "https://www.sec.gov/dera/data/financial-statement-data-sets.html">SEC Filings</a></li>
</ul>
<p>The data is currently being stored in an Amazon S3 bucket.</p>

## Presentation
I plan to present the results of this study using slides and a Flask web app that will allow the user to enter the stock ticker of a Fortune 500 company and get a prediction of the funded status of that company's pension plan.