# # utils.py
# from deepface import DeepFace
# from typing import Optional, Dict
#
# MODELS = [
#     "VGG-Face",
#     "Facenet",
#     "Facenet512",
#     "OpenFace",
#     "DeepFace",
#     "DeepID",
#     "ArcFace",
#     "Dlib",
#     "SFace",
#     "GhostFaceNet"
# ]
#
# DISTANCE_METRIC = "euclidean_l2"
# THRESHOLD = 0.75
#
#
# def verify_face(img_path: str, user_photos: Dict[str, str]) -> Optional[str]:
#     """
#     Проверяет, совпадает ли лицо на img_path с лицами в базе данных.
#     Возвращает имя пользователя, если совпадение найдено, иначе возвращает None.
#     """
#     print(f"Verifying face for image: {img_path}")
#     for model_name in MODELS:
#         for username, photo_path in user_photos.items():
#             print(f"Using model {model_name} to compare {img_path} with {photo_path}")
#             try:
#                 result = DeepFace.verify(
#                     img1_path=img_path,
#                     img2_path=photo_path,
#                     model_name=model_name,
#                     distance_metric=DISTANCE_METRIC
#                 )
#                 print(f"Result for {username}: {result}")
#
#                 if result["verified"]:
#                     return username
#
#             except Exception as e:
#                 print(f"Error verifying face for {username} using model {model_name}: {e}")
#
#     return None
