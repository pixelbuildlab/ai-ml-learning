from sentence_transformers import SentenceTransformer
import numpy as np

sentences = ["I was driving a Toyota", "Shoes are black in color"]

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
cats, dogs = model.encode(sentences)
print(cats.shape)


def find_similarity(a, b):
    # num
    # A.B
    # dem
    # |A|.|B|
    # res = num/dem
    num = np.dot(a, b)
    dem = np.linalg.norm(a) * np.linalg.norm(b)
    return num / dem


def find_dist(sim):
    return 1 - sim


sim = find_similarity(cats, dogs)
print(sim)
