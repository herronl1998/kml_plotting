import os
import pandas 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

pickle_file_path = './data/pickle/' #path to the data
save_file_path = './figures/' #path to where figures will be output
alt_thresh = 3200.5 #threshold for above vs below altitude (in meters); 10000ft = 3048m; using 3200 for safety
marker_size = .5

###load the data
all_data = pandas.DataFrame()
for filename in os.listdir(pickle_file_path):
    abs_path = os.path.abspath(pickle_file_path + filename)
    data = pandas.read_pickle(abs_path)
    all_data = pandas.concat([all_data, data])
#parse the data so only USAF flights are included
all_data = all_data.loc[all_data['mission_id'].str.startswith('AF')]


def m_to_f(m):
    f = 3.28084 * m
    return f

###plot the data
above_10k = all_data.loc[all_data['plane_z'] > alt_thresh] 
below_10k = all_data.loc[all_data['plane_z'] <= alt_thresh]

#all tracks
fig = plt.figure(figsize = (30,10))
ax = fig.add_subplot(projection = ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND)
ax.gridlines(draw_labels = True)
ax.scatter(all_data['lon'], all_data['lat'], c = 'blue', s = marker_size, label = f'All Tracks')
ax.legend()
plt.title('Tracks (2020-2023)')
plt.savefig(os.path.abspath(save_file_path + 'all_tracks.png'), bbox_inches = 'tight')

#both
fig = plt.figure(figsize = (30,10))
ax = fig.add_subplot(projection = ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND)
ax.gridlines(draw_labels = True)
ax.scatter(above_10k['lon'], above_10k['lat'], c = 'red', s = marker_size, label = f'> {round(m_to_f(alt_thresh))}ft')
ax.scatter(below_10k['lon'], below_10k['lat'], c = 'green', s = marker_size, label = f'<= {round(m_to_f(alt_thresh))}ft')
ax.legend()
plt.title(f'Tracks Above vs Below {round(m_to_f(alt_thresh))}ft (2020-2023)')
plt.savefig(os.path.abspath(save_file_path + 'both.png'), bbox_inches = 'tight')

#above
fig = plt.figure(figsize = (30,10))
ax = fig.add_subplot(projection = ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND)
ax.gridlines(draw_labels = True)
ax.scatter(above_10k['lon'], above_10k['lat'], c = 'red', s = marker_size, label = f'> {round(m_to_f(alt_thresh))}ft')
ax.legend()
plt.title(f'Tracks Above {round(m_to_f(alt_thresh))}ft (2020-2023)')
plt.savefig(os.path.abspath(save_file_path + 'above.png'), bbox_inches = 'tight')

#below
fig = plt.figure(figsize = (30,10))
ax = fig.add_subplot(projection = ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND)
ax.gridlines(draw_labels = True)
ax.scatter(below_10k['lon'], below_10k['lat'], c = 'green', s = marker_size, label = f'<= {round(m_to_f(alt_thresh))}ft')
ax.legend()
plt.title(f'Tracks Below {round(m_to_f(alt_thresh))}ft (2020-2023)')
plt.savefig(os.path.abspath(save_file_path + 'below.png'), bbox_inches = 'tight')


