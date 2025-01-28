
modeh = [{'pred': 'flies', 'n': '*', 'type': 'bird', 'sign': '+'}]

background = [['clause', {'head': {'pred': 'bird', 'term': 'X'}, 'tail': {'pred': 'penguin', 'term': 'X'}}], 
            ['fact', {'pred': 'bird', 'term': 'a'}], 
            ['fact', {'pred': 'bird', 'term': 'b'}], 
            ['fact', {'pred': 'bird', 'term': 'c'}], 
            ['fact', {'pred': 'penguin', 'term': 'd'}]]

examples = [{'pred': 'flies', 'term': 'a'},
            {'pred': 'flies', 'term': 'b'},
            {'pred': 'flies', 'term': 'c'},
            {'pred': 'flies', 'term': 'd', 'negation': True}]


for mh in modeh:
    pred = modeh['pred']
    type = modeh['type']
    p_clause = {'head': {'pred': pred, 'term': 'X'}, 'tail1': {'pred': pred + "*", 'term': 'X'}, 'tail2': {'pred': pred + "'", 'term': 'X'}}
    p_star_clause = {'head': {'pred': pred+'*', 'term': 'X'}, 'tail': {'pred': 'penguin', 'term': 'X'}}
    
    for e in examples:
        
        p_star = mh
