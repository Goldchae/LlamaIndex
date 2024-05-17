import secret

import logging
import sys
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
import openai

openai.api_key = secret.OPENAI_API_KEY  # secret 모듈에서 API 키 가져오기

# 내부 동작 확인용 로그
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# 기본 코드

# # 데이터 로드
# documents = SimpleDirectoryReader("data").load_data()
# # 인덱스 생성
# index = VectorStoreIndex.from_documents(documents)


# 인덱스 저장소 이용 - 시간/돈 절약하기
# 저장소가 이미 존재하는지 확인
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # 기존 인덱스를 로드
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)


# 인덱스에 대한 질문 응답 엔진 생성
query_engine = index.as_query_engine()
# 질문하기
response = query_engine.query("정은채의 독서 목표에 대해 알려줘")
print(response)
