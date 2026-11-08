import geopandas as gpd
import os
import numpy as np
from libpysal.weights import DistanceBand
from libpysal.weights.util import min_threshold_distance
from esda.moran import Moran
import statsmodels.api as sm
import matplotlib.pyplot as plt
os.environ["SHAPE_RESTORE_SHX"] = "YES"

g = gpd.read_file("/Users/ahmedal-kinani/Desktop/GGR276/A3/Assign3_Data/Peel_Data.shp")

g = g.to_crs(26917)

g["density"] = g["Pop21"] / (g.area / 1e6)

print(g[["Median_a_2", "density"]].describe())
print("-"*100)
coords = np.column_stack([g.centroid.x, g.centroid.y])
threshold = min_threshold_distance(coords)
w = DistanceBand(coords, threshold=threshold, binary=False, alpha=-1.0)

for col in ["Median_a_2", "density"]:
    m = Moran(g[col].values, w, transformation="O")
    print(col, "Moran's I =", round(m.I, 3), "z =", round(m.z_norm, 2), "p =", m.p_norm)
print("-"*100)
X = sm.add_constant(g["density"])
model = sm.OLS(g["Median_a_2"], X).fit()
print(model.summary())
print("-"*100)

resid_norm = Moran(model.resid.values, w, transformation="O")
print(f"Residual Moran's I = {round(resid_norm.I, 3)}, p = {resid_norm.p_norm}")
print("-"*100)
g["resid"] = model.resid
'''vmax = g["resid"].abs().max()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
g.plot(column="Median_a_2", cmap="viridis", legend=True, ax=axes[0])
axes[0].set_title("Median after-tax household income ($)")
g.plot(column="resid", cmap="RdBu", vmin=-vmax, vmax=vmax, legend=True, ax=axes[1])
axes[1].set_title("Regression residuals (blue = above prediction)")
for ax in axes:
    ax.set_axis_off()
plt.savefig("maps.png", dpi=200, bbox_inches="tight")
plt.show()'''
cols = ["CTUID", "Pop21", "Median_a_2", "density", "resid"]
print("Most over-predicted (model guessed too high):")
print(g.sort_values("resid").head(5)[cols])
print("Most under-predicted (model guessed too low):")
print(g.sort_values("resid").tail(5)[cols])
