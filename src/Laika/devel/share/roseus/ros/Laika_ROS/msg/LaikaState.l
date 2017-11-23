;; Auto-generated. Do not edit!


(when (boundp 'Laika_ROS::LaikaState)
  (if (not (find-package "LAIKA_ROS"))
    (make-package "LAIKA_ROS"))
  (shadow 'LaikaState (find-package "LAIKA_ROS")))
(unless (find-package "LAIKA_ROS::LAIKASTATE")
  (make-package "LAIKA_ROS::LAIKASTATE"))

(in-package "ROS")
;;//! \htmlinclude LaikaState.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass Laika_ROS::LaikaState
  :super ros::object
  :slots (_body_id _position _orientation _lin_vel _ang_vel ))

(defmethod Laika_ROS::LaikaState
  (:init
   (&key
    ((:body_id __body_id) 0)
    ((:position __position) (instance geometry_msgs::Point :init))
    ((:orientation __orientation) (instance geometry_msgs::Point :init))
    ((:lin_vel __lin_vel) (instance geometry_msgs::Point :init))
    ((:ang_vel __ang_vel) (instance geometry_msgs::Point :init))
    )
   (send-super :init)
   (setq _body_id (round __body_id))
   (setq _position __position)
   (setq _orientation __orientation)
   (setq _lin_vel __lin_vel)
   (setq _ang_vel __ang_vel)
   self)
  (:body_id
   (&optional __body_id)
   (if __body_id (setq _body_id __body_id)) _body_id)
  (:position
   (&rest __position)
   (if (keywordp (car __position))
       (send* _position __position)
     (progn
       (if __position (setq _position (car __position)))
       _position)))
  (:orientation
   (&rest __orientation)
   (if (keywordp (car __orientation))
       (send* _orientation __orientation)
     (progn
       (if __orientation (setq _orientation (car __orientation)))
       _orientation)))
  (:lin_vel
   (&rest __lin_vel)
   (if (keywordp (car __lin_vel))
       (send* _lin_vel __lin_vel)
     (progn
       (if __lin_vel (setq _lin_vel (car __lin_vel)))
       _lin_vel)))
  (:ang_vel
   (&rest __ang_vel)
   (if (keywordp (car __ang_vel))
       (send* _ang_vel __ang_vel)
     (progn
       (if __ang_vel (setq _ang_vel (car __ang_vel)))
       _ang_vel)))
  (:serialization-length
   ()
   (+
    ;; uint32 _body_id
    4
    ;; geometry_msgs/Point _position
    (send _position :serialization-length)
    ;; geometry_msgs/Point _orientation
    (send _orientation :serialization-length)
    ;; geometry_msgs/Point _lin_vel
    (send _lin_vel :serialization-length)
    ;; geometry_msgs/Point _ang_vel
    (send _ang_vel :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _body_id
       (write-long _body_id s)
     ;; geometry_msgs/Point _position
       (send _position :serialize s)
     ;; geometry_msgs/Point _orientation
       (send _orientation :serialize s)
     ;; geometry_msgs/Point _lin_vel
       (send _lin_vel :serialize s)
     ;; geometry_msgs/Point _ang_vel
       (send _ang_vel :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _body_id
     (setq _body_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; geometry_msgs/Point _position
     (send _position :deserialize buf ptr-) (incf ptr- (send _position :serialization-length))
   ;; geometry_msgs/Point _orientation
     (send _orientation :deserialize buf ptr-) (incf ptr- (send _orientation :serialization-length))
   ;; geometry_msgs/Point _lin_vel
     (send _lin_vel :deserialize buf ptr-) (incf ptr- (send _lin_vel :serialization-length))
   ;; geometry_msgs/Point _ang_vel
     (send _ang_vel :deserialize buf ptr-) (incf ptr- (send _ang_vel :serialization-length))
   ;;
   self)
  )

(setf (get Laika_ROS::LaikaState :md5sum-) "c9eae5e56960b9b108fffef42a77bc21")
(setf (get Laika_ROS::LaikaState :datatype-) "Laika_ROS/LaikaState")
(setf (get Laika_ROS::LaikaState :definition-)
      "uint32 body_id
geometry_msgs/Point position
geometry_msgs/Point orientation
geometry_msgs/Point lin_vel
geometry_msgs/Point ang_vel

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

")



(provide :Laika_ROS/LaikaState "c9eae5e56960b9b108fffef42a77bc21")


