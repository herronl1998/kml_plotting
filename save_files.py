import tropycal
import tropycal.tracks


###get the data and save it as pickle files
years = [2023, 2022, 2021, 2020]
basin_key = 'both'

basin = tropycal.tracks.TrackDataset(basin_key)
for year in years:
    season = basin.get_season(year)
    season_summary = season.summary()
    storm_ids = season_summary['id']
    for storm_id in storm_ids:
        storm = basin.get_storm(storm_id)
        try: #get_hdobs is liable to fail if there are no obs
            storm.recon.get_hdobs() #populates the storm object with the obs (takes some time)
            storm.recon.hdobs.to_pickle(f'./data/pickle/{storm.name}{storm.year}_hdobs.pickle')
        except:
            continue