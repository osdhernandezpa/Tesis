(set! num-bands 20)

(set! resolution 512)

(set! mesh-size 50)

(set! k-points (list (vector3 -0.5 0 0)
                     (vector3 0.5 0 0)))

(set! k-points (interpolate 500 k-points))

(set! geometry (list (make block
                       (center 0 0 0) (size 0.81 infinity infinity)
                       (material (make dielectric (epsilon 2.35)) ) )
                     (make block
                       (center 0.5 0 0) (size 0.19 infinity infinity) 
                       (material (make dielectric (epsilon 1.0)) ) ) ))

(set! geometry-lattice (make lattice (size 1 no-size no-size)))

(run-te display-group-velocities (output-at-kpoint (vector3 0 0 0)
                          fix-efield-phase output-efield-z))

(run-tm display-group-velocities (output-at-kpoint (vector3 0 0 0)
                          fix-efield-phase output-efield-z))

;(include "dos.scm")
;(print-dos 0 2.1 100)


