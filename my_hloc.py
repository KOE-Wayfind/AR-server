# import tqdm, tqdm.notebook
# tqdm.tqdm = tqdm.notebook.tqdm  # notebook-friendly progress bars
from pathlib import Path

from hloc import extract_features, match_features, reconstruction, visualization, pairs_from_exhaustive
from hloc.visualization import plot_images, read_image
# from hloc.utils import viz_3d
import numpy as np
import pycolmap
from hloc.localize_sfm import QueryLocalizer, pose_from_cluster

images = Path('koe-datasets/raw')
outputs = Path('outputs/demo/')
sfm_pairs = outputs / 'pairs-sfm.txt'
loc_pairs = outputs / 'pairs-loc.txt'
sfm_dir = outputs / 'sfm'
features = outputs / 'features.h5'
matches = outputs / 'matches.h5'

# feature_conf = extract_features.confs['superpoint_aachen'] # for outdoor
feature_conf = extract_features.confs['superpoint_inloc'] # for indoor
matcher_conf = match_features.confs['superglue']

landmark = "e1-l2-conference-room-b*.jpg" # Use * for wildcard
references = [str(p.relative_to(images)) for p in (images / 'day/').glob(landmark)]
print(references)
print(len(references), "mapping images")
plot_images([read_image(images / r) for r in references], dpi=25)

extract_features.main(feature_conf, images, image_list=references, feature_path=features)
pairs_from_exhaustive.main(sfm_pairs, image_list=references)
match_features.main(matcher_conf, sfm_pairs, features=features, matches=matches);

model = reconstruction.main(sfm_dir, images, sfm_pairs, features, matches, image_list=references)

query = 'night/e1-l2-conference-room-b_3.jpg'

references_registered = [model.images[i].name for i in model.reg_image_ids()]
extract_features.main(feature_conf, images, image_list=[query], feature_path=features, overwrite=True)
pairs_from_exhaustive.main(loc_pairs, image_list=[query], ref_list=references_registered)
match_features.main(matcher_conf, loc_pairs, features=features, matches=matches, overwrite=True);

camera = pycolmap.infer_camera_from_image(images / query)
ref_ids = [model.find_image_with_name(n).image_id for n in references_registered]
conf = {
    'estimation': {'ransac': {'max_error': 12}},
    'refinement': {'refine_focal_length': True, 'refine_extra_params': True},
}
localizer = QueryLocalizer(model, conf)
ret, log = pose_from_cluster(localizer, query, camera, ref_ids, features, matches)

n = len(log['db'])
inliers = np.array(log['PnP_ret']['inliers'])
counts = n = len(log['db'])

# display the database images with the most inlier matches
db_sort = np.argsort(-counts)
for db_idx in db_sort[:2]:
  db = model.images[log['db'][db_idx]]
  db_name = db.name
  print(db_name)