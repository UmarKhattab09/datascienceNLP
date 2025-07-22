import pandas as pd
import glob
def load_subtitles(dataset_path):
  path = glob.glob(dataset_path)

  scripts=[]
  episodenums=[]
  for files in path:
    # print(path)
    with open(files, 'r') as file:
      ass_content = file.readlines()
      ass_content = ass_content[27:]
      lines = [",".join(line.split(',')[9:]) for line in ass_content]
    lines = [line.replace('\\N',' ' ) for line in lines]
    scripts.append(" ".join(lines))
    episodenums.append(int(files.split('-')[-1].split('[')[0]))
        # Defensive check before creating dataframe
    if not scripts or not episodenums:
      raise ValueError("No valid subtitle scripts or episode numbers were parsed.")

  dataframe = pd.DataFrame({'episode': episodenums, 'script': scripts})
  return dataframe



