import math
import pprint
import random


def cal_pair_distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


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

# centroids = [pts["b"]["value"], pts["c"]["value"], pts["e"]["value"]]
centroids = random.sample([v['value'] for v in pts.values()], k=K)
print(centroids)

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
            dist = cal_pair_distance(pt_value, centroid_value)
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

    if (
        sum([cal_pair_distance(c, new_c) for c, new_c in zip(centroids, new_centroids)])
        == 0
    ):
        break

    centroids = new_centroids
    iteration += 1

print("Kmeans Over")
