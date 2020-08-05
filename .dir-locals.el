;;; Directory Local Variables
((rst-mode
  (flyspell-mode . t)
  (ispell-local-dictionary . "francais")
  (indent-tabs-mode . nil)
  )
 )
;; https://stackoverflow.com/questions/16237506/
((nil . ((eval . (progn
                   (require 'grep)
                   (add-to-list
                    (make-local-variable 'grep-find-ignored-directories)
                    "_build"))))))
