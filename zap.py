#!/usr/bin/python
import csv, os, requests, re, datetime
from requests.structures import CaseInsensitiveDict
print("")
print("~ ~ ~ zap.py - zero access provider ~ ~ ~")
print("")
date = datetime.datetime.now()
#ask for a taxonomy key
taxkey = input("What's the taxonomy key for the collection you're analyzing? ")
print("")
#ask user which csv file they want to use
print("Found these csv files: ")
print("")
for file in os.listdir("."):
    if file.endswith(".csv"):
        print(file)
print("")
selectedfile = input("Which csv file do you want to analyze? ")
print("")
#take URLs from csv file and put them in a txt file
print("making a list of URLs in the csv files...")
ga_topics = taxkey + "-ga_topics" + date.strftime("%Y") + date.strftime("%m") + date.strftime("%d") + ".txt"
with open(selectedfile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sourcepage = row['Page Complete URL (CD13)']
        with open(ga_topics, "a") as f1:
            f1.write(sourcepage + "\n")
#ok, now let's grab the sitemap and put it in a txt file
print("")
print("Grabbing a list of URLs in the sitemap for " + taxkey + "...")
sitemapxml = taxkey + "-sitemap" + date.strftime("%Y") + date.strftime("%m") + date.strftime("%d") + ".xml"
with open(sitemapxml, "a") as f2:
    url = "https://ibmdocs-test.mybluemix.net/docs/api/v1/sitemap/" + taxkey
    headers = CaseInsensitiveDict()
    headers["accept"] = "*/*"
    sm = requests.get(url, headers=headers)
    sitemap = str(sm.content).replace("b'", "").replace(">'", "")
    f2.write(sitemap)
#now let's extract the URLs from the <loc> elements and output to sitemap.txt
sitemaptxt = taxkey + "-sitemap" + date.strftime("%Y") + date.strftime("%m") + date.strftime("%d") + ".txt"
with open(sitemapxml, "r") as f2:
    text = f2.read()
    loc = re.findall("<loc>(.*?)</loc>", text)
    outloc = "\n".join(loc)
    with open(sitemaptxt, "a") as f3:
        f3.write(outloc)
print("")
print("Comparing the two URL lists...")
#and now we diff
with open(ga_topics, "r") as f4:
    with open(sitemaptxt, "r") as f5:
        differ = set(f5).difference(f4)
diffout = taxkey + "-diff-" + date.strftime("%Y") + date.strftime("%m") + date.strftime("%d") + ".txt"
with open(diffout, "a") as f6:
    f6.write("It looks like there were zero hits on these topics: " + "\n")
    f6.write("\n")
    for line in sorted(differ):
        f6.write(line)
os.remove(sitemapxml)
#os.remove(stemaptxt)
#os.remove(ga_topics)
print("")
print("Done! Check " + diffout + " for a list of topics that seem to have zero hits.")
