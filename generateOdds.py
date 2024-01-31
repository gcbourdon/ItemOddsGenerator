import math

class Item:
    def __init__(self, rarity, name):
        self.rarity = rarity
        self.name = name
        self.amount = 0

def distributeBehind(items, amountRemaining, prev, leastRare, deltaMap):
    if len(items) == 0:
        return

    idx = len(items)-1
    item = items[idx]
    if item.rarity == prev.rarity:
        item.amount = prev.amount
        distributeBehind(items[:idx], amountRemaining, item, leastRare, deltaMap)

    elif item.rarity == leastRare:
        keep = max(math.floor(amountRemaining/(idx+1)), 1)
        item.amount += keep
        amountRemaining -= keep
        distributeBehind(items[:idx], amountRemaining, item, leastRare, deltaMap)
    
    else:
        deltaPct = deltaMap[item.rarity - leastRare]
        keep = max(math.floor((amountRemaining/(idx+1)) * deltaPct), 1)
        item.amount += keep
        amountRemaining -= keep
        distributeBehind(items[:idx], amountRemaining, item, leastRare, deltaMap)
        
def generate(items, totalItems):
    if len(items) == 0:
        return None

    # determine least rare
    leastRare = min(set([item.rarity for item in items]))

    # apply item amount
    baseAmount = math.floor(totalItems / len(items))
    deltaMap = {1: 0.25, 2: .50, 3: .15, 4: .05}
    prev = None
    for i, item in enumerate(items):
        if prev:
            if item.rarity == prev.rarity:
                item.amount = prev.amount
            elif item.rarity > prev.rarity:
                delta = deltaMap[item.rarity - leastRare]
                keep = max(math.floor(baseAmount * delta), 1)
                item.amount += keep
                amountRemaining = baseAmount - keep
                distributeBehind(items[:i], amountRemaining, item, leastRare, deltaMap)
        else:
            item.amount = baseAmount

        prev = item
    
    # calculate amount of most common
    leastRareAmount = len(list(filter(lambda item: (item.rarity == leastRare), items)))

    # distribute remaining padding to most common
    amountDistributed = 0
    for item in items:
        amountDistributed += item.amount

    remaining = totalItems - amountDistributed
    padding = math.floor(remaining/leastRareAmount)
    for item in items:
        if item.rarity != leastRare:
            break
        item.amount += padding
    
    # distributing any remainders across items
    amountDistributed = 0
    for item in items:
        amountDistributed += item.amount
    remaining = totalItems - amountDistributed
    while remaining > 0:
        for item in items:
            item.amount += 1
            remaining -= 1
            if remaining <= 0:
                break
                
    amount = 0
    for item in items:
        amount += item.amount
    
    print(f"total amount distributed: {amount}")

def main():
    itemRarities = [1,1,1,1,1,2,2,2,3,3,3,4,4,5]
    itemNames = ['itemA', 'itemB', 'itemC', 'itemD', 'itemE', 'itemG', 'itemH', 'itemI', 'itemJ', 'itemK', 'itemL', 'itemM', 'itemN', 'itemO']
    items = []
    for i, rarity in enumerate(itemRarities):
        item = Item(rarity, itemNames[i])
        items.append(item)

    # generate item distributions
    generate(items, 10000)

    amountMap = {item.name: item.amount for item in items}
    print(amountMap)
if __name__ == '__main__':
    main()
