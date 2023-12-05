# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max, sum

# Spark 세션 및 컨텍스트 생성
spark = SparkSession.builder.appName("LikeContentAnalysis").config("spark.sql.session.timeZone", "UTC").getOrCreate()

# 데이터 불러오기
content = spark.read.csv("termproject/data/content_back.csv", header=True, sep=",", inferSchema=True)

# like 열을 기준으로 내림차순 정렬
sorted_content = content.orderBy(col("like").desc())

# 정렬된 결과를 출력
sorted_content.limit(10).collect()  # 예시로 상위 10개의 행만 출력하도록 제한

# like 열의 최대값과 해당하는 company_name 출력
max_like_info = sorted_content.select("company_name", "like").limit(1)
max_like_info.show()

# like 열의 합 출력
content.select(sum("like")).show()
