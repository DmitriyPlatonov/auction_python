__author__ = 'Dmitriy Platonov'
import copy
import random
import unittest


def max_index(arr, value):
    # finding the max index of the array element (arr - prices array, value - max element)
    # if there are several equal max prices, returns the index of random one
    index = []
    for i in range(len(arr)):
        if arr[i] == value:
            index.append(i)
    if len(index) == 1:
        return index[0]
    else:
        return random.choice(index)


def input_validation(creatives):
    b = True
    if len(creatives) == 0:
        b = False
    for i in range(len(creatives)):
        if len(creatives[i]) < 2:
            b = False
            break
    return b


def auction(creatives, winnersnum, *country):
    # finding the winners (creatives - [price,id,country], winnersnum - number of winners, country - *optional)
    competitors = []  # creatives which can be among winners
    winners = []
    if not input_validation(creatives):  # input data validation
        return []
    if len(country) > 0:
        for i in range(len(creatives)):
            if len(creatives[i]) == 2:  # if creative has no country
                competitors.append(creatives[i])
            elif len(creatives[i]) > 2 and creatives[i][2] == country[0]:  # if creative has the same country
                competitors.append(creatives[i])
    else:
        competitors = copy.deepcopy(creatives)
    prices = [list(i) for i in zip(*competitors)][0]
    while winnersnum > 0 and len(competitors) > 0:
        maxVal = max(prices)
        maxInd = max_index(prices, maxVal)
        if len(winners) > 0:
            for i in range(len(winners)):  # unique id check
                if competitors[maxInd][1] == winners[i][1]:
                    break
                elif i == len(winners) - 1:
                    winners.append(competitors[maxInd])
                    winnersnum -= 1
        else:
            winners.append(competitors[maxInd])
            winnersnum -= 1
        del competitors[maxInd], prices[maxInd]
    return winners


class Test(unittest.TestCase):
    one_winner = 1
    two_winners = 2
    three_winners = 3

    def test_auction_without_country(self):
        creatives = [[5000, 1], [4900, 2, "Russia"], [4000, 3], [6000, 4, "England"], [9200, 5], [1500, 6], [1900, 7]]
        self.assertEqual(auction(creatives, self.one_winner), [creatives[4]])
        self.assertEqual(auction(creatives, self.two_winners), [creatives[4], creatives[3]])
        self.assertEqual(auction(creatives, self.three_winners), [creatives[4], creatives[3], creatives[0]])

    def test_auction_with_country(self):
        creatives = [[5000, 1], [4900, 2, "Russia"], [4000, 3, "Russia"], [6000, 4, "England"], [9200, 5, "USA"],
                     [1500, 6, "Spain"], [1900, 7]]
        self.assertEqual(auction(creatives, self.one_winner, "Russia"), [creatives[0]])
        self.assertEqual(auction(creatives, self.two_winners, "Russia"), [creatives[0], creatives[1]])
        self.assertEqual(auction(creatives, self.three_winners, "Russia"), [creatives[0], creatives[1], creatives[2]])

    def test_auction_same_id(self):
        creatives = [[5000, 1], [4900, 1, "Russia"], [4000, 2, "Russia"], [6000, 2, "England"], [9200, 2, "USA"],
                     [1500, 2, "Spain"], [1900, 2]]
        self.assertEqual(auction(creatives, self.one_winner), [creatives[4]])
        self.assertEqual(auction(creatives, self.two_winners, "Russia"), [creatives[0], creatives[2]])
        self.assertEqual(auction(creatives, self.three_winners, "Russia"), [creatives[0], creatives[2]])

    def test_auction_wrong_input(self):
        creatives = [[]]
        self.assertEqual(auction(creatives, self.one_winner), [])
        self.assertEqual(auction(creatives, self.two_winners, "England"), [])
        self.assertEqual(auction(creatives, self.three_winners, "Russia", "Spain"), [])

    def test_auction_same_maxprice(self):
        creatives = [[5000, 1], [5000, 2, "Russia"], [3000, 3], [5000, 4, "England"], [4200, 5], [1500, 6], [1900, 7]]
        result = auction(creatives, self.one_winner, "Russia")  # result must be [5000,1] or [5000,2,"Russia"]
        self.assertIn(result[0], [creatives[0], creatives[1]])


if __name__ == '__main__':
    unittest.main()
