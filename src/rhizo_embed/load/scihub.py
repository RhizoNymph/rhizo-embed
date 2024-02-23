from scidownl import scihub_download

def download_paper(paper_title):
    paper_type = "title"
    out = "./papers/{}.pdf".format(paper_title)
    scihub_download(paper_title, paper_type=paper_type, out=out)


