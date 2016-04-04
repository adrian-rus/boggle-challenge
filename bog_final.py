from random import choice
from string import ascii_uppercase
import time

import logging


logging.basicConfig(level=logging.INFO)


def timeit(method):
    def timed(*args, **kw):
        t1 = time.time()
        result = method()
        print '%r %2.2f sec' % (method.__name__, time.time()-t1)
        return result
    return timed


def get_grid():
    return {(x, y): choice(ascii_uppercase) for x in range(X) for y in range(Y)}


def get_neighbours():
    neighbours = {}

    for position in grid:
        x, y = position
        positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                     (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
        neighbours[position] = [p for p in positions if 0 <= p[0] < X and 0 <= p[1] < Y]
    return neighbours


def path_to_word(path):
    return ''.join([grid[p] for p in path])


def search(path):
    word = path_to_word(path)
    logging.debug('%s: %s' % (path, word))
    if word not in stems:
        return
    if word in dictionary:
        paths.append(path)
    for next_pos in neighbours[path[-1]]:
        if next_pos not in path:
            search(path + [next_pos])
        else:
            logging.debug('%s: skipping %s because in path' % (path, grid[next_pos]))

@timeit
def get_dictionary():
    stems, dictionary = set(), set()

    with open('words.txt') as f:
        for word in f:
            word = word.strip().upper()
            dictionary.add(word)

            for i in range(len(word)):
                stems.add(word[:i+1])
    return dictionary, stems


@timeit
def get_words():
    for position in grid:
        logging.info('searching %s' % str(position))
        search([position])
    return [path_to_word(p) for p in paths]


def print_grid(grid):
    s = ''
    for y in range(Y):
        for x in range(X):
            s += grid[x, y] + '  '
        s += '\n'
    print s


size = X, Y = 8, 8

grid = get_grid()


def replace(grid):
    for i in grid:
        if grid[i] == 'Q':
            grid[i] = 'QU'
    return grid

replace(grid)
print_grid(grid)

neighbours = get_neighbours()
dictionary, stems = get_dictionary()
paths = []


def remove_duplicates(values):
    final = []
    seen = set()
    for value in values:
        if value not in seen:
            final.append(value)
            seen.add(value)
    return final

words = remove_duplicates(sorted(get_words()))

print len(words), 'Words: ', words

"""Must finish challenges"""