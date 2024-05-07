# Fair Grants, an open data pipeline

![DataPipeline](gif/DataPipeline.gif)

Fair Grants is an open data pipeline to mitigate fraud in permissionless quadratic funding of public goods.

Quadratic funding serves as a more egalitarian approach to financing public goods, championing the democratization of contributions. It amplifies the influence of smaller donors, thereby diminishing the stronghold of plutocracy. Moreover, it fosters a more efficient allocation of funds as donors are incentivized to contribute to multiple projects.
However, like all strategies, quadratic funding isn't impervious to challenges - particularly fraudulent activities such as Sybil attacks. In these scenarios, fraudsters fabricate numerous accounts, feigning widespread public support for their projects to amass larger matching funds. The intricacies of quadratic grants and the possibility for participant collusion render these grants notably vulnerable to such attacks.

To counteract this growing concern, Fair Grants has pioneered a solution: an open data pipeline. This groundbreaking system streamlines the automated tracking of voters for specific grants and distills transaction data to more accurately determine voter qualification. The function of this pipeline is dual-pronged: it empowers grant operators to pinpoint and respond to fraudulent behavior promptly and furnishes a trustworthy data source for fraud data scientists seeking to identify novel fraudulent schemes.

Gitcoin has recently unveiled the 'allo' protocol, empowering anyone to initiate these grants on the blockchain. This development necessitates that new grant round operators are equipped with tools to transparently monitor and identify suspicious activities. Fair Grants rises to this challenge, offering a compelling solution.

# Technical details

The Fair Grants pipeline is built on a Python backend, leveraging the Flask framework. We use the Gitcoin API to fetch grant data and the thegraph API to fetch blockchain data. The data is stored in a PostgreSQL database. 

Basicelly the pipeline is divided into 3 main components:

1. Data Fetching: Fetches data from the Gitcoin API and thegraph API.
2. Data Processing: Processes the fetched data to identify fraudulent activities.
3. Data Visualization: Visualizes the processed data to help grant operators identify fraudulent activities.