from generate_data import generate_datum
from operator import itemgetter
from factors import *


FACTOR_FUC = [location_factor, bedrooms_factor, bathrooms_factor, dwelling_type_factor, living_area_factor, pool_factor, list_price_factor]
WEIGHT = [0.15, 0.15, 0.05, 0.3, 0.2, 0.1, 0.05]
NORMALIZATION = [True, False, False, False, True, False, True]


class ProximitySearch(object):
    """Take a home as input, return its n most similiar homes based on m randomly generated data points."""

    def __init__(self, data_size = 10000):
        self.data_size = data_size
        self.homes = self.generate_homes()


    def generate_homes(self):
        return [generate_datum() for x in xrange(self.data_size)]


    def n_most_similar_homes(self, home, n):
        # A list of similarities between the home and the system generated homes. 
        # similarity is in the form of [(home1_idx, similarity), (home2_idx, similarity), ... ]
        similarity = self.compute_similarity(home)
        # similarity = self.compute_similarity_mp(home, 4)
        # Sort similarity
        similarity.sort(key=itemgetter(1), reverse=True)
        # Return the n most similarity homes
        return [self.homes[h[0]] for h in similarity[:n]]


    def compute_similarity(self, home):
        """Compute the similarity between two homes. The formula used here is based on the home's attributes and their weights.
        The similarity formula can be customized with combinations of different factors.

        similarity(p, q) = w1 * factor1 + w2 * factor2 + ... + wn * factorn
        range of similarity = [0, 1]

        current available factors:
        location_factor, bedroom_factor, bathroom_factor, dwelling_type_factor, living_area_factor, pool_factor, list_price_factor

        w1~wn are the respective weights, which can also be customized in this model. And sum(w1~wn) = 1
        """
        unnormalized_factors = [self.compute_factors(home, other_home) for other_home in self.homes]

        # Compute the normalization constant for each factor.
        normal_const = []
        for idx, n in enumerate(NORMALIZATION):
            if n:
                normal_const.append(1 / max(unnormalized_factors, key=itemgetter(idx))[idx])
            else:
                normal_const.append(1)

        # Compute the final similarity for all homes.
        similarity = []
        for idx, fac in enumerate(unnormalized_factors):
            similarity.append((idx, sum([a*b*c for a,b,c in zip(WEIGHT, normal_const, fac)])))

        return similarity


    def compute_factors(self, p, q):
        """Return a list of unnormalzed similarity factors between two homes."""
        return [f(p, q) for f in FACTOR_FUC]


def main():
    ps = ProximitySearch()
    home = generate_datum()
    n = 10
    print 'Input:\n'
    print home, '\n'

    result = ps.n_most_similar_homes(home, n)
    print 'The ' + str(n) + ' most similar homes:\n'
    for h in result:
        print h

    save_csv(home, result)

def save_csv(home, homes):
    with open('n_most_similar_homes.csv', 'w') as f:
        f.write(",".join(home._fields) + '\n')
        f.write(",".join(map(str,home)) + '\n')
        for h in homes:
            f.write(",".join(map(str, h)) + '\n')

if __name__ == '__main__':
    main()







            
