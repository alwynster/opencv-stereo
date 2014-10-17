import numpy as np
import parse
import cv2
import matplotlib.pyplot as pp
import images
import math
import timer

def read_velo(frame): #, position):
    # position, heading = position

    # print 'read_velo position', position
    inputfile = open("kitti/velodyne_points/%010d.txt" % frame, 'r')
    velo = list()
    for line in inputfile:
        velo.append(np.array(list(parse.parse("{};{};{};{}\n", line))))
    velo = np.array(velo).astype('float32')
    inputfile.close()
    
    # Convert to measurements
    meas = list()
    for m in velo:
        meas.append(m)
    
    # meas = rotate(meas, heading)
    
    return meas

def rotate(vectors, heading):
    """ Rotate and return vector by heading (roll, pitch, yaw) """
    
    begin = clock()
    
    vectors = np.atleast_2d(vectors)

    roll, pitch, yaw = heading
    roll = float(roll)
    pitch = float(pitch)
    yaw = float(yaw)
    c1 = math.cos(yaw); c2 = math.cos(pitch); c3 = math.cos(roll)
    s1 = math.sin(yaw); s2 = math.sin(pitch); s3 = math.sin(roll)
    
    r1 = np.array([c1 * c3 - c2 * s1 * s3, -c1 * s3 - c2 * c3 * s1, s1 * s2])
    r2 = np.array([c3 * s1 + c1 * c2 * s3, c1 * c2 * c3 - s1 * s3, -c1 * s2])
    r3 = np.array([s2 * s3, c3 * s2, c2]) 

    Qt = np.transpose(np.array([r1, r2, r3]))
        
    for i in range(np.shape(vectors)[0]):
        x, y, z = np.dot(Qt, vectors[i])
        vectors[i, :] = [x, y, z]
        
    # print np.dot(R, np.transpose(np.array([r1, r2, r3])))
    
    # Convert back to map coordinates
    # X, Y, Z = -y, x, z
    
    return vectors

def rotateCam(vectors, heading):
    """ Rotate and return vector by heading (roll, pitch, yaw) """
    
    vectors = np.array(vectors)
    vectors = np.atleast_2d(vectors)
    # from right down forward to right forward up
    trans_vectors = np.transpose(np.array([vectors[:, 2], -vectors[:, 0], -vectors[:, 1]]))
    
    roll, pitch, yaw = heading
    c1 = math.cos(yaw); c2 = math.cos(pitch); c3 = math.cos(roll)
    s1 = math.sin(yaw); s2 = math.sin(pitch); s3 = math.sin(roll)
    
    r1 = np.array([c1 * c3 - c2 * s1 * s3, -c1 * s3 - c2 * c3 * s1, s1 * s2])
    r2 = np.array([c3 * s1 + c1 * c2 * s3, c1 * c2 * c3 - s1 * s3, -c1 * s2])
    r3 = np.array([s2 * s3, c3 * s2, c2]) 
    
#     r1 = np.array([c3 * c1, c3 * s1, -s3])
#     r2 = np.array([s2 * s3 * c1 - c2 * s1, s2 * s3 * s1 + c2 * c1, s2 * c3])
#     r3 = np.array([c2 * s3 * c1 + s2 * s1, c2 * s3 * s1 - s2 * c1, c2 * c3])
    
    Qt = np.transpose(np.array([r1, r2, r3]))
    
    for i in range(np.shape(trans_vectors)[0]):
        x, y, z = np.dot(Qt, trans_vectors[i])
        # from right forward up to right down forward
        vectors[i, :] = [-y, -z, x]
        
    return vectors

def inbounds(x, bounds):
    if x < bounds[0]:
        return False
    elif x > bounds[1]:
        return False
    else:
        return True

def project_velo(data, img_size, R2, T2):

    midx, midy = np.array(img_size)[0:2] / 2.
    output = np.zeros(np.array(img_size)[0:2], dtype='float32')
    for info in data:
        # forward left up
        p = np.array(info)[0:3] # velo coords

        # p = rotateCam(p, heading)
        # velo to cam

        l = math.sqrt(p[0] ** 2. + p[1] ** 2. + p[2] ** 2.)

        p = np.transpose(np.dot(R2, np.transpose(p))) + T2

        # velo to gps 
        # p = np.transpose(np.dot(R, np.transpose(p))) - np.transpose(np.dot(R, np.transpose(T)))
        # forward left up
        # p = p + position

        # right down forward
        xv, yv, zv = p
        
        

        px = f * b / zv
        i = float(yv) / b * px + midx # down
        j = (xv - b/2.) / b * px + midy # right

        if inbounds(i, (0, img_size[0])) and inbounds(j, (0, img_size[1])):
            if zv < 0: continue
            output[int(i), int(j)] = float(px)

    return output

