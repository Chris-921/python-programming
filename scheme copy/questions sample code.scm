(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Returns a list of two-element lists
(define (enumerate s)
  (define (helper s i)
     (if (null? s) nil (cons (list i (car s)) (helper (cdr s) (+ 1 i)))))
 (helper s 0)
  )


;; Merge two lists LIST1 and LIST2 according to ORDERED? and return
;; the merged lists.
(define (merge ordered? list1 list2)
  (cond
     ((null? list1) list2)
     ((null? list2) list1)
     ((ordered? (car list1) (car list2)) (cons (car list1) (merge ordered? (cdr list1) list2)))
     (else (cons (car list2) (merge ordered? list1 (cdr list2))))
  )
)

