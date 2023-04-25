(set! num-bands 8)

(set! resolution 512)

(set! mesh-size 10)

(set! k-points (list (vector3 -0.5 0 0)
                     (vector3 0.5 0 0)))

(set! k-points (interpolate 500 k-points))

(define-param index-min 1.0)
(define-param index-max 3.0)

(define (eps-func p)
  (make dielectric ;(index index-max) ))
    (index  (+ index-min (* (- index-max  index-min )  (+ 0.5 (vector3-x p)) ) ) )))

(set! geometry-lattice (make lattice (size 1 no-size no-size)))

(set! default-material (make material-function (material-func eps-func)))

(run-te display-group-velocities)

(run-tm display-group-velocities)

