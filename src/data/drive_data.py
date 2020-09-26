import os
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

def get_all_csv_as_df_2(folder_key):

  # 1. Authenticate and create the PyDrive client.
  auth.authenticate_user()
  gauth = GoogleAuth()
  gauth.credentials = GoogleCredentials.get_application_default()
  drive = GoogleDrive(gauth)

  # choose a local (colab) directory to store the data.
  local_download_path = os.path.expanduser('~/data')
  try:
    os.makedirs(local_download_path)
  except: pass

  # 2. Auto-iterate using the query syntax
  #    https://developers.google.com/drive/v2/web/search-parameters
  file_list = drive.ListFile(
      {'q': "'"+folder_key+"' in parents"}).GetList()
  
  csv_df_list = []
  for f in file_list:
    # 3. Create & download by id.
    print('title: %s, id: %s' % (f['title'], f['id']))
    fname = os.path.join(local_download_path, f['title'])
    print('downloading to {}'.format(fname))
    f_ = drive.CreateFile({'id': f['id']})
    f_.GetContentFile(fname)

    #Se abre cada archivo
    with open(fname, 'r') as f:
      csv_df_list.append(pd.read_csv(f))

  return csv_df_list

# Gracias Totales
