from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import csv
from io import StringIO

# 영어 단어를 포함하는 정규 표현식
WORD_RE = re.compile(r'[A-Za-z]+', re.UNICODE)

class MRWordFrequencyCount(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.sort_by_frequency_reducer)
        ]

    def mapper(self, _, line):
        line_buffer = StringIO(line)
        reader = csv.reader(line_buffer)
        for row in reader:
            for column in row[4:7]:  # 4번째, 5번째, 6번째 열
                for word in WORD_RE.findall(column):
                    yield (word.lower(), 1)

    def reducer(self, word, counts):
        # 단어의 총 빈도수를 계산
        yield None, (sum(counts), word)

    def sort_by_frequency_reducer(self, _, word_counts):
        # 단어 빈도수에 따라 정렬
        sorted_words = sorted(word_counts, reverse=True)
        for count, word in sorted_words:
            yield word, count

if __name__ == '__main__':
    MRWordFrequencyCount.run()
