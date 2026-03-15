import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.widgets import Button

# ==========================
# 1. CẤU HÌNH CELL (1 cell = 1km)
# ==========================

cellSize = 0.01

def to_cell(lat, lon):
    return int(lat // cellSize), int(lon // cellSize)

def cell_to_latlon(ci, cj):
    return (ci * cellSize, cj * cellSize)


# ==========================
# 2. DỮ LIỆU 10 TUYẾN (SQL)
# ==========================

routes = {
    1001: [(2109,10581),(2108,10582),(2107,10583),(2106,10583),(2105,10584),(2104,10584),(2103,10582),(2100,10581)],
    1002: [(2114,10584),(2113,10583),(2111,10583),(2110,10582),(2109,10582),(2108,10581),(2107,10580),(2106,10579),(2105,10578),(2104,10578)],
    1003: [(2106,10590),(2105,10589),(2105,10588),(2104,10587),(2104,10586),(2103,10585),(2104,10584),(2104,10583),(2105,10582)],
    1004: [(2098,10577),(2099,10578),(2100,10579),(2101,10580),(2102,10581),(2103,10582),(2104,10583),(2105,10583),(2106,10584),(2107,10584)],
    1005: [(2103,10595),(2103,10594),(2103,10593),(2103,10592),(2102,10590),(2102,10589),(2102,10588),(2103,10586),(2103,10585)],
    1006: [(2108,10574),(2107,10575),(2106,10577),(2106,10578),(2105,10579),(2104,10580),(2104,10581),(2103,10583),(2102,10583),(2101,10584)],
    1007: [(2100,10574),(2101,10573),(2102,10572),(2103,10572),(2104,10571),(2105,10571),(2106,10570),(2107,10570),(2108,10570),(2109,10570)],
    1008: [(2095,10584),(2096,10584),(2097,10583),(2098,10583),(2099,10583),(2100,10582),(2101,10582),(2102,10582),(2104,10581),(2105,10581)],
    1009: [(2125,10581),(2124,10582),(2122,10582),(2121,10582),(2120,10582),(2119,10582),(2118,10582),(2116,10583),(2115,10584),(2114,10584)],
    1010: [(2105,10590),(2105,10589),(2104,10588),(2104,10587),(2103,10586),(2103,10585),(2104,10584),(2104,10583),(2105,10582),(2106,10582)],
}


# ==========================
# 3. VỊ TRÍ KHÁCH
# ==========================

customerLat = 21.0302
customerLon = 105.85105
customer_cell = to_cell(customerLat, customerLon)
i0, j0 = customer_cell
R = 1

print("Customer cell:", customer_cell)


# ==========================
# 4. TÌM TUYẾN ĐI QUA KHÁCH
# ==========================

candidateRoutes = set()

for rid, cells in routes.items():
    for (ci, cj) in cells:
        if (i0 - R) <= ci <= (i0 + R) and (j0 - R) <= cj <= (j0 + R):
            candidateRoutes.add(rid)
            break

print("Candidate routes:", candidateRoutes)


# ==========================
# 5. TẠO FIGURE – FULLSCREEN
# ==========================

fig, ax = plt.subplots(figsize=(14, 9))

try:
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
except:
    pass

# CHỈNH PADDING CHO TRỤC Y KHÔNG BỊ CHE
fig.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.07)

ax.set_aspect("auto")  # không dùng equal


# ==========================
# 6. VẼ KHÁCH
# ==========================

ax.scatter(customerLon, customerLat, s=120, color="blue", zorder=5)
ax.text(customerLon + 0.0004, customerLat + 0.0004, "Khách", fontsize=11, color="blue")


# ==========================
# 7. VÙNG 3×3 CELL
# ==========================

rect_min_lat = (i0 - R) * 0.01
rect_min_lon = (j0 - R) * 0.01

search_box = patches.Rectangle(
    (rect_min_lon, rect_min_lat), 0.02, 0.02,
    linewidth=2, edgecolor='orange', facecolor='none'
)
ax.add_patch(search_box)


# ==========================
# 8. VẼ CÁC TUYẾN
# ==========================

for rid, cells in routes.items():
    xs, ys = [], []
    for (ci, cj) in cells:
        lat, lon = cell_to_latlon(ci, cj)
        ys.append(lat)
        xs.append(lon)

    color = "red" if rid in candidateRoutes else "gray"
    lw = 2.5 if rid in candidateRoutes else 1.2

    ax.plot(xs, ys, "-o", color=color, linewidth=lw)
    ax.text(xs[-1], ys[-1], str(rid), fontsize=9, color=color, weight="bold")


