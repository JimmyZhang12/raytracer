Raytracing Project by Jimmy Zhang (jimmyjz2@illinois.edu)

Dependencies:
    Python3.8+
    numpy
    PIL

This project can be run with:
    python3 main.py

    This project will output a "scene.png" in the current working directory


RayTracer Features:
    Positionable camera	
    Spheres
    Planes
    Diffuse material	
    Metal material		
    Dielectrics	
    Instancing
    Bounding Volume Hierarchy
    Textures
    Shadows
    

Files:
    boundingbox.py 
        classes implementing the Bounding Hierarchy Tree
    camera.py
        implements the moveable camera
    main.py
        contains the main driver function, instantiates the world and runs the RayTracer
    materials.py
        classes describing materials and textures
    objects.py
        classes of physical objects within the world and the world itself
    util.py
        helper classes including a Vec3 class, and a Ray class
        The ray class represents a ray through 2 Vec3s, a point and direction

    wood.png
        A wood texture used for the floor plane

    scene_golden.png
        A sample output of the ray RayTracer
        Generated with the following:
            samples_per_pixel = 600
            aspect_ratio = 16.0/9.0
            image_width = 600
            ray_depth = 25
        You can customize the settings by editing the constants marked "PARAMETERS"
        at the start of: RayTracer() in main.py

Remarks:
    My raytracer follows the architecture decribed by "Ray Tree

Citations:
https://raytracing.github.io/books/RayTracingInOneWeekend.html
https://raytracing.github.io/books/RayTracingTheNextWeek.html
https://www.pexels.com/photo/brown-wooden-parquet-flooring-129731/