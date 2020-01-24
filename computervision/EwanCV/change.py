# lower_green = np.array([15, 30, 200])
#     upper_green = np.array([30, 90, 255])
#
#     mask = cv2.inRange(hsv, lower_green, upper_green)
#     kernel = np.ones((7, 7), np.uint8)
#     dilatemask = cv2.dilate(mask, kernel, iterations=1)
#     resg = cv2.bitwise_and(frame, frame, mask=dilatemask)
#     cv2.imshow('green', resg)
#     resg2 = cv2.bitwise_and(edges, edges, mask=dilatemask)
#
#     greencnts = cv2.findContours(resg2.copy(),
#                                   cv2.RETR_EXTERNAL,
#                                   cv2.CHAIN_APPROX_SIMPLE)[-2]
#     if len(greencnts) > 0:
#         green_area = max(greencnts, key=cv2.contourArea)
#         (xg, yg, wg, hg) = cv2.boundingRect(green_area)
#         # if hg > 137:
#         print(hg)
#         print(wg)
#
#     #if 135 > hg > 125 and 40 > wg > 30:
#     gready = True
#     greenx = xg
#     greeny = yg
#     greenh = hg
#     greenw = wg
#     greencx = int(greenx + (greenw / 2))
#     greency = int(greeny + (greenh / 2))
#     print('done')
#
#     if gready:
#         cv2.rectangle(frame, (greenx, greeny), (greenx + greenw, greeny + greenh), (0, 0, 255), 2)
#         cv2.circle(frame, (greencx, greency), 1, (0, 0, 255), 3)