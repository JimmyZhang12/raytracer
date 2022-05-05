Raytracing Project by Jimmy Zhang (jimmyjz2@illinois.edu)

Dependencies:
    numpy
    PIL

This project can be run with:
    python3 main.py

This project will output a "my.jpg" in the current working directory
wherever the programmed is executed from

RayTracer Features:
    Positionable camera	
    Spheres
    Diffuse material	
    Metal material		
    Dielectrics	
    Instances (of spheres)
    Bounding Volume Hierarchy

Files:
    boundingbox.py 
        classes implementing the Bounding Hierarchy Tree
    camera.py
        implements the moveable camera
    main.py
        contains the main driver function, instantiates the world and runs the RayTracer
    objects.py
        classes of physical objects within the world including:
            materials, spheres, textures, the world itself
    util.py
        helper classes including a Vec3 class, and a Ray class
        The ray class represents a ray through 2 Vec3s, a point and direction

    my.png
        The output of the ray RayTracer
        Generated with the following:
            samples_per_pixel = 200
            aspect_ratio = 16.0/9.0
            image_width = 400
            ray_depth = 8
        You can customize the settings by editing the constants marked "PARAMETERS"
        at the start of: run() in main.py
