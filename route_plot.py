import matplotlib.pyplot as plt
import math

# ======== HÀM HỖ TRỢ ======== #
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # bán kính Trái Đất (km)
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def closest_point_on_segment(A, B, P):
    """Tìm điểm gần P nhất nằm trên đoạn AB (theo toạ độ phẳng xấp xỉ)"""
    x1, y1 = A
    x2, y2 = B
    x0, y0 = P
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return A
    t = ((x0 - x1)*dx + (y0 - y1)*dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))
    return (x1 + t*dx, y1 + t*dy)

# ======== DANH SÁCH CÁC ĐIỂM TUYẾN ĐƯỜNG (tọa độ thực tế) ======== #
points = {
    'A': (21.028, 105.778),  # Mỹ Đình
    'B': (21.025, 105.785),
    'C': (21.021, 105.795),
    'D': (21.018, 105.805),
    'E': (21.015, 105.815),
    'F': (21.011, 105.825),
    'G': (21.007, 105.835),
    'H': (21.004, 105.845),
    'I': (21.000, 105.855),
    'J': (20.994, 105.866)
       # Times City
}

# Vị trí khách: Royal City
points['S'] = (20.992, 105.816)

# ======== TÌM ĐIỂM GẦN NHẤT TRÊN TUYẾN ======== #
route_order = ['A','B','C','D','E','F','G','H','I','J']
customer = points['S']

min_dist = float('inf')
closest_pt = None

# duyệt từng đoạn giữa các điểm liên tiếp
for i in range(len(route_order) - 1):
    A = points[route_order[i]]
    B = points[route_order[i+1]]
    C = closest_point_on_segment((A[1], A[0]), (B[1], B[0]), (customer[1], customer[0]))  # (lon, lat)
    # đổi lại về (lat, lon)
    C = (C[1], C[0])
    d = haversine(customer[0], customer[1], C[0], C[1])
    if d < min_dist:
        min_dist = d
        closest_pt = C

# ======== VẼ TUYẾN ĐƯỜNG ======== #
x = [points[p][1] for p in route_order]  # Kinh độ
y = [points[p][0] for p in route_order]  # Vĩ độ

plt.figure(figsize=(9, 7))
plt.plot(x, y, '-o', color='dodgerblue', linewidth=2, label='Tuyến đường tài xế (≈20 km)')

# ======== VẼ CÁC ĐIỂM ======== #
for name, (lat, lon) in points.items():
    if name == 'S':
        plt.scatter(lon, lat, color='red', s=90, zorder=3, label='Vị trí khách (Royal City)')
        plt.text(lon + 0.001, lat + 0.0005, f'{name}{points[name]}', color='red', fontsize=9)
    else:
        plt.scatter(lon, lat, color='green', s=60, zorder=3)
        plt.text(lon - 0.001, lat + 0.0005, f'{name}', color='green', fontsize=8)

# ======== VẼ ĐIỂM GẦN NHẤT ======== #
plt.scatter(closest_pt[1], closest_pt[0], color='orange', s=100, zorder=4, label='Điểm gần khách nhất')
plt.text(closest_pt[1] + 0.001, closest_pt[0] - 0.0005,
         f'Closest {closest_pt}\n{min_dist:.2f} km', color='orange', fontsize=9)

# ======== CÀI ĐẶT BIỂU ĐỒ ======== #
plt.grid(True, linestyle='--', alpha=0.6)
plt.axis('equal')
plt.xlabel('Kinh độ (Longitude)')
plt.ylabel('Vĩ độ (Latitude)')
plt.title('Tuyến đường tài xế từ Mỹ Đình đến Times City & điểm gần khách nhất')
plt.legend()
plt.tight_layout()
plt.show()

print("📍 Khách:", customer)
print("🎯 Điểm gần nhất trên tuyến:", closest_pt)
print(f"📏 Khoảng cách: {min_dist:.3f} km")
