;; Auto-generated. Do not edit!


(when (boundp 'Laika_ROS::LaikaCommand)
  (if (not (find-package "LAIKA_ROS"))
    (make-package "LAIKA_ROS"))
  (shadow 'LaikaCommand (find-package "LAIKA_ROS")))
(unless (find-package "LAIKA_ROS::LAIKACOMMAND")
  (make-package "LAIKA_ROS::LAIKACOMMAND"))

(in-package "ROS")
;;//! \htmlinclude LaikaCommand.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass Laika_ROS::LaikaCommand
  :super ros::object
  :slots (_header _cmd ))

(defmethod Laika_ROS::LaikaCommand
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:cmd __cmd) "")
    )
   (send-super :init)
   (setq _header __header)
   (setq _cmd (string __cmd))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:cmd
   (&optional __cmd)
   (if __cmd (setq _cmd __cmd)) _cmd)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; string _cmd
    4 (length _cmd)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; string _cmd
       (write-long (length _cmd) s) (princ _cmd s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; string _cmd
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _cmd (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get Laika_ROS::LaikaCommand :md5sum-) "4276af4fed90fb499f3ed97a1942bbe3")
(setf (get Laika_ROS::LaikaCommand :datatype-) "Laika_ROS/LaikaCommand")
(setf (get Laika_ROS::LaikaCommand :definition-)
      "Header header
string cmd

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



(provide :Laika_ROS/LaikaCommand "4276af4fed90fb499f3ed97a1942bbe3")


