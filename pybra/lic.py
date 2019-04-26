import numpy as np
try:
    from pybra.external.lic_internal  import line_integral_convolution
except:
    print("""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Error loading lic_internal, please compile it using cython.

Find the package `pybra/external/` and follow the compilation instructions.

A substitude dummy function is provided for the current script to run
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

""")
    def line_integral_convolution(v,t,k):
        return np.one(v[:,:,0].shape)*len(k)/2


def lic(u,v,texture=None,kernel=31):
    nx,ny=u.shape

    if texture is None:
        texture = np.random.rand(nx,ny).astype(np.float32)

    # Kernel
    if type(kernel) is int:
        n=kernel
        kernel = np.sin(np.arange(n)*np.pi/n)
        #For movies:
        #   kernel = np.sin(np.arange(n)*np.pi/n)*(1+np.sin(2*np.pi*freq*(np.arange(n)/float(n)+t)))
        #   kernel = np.sin(np.arange(n)*np.pi/n)*(1+np.sin(2*np.pi*freq*(np.arange(n)/float(n)+t)))
    elif type(kernel) is np.ndarray:
        pass
    else:
        raise Exception('Unsupported kernel type. Kernel should be an integer or a numpy array')
    kernel = kernel.astype(np.float32)

    vectors = np.zeros((nx,ny,2),dtype=np.float32)
    vectors[:,:,0]=u
    vectors[:,:,1]=v

    # calling internal function
    image = lic_internal.line_integral_convolution(vectors, texture, kernel)

    return image



def lic_flow(vectors,len_pix=10):
    """ MANU: was side to side with lic_internal????? """
    vectors = np.asarray(vectors)
    m,n,two = vectors.shape
    if two!=2:
        raise ValueError
    result = np.zeros((2*len_pix+1,m,n,2),dtype=np.int32) # FIXME: int16?
    center = len_pix
    result[center,:,:,0] = np.arange(m)[:,np.newaxis]
    result[center,:,:,1] = np.arange(n)[np.newaxis,:]
    for i in range(m):
        for j in range(n):
            y = i
            x = j
            fx = 0.5
            fy = 0.5
            for k in range(len_pix):
                vx, vy = vectors[y,x]
                print(x, y, vx, vy)
                if vx>=0:
                    tx = (1-fx)/vx
                else:
                    tx = -fx/vx
                if vy>=0:
                    ty = (1-fy)/vy
                else:
                    ty = -fy/vy
                if tx<ty:
                    print("x step")
                    if vx>0:
                        x+=1
                        fy+=vy*tx
                        fx=0.
                    else:
                        x-=1
                        fy+=vy*tx
                        fx=1.
                else:
                    print("y step")
                    if vy>0:
                        y+=1
                        fx+=vx*ty
                        fy=0.
                    else:
                        y-=1
                        fx+=vx*ty
                        fy=1.
                if x<0: x=0
                if y<0: y=0
                if x>=n: x=n-1
                if y>=m: y=m-1
                result[center+k+1,i,j,:] = y, x
    return result
