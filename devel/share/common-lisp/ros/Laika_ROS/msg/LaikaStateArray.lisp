; Auto-generated. Do not edit!


(cl:in-package Laika_ROS-msg)


;//! \htmlinclude LaikaStateArray.msg.html

(cl:defclass <LaikaStateArray> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (states
    :reader states
    :initarg :states
    :type (cl:vector Laika_ROS-msg:LaikaState)
   :initform (cl:make-array 0 :element-type 'Laika_ROS-msg:LaikaState :initial-element (cl:make-instance 'Laika_ROS-msg:LaikaState)))
   (cable_rl
    :reader cable_rl
    :initarg :cable_rl
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass LaikaStateArray (<LaikaStateArray>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LaikaStateArray>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LaikaStateArray)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name Laika_ROS-msg:<LaikaStateArray> is deprecated: use Laika_ROS-msg:LaikaStateArray instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <LaikaStateArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:header-val is deprecated.  Use Laika_ROS-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'states-val :lambda-list '(m))
(cl:defmethod states-val ((m <LaikaStateArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:states-val is deprecated.  Use Laika_ROS-msg:states instead.")
  (states m))

(cl:ensure-generic-function 'cable_rl-val :lambda-list '(m))
(cl:defmethod cable_rl-val ((m <LaikaStateArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:cable_rl-val is deprecated.  Use Laika_ROS-msg:cable_rl instead.")
  (cable_rl m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LaikaStateArray>) ostream)
  "Serializes a message object of type '<LaikaStateArray>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'states))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'states))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'cable_rl))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'cable_rl))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LaikaStateArray>) istream)
  "Deserializes a message object of type '<LaikaStateArray>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'states) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'states)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'Laika_ROS-msg:LaikaState))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'cable_rl) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'cable_rl)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LaikaStateArray>)))
  "Returns string type for a message object of type '<LaikaStateArray>"
  "Laika_ROS/LaikaStateArray")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LaikaStateArray)))
  "Returns string type for a message object of type 'LaikaStateArray"
  "Laika_ROS/LaikaStateArray")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LaikaStateArray>)))
  "Returns md5sum for a message object of type '<LaikaStateArray>"
  "e19ca31cf4a3cbb12d873eb3d8084a5d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LaikaStateArray)))
  "Returns md5sum for a message object of type 'LaikaStateArray"
  "e19ca31cf4a3cbb12d873eb3d8084a5d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LaikaStateArray>)))
  "Returns full string definition for message of type '<LaikaStateArray>"
  (cl:format cl:nil "Header header~%LaikaState[] states~%float32[] cable_rl~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: Laika_ROS/LaikaState~%uint32 body_id~%geometry_msgs/Point position~%geometry_msgs/Point orientation~%geometry_msgs/Point lin_vel~%geometry_msgs/Point ang_vel~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LaikaStateArray)))
  "Returns full string definition for message of type 'LaikaStateArray"
  (cl:format cl:nil "Header header~%LaikaState[] states~%float32[] cable_rl~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: Laika_ROS/LaikaState~%uint32 body_id~%geometry_msgs/Point position~%geometry_msgs/Point orientation~%geometry_msgs/Point lin_vel~%geometry_msgs/Point ang_vel~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LaikaStateArray>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'states) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'cable_rl) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LaikaStateArray>))
  "Converts a ROS message object to a list"
  (cl:list 'LaikaStateArray
    (cl:cons ':header (header msg))
    (cl:cons ':states (states msg))
    (cl:cons ':cable_rl (cable_rl msg))
))
