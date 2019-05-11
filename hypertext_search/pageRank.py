import numpy as np
from scraper import crawlAndCreateMatrix

from .models import WebPage


def pagerankPowerMethod(H, a, eps = 1.0e-8, alpha = 0.85, iterations = 50):
    N = H.shape[1]
    #initial vector
    v = np.ones((N, 1)) / N
    last_v = np.ones((N, 1)) * 100
    cnt = 0
    while True:
        if(np.linalg.norm(v - last_v, 2) < eps or cnt == iterations):
            break
        last_v = v
        x = alpha * np.matmul(H, v)
        v = x + (np.matmul(x, a) + 1 - alpha) * np.ones((N,1)) / N
        cnt += 1

    return v


def pageRank(H, a, eps = 1.0e-8, alpha = 0.85, iterations = 50):
    N = H.shape[1]
    #initial vector
    v = np.ones((N, 1)) / N
    last_v = np.ones((N, 1)) * 100
    cnt = 0
    while True:
        if(np.linalg.norm(v - last_v, 2) < eps or cnt == iterations):
            break
        last_v = v
        v = np.matmul(H, v) + np.matmul(a, np.ones((N,1))) / N
        cnt += 1
        
    return v

def calculateDanglingVector(H):
    a = H.shape[0] * [0]
    for i in range(H.shape[0]):
        if np.count_nonzero(H[i]) == 0:
            a[i] = 1
    return np.asmatrix(a)


def replaceZeros(a, H, num = 1.0e-8):
    a = np.array(a)
    M = H
    for i in range(H.shape[0]):
        if a.item(i) == 0:
            M[i,:] = np.where(M[i,:] == 0, num, M[i,:])
    return M

def match_urls_with_pagerank(urls, page_rank_values):
    mongo_urls = WebPage.objects.all()
    for url in mongo_urls:
        lookup_index = urls.index(url)
        #url.update(rank=page_rank_values.item(lookup_index))
        url.rank = page_rank_values.item(lookup_index)
        url.save()

def start_ranking():
    crawl_urls_tuple = crawlAndCreateMatrix('https://fit.cvut.cz/', 5)
    H_matrix = np.array(crawl_urls_tuple[1])
    dangling_vector = calculateDanglingVector(H_matrix)
    H_matrix_without_zeros = replaceZeros(dangling_vector, H_matrix)
    pageRank_values = pageRank(H_matrix_without_zeros, dangling_vector)
    match_urls_with_pagerank(crawl_urls_tuple[0], pageRank_values)

