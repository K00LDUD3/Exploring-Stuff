import numpy as np, matplotlib.pyplot as plt

def Main():
    arr = np.loadtxt("Numbers2.csv", delimiter=",", dtype=float).transpose()
    print(arr.shape)


    z, m_vals, c_vals = Error(arr[0],arr[1])

    z_1d = z.flatten()
    print(f"{z_1d=}")
    print(f"{z_1d.shape=}")

    print(f"{min(z_1d)=}")

    # Create the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    print(f"{m_vals.shape=}\n\n\n{c_vals.shape=}\n\n{z.shape=}")
    print(m_vals)
    # quit()
    ax.plot_surface(m_vals, c_vals, z, cmap='viridis')
    ax.scatter(m_vals, c_vals,z)


    # Set the labels
    # ax.set_xlabel('M')
    ax.set_ylabel('C')
    ax.set_zlabel('Error')

    # Show the plot
    plt.show()
    
def Error(x,y, m_res = 0.1, c_res=0.1):
    m_vals = np.array([i for i in range(int(-2/m_res),int(2/m_res))]) * m_res
    c_vals = np.array([i for i in range(int(-2/c_res),int(2/c_res))]) * c_res
    err = np.zeros((int(4/m_res), int(4/c_res)))
    print(err.shape)
    for i in range(len(m_vals)):
        for j in range(len(c_vals)):
            s = 0
            for k in range(len(y)):
                s += np.square(y[k] - m_vals[i]*x[k]-c_vals[j])
            err[i,j] = s
                    
            pass
    print(err)
    np.savetxt('test.csv', err, delimiter=',') 
    return (err, m_vals, c_vals)


Main()