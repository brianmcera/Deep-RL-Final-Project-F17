
(cl:in-package :asdf)

(defsystem "Laika_ROS-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "LaikaAction" :depends-on ("_package_LaikaAction"))
    (:file "_package_LaikaAction" :depends-on ("_package"))
    (:file "LaikaCommand" :depends-on ("_package_LaikaCommand"))
    (:file "_package_LaikaCommand" :depends-on ("_package"))
    (:file "LaikaState" :depends-on ("_package_LaikaState"))
    (:file "_package_LaikaState" :depends-on ("_package"))
    (:file "LaikaStateArray" :depends-on ("_package_LaikaStateArray"))
    (:file "_package_LaikaStateArray" :depends-on ("_package"))
  ))