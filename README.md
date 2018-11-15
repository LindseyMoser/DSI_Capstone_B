<a href="https://www.forbes.com/sites/nextavenue/2018/10/22/the-next-retirement-crisis-americas-public-pensions/#2146b77a26f2"><img src="/images/pension_gamble.jpg" alt="the pension gamble"></a>

<h1> Predicting Pension Funded Status</h1>

<h2> Background and Motivation</h2>
<p>The Pension Benefit Guaranty Corporation (PBGC) is a U.S. government agency tasked with insuring the pensions of roughly 40 million Americans across nearly 24,000 pension plans.  The PBGC provides government-mandated coverage for privately sponsored pension plans and charges premium amounts determined by Congress.  Plan sponsors are obligated to report plan funding information determined from an actuarial valuation of the plan annually to the PBGC.  However, plan participants may be interested in knowing (or estimating) the funded status of their plan between annual valuation points.</p>
<p>The PBGC requires plan sponsors to provide advance and/or post-event notice for certain qualifying events deemed <a href = "https://www.pbgc.gov/prac/reporting-and-disclosure/reportable-events">Reportable Events</a>.  In addition, the PBGC maintains an <a href = "https://www.pbgc.gov/prac/risk-mitigation">Early Warning Program </a> whereby it monitors a variety of corporate transactions and events that may pose an increased risk to the funding of a particular plan, or even to the system at large. </p>
<p>Per its website on the  <a href = "https://www.pbgc.gov/prac/risk-mitigation">Early Warning Program </a>, the PBGC indicates it learns of such transactions through its own monitoring efforts, reports in the financial press, and notices provided by companies as reportable events.</p>
<p>In its <a href ="https://www.pbgc.gov/sites/default/files/pbgc-strategic-plan-2018-2022.pdf">Strategic Plan FY2018-2022</a>, the PBGC indicates that it utilizes stochastic modeling to run many simulations under a variety of economic scenarios to derive a probabilistic forecast.</p>

<h2>The Problem</h2>
<p>Gathering information and performing actuarial valuations for plans which are currently or are projected to become underfunded is costly; therefore I will create a model that allows interested parties to make predictions on a pension plan's funded status using free, publicly available data.</p>
<p>I will use publicly available data on pension plan sponsors covered by the PBGC to predict the funded status of a pension plan at a given point in time.  I will rely primarily on PBGC filings, along with Form 5500 information (filed with the Department of Labor) and Securities and Exchange Commission (SEC) filings.  Since measures of funded status rely on interest rates, I will also use interest rate data from a Kaggle dataset.</p>


<h2>Data Sources and Storage</h2>
<ul>
<li><a href = "https://www.pbgc.gov/open/index">PGGC Open Data</a></li>
<li><a href = "https://www.pbgc.gov/about/budget-performance-and-planning/statebystate"> PBGC benefits paid across number of retirees by congressional district per state</a></li>
<li><a href = "https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/public-disclosure/foia/form-5500-datasets">US DOL Form 5500 Annual Return/Report of Employee Benefit Plan</a></li>
<li><a href = "https://www.sec.gov/dera/data/financial-statement-data-sets.html">SEC Filings</a></li>
<li><a href = "https://www.kaggle.com/sohier/interest-rate-records">Historical federal interest rate records</a></li>
</ul>
<p>The data is currently being stored in an Amazon S3 bucket.</p>

<h2>Anticipated Issues</h2>
<p>The data is derived from multiple sources (DOL, PBGC, SEC), each with distinct IDs within their system.  I anticipate issues linking the sources together.  I plan to try and match on company name, which is available in all data sources and see potential here for using NLP techniques to aid in name matching.  </p>
<p>I will be using a combination of time series data and feature data so there could be multicollinearity of features.  I plan to use PCA and correlation plots to identify and deal with such features.</p>

<!--
<h2>Model Theory</h2>
A particular pension plan's funded status, FS<sub>t</sub> at a given point in time t, can be calculated as:<br>
<p><i>FS<sub>t</sub> = FS<sub>t-1</sub> + g<sub>&Delta;t</sub> + i<sub>&Delta;t</sub> + &alpha;<sub>&Delta;t</sub>+ &sigma;<sub>&Delta;t</sub></i></p>
where:<br>
<ul>
<li>F<sub>t-1</sub> is the funded status at a prior measurement date</li>
<li>g<sub>&Delta;t</sub> is the growth in plan obligation due to active participant accruals since the prior measurement date</li>
<li>i<sub>&Delta;t</sub> is the growth in plan obligation and plan assets due to interest accruals since the prior measurement date</li>
<li>a<sub>&Delta;t</sub> is the excess (or under) performance of plan assets relative to the interest rate used to value plan obligation (since the prior measurement date)</li>
<li>&sigma;<sub>&Delta;t</sub> is the remaining change due to features not otherwise accounted for (i.e. census data changes, plan benefit increases/decreases, etc.)</li>
</ul>
<p>I have access to F<sub>t-1</sub>, g<sub>&Delta;t</sub>, and i<sub>&Delta;t</sub> from historical Form 5500 filings.  Therefore I will need to create models to estimate &alpha;<sub>&Delta;t</sub>, and &sigma;<sub>&Delta;t</sub> in order to estimate FS<sub>t</sub>, the funded status at time t.</p>
<p></p>-->

<h2>Presentation</h2>
<p>I plan to present the results of this study using slides and a Flask web app that will allow the user to enter the stock ticker of a Fortune 500 company and get a prediction of the funded status of that company's pension plan.</p>

<h2>Technology Stack</h2>
<img src="/images/python_img.png" alt="python"> <img src="/images/postgres_img.png" alt="postgres_sql"><img src="/images/numpy_img.png" alt="numpy"><img src="/images/aws_img.png" alt="amazon web services">
