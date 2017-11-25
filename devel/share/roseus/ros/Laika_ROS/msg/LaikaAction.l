;; Auto-generated. Do not edit!


(when (boundp 'Laika_ROS::LaikaAction)
  (if (not (find-package "LAIKA_ROS"))
    (make-package "LAIKA_ROS"))
  (shadow 'LaikaAction (find-package "LAIKA_ROS")))
(unless (find-package "LAIKA_ROS::LAIKAACTION")
  (make-package "LAIKA_ROS::LAIKAACTION"))

(in-package "ROS")
;;//! \htmlinclude LaikaAction.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass Laika_ROS::LaikaAction
  :super ros::object
  :slots (_header _actions ))

(defmethod Laika_ROS::LaikaAction
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:actions __actions) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _header __header)
   (setq _actions __actions)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:actions
   (&optional __actions)
   (if __actions (setq _actions __actions)) _actions)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64[] _actions
    (* 8    (length _actions)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64[] _actions
     (write-long (length _actions) s)
     (dotimes (i (length _actions))
       (sys::poke (elt _actions i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64[] _actions
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _actions (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _actions i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get Laika_ROS::LaikaAction :md5sum-) "9d3cd45f80f16d72487ecd17a073e278")
(setf (get Laika_ROS::LaikaAction :datatype-) "Laika_ROS/LaikaAction")
(setf (get Laika_ROS::LaikaAction :definition-)
      "Header header
float64[] actions

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :Laika_ROS/LaikaAction "9d3cd45f80f16d72487ecd17a073e278")