# ==========================
# 9. AUTO SCALE TRỤC
# ==========================

all_lats, all_lons = [], []

for rid, cells in routes.items():
    for (ci, cj) in cells:
        lat, lon = cell_to_latlon(ci, cj)
        all_lats.append(lat)
        all_lons.append(lon)

all_lats.append(customerLat)
all_lons.append(customerLon)

xmin = min(all_lons) - 0.002
xmax = max(all_lons) + 0.002
ymin = min(all_lats) - 0.002
ymax = max(all_lats) + 0.002

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Lưu để Reset View
full_xmin, full_xmax = xmin, xmax
full_ymin, full_ymax = ymin, ymax


# ==========================
# 10. GHI CHÚ
# ==========================

annot = (
    "Các tuyến màu ĐỎ là tuyến đi qua vị trí khách\n"
    f"Tuyến qua khách: {', '.join(str(r) for r in sorted(candidateRoutes))}"
)

ax.text(
    0.02, 0.98, annot, transform=ax.transAxes,
    fontsize=12, color="red", va='top',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='red')
)


# ==========================
# 11. LEGEND
# ==========================

legend_items = [
    Line2D([0], [0], color="red", lw=3, label="Tuyến đi qua khách"),
    Line2D([0], [0], color="gray", lw=2, label="Tuyến khác"),
    Line2D([0], [0], marker="o", color="blue", markersize=10, lw=0, label="Khách"),
]
ax.legend(handles=legend_items, loc="lower right")


# ==========================
# 12. ZOOM CHUẨN GOOGLE MAPS
# ==========================

zoom_scale = 0.2  # tốc độ zoom

def on_scroll(event):
    if not event.inaxes:
        return
    if event.key != "control":
        return

    ax = event.inaxes
    x = event.xdata
    y = event.ydata

    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()

    x_left, x_right = cur_xlim
    y_bottom, y_top = cur_ylim

    x_range = (x_right - x_left)
    y_range = (y_top - y_bottom)

    if event.button == 'up':      # zoom in
        scale = 1 - zoom_scale
    else:                         # zoom out
        scale = 1 + zoom_scale

    relx = (x - x_left) / x_range
    rely = (y - y_bottom) / y_range

    new_xrange = x_range * scale
    new_yrange = y_range * scale

    new_left = x - relx * new_xrange
    new_right = new_left + new_xrange
    new_bottom = y - rely * new_yrange
    new_top = new_bottom + new_yrange

    ax.set_xlim(new_left, new_right)
    ax.set_ylim(new_bottom, new_top)

    ax.figure.canvas.draw_idle()

fig.canvas.mpl_connect("scroll_event", on_scroll)


# ==========================
# 13. PAN BẰNG CHUỘT TRÁI
# ==========================

is_panning = False
press_x = None
press_y = None

def on_press(event):
    global is_panning, press_x, press_y
    if event.button == 1 and event.inaxes:
        is_panning = True
        press_x = event.xdata
        press_y = event.ydata

def on_release(event):
    global is_panning
    is_panning = False

def on_motion(event):
    if not is_panning or not event.inaxes:
        return

    dx = event.xdata - press_x
    dy = event.ydata - press_y

    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()

    ax.set_xlim(cur_xlim[0] - dx, cur_xlim[1] - dx)
    ax.set_ylim(cur_ylim[0] - dy, cur_ylim[1] - dy)

    ax.figure.canvas.draw_idle()

fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("button_release_event", on_release)
fig.canvas.mpl_connect("motion_notify_event", on_motion)


# ==========================
# 14. NÚT RESET VIEW
# ==========================

reset_ax = plt.axes([0.88, 0.01, 0.11, 0.05])
reset_btn = Button(reset_ax, "RESET VIEW", color="lightgray")

def reset_view(event):
    ax.set_xlim(full_xmin, full_xmax)
    ax.set_ylim(full_ymin, full_ymax)
    ax.figure.canvas.draw_idle()

reset_btn.on_clicked(reset_view)


# ==========================
# 15. HIỂN THỊ
# ==========================

plt.show()


print("\n Tuyến đi qua khách:")
for r in sorted(candidateRoutes):
    print(" -", r)
