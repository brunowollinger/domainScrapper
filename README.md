## Description

- Download the free list of newly registered domains from [whoisds.com]('https://www.whoisds.com/newly-registered-domains');
- Apply the Levenshtein algorithm using a provided domain and the downloaded list;
- Output the results to a .csv which can help to identify phishing domains.

## Usage

Provide the target domain as a command line argument:

```
python3 domainScrapper.py example.com
```

A .csv file will be generated on `reports/`
