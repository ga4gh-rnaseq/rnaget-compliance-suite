# Rnaget Compliance Suite

Repository for the [rnaget API](https://github.com/ga4gh-rnaseq/schema) Compliance document and test suite and based on the [refget compliance suite](https://github.com/ga4gh/refget-compliance-suite).

## Installing the compliance suite

Installing the compliance suite require downloading (or cloning)
[the source](ihttps://github.com/ga4gh-rnaseq/rnaget-compliance-suite)
from GitHub and running setup.py

```bash
python setup.py install
```

## Running the compliance suite

The following will generate a HTML report for your server and serve said HTML. It will also generate a tarball locally of the report

```bash
rnaget-compliance report -s https://rnaget.server.com/ --serve
```

The following will generate a JSON report of your server:

```bash
rnaget-compliance report -s https://rnaget.server.com/ --json server.json
```

Setting `--json -` will have the compliance suite write the JSON to STDOUT.

## Example report output

An example of the json and html reports can be found in
[report](https://github.com/ga4gh-rnaseq/rnaget-compliance-suite/report].
