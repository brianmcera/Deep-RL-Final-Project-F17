;; Auto-generated. Do not edit!


(when (boundp 'Laika_ROS::LaikaStateArray)
  (if (not (find-package "LAIKA_ROS"))
    (make-package "LAIKA_ROS"))
  (shadow 'LaikaStateArray (find-package "LAIKA_ROS")))
(unless (find-package "LAIKA_ROS::LAIKASTATEARRAY")
  (make-package "LAIKA_ROS::LAIKASTATEARRAY"))

(in-package "ROS")
;;//! \htmlinclude LaikaStateArray.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass Laika_ROS::LaikaStateArray
  :super ros::object
  :slots (_header _states _cable_rl ))

(defmethod Laika_ROS::LaikaStateArray
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:states __states) (let (r) (dotimes (i 0) (push (instance Laika_ROS::LaikaState :init) r)) r))
    ((:cable_rl __cable_rl) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _header __header)
   (setq _states __states)
   (setq _cable_rl __cable_rl)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:states
   (&rest __states)
   (if (keywordp (car __states))
       (send* _states __states)
     (progn
       (if __states (setq _states (car __states)))
       _states)))
  (:cable_rl
   (&optional __cable_rl)
   (if __cable_rl (setq _cable_rl __cable_rl)) _cable_rl)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; Laika_ROS/LaikaState[] _states
    (apply #'+ (send-all _states :serialization-length)) 4
    ;; float32[] _cable_rl
    (* 4    (length _cable_rl)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; Laika_ROS/LaikaState[] _states
     (write-long (length _states) s)
     (dolist (elem _states)
       (send elem :serialize s)
       )
     ;; float32[] _cable_rl
     (write-long (length _cable_rl) s)
     (dotimes (i (length _cable_rl))
       (sys::poke (elt _cable_rl i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; Laika_ROS/LaikaState[] _states
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _states (let (r) (dotimes (i n) (push (instance Laika_ROS::LaikaState :init) r)) r))
     (dolist (elem- _states)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; float32[] _cable_rl
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _cable_rl (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _cable_rl i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get Laika_ROS::LaikaStateArray :md5sum-) "e19ca31cf4a3cbb12d873eb3d8084a5d")
(setf (get Laika_ROS::LaikaStateArray :datatype-) "Laika_ROS/LaikaStateArray")
(setf (get Laika_ROS::LaikaStateArray :definition-)
      "Header header
LaikaState[] states
float32[] cable_rl

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

================================================================================
MSG: Laika_ROS/LaikaState
uint32 body_id
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



(provide :Laika_ROS/LaikaStateArray "e19ca31cf4a3cbb12d873eb3d8084a5d")


