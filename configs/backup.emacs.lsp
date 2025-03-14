;; Include deft load path at start and run package
(add-to-list 'load-path "~/.deft")
(require 'deft)

;; Do some fun line formatting
(global-visual-line-mode 1)
(menu-bar-mode -1)
(ido-mode 1)
(ido-everywhere 1)

;; BIG SECTION OF ORGMODE STUFF
;; Org file path settings
(setq org-archive-location "~/sbemode/orgmode/zzzorg-archive.log::")
(setq org-agenda-files (directory-files-recursively "~/sbemode/orgmode/" "\\.org$"))
(setq backup-directory-alist '(("." . "~/zzzemacs-backups")))

;; Org-mode keyword settings
(setq org-todo-keywords
      '((sequence "TODO(t)"
		  "InProc(i)"
		  "PROJECT(p)"
		  "Future(f)"
		  "Chat(c)"
		  "GOAL(g)"
		  "|"
		  "DONE(d)")))

;; Orgmode colorful bits and bobs
(setq org-todo-keyword-faces
    '(("TODO" . (:foreground "brightwhite" :background "brightred"))
	("InProc" . (:foreground "black" :background "brightgreen"))
	("PROJECT" . (:foreground "black" :background "brightwhite"))
	("Future" . (:foreground "brightwhite" :background "brightblue"))
	("Chat" . (:foreground "black" :background "brightyellow"))
	("GOAL" . (:foreground "brightwhite" :background "darkorchid"))
    ("DONE" . (:foreground "brightblack" :background "black"))))

;; Org-mode tag settings
(setq org-tag-alist
    '(("work" .?w)
	("Steve" .?s)
	("Team" .?t)
	("home" .?h)
	("church" .?c)
	("Learning" .?L)))

;; Org-mode custom agenda views
;; ---> Org agendas by tag
(setq org-agenda-custom-commands
      '(("1" "Steve Meeting"
         tags-todo ":Steve:")
        ("2" "Team Meeting"
         tags-todo ":Team:")
		 ("3" "Learning Items"
		 tags-todo ":Learning")))

;; deft notes information
(custom-set-variables
 '(package-selected-packages '(deft)))
(setq deft-extensions '("txt" "org" "md"))
(setq deft-directory "~/sbemode/orgmode/defts")
(setq deft-default-extension "org")
(setq deft-new-file-format "%Y%b%d")

;; MELPA Package Downloads
(require 'package)
(add-to-list 'package-archives
    '("melpa-stable" . "https://stable.melpa.org/packages/"))
(package-initialize)

;; Custom Keybinding
(global-set-key (kbd "C-c t") 'org-sparse-tree)
(global-set-key (kbd "C-x C-d") 'deft)
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
