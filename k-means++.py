import math
import pprint
import random


def cal_distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


def cal_distances(pt, pts):
    return [cal_distance(pt, _pt) for _pt in pts]


def cal_centroid(pts):
    centroid = [0, 0]
    for pt in pts:
        centroid[0] += pt[0]
        centroid[1] += pt[1]
    centroid[0] /= len(pts)
    centroid[1] /= len(pts)
    return centroid


pts = dict(
    a=dict(centroid=None, value=(-5.379713, -3.362104)),
    b=dict(centroid=None, value=(-3.487105, -1.724432)),
    c=dict(centroid=None, value=(0.450614, -3.302219)),
    d=dict(centroid=None, value=(-0.392370, -3.963704)),
    e=dict(centroid=None, value=(-3.453687, 3.424321)),
)

K = 3
random.seed(0)
pt_names = list(pts.keys())
# centroids = [random.choice([pt["value"] for pt in pts.values()])]
centroids = [pts["d"]["value"]]
print(centroids)

for i in range(K - 1):
    total_dists = []
    for pt_name in pt_names:
        pt_info = pts[pt_name]
        pt_value = pt_info["value"]
        # 计算与现有质心的距离集合
        dists = cal_distances(pt_value, centroids)
        # 选择最短距离并记录
        min_dist = None
        for dist in dists:
            if min_dist is None or dist < min_dist:
                min_dist = dist
        total_dists.append(min_dist)

    # 接下来是根据各点对应的最小距离确定点采样的概率。
    # 如何根据权重来确定概率，实现这点的算法有很多，其中比较简单的是轮盘法。
    # 轮盘赌法：即将所有样本各自对应的权重值等价为轮盘区块的面积，并使用一个0~1均匀采样获得最终的概率采样。
    # 这一过程就类似于轮盘指针的旋转。这里的实现实际上是按照累计概率的方式进行的。
    sample_dist = sum(total_dists) * random.random()
    for i, dist in enumerate(total_dists):
        sample_dist -= dist
        if sample_dist <= 0:
            centroid_name = pt_names[i]
            centroid_value = pts[centroid_name]["value"]
            break
    centroids.append(centroid_value)

print("初始质心：", centroids)

iteration = 0
while True:
    print("Start Iteration: ", iteration)
    # 根据执行计算各点与当前质心的距离，并按照最短距离判定各点属于哪个质心
    for pt_name, pt_info in pts.items():
        pt_value = pt_info["value"]
        if pt_value in centroids:
            pts[pt_name]["centroid"] = pt_value
            continue

        min_dist_pt_to_centroids = None
        pt_centroid_value = None
        for centroid_value in centroids:
            dist = cal_distance(pt_value, centroid_value)
            if pt_centroid_value is None or dist < min_dist_pt_to_centroids:
                min_dist_pt_to_centroids = dist
                pt_centroid_value = centroid_value
        pts[pt_name]["centroid"] = pt_centroid_value

    # 更新质心
    new_centroids = []
    for centroid_value in centroids:
        pt_group = []
        for pt_name, pt_info in pts.items():
            if pt_info["centroid"] == centroid_value:
                pt_group.append(pt_info["value"])
        new_centroid = cal_centroid(pt_group)
        new_centroids.append(new_centroid)
        for pt_name, pt_info in pts.items():
            if pt_info["centroid"] == centroid_value:
                pt_info["centroid"] = new_centroid

    # print(new_centroids)
    pprint.pprint(pts)

    if sum([cal_distance(c, new_c) for c, new_c in zip(centroids, new_centroids)]) == 0:
        break

    centroids = new_centroids
    iteration += 1

print("Kmeans Over")
