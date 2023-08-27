import geopy
import geojson
import geopandas
import overpy
import movingpandas
import prefect
from prefect import flow, task
from typing import List
import httpx

print('Geopy version:{}'.format(geopy.__version__))
print('Geojson version:{}'.format(geojson.__version__))
print('Geopandas version:{}'.format(geopandas.__version__))
print('Overpy version:{}'.format(overpy.__version__))
print('Movingpandas version:{}'.format(movingpandas.__version__))
print('Prefect version:{}'.format(prefect.__version__))


from shapely.geometry import Point
d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")

print('Current CRS:{}'.format(gdf.crs))
gdf.to_crs(3857,inplace=True)
print('Current CRS:{}'.format(gdf.crs))
gdf.to_crs(4326,inplace=True)
print('Current CRS:{}'.format(gdf.crs))
from geopy.distance import geodesic
print('Distance between the two points is:{}'.format(geodesic(gdf.loc[0]['geometry'].coords,gdf.loc[1]['geometry'].coords).miles))


@task(retries=3)
def get_stars(repo: str):
    url = f"https://api.github.com/repos/{repo}"
    count = httpx.get(url).json()["stargazers_count"]
    print(f"{repo} has {count} stars!")


@flow(name="GitHub Stars")
def github_stars(repos: List[str]):
    for repo in repos:
        get_stars(repo)


# run the flow!
github_stars(["PrefectHQ/Prefect"])
