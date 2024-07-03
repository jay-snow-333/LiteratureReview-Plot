import pandas as pd
import folium
from geopy.geocoders import Nominatim

# 示例数据，实际中请替换为你自己的数据
data = {
    'Country': ['China', 'India', 'United States', 'Indonesia'],
    'Population': [5, 30, 150, 400]
}
df = pd.DataFrame(data)

# 使用 geopy 获取国家的经纬度坐标
geolocator = Nominatim(user_agent="geoapiExercises")

def get_country_coordinates(country):
    location = geolocator.geocode(country)
    return (location.latitude, location.longitude)

# 使用 folium 创建一个世界地图
world_map = folium.Map(zoom_start=2)

# 加载包含国家边界的 GeoJSON 数据，只需加载一次
geo_json_data = 'world-countries.json'
folium.GeoJson(geo_json_data, name='geojson').add_to(world_map)

# 循环处理每个国家
for index, row in df.iterrows():
    country = row['Country']
    population = row['Population']

    # 获取国家的经纬度坐标
    country_coordinates = get_country_coordinates(country)
    # 计算颜色值
    if population <= 50:
        color = '#00FF00'  # 绿色
    elif population <= 75:
        color = '#FFFF00'  # 黄色
    else:
        color = '#FF0000'  # 红色
    # 根据人口数量设置圆的大小
    radius = population / 100  # 人口数量越大，圆越大
    folium.CircleMarker(location=country_coordinates,
                        radius=radius,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.6,
                        # color='grey'
                        ).add_to(world_map)

# 添加一个简单的图例
legend_html = '''
<style>
    .legend {
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 120px;
        height: 60px;
        border: 2px solid grey;
        z-index: 9999;
        font-size: 14px;
        background-color: white;
        padding: 5px;
    }

    .gradient-bar {
        height: 10px;
        width: 100%;
        background: linear-gradient(to right, 
                        rgb(0, 255, 0) 0%, 
                        rgb(255, 255, 0) 50%, 
                        rgb(255, 0, 0) 100%);
    }
</style>

<div class="legend">
    &nbsp; Population <br>
    <div class="gradient-bar"></div>
    <span style="font-size: 10px; color: grey;">Low &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; High</span>
</div>
'''

world_map.get_root().html.add_child(folium.Element(legend_html))

# 保存地图为 HTML 文件，或者直接显示在 Jupyter Notebook 中
world_map.save('world_population_map.html')
world_map
