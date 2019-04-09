def getPageranks(urteilListe):
        pagerankPattern = "\d StR \d+/\d+"
        pagerankdict = defaultdict(int)
        for urteil in urteilListe:
            references = re.findall(pagerankPattern, urteil.gruende)
            for ref in references:
                pagerankdict[ref] += 1
        return(pagerankdict)