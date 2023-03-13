
# seoparse - Parse a SEO poisoned URL and find all domains in a cluster

Given an initial URL, fetch, parse and interate
to find all hosts in a malicious cluster.

## Setup

```
python3 -m venv env
source env/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## Run

```bash
./seoparse.py {URL} | tee -a job-$(date +%s).txt
```

## Example Output

```bash
$ ./seoparse.py https://pzkh.geschenkboutique-ohni.de/hymns-about-mercy-and-compassion.html | tee -a job-$(date +%s).txt                             
jobdir=job.pzkh.geschenkboutique-ohni.de.1677603118
PAGE:0 https://pzkh.geschenkboutique-ohni.de/hymns-about-mercy-and-compassion.html
Getting https://pzkh.geschenkboutique-ohni.de/hymns-about-mercy-and-compassion.html
10 page_urls found
PAGE:1 https://dcos.werbetrommel-nordholz.de/property-portfolio-limit-lemonade.html
Getting https://dcos.werbetrommel-nordholz.de/property-portfolio-limit-lemonade.html
0 page_urls found
...
PAGE:1 https://mvo.solidea-lipoedem.de/xenoblade-wiki.html
Getting https://mvo.solidea-lipoedem.de/xenoblade-wiki.html
0 page_urls found
PAGE:1 https://vnbl.modernart-meissen.de/fantasy-novella-submissions.html
Getting https://vnbl.modernart-meissen.de/fantasy-novella-submissions.html
0 page_urls found
URLs found: 11
Base domains found: 10

evatechnology.de
geschenkboutique-ohni.de
juhiwoll.de
mik2017.de
modernart-meissen.de
nd-neurochirurgentag.de
solidea-lipoedem.de
werbetrommel-nordholz.de
werner-saumweber.de
wiederaufnahme-anwalt.de
```

## Notes

When fetching the URLs by hand, it may be necessary to masquerade as Googlebot.

```bash
wget -U "Googlebot/2.1 (+http://www.google.com/bot.html)" {URL}
curl -A "Googlebot/2.1 (+http://www.google.com/bot.html)" {URL}
```

