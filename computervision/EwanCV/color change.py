bluecnts = cv2.findContours(blue_mask.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

if len(bluecnts) > 0:
    blue_area = max(bluecnts, key=cv2.contourArea)
    (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
    cv2.rectangle(image, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

blue_x = xg
blue_y = yg
blue_height = hg
blue_width = wg

blue_centerx = int(blue_x + (blue_width/2))
blue_centery = int(blue_y + (blue_height/2))

cv2.circle(image, (blue_centerx, blue_centery), 2, (0, 0, 255), 5)