image_only = image_basenames - mask_basenames
mask_only = mask_basenames - image_basenames

print("마스크 없는 이미지:", image_only)
print("이미지 없는 마스크:", mask_only)

