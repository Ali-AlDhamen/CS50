import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    # i feel like its not needed
    pass


def sample_pagerank(corpus, damping_factor, n):
    samples = {}
    N = len(corpus)
    final = {page: 1/N for page in corpus}
    current_page = corpus[random.choice([page for page in corpus])]
    
    s =0
    while n>s:
        for page in corpus:
            if page in current_page:
                samples[page] = ((1-damping_factor)/N)+ (0.85/len(current_page))
            else:
                samples[page] = round((1-damping_factor)/len(corpus), 5)
        temp = []
        for page , link in samples.items():
            if link == max(samples.values()):
                temp.append(page)
        
        rand = random.choice(temp)
        current_page = corpus[rand]
        final[rand] += 1
        temp.clear()
        s+=1
    for page in corpus:
        final[page]/=n
    return final

    



def iterate_pagerank(corpus, damping_factor):
    N = len(corpus)
    samples = {page:1/N for page in corpus}  
    differnce = 0.001
    sum = 0
    rest = 0
    while True:
        counter = 0
        for main in corpus:
            sum = (1-damping_factor)/N
            rest = 0
            for page in corpus:
                if main in corpus[page]:
                    links = len(corpus[page])
                    rest+= samples[page]/links
            rest *= 0.85
            sum += rest
            if abs(samples[main] - sum) < differnce:
                counter+=1
            samples[main] = sum
        if counter ==N:
            break
    return samples


if __name__ == "__main__":
    main()
