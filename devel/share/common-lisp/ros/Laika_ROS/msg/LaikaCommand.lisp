; Auto-generated. Do not edit!


(cl:in-package Laika_ROS-msg)


;//! \htmlinclude LaikaCommand.msg.html

(cl:defclass <LaikaCommand> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (cmd
    :reader cmd
    :initarg :cmd
    :type cl:string
    :initform ""))
)

(cl:defclass LaikaCommand (<LaikaCommand>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LaikaCommand>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LaikaCommand)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name Laika_ROS-msg:<LaikaCommand> is deprecated: use Laika_ROS-msg:LaikaCommand instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <LaikaCommand>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:header-val is deprecated.  Use Laika_ROS-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'cmd-val :lambda-list '(m))
(cl:defmethod cmd-val ((m <LaikaCommand>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:cmd-val is deprecated.  Use Laika_ROS-msg:cmd instead.")
  (cmd m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LaikaCommand>) ostream)
  "Serializes a message object of type '<LaikaCommand>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'cmd))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'cmd))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LaikaCommand>) istream)
  "Deserializes a message object of type '<LaikaCommand>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cmd) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'cmd) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LaikaCommand>)))
  "Returns string type for a message object of type '<LaikaCommand>"
  "Laika_ROS/LaikaCommand")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LaikaCommand)))
  "Returns string type for a message object of type 'LaikaCommand"
  "Laika_ROS/LaikaCommand")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LaikaCommand>)))
  "Returns md5sum for a message object of type '<LaikaCommand>"
  "4276af4fed90fb499f3ed97a1942bbe3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LaikaCommand)))
  "Returns md5sum for a message object of type 'LaikaCommand"
  "4276af4fed90fb499f3ed97a1942bbe3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LaikaCommand>)))
  "Returns full string definition for message of type '<LaikaCommand>"
  (cl:format cl:nil "Header header~%string cmd~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LaikaCommand)))
  "Returns full string definition for message of type 'LaikaCommand"
  (cl:format cl:nil "Header header~%string cmd~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LaikaCommand>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:length (cl:slot-value msg 'cmd))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LaikaCommand>))
  "Converts a ROS message object to a list"
  (cl:list 'LaikaCommand
    (cl:cons ':header (header msg))
    (cl:cons ':cmd (cmd msg))
))
