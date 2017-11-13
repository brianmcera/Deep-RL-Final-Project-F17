; Auto-generated. Do not edit!


(cl:in-package Laika_ROS-msg)


;//! \htmlinclude LaikaState.msg.html

(cl:defclass <LaikaState> (roslisp-msg-protocol:ros-message)
  ((body_id
    :reader body_id
    :initarg :body_id
    :type cl:integer
    :initform 0)
   (position
    :reader position
    :initarg :position
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (orientation
    :reader orientation
    :initarg :orientation
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (lin_vel
    :reader lin_vel
    :initarg :lin_vel
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (ang_vel
    :reader ang_vel
    :initarg :ang_vel
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point)))
)

(cl:defclass LaikaState (<LaikaState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LaikaState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LaikaState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name Laika_ROS-msg:<LaikaState> is deprecated: use Laika_ROS-msg:LaikaState instead.")))

(cl:ensure-generic-function 'body_id-val :lambda-list '(m))
(cl:defmethod body_id-val ((m <LaikaState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:body_id-val is deprecated.  Use Laika_ROS-msg:body_id instead.")
  (body_id m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <LaikaState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:position-val is deprecated.  Use Laika_ROS-msg:position instead.")
  (position m))

(cl:ensure-generic-function 'orientation-val :lambda-list '(m))
(cl:defmethod orientation-val ((m <LaikaState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:orientation-val is deprecated.  Use Laika_ROS-msg:orientation instead.")
  (orientation m))

(cl:ensure-generic-function 'lin_vel-val :lambda-list '(m))
(cl:defmethod lin_vel-val ((m <LaikaState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:lin_vel-val is deprecated.  Use Laika_ROS-msg:lin_vel instead.")
  (lin_vel m))

(cl:ensure-generic-function 'ang_vel-val :lambda-list '(m))
(cl:defmethod ang_vel-val ((m <LaikaState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Laika_ROS-msg:ang_vel-val is deprecated.  Use Laika_ROS-msg:ang_vel instead.")
  (ang_vel m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LaikaState>) ostream)
  "Serializes a message object of type '<LaikaState>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'body_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'body_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'body_id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'body_id)) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'orientation) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'lin_vel) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'ang_vel) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LaikaState>) istream)
  "Deserializes a message object of type '<LaikaState>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'body_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'body_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'body_id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'body_id)) (cl:read-byte istream))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'orientation) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'lin_vel) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'ang_vel) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LaikaState>)))
  "Returns string type for a message object of type '<LaikaState>"
  "Laika_ROS/LaikaState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LaikaState)))
  "Returns string type for a message object of type 'LaikaState"
  "Laika_ROS/LaikaState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LaikaState>)))
  "Returns md5sum for a message object of type '<LaikaState>"
  "c9eae5e56960b9b108fffef42a77bc21")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LaikaState)))
  "Returns md5sum for a message object of type 'LaikaState"
  "c9eae5e56960b9b108fffef42a77bc21")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LaikaState>)))
  "Returns full string definition for message of type '<LaikaState>"
  (cl:format cl:nil "uint32 body_id~%geometry_msgs/Point position~%geometry_msgs/Point orientation~%geometry_msgs/Point lin_vel~%geometry_msgs/Point ang_vel~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LaikaState)))
  "Returns full string definition for message of type 'LaikaState"
  (cl:format cl:nil "uint32 body_id~%geometry_msgs/Point position~%geometry_msgs/Point orientation~%geometry_msgs/Point lin_vel~%geometry_msgs/Point ang_vel~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LaikaState>))
  (cl:+ 0
     4
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'orientation))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'lin_vel))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'ang_vel))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LaikaState>))
  "Converts a ROS message object to a list"
  (cl:list 'LaikaState
    (cl:cons ':body_id (body_id msg))
    (cl:cons ':position (position msg))
    (cl:cons ':orientation (orientation msg))
    (cl:cons ':lin_vel (lin_vel msg))
    (cl:cons ':ang_vel (ang_vel msg))
))