def interpolate(data, num=2):
    ''' Input is disparity map, output is same size disparity map with all unused values
        assigned to the nearest neighbor value '''


    down = downSample(data, num)

    sh = np.shape(data)
    output = np.zeros(sh, dtype=data.dtype)
    for i in range(sh[1]):
        for j in range(sh[0]):
            if data[j, i] > 0:
                output[j, i] = data[j, i]
            else:
                output[j, i] = down[j, i]
    return output
    

def downSample(data, num=3):
    ''' modified pyrdown '''
    output = np.zeros_like(data)
    sh = np.shape(data)
    smaller = np.zeros((sh[0]/num, sh[1]/num), dtype=data.dtype)
    sm = np.shape(smaller)
    # tm = timer.timer(0, sh[0] * sh[1] / 4, True)
    offset = int(num/2)
    for i in range(sh[0]):
        for j in range(sh[1]):
            # tm.progress(i * j + j)
            v = 0

            for x in range(i - offset, i + offset + 1):
                for y in range(j - offset, j + offset + 1):
                    try:
                        v = data[x, y]
                        if v > 0:
                            break
                    except IndexError:
                        break
                if v > 0:
                    break
            output[max(i - offset, 0):min(sh[0], i + offset + 1), max(0, j - offset):min(sh[1], j + offset + 1)] = v
    return output

def consolodate(images):
    ''' consolodate a set of images into a single image with priorities '''
    sh = np.shape(images[0])
    output = np.zeros(sh, dtype=images[0].dtype)
    for i in range(sh[0]):
        for j in range(sh[1]):
            for image in images:
                output[i, j] = image[i, j]
                if output[i, j] > 0:
                    break
    return output

if __name__ == "__main__":
    h = "P_rect_01: "
    h2 = "R: "
    T = None
    R = None
    # , "calib_imu_to_velo.txt",
    for line in file("kitti/calib_cam_to_cam.txt"):
        if line[0:len(h)] == h:
            l = line[len(h)::]
            parts = l.split(" ")
            f = float(parts[0])
            b = float(parts[3]) / -f
            break

    h = "T: "
    h2 = "R: "
    T2 = None
    R2 = None
    for line in file("kitti/calib_velo_to_cam.txt"):
        
        if line[0:len(h)] == h:
            l = line[len(h)::]
            parts = l.split(" ")
            T2 = np.array([float(parts[0]), float(parts[1]), float(parts[2])])
            break
        
        elif line[0:len(h2)] == h2:
            l = line[len(h2)::]
            parts = l.split(" ")
            R2 = np.array([[float(parts[0]), float(parts[1]), float(parts[2])], [float(parts[3]), float(parts[4]), float(parts[5])], [float(parts[6]), float(parts[7]), float(parts[8])]]) 

    print 'T'
    print T2
    print 'R'
    print R2

    __draw__ = False
    start = 40
    end = 40
    tm = timer.timer(start, end, date=True)
    for frame in range(start, end+1):
        tm.progress(frame)
        data = read_velo(frame)
        img = images.fetch_disp('bm', frame, lib='kitti')

        if __draw__:
            cv2.imshow('left', images.fetch_orig(frame, lib='kitti'))
        
        disp = project_velo(data, np.shape(img), R2, T2)
        print 'disp type', disp.dtype
        disps = list()

        disps.append(disp)

        #disps.append(interpolate(disp, 3))
        #disps.append(interpolate(disp, 5))
        #disps.append(interpolate(disp, 7))
        #disps.append(interpolate(disp, 9))
        
        ground = consolodate(disps)

        if __draw__:
            cv2.imshow('disps', images.drawable(img, False))
        
            cv2.imshow('laser', images.drawable(disp, False))
            cv2.imshow('interp', images.drawable(ground, False))
            cv2.waitKey()
        else:
            np.savez('kitti/laser/disp_kitti_la_%05d_sparse.npz' % frame, ground=ground)
            # cv2.imwrite('kitti/laser/disp_kitti_la_%05d.png' % frame, ground)
