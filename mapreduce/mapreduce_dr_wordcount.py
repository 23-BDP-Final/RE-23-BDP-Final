from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordCount(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.map_count, combiner=self.combine_count, reducer=self.reduce_count),
            MRStep(reducer=self.reduce_sort)
        ]

    def map_count(self, _, line):
        for word in line.split():
            yield (word, 1)

    def combine_count(self, word, counts):
        yield (word, sum(counts))

    def reduce_count(self, word, counts):
        yield None,( str(sum(counts)).zfill(6),word)

    def reduce_sort(self, _, pair):
        sorted_pair = sorted(pair,reverse=True)
        for count,word in sorted_pair:
            yield word, count

if __name__ == '__main__':
    MRWordCount.run()
