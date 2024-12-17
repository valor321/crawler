# crawler
asses3

OPTIMISATION

in the "load graph" function - i changed the "'url = node[0]' and 'target = node[1]'" to url, target = node[0], node[1]
to save time on unloading them separately 

I also changed the 'graphL = {}' to 'graphL = defaultdict(list)' which makes it more efficient
it also means I don't have to check if the url already exists. this means I can have one line code instead of three
" if url in graphL:
                    graphL[url].append(target)
                else:
                    #otherwise created a new dic value
                    graphL[url] = [target]

"
and now it is 
"graphL[url].append(target)"

in the "stochastic_page_rank" - i changed the 'hit_count = {node: 0 for node in graphP}' into 'hit_count = defaultdict(int)'
which means it only has to store 'ints' which makes it more efficient

in the "distribution_page_rank" - i changed the   "node_prob = {node: 1/len(graphD) for node in graphD}" into "node_prob = defaultdict(float, {node: 1/len(graphD) for node in graphD})"
which means it doesn't have to check what value it is so it is more efficient 
i also changed "next_prob = {node: 0 for node in graphD}" into "next_prob = defaultdict(float)" which makes it more efficient

